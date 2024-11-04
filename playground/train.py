import torch
import numpy as np
from env import ReinforcedShrineAdventureEnv
from agent import ShrineAgent
import matplotlib.pyplot as plt
from datetime import datetime
import os


def plot_scores(scores, filename):
    """Plot and save the training scores."""
    plt.figure(figsize=(10, 5))
    plt.plot(scores)
    plt.title("Training Scores over Episodes")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.savefig(filename)
    plt.close()


def moving_average(data, window_size=100):
    """Calculate the moving average of the data."""
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


def main():
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
    num_episodes = 100

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

    scores = []
    window_size = 10  # Smaller window for more frequent updates

    # Train the agent
    print("Starting training...")
    for episode in range(num_episodes):
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

        # Update live plots every episode
        scores_line.set_data(range(len(scores)), scores)

        # Calculate and update moving average
        if len(scores) >= window_size:
            moving_avgs = moving_average(scores, window_size)
            avg_line.set_data(range(window_size - 1, len(scores)), moving_avgs)

        # Adjust y-axis limits if needed
        if len(scores) > 0:
            ymin = min(min(scores), -5)
            ymax = max(max(scores), 5)
            ax1.set_ylim(ymin - 0.5, ymax + 0.5)
            if len(scores) >= window_size:
                ax2.set_ylim(ymin - 0.5, ymax + 0.5)

        # Force redraw
        fig.canvas.draw()
        fig.canvas.flush_events()

        if episode % 10 == 0:
            print(
                f"Episode: {episode}, Score: {total_reward}, Epsilon: {agent.epsilon:.2f}"
            )
            torch.cuda.empty_cache()

    plt.ioff()  # Turn off interactive mode

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save final plots
    plt.savefig(f"{results_dir}/training_progress_{timestamp}.png")

    # Save model
    torch.save(
        {
            "model_state_dict": agent.qnetwork.state_dict(),
            "optimizer_state_dict": agent.optimizer.state_dict(),
            "scores": scores,
            "epsilon": agent.epsilon,
        },
        f"{results_dir}/shrine_agent_{timestamp}.pth",
    )

    print(f"Training completed. Results saved with timestamp: {timestamp}")

    # Print final statistics
    print(f"Final epsilon value: {agent.epsilon:.4f}")
    print(
        f"Average score over last {window_size} episodes: {np.mean(scores[-window_size:]):.2f}"
    )
    print(f"Best score: {max(scores):.2f}")

    plt.show()  # Keep the final plot window open


if __name__ == "__main__":
    main()
