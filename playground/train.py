from playground.story import StoryEnvironment, StoryAgent
from torch.optim import Adam
import torch
import torch.nn.functional as F
from torch.distributions import Categorical

def train_agent(num_episodes=1000):
    env = StoryEnvironment()
    agent = StoryAgent()
    optimizer = Adam(agent.parameters(), lr=3e-4)
    
    # PPO hyperparameters
    clip_epsilon = 0.2
    value_coef = 0.5
    entropy_coef = 0.01
    ppo_epochs = 4
    batch_size = 32
    
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        episode_reward = 0
        
        # Storage for PPO update
        states = []
        actions = []
        rewards = []
        values = []
        log_probs = []
        
        while not done:
            # Get action from policy
            text_embeddings, attributes = state
            choices = env.story.get_current_choices()
            action_logits, value = agent(text_embeddings, attributes, choices)
            action_probs = F.softmax(action_logits, dim=-1)
            dist = Categorical(action_probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
            
            # Take action in environment
            next_state, reward, done, _ = env.step(action.item())
            episode_reward += reward
            
            # Store transition
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            values.append(value)
            log_probs.append(log_prob)
            
            state = next_state
        
        # Calculate returns and advantages
        returns = []
        advantages = []
        R = 0
        for r, v in zip(reversed(rewards), reversed(values)):
            R = r + 0.99 * R  # gamma = 0.99
            advantage = R - v.item()
            returns.append(R)
            advantages.append(advantage)
        
        returns = torch.tensor(list(reversed(returns)))
        advantages = torch.tensor(list(reversed(advantages)))
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # PPO update
        for _ in range(ppo_epochs):
            # Process in batches
            for start_idx in range(0, len(states), batch_size):
                end_idx = start_idx + batch_size
                batch_states = states[start_idx:end_idx]
                batch_actions = actions[start_idx:end_idx]
                batch_log_probs = log_probs[start_idx:end_idx]
                batch_returns = returns[start_idx:end_idx]
                batch_advantages = advantages[start_idx:end_idx]
                
                # Get current policy outputs
                text_embeddings, attributes = zip(*batch_states)
                text_embeddings = torch.cat(text_embeddings)
                attributes = torch.stack(attributes)
                choices = env.story.get_current_choices()  # Assuming choices remain same
                
                new_action_logits, new_values = agent(text_embeddings, attributes, choices)
                new_action_probs = F.softmax(new_action_logits, dim=-1)
                new_dist = Categorical(new_action_probs)
                
                # Calculate ratios and surrogate losses
                new_log_probs = new_dist.log_prob(torch.stack(batch_actions))
                ratios = torch.exp(new_log_probs - torch.stack(batch_log_probs))
                
                surr1 = ratios * batch_advantages
                surr2 = torch.clamp(ratios, 1 - clip_epsilon, 1 + clip_epsilon) * batch_advantages
                
                # Calculate losses
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = F.mse_loss(new_values.squeeze(), batch_returns)
                entropy_loss = -new_dist.entropy().mean()
                
                # Combined loss
                total_loss = policy_loss + value_coef * value_loss - entropy_coef * entropy_loss
                
                # Update network
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()
        
        print(f"Episode {episode}, Reward: {episode_reward}")
