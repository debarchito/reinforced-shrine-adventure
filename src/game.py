import pygame
from utils import render_text_with_effects
from init import Assets

assets = Assets()

info = pygame.display.Info()
font = assets.fonts.monogram_extended(100)
background = pygame.transform.scale(
    assets.images.backgrounds.moon_sky(),
    (info.current_w - 100, info.current_h - 100)
)
sound = assets.sounds.ambient_evening()

# Set default background
screen = pygame.display.set_mode(background.get_size())

# Set default music/sound
pygame.mixer.music.load(sound)
pygame.mixer.music.play(-1)

# Create a heading
heading = font.render(
    "Reinforced Shrine Adventure", True, (255, 255, 255)
)
heading_position = (
    (screen.get_width() - heading.get_width()) / 2,
    screen.get_height() * 0.3,
)

# Load button surfaces
button_normal = pygame.transform.scale(assets.images.ui.button_start(), (200, 100))
button_hover = pygame.transform.scale(assets.images.ui.button_start_hover(), (200, 100))

# Define start button rect and position
start_button_rect = button_normal.get_rect(
    center=(screen.get_width() // 2, int(screen.get_height() * 0.6))
)


def handle_events(is_fullscreen: bool) -> tuple[bool, bool, bool]:
    global background, screen, start_button_rect
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
                        info.current_w - 100,
                        info.current_h - 100,
                    )
                )
            )
            background = pygame.transform.scale(background, screen.get_size())
            start_button_rect.center = (
                screen.get_width() // 2,
                int(screen.get_height() * 0.6),
            )
        elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
            print("Button clicked!")

    is_hovering = start_button_rect.collidepoint(pygame.mouse.get_pos())

    return is_running, is_fullscreen, is_hovering


def main():
    clock = pygame.time.Clock()
    is_running, is_fullscreen = True, False

    while is_running:
        is_running, is_fullscreen, is_hovering = handle_events(is_fullscreen)
        screen.blit(background, (0, 0))

        render_text_with_effects(
            screen,
            "Reinforced Shrine Adventure",
            font,
            heading_position,
            (0, 0, 0),
            (100, 100, 100),
            3,
        )

        screen.blit(button_hover if is_hovering else button_normal, start_button_rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
