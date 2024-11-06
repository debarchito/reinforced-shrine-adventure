"""
Custom Gymnasium environment for text-based adventure game using Ink story format.
Implements a reinforcement learning environment with:
- Text observations with choices
- Item inventory system
- Reward shaping based on key dialogue moments

The environment follows the Gymnasium interface and includes:
- Dict observation space with text, choices, and items
- Discrete action space for selecting choices
- Reward calculation based on key dialogue moments
- State tracking for items and story progress

Key features:
- Item collection and tracking
- Path choice consequences
- Reward shaping for exploration and preparation
- Episode termination conditions
"""

import gymnasium as gym
from gymnasium import spaces
from bink.story import story_from_file
import numpy as np


class ReinforcedShrineAdventureEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super().__init__()
        self.story = story_from_file("story/json/story.ink.json")
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict(
            {
                "text": spaces.Text(max_length=2000),
                "choices": spaces.Sequence(spaces.Text(max_length=100)),
                "items": spaces.Box(
                    low=np.array([0] * 5),
                    high=np.array([1] * 5),
                    dtype=np.float16,
                ),
            }
        )

        # Only track essential items
        self.items = {
            "has_talisman": False,
            "has_flashlight": False,
            "has_water": False,
            "has_first_aid_kit": False,
            "has_snacks": False,
        }

        self.episode_steps = 0
        self.max_steps = 20
        self.reset()

    def calculate_reward(self) -> float:
        """Calculate reward based on key dialogue moments"""
        reward = 0.0

        # Positive dialogue indicators (showing engagement/interest)
        positive_dialogues = [
            # Summer Break Choice
            "sounds kinda sketchy",
            "i still don't know",
            "if they're super powerful",
            "just thinking about what to pack",
            "better to be prepared,",
        ]

        # Negative dialogue indicators (showing disengagement/avoidance)
        negative_dialogues = [
            # Summer Break Choice
            "can't wait to see what's in there",
            "i'm sorry, but i really can't",
            "safety comes first",
            "ignore the pang of regret",
        ]

        text_lower = self.current_text.lower()

        # Check for positive dialogues
        for dialogue in positive_dialogues:
            if dialogue in text_lower:
                reward += 5.0

        # Check for negative dialogues
        for dialogue in negative_dialogues:
            if dialogue in text_lower:
                reward -= 5.0

        # Add small positive reward for survival
        if not self.done:
            reward += 0.1

        # Increase preparation rewards
        if self.done:
            if self.is_well_prepared():
                reward += 15.0

        return reward

    def is_well_prepared(self):
        """Check if player has essential items"""
        return (
            self.items["has_talisman"]
            and self.items["has_flashlight"]
            and self.items["has_water"]
            and self.items["has_first_aid_kit"]
        )

    def update_items(self, choice_text: str):
        """Track only essential item acquisitions"""
        if "Accept talisman" in choice_text:
            self.items["has_talisman"] = True
        elif "Pack a flashlight" in choice_text:
            self.items["has_flashlight"] = True
        elif "Pack water" in choice_text:
            self.items["has_water"] = True
        elif "Pack a first aid kit" in choice_text:
            self.items["has_first_aid_kit"] = True
        elif "Pack snacks" in choice_text:
            self.items["has_snacks"] = True

    def step(self, action):
        self.episode_steps += 1
        truncated = self.episode_steps >= self.max_steps

        if action >= len(self.current_choices):
            return self._get_observation(), -1.0, True, truncated, {}

        # Take action and update state
        choice_text = self.current_choices[action]
        self.story.choose_choice_index(action)
        self.update_items(choice_text)

        # Get new text and choices
        self.current_text = ""
        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]

        self.done = len(self.current_choices) == 0 or truncated
        reward = self.calculate_reward()

        return self._get_observation(), reward, self.done, truncated, {}

    def _get_observation(self):
        return {
            "text": self.current_text,
            "choices": self.current_choices,
            "items": np.array(
                [float(v) for v in self.items.values()], dtype=np.float16
            ),
        }

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.story = story_from_file("story/json/story.ink.json")
        self.done = False
        self.current_text = ""
        self.items = {key: False for key in self.items}
        self.episode_steps = 0

        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]

        return self._get_observation(), {}

    def render(self, mode="human"):
        print("\nCurrent text:")
        print(self.current_text)
        print("\nItems:", self.items)
        print("\nAvailable choices:")
        for i, choice in enumerate(self.current_choices):
            print(f"{i}: {choice}")

    def play_story(self):
        """Run interactive story mode for human players."""
        self.reset()
        done = False
        total_reward = 0

        while not done:
            # Clear screen and show current state
            print("\n" + "=" * 50 + "\n")
            self.render()

            # Get valid player input
            while True:
                try:
                    choice = int(input("\nEnter choice number: "))
                    if 0 <= choice < len(self.current_choices):
                        break
                    print("Invalid choice number. Try again.")
                except ValueError:
                    print("Please enter a valid number.")

            # Take step based on player's choice
            observation, reward, done, truncated, info = self.step(choice)
            total_reward += reward

            if reward != 0:
                print(f"\nReward: {reward}")

        print("\n" + "=" * 50)
        print("\nGame Over!")
        print(f"Final Score: {total_reward}")
        print("Final Items:", self.items)


if __name__ == "__main__":
    # Create and run interactive story
    env = ReinforcedShrineAdventureEnv()
    env.play_story()
