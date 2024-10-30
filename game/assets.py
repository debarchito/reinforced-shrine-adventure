"""
Load assets and story (special asset) while providing a type-safe interface to access them.
"""

import pygame
from bink.story import story_from_file


class Fonts:
    """
    Load and provide type-safe access to fonts.
    """

    def monogram_extended(self, size: int) -> pygame.font.Font:
        return pygame.font.Font("assets/fonts/truetype/monogram_extended.ttf", size)

    def monogram_extended_italic(self, size: int) -> pygame.font.Font:
        return pygame.font.Font(
            "assets/fonts/truetype/monogram_extended_italic.ttf", size
        )


class Backgrounds:
    """
    Load and provide type-safe access to background images.
    """

    def moon_sky(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/backgrounds/moon_sky.png", namehint)

    def empty_classroom(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load(
            "assets/images/backgrounds/empty_classroom.jpg", namehint
        )


class UI:
    """
    Load and provide type-safe access to UI elements.
    """

    def button_start(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_start.png", namehint)

    def button_start_hover(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_start_hover.png", namehint)

    def button_start_active(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_start_active.png", namehint)

    def button_cog(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_cog.png", namehint)

    def button_cog_hover(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_cog_hover.png", namehint)

    def button_cog_active(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_cog_active.png", namehint)

    def button_quit(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_quit.png", namehint)

    def button_quit_hover(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_quit_hover.png", namehint)

    def button_quit_active(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_quit_active.png", namehint)

    def button_home(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_home.png", namehint)

    def button_home_hover(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_home_hover.png", namehint)

    def button_home_active(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_home_active.png", namehint)

    def button_arrow_left(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_arrow_left.png", namehint)

    def button_arrow_left_hover(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load(
            "assets/images/ui/button_arrow_left_hover.png", namehint
        )

    def button_arrow_left_active(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load(
            "assets/images/ui/button_arrow_left_active.png", namehint
        )

    def banner_dialogue_wood(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/banner_dialogue_wood.png", namehint)

    def banner_choice_wood(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/banner_choice_wood.png", namehint)


class Images:
    """
    Load and provide type-safe access to images.
    """

    def __init__(self):
        self.backgrounds = Backgrounds()
        self.ui = UI()


class Sounds:
    """
    Load and provide type-safe access to sound effects and music.
    """

    def ambient_evening(self) -> str:
        return "assets/sounds/music/ambient_evening.mp3"

    def button_click_1(self) -> str:
        return "assets/sounds/sfx/button_click_1.mp3"


class Assets:
    """
    Load and provide type-safe access to assets.
    """

    def __init__(self):
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
        self.story = story_from_file("story/json/story.ink.json")
