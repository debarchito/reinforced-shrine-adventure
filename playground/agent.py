"""
Reinforcement learning agent implementation using PPO.
Uses DistilBERT for text processing and a custom actor-critic architecture.

The implementation includes:
- RolloutBuffer: Stores trajectories during agent rollouts
- ActorCritic: Neural network with BERT text encoder and separate actor/critic heads
- ShrineAgent: Main PPO agent implementation

The agent uses mixed precision training with automatic mixed precision (AMP)
and gradient scaling for better performance on GPUs.

Key features:
- DistilBERT for text encoding (frozen parameters)
- PPO with clipped objective and GAE-Lambda advantage estimation
- Combined text and game state features
- Automatic action masking for invalid choices
"""

import gc
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
from transformers import DistilBertTokenizer, DistilBertModel
from torch.distributions import Categorical


class RolloutBuffer:
    """Stores trajectories collected during agent rollouts."""

    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []
        self.log_probs = []
        self.values = []

    def clear(self):
        """Clears all stored trajectories."""
        self.states.clear()
        self.actions.clear()
        self.rewards.clear()
        self.next_states.clear()
        self.dones.clear()
        self.log_probs.clear()
        self.values.clear()

    def add(self, state, action, reward, next_state, done, log_prob, value):
        """Adds a single transition."""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_states.append(next_state)
        self.dones.append(done)
        self.log_probs.append(log_prob)
        self.values.append(value)


class ActorCritic(nn.Module):
    """Neural network implementing both actor and critic networks.
    Uses DistilBERT for text processing."""

    def __init__(self, model_name="distilbert-base-uncased", hidden_size=128):
        super(ActorCritic, self).__init__()
        self.bert = DistilBertModel.from_pretrained(
            model_name, torch_dtype=torch.float16
        )
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)

        # Freeze BERT parameters
        self.bert.eval()
        for param in self.bert.parameters():
            param.requires_grad = False

        # Combines BERT output with game state features
        self.feature_combiner = nn.Sequential(
            nn.Linear(768 + 5, hidden_size),  # Updated for 5 item features
            nn.ReLU(),
            nn.LayerNorm(hidden_size),
            nn.Dropout(0.2),
        )

        # Actor network
        self.actor = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.LayerNorm(64),
            nn.Dropout(0.1),
            nn.Linear(64, 4),
            nn.Softmax(dim=-1),
        )

        # Critic network
        self.critic = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.LayerNorm(64),
            nn.Dropout(0.1),
            nn.Linear(64, 1),
        )

    @torch.autocast(device_type="cuda")
    def forward(self, text_batch, stats, items):
        """Process text and game state features."""
        if isinstance(text_batch, str):
            text_batch = [text_batch]

        # Tokenize text
        tokens = self.tokenizer(
            text_batch,
            return_tensors="pt",
            max_length=256,
            truncation=True,
            padding=True,
        )

        # Move to device
        device = next(self.bert.parameters()).device
        tokens = {k: v.to(device, non_blocking=True) for k, v in tokens.items()}
        items = items.to(device, non_blocking=True)

        # Get BERT embeddings
        with torch.no_grad(), torch.autocast(device_type="cuda"):
            bert_output = self.bert(**tokens)[0][:, 0, :]

        # Combine features
        combined_input = torch.cat([bert_output, items], dim=1)
        features = self.feature_combiner(combined_input)

        # Get outputs
        action_probs = self.actor(features)
        value = self.critic(features)

        return action_probs, value


class ShrineAgent:
    """PPO agent for text adventure game."""

    def __init__(self, state_size, action_size, batch_size=256):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.backends.cudnn.benchmark = True

        self.policy = ActorCritic().to(self.device)
        self.optimizer = optim.AdamW(self.policy.parameters(), lr=0.0003)
        self.scaler = torch.amp.GradScaler()  # type: ignore

        self.memory = RolloutBuffer()

        # PPO hyperparameters
        self.gamma = 0.98
        self.gae_lambda = 0.97
        self.clip_epsilon = 0.15
        self.c1 = 1.0
        self.c2 = 0.02
        self.max_grad_norm = 0.5
        self.ppo_epochs = 12
        self.batch_size = batch_size

    @torch.no_grad()
    def get_state_representation(self, observation):
        """Convert observation to tensors."""
        text = observation["text"]
        items_array = np.array([observation["items"]])
        items = torch.tensor(items_array, dtype=torch.float16, device=self.device)
        return text, items

    @torch.no_grad()
    def act(self, observation):
        """Select an action using the policy."""
        text, items = self.get_state_representation(observation)
        action_probs, value = self.policy(text, items, items)

        # Improve action masking
        num_choices = len(observation["choices"])
        mask = torch.zeros_like(action_probs)
        mask[0, :num_choices] = 1

        # Add small epsilon to prevent zero probabilities
        masked_probs = action_probs * mask + 1e-8
        masked_probs = masked_probs / masked_probs.sum()

        # Add temperature scaling for exploration
        temperature = 1.0
        masked_probs = masked_probs.pow(1 / temperature)
        masked_probs = masked_probs / masked_probs.sum()

        dist = Categorical(masked_probs[0])
        action = dist.sample()

        return action.item(), dist.log_prob(action), value

    def update(self, entropy_coef=0.01):
        """Update policy using PPO."""
        returns = []
        advantages = []

        # Calculate returns and advantages
        next_value = 0
        advantage = 0
        for reward, value, done in zip(
            reversed(self.memory.rewards),
            reversed(self.memory.values),
            reversed(self.memory.dones),
        ):
            if done:
                next_value = 0
                advantage = 0

            td_error = reward + self.gamma * next_value * (1 - done) - value
            advantage = td_error + self.gamma * self.gae_lambda * advantage * (1 - done)

            returns.insert(0, advantage + value)
            advantages.insert(0, advantage)

            next_value = value

        # Convert to tensors
        returns = torch.tensor(returns, dtype=torch.float16, device=self.device)
        advantages = torch.tensor(advantages, dtype=torch.float16, device=self.device)
        old_log_probs = torch.stack(self.memory.log_probs)

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # PPO update loop
        for _ in range(self.ppo_epochs):
            # Prepare batch
            text_batch = [s["text"] for s in self.memory.states]
            items_array = np.array([s["items"] for s in self.memory.states])
            items_batch = torch.tensor(
                items_array, dtype=torch.float16, device=self.device
            )
            actions_batch = torch.tensor(self.memory.actions, device=self.device)

            # Get new probabilities and values
            action_probs, values = self.policy(text_batch, items_batch, items_batch)
            dist = Categorical(action_probs)
            new_log_probs = dist.log_prob(actions_batch)
            entropy = dist.entropy().mean()

            # Compute PPO objective
            ratio = (new_log_probs - old_log_probs).exp()
            surr1 = ratio * advantages
            surr2 = (
                torch.clamp(ratio, 1.0 - self.clip_epsilon, 1.0 + self.clip_epsilon)
                * advantages
            )

            # Compute losses with adjustable entropy coefficient
            actor_loss = -torch.min(surr1, surr2).mean()
            values_clipped = values.squeeze()
            values_clipped = torch.clamp(
                values_clipped,
                min=-100.0,  # Prevent extreme negative values
                max=100.0,  # Prevent extreme positive values
            )
            critic_loss = 0.5 * (returns - values_clipped).pow(2).mean()
            loss = actor_loss + self.c1 * critic_loss - entropy_coef * entropy

            # Optimize
            self.optimizer.zero_grad(set_to_none=True)
            self.scaler.scale(loss).backward()

            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)

            self.scaler.step(self.optimizer)
            self.scaler.update()

        # Clean up
        self.memory.clear()
        torch.cuda.empty_cache()
        gc.collect()
