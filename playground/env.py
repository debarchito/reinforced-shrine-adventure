"""
Custom Gymnasium environment for text-based adventure game using Ink story format.
Implements a reinforcement learning environment with:
- Text observations with choices
- Stats tracking (curiosity, social, caution, supernatural)
- Item inventory system
- Reward shaping based on choices and outcomes

The environment follows the Gymnasium interface and includes:
- Dict observation space with text, choices, stats and items
- Discrete action space for selecting choices
- Reward calculation based on choices and final outcome
- State tracking for stats, items and story progress

Key features:
- Bounded stats between min/max values
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
    MIN_STAT = -5
    MAX_STAT = 5

    def __init__(self):
        super(ReinforcedShrineAdventureEnv, self).__init__()
        self.story = story_from_file("story/json/story.ink.json")
        # Match action space to max choices in story
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict(
            {
                "text": spaces.Text(max_length=2000),
                "choices": spaces.Sequence(spaces.Text(max_length=100)),
                "stats": spaces.Box(
                    low=np.array([self.MIN_STAT] * 4),
                    high=np.array([self.MAX_STAT] * 4),
                    dtype=np.float16,
                ),
                "items": spaces.Box(
                    low=np.array([0] * 5),  # Updated for 5 items
                    high=np.array([1] * 5),
                    dtype=np.float16,
                ),
            }
        )

        self.stats = {"curiosity": 0, "social": 0, "caution": 0, "supernatural": 0}

        self.items = {
            "has_talisman": False,
            "has_snacks": False,
            "has_first_aid_kit": False,
            "has_water": False,
            "has_flashlight": False,
        }

        self.took_beach_path = True
        self.episode_steps = 0
        self.max_steps = 20
        self.reset()

    def update_stat(self, stat_name: str, change: int):
        """Update a stat while enforcing bounds"""
        current = self.stats[stat_name]
        self.stats[stat_name] = max(self.MIN_STAT, min(self.MAX_STAT, current + change))

    def update_variables_from_choice(self, choice_text: str):
        """Update variables based on choice text and context"""
        reward_mod = 0

        # Social interaction rewards
        if any(
            word in choice_text.lower()
            for word in ["share", "join", "defend", "help", "together"]
        ):
            self.update_stat("social", 1)
            reward_mod += 0.5

        # Curiosity rewards
        if any(
            word in choice_text.lower()
            for word in ["investigate", "research", "explore", "question", "learn"]
        ):
            self.update_stat("curiosity", 1)
            reward_mod += 0.5

        # Item collection rewards
        if "Accept talisman" in choice_text:
            self.items["has_talisman"] = True
            self.update_stat("supernatural", 2)
            self.update_stat("social", 1)
            reward_mod += 1.0

        elif "Pack a flashlight" in choice_text:
            self.items["has_flashlight"] = True
            self.update_stat("caution", 1)
            reward_mod += 0.5

        elif "Pack water" in choice_text:
            self.items["has_water"] = True
            self.update_stat("caution", 1)
            reward_mod += 0.5

        elif "Pack a first aid kit" in choice_text:
            self.items["has_first_aid_kit"] = True
            self.update_stat("caution", 2)
            reward_mod += 1.0

        elif "Pack some snacks" in choice_text:
            self.items["has_snacks"] = True
            self.update_stat("social", 1)
            reward_mod += 0.5

        # Path choice consequences
        if "Take the mountain path" in choice_text:
            self.took_beach_path = False
            if self.is_well_prepared():
                reward_mod += 2.0
            else:
                reward_mod -= 1.0
            self.update_stat("curiosity", 2)

        elif "Follow the original beach route" in choice_text:
            self.took_beach_path = True
            self.update_stat("caution", 1)
            reward_mod += 0.5

        # Negative rewards for avoidance
        if any(
            word in choice_text.lower()
            for word in ["decline", "reject", "ignore", "leave", "refuse"]
        ):
            self.update_stat("social", -1)
            reward_mod -= 0.5

        return reward_mod

    def is_well_prepared(self):
        """Check if player has essential items for safety"""
        return (
            self.items["has_flashlight"]
            and self.items["has_water"]
            and self.items["has_first_aid_kit"]
            and self.stats["caution"] >= 2
        )

    def calculate_reward(self, choice_reward: float = 0.0) -> float:
        """Calculate reward based on current state and path success"""
        # Amplify immediate choice rewards more significantly
        reward = choice_reward * 3.0

        # Reward for interaction and exploration
        if any(
            word in self.current_text.lower()
            for word in ["discovered", "found", "learned"]
        ):
            reward += 1.0

        if self.done:
            # Track successful path completion
            success_multiplier = 2.0 if self.is_well_prepared() else 0.5

            # Base completion reward
            if self.is_well_prepared():
                reward += 15.0  # Increased from 10.0
            else:
                reward -= 8.0  # Increased penalty from 5.0

            # Reward for collected items weighted by success
            items_bonus = sum(self.items.values()) * 3.0 * success_multiplier
            reward += items_bonus

            # Progressive stats rewards weighted by success
            stats_avg = sum(self.stats.values()) / len(self.stats)
            if stats_avg >= 1:
                reward += 3.0 * success_multiplier
            if stats_avg >= 2:
                reward += 6.0 * success_multiplier
            if stats_avg >= 3:
                reward += 12.0 * success_multiplier

        return reward

    def step(self, action):
        self.episode_steps += 1
        truncated = self.episode_steps >= self.max_steps

        if action >= len(self.current_choices):
            return self._get_observation(), -2.0, True, truncated, {}

        choice_text = self.current_choices[action]
        self.story.choose_choice_index(action)
        choice_reward = self.update_variables_from_choice(choice_text)

        self.current_text = ""
        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]

        self.done = len(self.current_choices) == 0 or truncated
        reward = self.calculate_reward(choice_reward)

        return self._get_observation(), reward, self.done, truncated, {}

    def _get_observation(self):
        return {
            "text": self.current_text,
            "choices": self.current_choices,
            "stats": np.array(
                [
                    self.stats["curiosity"],
                    self.stats["social"],
                    self.stats["caution"],
                    self.stats["supernatural"],
                ],
                dtype=np.float16,
            ),  # Match agent's tensor dtype
            "items": np.array(
                [
                    self.items["has_talisman"],
                    self.items["has_snacks"],
                    self.items["has_first_aid_kit"],
                    self.items["has_water"],
                    self.items["has_flashlight"],
                ],
                dtype=np.float16,
            ),  # Match agent's tensor dtype
        }

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.story = story_from_file("story/json/story.ink.json")
        self.done = False
        self.current_text = ""
        self.stats = {key: 0 for key in self.stats}
        self.items = {key: False for key in self.items}
        self.took_beach_path = True
        self.episode_steps = 0

        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]

        return self._get_observation(), {}

    def render(self, mode="human"):
        print("\nCurrent text:")
        print(self.current_text)
        print("\nStats:", self.stats)
        print("Items:", self.items)
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
            print("\n" + "="*50 + "\n")
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

        print("\n" + "="*50)
        print("\nGame Over!")
        print(f"Final Score: {total_reward}")
        print("\nFinal Stats:", self.stats)
        print("Final Items:", self.items)

if __name__ == "__main__":
    # Create and run interactive story
    env = ReinforcedShrineAdventureEnv()
    env.play_story()
