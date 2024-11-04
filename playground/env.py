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
        # Match action space to agent's actor network output size
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict(
            {
                "text": spaces.Text(max_length=2000),
                "choices": spaces.Sequence(spaces.Text(max_length=100)),
                # Match stats/items dimensions to agent's input expectations
                "stats": spaces.Box(
                    low=np.array([self.MIN_STAT] * 4),
                    high=np.array([self.MAX_STAT] * 4),
                    dtype=np.float16,  # Match agent's tensor dtype
                ),
                "items": spaces.Box(
                    low=np.array([0] * 3),
                    high=np.array([1] * 3),
                    dtype=np.float16,  # Match agent's tensor dtype
                ),
            }
        )

        self.stats = {"curiosity": 0, "social": 0, "caution": 0, "supernatural": 0}

        self.items = {
            "has_talisman": False,
            "has_snacks": False,
            "has_first_aid_kit": False,
            "has_first_aid_kit": False,
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

        if "Accept talisman" in choice_text:
            self.items["has_talisman"] = True
            self.update_stat("supernatural", 2)
            self.update_stat("social", 1)
            reward_mod += 1.0

        elif "Agree to pack snacks" in choice_text:
            self.items["has_snacks"] = True
            self.update_stat("social", 2)
            reward_mod += 1.0

        elif "Accept the responsibility" in choice_text:
            self.items["has_first_aid_kit"] = True
            self.update_stat("caution", 2)
            self.update_stat("social", 1)
            reward_mod += 1.0

        elif any(
            word in choice_text.lower()
            for word in ["decline", "reject", "ignore", "leave"]
        ):
            reward_mod -= 0.5

        if "Take the mountain path" in choice_text:
            self.took_beach_path = False
            if self.is_well_prepared():
                reward_mod += 1.0
            else:
                reward_mod -= 0.5

        elif (
            "Play it safe" in choice_text
            or "Follow the original beach route" in choice_text
        ):
            self.took_beach_path = True
            self.update_stat("caution", 1)
            reward_mod += 0.3

        if any(
            word in choice_text.lower()
            for word in ["explore", "investigate", "talk", "help", "join"]
        ):
            reward_mod += 0.5

        return reward_mod

    def is_well_prepared(self):
        return (
            self.items["has_talisman"]
            and self.items["has_snacks"]
            and self.items["has_first_aid_kit"]
            and self.stats["caution"] >= 2
        )

    def calculate_reward(self, choice_reward: float = 0.0) -> float:
        """Calculate reward based on current state"""
        reward = choice_reward * 2.0  # Amplify immediate choice rewards

        if self.done:
            if self.is_well_prepared():
                reward += 10.0  # Increase terminal reward for good preparation
            else:
                reward -= 5.0  # Penalize more for poor preparation

            items_bonus = sum(self.items.values()) * 2.0  # Double item bonus
            reward += items_bonus

            stats_avg = sum(self.stats.values()) / len(self.stats)
            if stats_avg >= 1:
                reward += 2.0
            if stats_avg >= 2:
                reward += 4.0
            if stats_avg >= 3:
                reward += 8.0  # Add extra tier for higher stats

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
