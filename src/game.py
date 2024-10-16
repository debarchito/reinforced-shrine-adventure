import pygame
from utils import render_text_with_effects
from init import Assets
from components.button import Button

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

# Create the start button using the Button class
start_button = Button(
    normal_image=pygame.transform.scale(assets.images.ui.button_start(), (200, 100)),
    hover_image=pygame.transform.scale(assets.images.ui.button_start_hover(), (200, 100)),
    position=(screen.get_width() // 2, screen.get_height() * 0.6),
    on_click=lambda: print("Button clicked!")
)

def handle_events(is_fullscreen: bool) -> tuple[bool, bool]:
    global background, screen
    is_running = True

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
            start_button.rect.center = (
                screen.get_width() // 2,
                int(screen.get_height() * 0.6),
            )

        start_button.handle_event(event)

    return is_running, is_fullscreen


def main():
    clock = pygame.time.Clock()
    is_running, is_fullscreen = True, False

    while is_running:
        is_running, is_fullscreen = handle_events(is_fullscreen)
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

        start_button.update()
        start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
