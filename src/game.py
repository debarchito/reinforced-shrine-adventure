import pygame

pygame.init()

dt = 0 # delta time aka time passed since last frame
is_running = True
is_fullscreen = False

display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w - 100, display_info.current_h - 100

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
