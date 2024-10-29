import torch
import torch.nn as nn
from transformers import DistilBertTokenizer, DistilBertModel
from bink.story import story_from_file

class StoryMemory(nn.Module):
    def __init__(self, hidden_size=256, num_layers=2):
        super().__init__()
        self.hidden_size = hidden_size
        # LSTM for processing story text
        self.lstm = nn.LSTM(
            input_size=768,  # Using BERT embeddings size
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        # Attention mechanism
        self.attention = nn.MultiheadAttention(hidden_size, num_heads=4)
        
    def forward(self, text_embeddings):
        # Process sequence through LSTM
        lstm_out, (h_n, c_n) = self.lstm(text_embeddings)
        # Apply attention
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        return attn_out, (h_n, c_n)

class StoryAgent(nn.Module):
    def __init__(self, state_size=256, hidden_size=128):
        super().__init__()
        self.memory = StoryMemory()
        # State processing
        self.state_encoder = nn.Sequential(
            nn.Linear(state_size + 5, hidden_size),  # +5 for attributes
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )       
        # Policy head
        self.policy = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)  # Output logits for each choice
        )
        # Value head for PPO
        self.value = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, text_embeddings, attributes, available_choices):
        # Process story context
        memory_out, _ = self.memory(text_embeddings)
        # Combine with attributes
        combined_state = torch.cat([memory_out[:, -1], attributes], dim=-1)
        state_features = self.state_encoder(combined_state)
        # Get action logits and value
        action_logits = self.policy(state_features)
        value = self.value(state_features)
        # Mask unavailable choices
        mask = torch.zeros_like(action_logits)
        mask[available_choices] = float('-inf')
        action_logits = action_logits + mask
        return action_logits, value

class StoryEnvironment:
    def __init__(self):
        self.story = story_from_file("story/json/story.ink.json")
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.encoder = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.reset()
        
    def reset(self):
        self.story = story_from_file("story/json/story.ink.json")
        self.current_text = ""
        self.attributes = {
            'curiosity': 0,
            'social': 0,
            'caution': 0,
            'agnostic': 0,
            'supernatural': 0
        }
        return self._get_state()
    
    def _get_state(self):
        # Get text embeddings
        tokens = self.tokenizer(self.current_text, return_tensors='pt', truncation=True)
        with torch.no_grad():
            embeddings = self.encoder(**tokens).last_hidden_state
        
        # Get attributes
        attr_tensor = torch.tensor([
            self.attributes['curiosity'],
            self.attributes['social'],
            self.attributes['caution'],
            self.attributes['agnostic'],
            self.attributes['supernatural']
        ])
        
        return embeddings, attr_tensor
    
    def step(self, action):
        self.story.choose_choice_index(action)
        
        # Accumulate text
        while self.story.can_continue():
            self.current_text += self.story.cont() + " "
        
        # Get new state
        state = self._get_state()
        choices = self.story.get_current_choices()
        done = len(choices) == 0
        
        # Calculate reward based on attribute changes
        reward = sum(self.attributes.values())
        
        return state, reward, done, {}
