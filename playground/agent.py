"""
Reinforcement learning agent implementation using PP.
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
    """Stores trajectories collected during agent rollouts.

    Attributes:
        states: List of environment observations
        actions: List of actions taken
        rewards: List of rewards received
        next_states: List of next observations
        dones: List of episode termination flags
        log_probs: List of action log probabilities
        values: List of state value estimates
    """

    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []
        self.log_probs = []
        self.values = []

    def clear(self):
        """Clears all stored trajectories to free memory."""
        self.states.clear()
        self.actions.clear()
        self.rewards.clear()
        self.next_states.clear()
        self.dones.clear()
        self.log_probs.clear()
        self.values.clear()

    def add(self, state, action, reward, next_state, done, log_prob, value):
        """Adds a single step transition to the buffer.

        Args:
            state: Current environment observation
            action: Action taken
            reward: Reward received
            next_state: Next environment observation
            done: Episode termination flag
            log_prob: Log probability of the action
            value: Estimated state value
        """
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_states.append(next_state)
        self.dones.append(done)
        self.log_probs.append(log_prob)
        self.values.append(value)


class ActorCritic(nn.Module):
    """Neural network that implements both actor and critic networks.
    Uses DistilBERT for text processing followed by separate actor/critic heads.

    The network architecture:
    1. DistilBERT text encoder (frozen)
    2. Feature combiner: Concatenates text features with game state
    3. Actor head: Outputs action probabilities
    4. Critic head: Outputs state value estimate

    Args:
        model_name: Name of pretrained BERT model to use
        hidden_size: Size of hidden layers after feature combination
    """

    def __init__(self, model_name="distilbert-base-uncased", hidden_size=128):
        super(ActorCritic, self).__init__()
        self.bert = DistilBertModel.from_pretrained(
            model_name, torch_dtype=torch.float16
        )
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)

        # Freeze BERT parameters for efficiency
        self.bert.eval()
        for param in self.bert.parameters():
            param.requires_grad = False

        # Combines BERT output (768) with game state features (9)
        self.feature_combiner = nn.Sequential(
            nn.Linear(768 + 9, hidden_size),
            nn.ReLU(),
            nn.LayerNorm(hidden_size),
            nn.Dropout(0.2),
        )

        # Actor network: outputs action probabilities
        self.actor = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.LayerNorm(64),
            nn.Dropout(0.1),
            nn.Linear(64, 4),
            nn.Softmax(dim=-1),
        )

        # Critic network: outputs state value estimate
        self.critic = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.LayerNorm(64),
            nn.Dropout(0.1),
            nn.Linear(64, 1),
        )

    @torch.autocast(device_type="cuda")
    def forward(self, text_batch, stats, items):
        """Process text through BERT and combine with game state features.

        Uses CUDA automatic mixed precision for better performance.

        Args:
            text_batch: String or list of strings containing game text
            stats: Tensor of game state statistics
            items: Tensor of inventory item flags

        Returns:
            Tuple of (action probabilities, state value estimate)
        """
        if isinstance(text_batch, str):
            text_batch = [text_batch]
        elif not isinstance(text_batch, list):
            raise ValueError("text_batch must be a string or list of strings")

        # Tokenize text for BERT
        tokens = self.tokenizer(
            text_batch,
            return_tensors="pt",
            max_length=128,
            truncation=True,
            padding=True,
        )

        # Move inputs to same device as model
        device = next(self.bert.parameters()).device
        tokens = {k: v.to(device, non_blocking=True) for k, v in tokens.items()}
        stats = stats.to(device, non_blocking=True)
        items = items.to(device, non_blocking=True)

        # Get BERT embeddings
        with torch.no_grad(), torch.autocast(device_type="cuda"):
            bert_output = self.bert(**tokens)[0][:, 0, :]

        # Combine text features with game state
        combined_input = torch.cat([bert_output, stats, items], dim=1)
        features = self.feature_combiner(combined_input)

        # Get actor and critic outputs
        action_probs = self.actor(features)
        value = self.critic(features)

        return action_probs, value


class ShrineAgent:
    """PPO agent implementation for text adventure games.

    Uses Proximal Policy Optimization with:
    - Clipped surrogate objective
    - Generalized Advantage Estimation (GAE)
    - Value function clipping
    - Entropy bonus

    Args:
        state_size: Size of environment state space
        action_size: Size of environment action space
    """

    def __init__(self, state_size, action_size):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.backends.cudnn.benchmark = True

        self.policy = ActorCritic().to(self.device)
        self.optimizer = optim.AdamW(self.policy.parameters(), lr=0.0003)
        self.scaler = torch.amp.GradScaler()  # type: ignore

        self.memory = RolloutBuffer()

        # PPO hyperparameters
        self.gamma = 0.98  # Increased to value future rewards more
        self.gae_lambda = 0.97  # Increased for better advantage estimation
        self.clip_epsilon = 0.15  # Decreased for more stable updates
        self.c1 = 1.0  # Value loss coefficient
        self.c2 = 0.02  # Increased entropy coefficient for more exploration
        self.max_grad_norm = 0.5
        self.ppo_epochs = 12  # Increased training epochs
        self.batch_size = 192  # Adjusted batch size

    @torch.no_grad()
    def get_state_representation(self, observation):
        """Convert environment observation to tensors.

        Args:
            observation: Dictionary containing environment observation

        Returns:
            Tuple of (text, stats tensor, items tensor)
        """
        text = observation["text"]
        stats_array = np.array([observation["stats"]])
        items_array = np.array([observation["items"]])
        stats = torch.tensor(stats_array, dtype=torch.float16, device=self.device)
        items = torch.tensor(items_array, dtype=torch.float16, device=self.device)
        return text, stats, items

    @torch.no_grad()
    def act(self, observation):
        """Select an action using the policy network.

        Masks invalid actions before sampling.

        Args:
            observation: Dictionary containing environment observation

        Returns:
            Tuple of (selected action, action log probability, state value)
        """
        text, stats, items = self.get_state_representation(observation)
        action_probs, value = self.policy(text, stats, items)

        # Mask invalid actions
        num_choices = len(observation["choices"])
        mask = torch.zeros_like(action_probs)
        mask[0, :num_choices] = 1
        masked_probs = action_probs * mask
        masked_probs = masked_probs / masked_probs.sum()

        dist = Categorical(masked_probs[0])
        action = dist.sample()

        return action.item(), dist.log_prob(action), value

    def update(self):
        """Update policy using PPO algorithm.

        Implements the PPO training loop:
        1. Compute returns and advantages
        2. Normalize advantages
        3. For each epoch:
            - Get minibatches of trajectories
            - Compute PPO objective
            - Compute value loss and entropy bonus
            - Update network parameters
        4. Clear memory buffers
        """
        returns = []
        advantages = []

        # Calculate returns and advantages using GAE
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
            # Prepare minibatch
            text_batch = [s["text"] for s in self.memory.states]
            stats_array = np.array([s["stats"] for s in self.memory.states])
            items_array = np.array([s["items"] for s in self.memory.states])
            stats_batch = torch.tensor(
                stats_array, dtype=torch.float16, device=self.device
            )
            items_batch = torch.tensor(
                items_array, dtype=torch.float16, device=self.device
            )
            actions_batch = torch.tensor(self.memory.actions, device=self.device)

            # Get new action probabilities and values
            action_probs, values = self.policy(text_batch, stats_batch, items_batch)
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

            # Compute losses
            actor_loss = -torch.min(surr1, surr2).mean()
            critic_loss = 0.5 * (returns - values.squeeze()).pow(2).mean()

            # Combined loss with entropy bonus
            loss = actor_loss + self.c1 * critic_loss - self.c2 * entropy

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
