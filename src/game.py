import pygame
from pathlib import Path
from utils import render_text_with_effects
from enum import Enum
from typing import cast

pygame.init()

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SHADOW = (100, 100, 100)

class Assets(Enum):
    BACKGROUND_MOON_SKY = (
        "assets/images/backgrounds/moon_sky.png",
        "image",
        (pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 100),
    )
    FONT_MONOGRAM_EXTENDED = ("assets/fonts/monogram-extended.ttf", "font", 100)
    SOUND_AMBIENT_EVENING = ("assets/sounds/ambient_evening.mp3", "sound")
    BUTTON_START_NORMAL = ("assets/images/ui/button_start.png", "image", (200, 100))
    BUTTON_START_HOVER = ("assets/images/ui/button_start_hover.png", "image", (200, 100))
    BUTTON_START_PRESSED = ("assets/images/ui/button_start_pressed.png", "image", (200, 100))
    BUTTON_OPTIONS_NORMAL = ("assets/images/ui/button_options.png", "image", (200, 100))
    BUTTON_OPTIONS_HOVER = ("assets/images/ui/button_options_hover.png", "image", (200, 100))
    BUTTON_OPTIONS_PRESSED = ("assets/images/ui/button_options_pressed.png", "image", (200, 100))
    BUTTON_EXIT_NORMAL = ("assets/images/ui/button_exit.png", "image", (200, 100))
    BUTTON_EXIT_HOVER = ("assets/images/ui/button_exit_hover.png", "image", (200, 100))
    BUTTON_EXIT_PRESSED = ("assets/images/ui/button_exit_pressed.png", "image", (200, 100))
    BUTTON_SETTINGS_NORMAL = ("assets/images/ui/button_settings.png", "image", (200, 100))
    BUTTON_SETTINGS_HOVER = ("assets/images/ui/button_settings_hover.png", "image", (200, 100))
    BUTTON_SETTINGS_PRESSED = ("assets/images/ui/button_settings_pressed.png", "image", (200, 100))
    BUTTON_CREDITS_NORMAL = ("assets/images/ui/button_credits.png", "image", (200, 100))
    BUTTON_CREDITS_HOVER = ("assets/images/ui/button_credits_hover.png", "image", (200, 100))
    BUTTON_CREDITS_PRESSED = ("assets/images/ui/button_credits_pressed.png", "image", (200, 100))
    POPUP_IMAGE = ("assets/images/backgrounds/moon_sky.png", "image")  # Replace with actual popup image path
    POPUP_CREDITS_IMAGE = ("assets/images/backgrounds/moon_sky.png", "image")  # Replace with actual credits popup image path

    def __init__(self, path: str, asset_type: str, *args: tuple) -> None:
        self.path = Path(path)
        self.asset_type = asset_type
        self.args = args
        self.asset: pygame.Surface | pygame.font.Font | None = self.load_asset()

    def load_asset(self) -> pygame.Surface | pygame.font.Font | None:
        if self.asset_type == "image":
            image = pygame.image.load(self.path)
            return pygame.transform.scale(image, self.args[0]) if self.args else image
        elif self.asset_type == "font":
            return pygame.font.Font(self.path, self.args[0])  # type: ignore
        elif self.asset_type == "sound":
            pygame.mixer.music.load(self.path)
            return None
        return None

screen = pygame.display.set_mode(
    cast(pygame.Surface, Assets.BACKGROUND_MOON_SKY.asset).get_size()
)
pygame.mixer.music.play(-1)

text_surface = cast(pygame.font.Font, Assets.FONT_MONOGRAM_EXTENDED.asset).render(
    "Reinforced Shrine Adventure", True, Colors.WHITE
)
text_position = (
    (screen.get_width() - text_surface.get_width()) / 2,
    screen.get_height() * 0.3,
)

# Start button position
button_rect = cast(pygame.Surface, Assets.BUTTON_START_NORMAL.asset).get_rect(
    center=(screen.get_width() // 2, screen.get_height() * 0.5)
)

# Positions for the new buttons (horizontal layout)
button_gap = 30  # Space between buttons
button_width = 200  # Width of each button

options_button_rect = cast(pygame.Surface, Assets.BUTTON_OPTIONS_NORMAL.asset).get_rect(
    center=(button_rect.centerx - (button_gap + button_width), button_rect.bottom + 40)
)

settings_button_rect = cast(pygame.Surface, Assets.BUTTON_SETTINGS_NORMAL.asset).get_rect(
    center=(button_rect.centerx, button_rect.bottom + 40)
)

credits_button_rect = cast(pygame.Surface, Assets.BUTTON_CREDITS_NORMAL.asset).get_rect(
    center=(button_rect.centerx + (button_gap + button_width), button_rect.bottom + 40)
)

exit_button_rect = cast(pygame.Surface, Assets.BUTTON_EXIT_NORMAL.asset).get_rect(
    center=(button_rect.centerx + 2 * (button_gap + button_width), button_rect.bottom + 40)
)

# Variable to track popup visibility
popup_visible = False
credits_popup_visible = False


def handle_events(is_fullscreen: bool) -> tuple[bool, bool, bool, bool, bool, bool, bool]:
    global screen, popup_visible, credits_popup_visible
    is_running = True
    is_hovering_start = is_hovering_options = is_hovering_settings = is_hovering_exit = is_hovering_credits = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            screen = (
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                if is_fullscreen
                else pygame.display.set_mode(
                    (
                        pygame.display.Info().current_w - 100,
                        pygame.display.Info().current_h - 100,
                    )
                )
            )
            Assets.BACKGROUND_MOON_SKY.asset = pygame.transform.scale(
                pygame.image.load(Assets.BACKGROUND_MOON_SKY.path), screen.get_size()
            )
            # Update button positions after screen size change
            button_rect.center = (screen.get_width() // 2, int(screen.get_height() * 0.5))
            options_button_rect.center = (button_rect.centerx - (button_gap + button_width), button_rect.bottom + 40)
            settings_button_rect.center = (button_rect.centerx, button_rect.bottom + 40)
            credits_button_rect.center = (button_rect.centerx + (button_gap + button_width), button_rect.bottom + 40)
            exit_button_rect.center = (button_rect.centerx + 2 * (button_gap + button_width), button_rect.bottom + 40)
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            is_hovering_start = button_rect.collidepoint(pos)
            is_hovering_options = options_button_rect.collidepoint(pos)
            is_hovering_settings = settings_button_rect.collidepoint(pos)
            is_hovering_exit = exit_button_rect.collidepoint(pos)
            is_hovering_credits = credits_button_rect.collidepoint(pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            pos = event.pos
            is_hovering_start = button_rect.collidepoint(pos)
            is_hovering_options = options_button_rect.collidepoint(pos)
            is_hovering_settings = settings_button_rect.collidepoint(pos)
            is_hovering_exit = exit_button_rect.collidepoint(pos)
            is_hovering_credits = credits_button_rect.collidepoint(pos)
            if is_hovering_start:
                print("Start button clicked!")
                popup_visible = True  # Show popup for Start
            elif is_hovering_options:
                print("Options button clicked!")
                popup_visible = True  # Show popup for Options
            elif is_hovering_settings:
                print("Settings button clicked!")
                popup_visible = True  # Show popup for Settings
            elif is_hovering_exit:
                print("Exit button clicked!")
                is_running = False  # Close the game when exit button is clicked
            elif is_hovering_credits:
                print("Credits button clicked!")
                credits_popup_visible = True  # Show credits popup

    return is_running, is_fullscreen, is_hovering_start, is_hovering_options, is_hovering_settings, is_hovering_exit, is_hovering_credits


def draw_popups():
    if popup_visible:
        popup_image = Assets.POPUP_IMAGE.asset
        popup_rect = popup_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(popup_image, popup_rect)

    if credits_popup_visible:
        credits_image = Assets.POPUP_CREDITS_IMAGE.asset
        credits_rect = credits_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(credits_image, credits_rect)


def main():
    clock = pygame.time.Clock()
    is_running, is_fullscreen = True, False

    while is_running:
        is_running, is_fullscreen, is_hovering_start, is_hovering_options, is_hovering_settings, is_hovering_exit, is_hovering_credits = handle_events(is_fullscreen)
        screen.blit(Assets.BACKGROUND_MOON_SKY.asset, (0, 0))
        render_text_with_effects(
            screen,
            "Reinforced Shrine Adventure",
            Assets.FONT_MONOGRAM_EXTENDED.asset,
            text_position,
            Colors.BLACK,
            Colors.SHADOW,
            3,
        )

        # Check for hover effects
        mouse_pos = pygame.mouse.get_pos()
        is_hovering_start = button_rect.collidepoint(mouse_pos)
        is_hovering_options = options_button_rect.collidepoint(mouse_pos)
        is_hovering_settings = settings_button_rect.collidepoint(mouse_pos)
        is_hovering_exit = exit_button_rect.collidepoint(mouse_pos)
        is_hovering_credits = credits_button_rect.collidepoint(mouse_pos)

        # Draw buttons
        screen.blit(
            Assets.BUTTON_START_HOVER.asset if is_hovering_start else Assets.BUTTON_START_NORMAL.asset,
            button_rect,
        )
        screen.blit(
            Assets.BUTTON_OPTIONS_HOVER.asset if is_hovering_options else Assets.BUTTON_OPTIONS_NORMAL.asset,
            options_button_rect,
        )
        screen.blit(
            Assets.BUTTON_SETTINGS_HOVER.asset if is_hovering_settings else Assets.BUTTON_SETTINGS_NORMAL.asset,
            settings_button_rect,
        )
        screen.blit(
            Assets.BUTTON_CREDITS_HOVER.asset if is_hovering_credits else Assets.BUTTON_CREDITS_NORMAL.asset,
            credits_button_rect,
        )
        screen.blit(
            Assets.BUTTON_EXIT_HOVER.asset if is_hovering_exit else Assets.BUTTON_EXIT_NORMAL.asset,
            exit_button_rect,
        )

        # Draw the popups if they're visible
        draw_popups()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()