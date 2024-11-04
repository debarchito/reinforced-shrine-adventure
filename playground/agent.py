import gc
import torch
import random
import torch.nn as nn
import torch.optim as optim
from collections import deque
from transformers import DistilBertTokenizer, DistilBertModel

class TextQNetwork(nn.Module):
    def __init__(self, model_name="distilbert-base-uncased", hidden_size=64):
        super(TextQNetwork, self).__init__()
        # Load models in half precision
        self.bert = DistilBertModel.from_pretrained(model_name, torch_dtype=torch.float16)
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        
        # Freeze and optimize memory
        self.bert.eval()
        for param in self.bert.parameters():
            param.requires_grad = False
            
        self.feature_combiner = nn.Sequential(
            nn.Linear(768 + 7, hidden_size),  # Removed bias for efficiency
            nn.ReLU(),
            nn.Dropout(0.1)
        )
        
        # Q-network layers
        self.advantage = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 4)
        )
        
        self.value = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    @torch.autocast(device_type='cuda')
    def forward(self, text, stats, items):
        tokens = self.tokenizer(text, return_tensors="pt", 
                            max_length=128, truncation=True, padding=True)  # Reduced max_length
        
        device = next(self.bert.parameters()).device
        tokens = {k: v.to(device, non_blocking=True) for k, v in tokens.items()}
        stats = stats.to(device, non_blocking=True)
        items = items.to(device, non_blocking=True)
        
        with torch.no_grad(), torch.autocast(device_type='cuda'):
            bert_output = self.bert(**tokens)[0][:, 0, :]
        
        combined_input = torch.cat([bert_output, stats, items], dim=1)
        features = self.feature_combiner(combined_input)
        
        advantage = self.advantage(features)
        value = self.value(features)
        
        # Combine value and advantage for Q-values
        return value + (advantage - advantage.mean(dim=1, keepdim=True))

class ShrineAgent:
    def __init__(self, state_size, action_size):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.backends.cudnn.benchmark = True  # Enable cudnn autotuner
        
        self.qnetwork = TextQNetwork().to(self.device)
        self.target_network = TextQNetwork().to(self.device)
        self.target_network.load_state_dict(self.qnetwork.state_dict())
        
        self.optimizer = optim.AdamW(self.qnetwork.parameters(), lr=0.0001, weight_decay=0.01)
        self.scaler = torch.amp.GradScaler()  # type: ignore
        
        # Simple replay buffer using deque
        self.memory = deque(maxlen=5000)
        
        self.batch_size = 32
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.target_update = 10
        self.step_counter = 0
        
        # Enable memory efficient optimizations
        self.qnetwork.share_memory()
        self.target_network.share_memory()

    @torch.no_grad()
    def get_state_representation(self, observation):
        text = observation["text"]
        stats = torch.tensor([observation["stats"]], dtype=torch.float16, device=self.device)
        items = torch.tensor([observation["items"]], dtype=torch.float16, device=self.device)
        return text, stats, items

    @torch.no_grad()
    def act(self, observation):
        num_choices = len(observation["choices"])
        if random.random() < self.epsilon:
            return random.randrange(num_choices)
        
        text, stats, items = self.get_state_representation(observation)
        q_values = self.qnetwork(text, stats, items)
        
        # Mask invalid actions by setting their Q-values to a very low number
        mask = torch.ones_like(q_values[0]) * float('-inf')
        mask[:num_choices] = 0
        masked_q_values = q_values[0] + mask
        
        return torch.argmax(masked_q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        with torch.autocast(device_type='cuda'):
            # Convert batch data to tensors
            state_texts = [s["text"] for s in states]
            state_stats = torch.tensor([s["stats"] for s in states], dtype=torch.float16, device=self.device)
            state_items = torch.tensor([s["items"] for s in states], dtype=torch.float16, device=self.device)
            
            next_state_texts = [s["text"] for s in next_states]
            next_state_stats = torch.tensor([s["stats"] for s in next_states], dtype=torch.float16, device=self.device)
            next_state_items = torch.tensor([s["items"] for s in next_states], dtype=torch.float16, device=self.device)
            
            actions = torch.tensor(actions, device=self.device)
            rewards = torch.tensor(rewards, dtype=torch.float16, device=self.device)
            dones = torch.tensor(dones, dtype=torch.bool, device=self.device)
            
            # Compute targets in half precision
            next_q_values = self.target_network(next_state_texts, next_state_stats, next_state_items)
            
            targets = rewards.clone()
            targets[~dones] += self.gamma * torch.max(next_q_values[~dones], dim=1)[0]
            
            current_q_values = self.qnetwork(state_texts, state_stats, state_items)
            
            loss = nn.MSELoss()(
                current_q_values.gather(1, actions.unsqueeze(1)).squeeze(),
                targets
            )

        # Optimize with gradient scaling
        self.optimizer.zero_grad(set_to_none=True)
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.step_counter += 1
        if self.step_counter % self.target_update == 0:
            self.target_network.load_state_dict(self.qnetwork.state_dict())
            torch.cuda.empty_cache()
            gc.collect()

def train_agent(env, agent, episodes=1000):
    scores = []
    
    for episode in range(episodes):
        observation, _ = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.act(observation)
            next_observation, reward, done, _, _ = env.step(action)
            
            agent.remember(observation, action, reward, next_observation, done)
            agent.replay()
            
            total_reward += reward
            observation = next_observation
            
        scores.append(total_reward)
        
        if episode % 10 == 0:
            print(f"Episode: {episode}, Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")
            torch.cuda.empty_cache()
    
    return scores
