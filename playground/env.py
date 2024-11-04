import gymnasium as gym
from gymnasium import spaces
from bink.story import story_from_file


class ReinforcedShrineAdventureEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(ReinforcedShrineAdventureEnv, self).__init__()
        self.story = story_from_file("../story/json/story.ink.json")
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict(
            {
                "text": spaces.Text(max_length=2000),
                "choices": spaces.Sequence(spaces.Text(max_length=20)),
                "stats": spaces.Box(low=-5, high=5, shape=(4,)),
                "items": spaces.MultiBinary(3),
            }
        )
        self.stats = {"curiosity": 0, "social": 0, "caution": 0, "supernatural": 0}
        self.items = {
            "has_talisman": False,
            "has_snacks": False,
            "has_first_aid_kit": False,
        }
        self.took_beach_path = True
        self.reset()

    def update_variables_from_choice(self, choice_text: str):
        """Update variables based on choice text and context"""
        if "Accept talisman" in choice_text:
            self.items["has_talisman"] = True
            self.stats["supernatural"] += 2
            self.stats["social"] += 1
        elif "Agree to pack snacks" in choice_text:
            self.items["has_snacks"] = True
            self.stats["social"] += 2
        elif "Accept the responsibility" in choice_text:
            self.items["has_first_aid_kit"] = True
            self.stats["caution"] += 2
            self.stats["social"] += 1

        if "Take the mountain path" in choice_text:
            self.took_beach_path = False
        elif (
            "Play it safe" in choice_text
            or "Follow the original beach route" in choice_text
        ):
            self.took_beach_path = True
            self.stats["caution"] += 1

    def calculate_reward(self) -> float:
        """Calculate reward based on current state"""
        reward = 0.0

        if self.done:
            reward += 1.0

        if self.items["has_talisman"]:
            reward += 0.5
        if self.items["has_snacks"]:
            reward += 0.5
        if self.items["has_first_aid_kit"]:
            reward += 0.5

        if self.stats["caution"] >= 2:
            reward += 0.5

        if not self.took_beach_path:
            prepared = (
                self.items["has_talisman"]
                and self.items["has_first_aid_kit"]
                and self.stats["caution"] >= 2
            )
            if prepared:
                reward += 2.0
            else:
                reward -= 1.0

        return reward

    def step(self, action):
        if action >= len(self.current_choices):
            raise ValueError(f"Invalid action {action}")

        choice_text = self.current_choices[action]
        self.story.choose_choice_index(action)
        self.update_variables_from_choice(choice_text)
        self.current_text = ""
        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]
        self.done = len(self.current_choices) == 0
        reward = self.calculate_reward()
        observation = {
            "text": self.current_text,
            "choices": self.current_choices,
            "stats": [
                self.stats["curiosity"],
                self.stats["social"],
                self.stats["caution"],
                self.stats["supernatural"],
            ],
            "items": [
                self.items["has_talisman"],
                self.items["has_snacks"],
                self.items["has_first_aid_kit"],
            ],
        }

        return observation, reward, self.done, False, {}

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.story = story_from_file("../story/json/story.ink.json")
        self.done = False
        self.current_text = ""
        self.stats = {key: 0 for key in self.stats}
        self.items = {key: False for key in self.items}
        self.took_beach_path = True

        while self.story.can_continue():
            self.current_text += self.story.cont() + "\n"
        self.current_choices = [choice for choice in self.story.get_current_choices()]

        observation = {
            "text": self.current_text,
            "choices": self.current_choices,
            "stats": [0, 0, 0, 0],
            "items": [False, False, False],
        }

        return observation, {}

    def render(self, mode="human"):
        print("\nCurrent text:")
        print(self.current_text)
        print("\nStats:", self.stats)
        print("Items:", self.items)
        print("\nAvailable choices:")
        for i, choice in enumerate(self.current_choices):
            print(f"{i}: {choice}")
