import pygame
from utils import render_text_with_effects

pygame.init()

assets = {
    # backgrounds
    "background_moon_sky": "assets/images/backgrounds/moon_sky.png",
    # fonts
    "font_monogram_extended": "assets/fonts/monogram-extended.ttf",
    "font_monogram_extended_italic": "assets/fonts/monogram-extended-itallic.ttf",
    # sounds
    "sound_ambient_evening": "assets/sounds/ambient_evening.mp3",
    # ui elements
    # buttons
    "button_start": "assets/images/ui/button_start.png",
    "button_start_hover": "assets/images/ui/button_start_hover.png",
    "button_start_pressed": "assets/images/ui/button_start_pressed.png",
}

# Set music
pygame.mixer.music.load(assets["sound_ambient_evening"])
pygame.mixer.music.play(-1) # Play indefinitely

# Sizing and background stuff
display_info = pygame.display.Info()
# Make it fit the screen but not to the edges
screen_width, screen_height = display_info.current_w - 100, display_info.current_h - 100
screen = pygame.display.set_mode((screen_width, screen_height))
# TODO: This is just a placeholder for default background.
# To replace with the actual one in future
background_image = pygame.image.load(assets["background_moon_sky"])
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Buttons
button_start_normal = pygame.image.load(assets["button_start"])
button_start_hover = pygame.image.load(assets["button_start_hover"])
button_start_normal = pygame.transform.scale(button_start_normal, (200, 100))
button_start_hover = pygame.transform.scale(button_start_hover, (200, 100))
button_rect = button_start_normal.get_rect(center=(screen_width // 2, screen_height * 0.6))

# Fonts and texts
font = pygame.font.Font(assets["font_monogram_extended"], 100)
text_surface = font.render("Reinforced Shrine Adventure", True, (255, 255, 255))
text_pos = ((screen_width - text_surface.get_width()) / 2, screen_height * 0.3)
border_color = (0, 0, 0)
shadow_color = (100, 100, 100)
shadow_offset = 3

# Others
is_running = True
is_fullscreen = False
is_hovering = False
clock = pygame.time.Clock()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((display_info.current_w - 100, display_info.current_h - 100))
            screen_width, screen_height = screen.get_size()
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            button_rect.center = (screen_width // 2, screen_height * 0.6)
            text_pos = ((screen_width - text_surface.get_width()) / 2, screen_height * 0.3)

        if event.type == pygame.MOUSEMOTION:
            is_hovering = button_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
            # TODO: Save the state of the game using sqlite
            print("Button clicked!")

    screen.blit(background_image, (0, 0))
    render_text_with_effects(screen, "Reinforced Shrine Adventure", font, text_pos, border_color, shadow_color, shadow_offset)

    if is_hovering:
        screen.blit(button_start_hover, button_rect)
    else:
        screen.blit(button_start_normal, button_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
