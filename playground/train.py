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
    """
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)

    # Create results directory
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # Initialize environment and agent
    env = ReinforcedShrineAdventureEnv()
    agent = ShrineAgent(state_size=None, action_size=4)

    # Training parameters
    num_episodes = 1000

    # Set up live plotting
    plt.ion()  # Turn on interactive mode
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

    # Set initial axis limits to prevent autoscaling delays
    ax1.set_xlim(0, num_episodes)
    ax1.set_ylim(-5, 5)  # Adjust based on expected score range
    ax2.set_xlim(0, num_episodes)
    ax2.set_ylim(-5, 5)  # Adjust based on expected score range

    window_size = 10  # Smaller window for more frequent updates
    scores = np.zeros(num_episodes, dtype=np.float16)
    moving_avg = np.array([], dtype=np.float16)

    # Train the agent
    print("Starting training...")
    for episode in range(num_episodes):
        observation, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            action, log_prob, value = agent.act(observation)
            next_observation, reward, done, _, _ = env.step(action)

            agent.memory.add(
                observation,
                action,
                reward,
                next_observation,
                done,
                log_prob,
                value.item(),
            )

            total_reward += reward
            observation = next_observation

            if len(agent.memory.states) >= agent.batch_size:
                agent.update()

        if len(agent.memory.states) > 0:
            agent.update()

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
        },
        f"{results_dir}/shrine_agent_{timestamp}.pth",
    )

    print(f"Training completed. Results saved with timestamp: {timestamp}")

    # Print final statistics
    print(
        f"Average score over last {window_size} episodes: {np.mean(scores[-window_size:]):.2f}"
    )
    print(f"Best score: {np.max(scores):.2f}")

    plt.show()  # Keep the final plot window open


if __name__ == "__main__":
    main()
