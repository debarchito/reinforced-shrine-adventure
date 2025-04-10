"""
Training script for the PPO agent in the text adventure game.
Implements training loop with live progress visualization.

The script includes:
- Training loop with PPO updates
- Live plotting of scores and moving averages
- Model and results saving
- Progress tracking and statistics

Key features:
- Interactive matplotlib visualization
- Automatic checkpointing
- Memory-efficient numpy arrays
- Progress logging and statistics
- Entropy reduction for successful paths
"""

import torch
import numpy as np
from env import ReinforcedShrineAdventureEnv
from agent import ShrineAgent
import matplotlib.pyplot as plt
from datetime import datetime
import os


def plot_scores(scores, filename):
    """Plot and save the training scores.

    Args:
        scores: Array of episode scores
        filename: Path to save the plot
    """
    plt.figure(figsize=(10, 5))
    plt.plot(scores)
    plt.title("Training Scores over Episodes")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.savefig(filename)
    plt.close()


def moving_average(data, window_size=100):
    """Calculate the moving average of the data.

    Args:
        data: Array of values to average
        window_size: Size of sliding window

    Returns:
        Array of moving averages
    """
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


def main():
    """Main training loop.

    Implements:
    1. Environment and agent setup
    2. Episode rollouts with PPO updates
    3. Live progress visualization
    4. Model checkpointing and results saving
    5. Entropy reduction for successful paths
    """
    torch.manual_seed(42)
    np.random.seed(42)

    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    env = ReinforcedShrineAdventureEnv()
    agent = ShrineAgent(
        state_size=773, action_size=4, batch_size=256
    )

    num_episodes = 1000
    initial_entropy_coef = 0.02
    min_entropy_coef = 0.005
    entropy_decay = 0.98

    # plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    (scores_line,) = ax1.plot([], [], "b-", label="Episode Scores")
    (avg_line,) = ax2.plot([], [], "r-", label="Moving Average")

    ax1.set_title("Training Progress")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Score")
    ax1.legend()

    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Moving Average Score")
    ax2.legend()

    # Set initial axis limits
    ax1.set_xlim(0, num_episodes)
    ax1.set_ylim(-10, 50)
    ax2.set_xlim(0, num_episodes)
    ax2.set_ylim(-10, 50)

    window_size = 10
    scores = np.zeros(num_episodes, dtype=np.float16)
    moving_avg = np.array([], dtype=np.float16)

    # Track successful episodes
    success_history = []
    best_reward = float("-inf")
    success_threshold = 20.0
    current_entropy_coef = initial_entropy_coef

    # Train the agent
    print("Starting training...")
    for episode in range(num_episodes):
        observation, _ = env.reset()
        total_reward = 0
        done = False
        truncated = False
        episode_choices = []

        while not done and not truncated:
            action, log_prob, value = agent.act(observation)
            next_observation, reward, done, truncated, _ = env.step(action)

            # Record episode details
            if action < len(observation["choices"]):
                episode_choices.append(observation["choices"][action])

            agent.memory.add(
                observation,
                action,
                reward,
                next_observation,
                done or truncated,
                log_prob,
                value,
            )

            total_reward += reward
            observation = next_observation

            if len(agent.memory.states) >= agent.batch_size:
                # Update with current entropy coefficient
                agent.update(entropy_coef=current_entropy_coef)

        # Track successful episodes
        was_successful = total_reward > success_threshold
        success_history.append(was_successful)

        # Calculate success rate over recent episodes
        window = 50  # or another suitable size
        if len(success_history) >= window:
            recent_success_rate = sum(success_history[-window:]) / window

            # Adjust entropy based on success rate
            if recent_success_rate > 0.7:  # if successful more than 70% of time
                current_entropy_coef = max(
                    min_entropy_coef, current_entropy_coef * entropy_decay
                )
            elif recent_success_rate < 0.3:  # if struggling
                current_entropy_coef = min(
                    initial_entropy_coef, current_entropy_coef / entropy_decay
                )

        # If this was the best episode so far, save the successful path
        if total_reward > best_reward:
            best_reward = total_reward
            print(f"\nNew best episode! Reward: {total_reward:.2f}")
            print("Successful choices:", episode_choices)
            print("Final items:", observation["items"])
            print(f"Current entropy coefficient: {current_entropy_coef:.6f}")

        scores[episode] = total_reward

        # Update the plots
        scores_line.set_data(np.arange(episode + 1), scores[: episode + 1])

        if episode >= window_size - 1:
            moving_avg = moving_average(scores[: episode + 1], window_size)
            avg_line.set_data(np.arange(window_size - 1, episode + 1), moving_avg)

        # Adjust y-axis limits if needed
        ax1.set_ylim(
            np.min(scores[: episode + 1]) - 1, np.max(scores[: episode + 1]) + 1
        )
        if episode >= window_size - 1:
            ax2.set_ylim(np.min(moving_avg) - 1, np.max(moving_avg) + 1)

        fig.canvas.draw()
        fig.canvas.flush_events()

        if episode % 10 == 0:
            print(f"Episode: {episode}, Score: {total_reward}")
            torch.cuda.empty_cache()

    plt.ioff()  # Turn off interactive mode

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save final plots
    plt.savefig(f"{results_dir}/training_progress_{timestamp}.png")

    # Save model
    torch.save(
        {
            "model_state_dict": agent.policy.state_dict(),
            "optimizer_state_dict": agent.optimizer.state_dict(),
            "scores": scores,
            "entropy_coef": current_entropy_coef,
        },
        f"{results_dir}/shrine_agent_{timestamp}.pth",
    )

    print(f"Training completed. Results saved with timestamp: {timestamp}")

    # Print final statistics
    print(
        f"Average score over last {window_size} episodes: {np.mean(scores[-window_size:]):.2f}"
    )
    print(f"Best score: {np.max(scores):.2f}")
    print(f"Success rate: {sum(success_history)/len(success_history)*100:.1f}%")
    print(f"Final entropy coefficient: {current_entropy_coef:.6f}")

    plt.show()  # Keep the final plot window open


if __name__ == "__main__":
    main()
