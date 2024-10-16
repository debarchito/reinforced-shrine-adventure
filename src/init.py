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

    def button_start_pressed(self, namehint: str = "") -> pygame.Surface:
        return pygame.image.load("assets/images/ui/button_start_pressed.png", namehint)


class Images:
    def __init__(self):
        self.backgrounds = Backgrounds()
        self.ui = UI()


class Sounds:
    def ambient_evening(self) -> Path:
        return Path("assets/sounds/ambient_evening.mp3")


class Assets:
    def __init__(self):
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
