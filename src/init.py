"""
Initialize pygame and load assets.
"""

import pygame
from enum import Enum
from pathlib import Path
from typing import cast

pygame.init()
info = pygame.display.Info()

class Assets(Enum):
    BACKGROUND_MOON_SKY = (
        "assets/images/backgrounds/moon_sky.png",
        "image",
        (info.current_w - 100, info.current_h - 100),
    )
    FONT_MONOGRAM_EXTENDED = ("assets/fonts/monogram-extended.ttf", "font", 100)
    SOUND_AMBIENT_EVENING = ("assets/sounds/ambient_evening.mp3", "sound")
    BUTTON_START_NORMAL = ("assets/images/ui/button_start.png", "image", (200, 100))
    BUTTON_START_HOVER = (
        "assets/images/ui/button_start_hover.png",
        "image",
        (200, 100),
    )

    def __init__(self, path: str, asset_type: str, *args: tuple) -> None:
        self.path = Path(path)
        self.asset_type = asset_type
        self.args = args
        self.asset = self.load_asset()

    def load_asset(self) -> pygame.Surface | pygame.font.Font | Path | None:
        """
        Loads the asset, given the asset type and arguments.
        """

        if self.asset_type == "image":
            image = pygame.image.load(self.path)
            return pygame.transform.scale(image, self.args[0]) if self.args else image
        elif self.asset_type == "font":
            return pygame.font.Font(self.path, cast(tuple[int], self.args)[0])
        elif self.asset_type == "sound":
            # Sounds should be loaded manually
            return self.path
        return None
