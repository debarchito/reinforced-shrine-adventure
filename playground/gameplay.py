import torch
import os
from env import ReinforcedShrineAdventureEnv
from agent import ShrineAgent


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_latest_model(results_dir):
    # Find the latest model file
    model_files = [f for f in os.listdir(results_dir) if f.endswith(".pth")]
    if not model_files:
        raise FileNotFoundError("No trained models found in results directory")

    latest_model = max(
        model_files, key=lambda x: os.path.getctime(os.path.join(results_dir, x))
    )
    model_path = os.path.join(results_dir, latest_model)

    print(f"Loading model: {latest_model}")
    return torch.load(model_path)


def play_game():
    # Initialize environment and agent
    env = ReinforcedShrineAdventureEnv()
    agent = ShrineAgent(state_size=None, action_size=4)

    # Load the trained model
    checkpoint = load_latest_model("results")
    agent.qnetwork.load_state_dict(checkpoint["model_state_dict"])
    agent.epsilon = 0  # No exploration during gameplay

    # Start game
    observation, _ = env.reset()
    total_reward = 0
    done = False
    choices_made = []  # Keep track of choices

    while not done:
        clear_screen()
        print("\n=== Shrine Adventure ===\n")

        # Display current game state
        print(observation["text"])
        print(
            "\nStats:",
            {
                k: v
                for k, v in zip(
                    ["curiosity", "social", "caution", "supernatural"],
                    observation["stats"],
                )
            },
        )
        print(
            "Items:",
            {
                k: v
                for k, v in zip(
                    ["talisman", "snacks", "first_aid_kit"], observation["items"]
                )
            },
        )
        print("\nChoices:")
        for i, choice in enumerate(observation["choices"]):
            print(f"{i}: {choice}")

        # Get agent's action
        action = agent.act(observation)
        chosen_text = observation["choices"][action]
        choices_made.append(chosen_text)  # Record the choice
        print(f"\nAgent chooses: {chosen_text}")

        # Wait for user to press enter
        input("\nPress Enter to continue...")

        # Take step
        next_observation, reward, done, _, _ = env.step(action)
        total_reward += reward
        observation = next_observation

    # Game over
    clear_screen()
    print("\n=== Game Over ===\n")
    print(observation["text"])
    print(f"\nFinal reward: {total_reward}")

    # Display all choices made
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
