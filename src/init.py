"""
Initialize pygame and load assets.
"""

import pygame
from pathlib import Path

pygame.init()


class Fonts:
    def monogram_extended(self, size: int) -> pygame.font.Font:
        return pygame.font.Font("assets/fonts/monogram_extended.ttf", size)

    def monogram_extended_italic(self, size: int) -> pygame.font.Font:
        return pygame.font.Font("assets/fonts/monogram_extended_italic.ttf", size)


class Backgrounds:
    def moon_sky(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/backgrounds/moon_sky.png", namehint)


class UI:
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


class Images:
    def __init__(self):
        self.backgrounds = Backgrounds()
        self.ui = UI()


class Sounds:
    def ambient_evening(self) -> Path:
        return Path("assets/sounds/ambient_evening.mp3")

    def button_click_1(self) -> Path:
        return Path("assets/sounds/button_click_1.mp3")


class Assets:
    def __init__(self):
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
