import pygame
from utils import render_text_with_effects
from pathlib import Path
from typing import cast
from init import Assets

# Set default background
screen = pygame.display.set_mode(
    cast(pygame.Surface, Assets.BACKGROUND_MOON_SKY.asset).get_size()
)

# Set default music
pygame.mixer.music.load(cast(Path, Assets.SOUND_AMBIENT_EVENING.asset))
pygame.mixer.music.play(-1)

# Create a heading
heading = cast(pygame.font.Font, Assets.FONT_MONOGRAM_EXTENDED.asset).render(
    "Reinforced Shrine Adventure", True, (255, 255, 255)
)
heading_position = (
    (screen.get_width() - heading.get_width()) / 2,
    screen.get_height() * 0.3,
)

# Create a start button
start_button = cast(pygame.Surface, Assets.BUTTON_START_NORMAL.asset).get_rect(
    center=(screen.get_width() // 2, screen.get_height() * 0.6)
)


def handle_events(is_fullscreen: bool) -> tuple[bool, bool, bool]:
    global screen
    is_running, is_hovering = True, False

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
            start_button.center = (
                screen.get_width() // 2,
                int(screen.get_height() * 0.6),
            )
        elif event.type == pygame.MOUSEMOTION:
            is_hovering = start_button.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
            print("Button clicked!")
    return is_running, is_fullscreen, is_hovering


def main():
    clock = pygame.time.Clock()
    is_running, is_fullscreen = True, False

    while is_running:
        is_running, is_fullscreen, is_hovering = handle_events(is_fullscreen)
        screen.blit(Assets.BACKGROUND_MOON_SKY.asset, (0, 0))
        render_text_with_effects(
            screen,
            "Reinforced Shrine Adventure",
            Assets.FONT_MONOGRAM_EXTENDED.asset,
            heading_position,
            (0, 0, 0),
            (100, 100, 100),
            3,
        )
        screen.blit(
            (
                Assets.BUTTON_START_HOVER.asset
                if is_hovering
                else Assets.BUTTON_START_NORMAL.asset
            ),
            start_button,
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
