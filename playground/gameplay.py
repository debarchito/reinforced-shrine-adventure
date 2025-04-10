"""
Interactive gameplay module for running the trained agent.

Provides functionality to:
- Load trained model checkpoints
- Run interactive gameplay sessions
- Display game state and agent decisions
- Track choices and statistics

The gameplay loop:
1. Loads the latest trained model
2. Initializes environment and agent
3. Runs interactive episodes with user input between steps
4. Displays game text, choices and agent decisions
5. Records and shows history of choices made

Uses numpy arrays for efficient state tracking and statistics.
"""

import torch
import os
import numpy as np
from env import ReinforcedShrineAdventureEnv
from agent import ShrineAgent


def clear_screen():
    """Clear the terminal screen based on OS."""
    os.system("cls" if os.name == "nt" else "clear")


def load_latest_model(results_dir):
    """Load the most recently saved model checkpoint.

    Args:
        results_dir: Directory containing model checkpoints

    Returns:
        Loaded model checkpoint dictionary

    Raises:
        FileNotFoundError: If no checkpoint files found
    """
    # Find the latest model file
    model_files = [f for f in os.listdir(results_dir) if f.endswith(".pth")]
    if not model_files:
        raise FileNotFoundError("No trained models found in results directory")

    latest_model = max(
        model_files, key=lambda x: os.path.getctime(os.path.join(results_dir, x))
    )
    model_path = os.path.join(results_dir, latest_model)

    print(f"Loading model: {latest_model}")
    return torch.load(model_path, weights_only=False)


def play_game():
    """Run an interactive gameplay session with the trained agent.

    Initializes environment and agent, loads trained model,
    and runs the game loop with user input between steps.
    Tracks and displays game state, choices and statistics.

    Uses numpy arrays for efficient state management.
    """
    # Initialize environment and agent
    env = ReinforcedShrineAdventureEnv()
    agent = ShrineAgent(state_size=773, action_size=4)

    # Load the trained model
    checkpoint = load_latest_model("results")
    agent.policy.load_state_dict(checkpoint["model_state_dict"])

    # Start game
    observation, _ = env.reset()
    total_reward = 0
    done = False
    truncated = False
    choices_made = np.array([], dtype=str)  # Track choices as numpy array

    while not done and not truncated:
        clear_screen()
        print("\n=== Shrine Adventure ===\n")

        # Display current game state
        print(observation["text"])

        # Display items
        item_names = ["talisman", "flashlight", "water", "first_aid_kit", "snacks"]
        items = observation["items"]
        print("\nItems:", {name: bool(val) for name, val in zip(item_names, items)})

        print("\nChoices:")
        for i, choice in enumerate(observation["choices"]):
            print(f"{i}: {choice}")

        # Get agent's action
        action, _, _ = agent.act(observation)
        chosen_text = observation["choices"][action]
        choices_made = np.append(choices_made, chosen_text)  # Record choice
        print(f"\nAgent chooses: {chosen_text}")

        # Wait for user input
        input("\nPress Enter to continue...")

        # Take step
        next_observation, reward, done, truncated, _ = env.step(action)
        total_reward += reward
        observation = next_observation

        if reward != 0:
            print(f"\nReward: {reward}")

    # Game over
    clear_screen()
    print("\n=== Game Over ===\n")
    print(observation["text"])
    print(f"\nFinal reward: {total_reward}")

    # Display choice history
    print("\nChoices made throughout the game:")
    for i, choice in enumerate(choices_made, 1):
        print(f"-> Choice {i}: {choice}")


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
