import pygame
import logging
from init import Assets
from surface import SurfaceManager

# from surfaces.root import RootSurface
# from surfaces.settings import SettingsSurface

logging.basicConfig(level=logging.INFO)


def main():
    assets = Assets()
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    manager = SurfaceManager(surface, assets)

    for module_name in ["root", "settings"]:
        manager.load_surface(module_name)

    manager.set_active_surface("root")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update()
        manager.draw()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
