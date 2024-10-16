import pygame

pygame.init()

dt = 0 # delta time aka time passed since last frame
is_running = True
is_fullscreen = False
assets = {
    "bg_moon_sky": "assets/images/backgrounds/moon_sky.png",
    "font_monogram_extended": "assets/fonts/monogram-extended.ttf",
    "sound_ambient_evening": "assets/sounds/ambient_evening.mp3"
}

display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w - 100, display_info.current_h - 100

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.image.load(assets["bg_moon_sky"])
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

font = pygame.font.Font(assets["font_monogram_extended"], 86)
text_surface = font.render("Reinforced Shrine Adventure", True, (255, 255, 255))
text_pos = ((screen_width - text_surface.get_width()) / 2, (screen_height - text_surface.get_height()) / 2)

pygame.mixer.music.load(assets["sound_ambient_evening"])
pygame.mixer.music.play(-1)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                screen_width, screen_height = screen.get_size()
            else:
                screen = pygame.display.set_mode((display_info.current_w - 100, display_info.current_h - 100))
                screen_width, screen_height = screen.get_size()
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            text_pos = ((screen_width - text_surface.get_width()) / 2, (screen_height - text_surface.get_height()) / 2)

    screen.blit(background_image, (0, 0))
    screen.blit(text_surface, text_pos)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
