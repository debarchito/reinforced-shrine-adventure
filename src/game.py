import pygame
from init import Assets
from surface import SurfaceManager
from surfaces.root import RootSurface
from surfaces.settings import SettingsSurface


def main():
    assets = Assets()
    surface = pygame.display.set_mode((0, 0))

    manager = SurfaceManager(surface)
    root_surface = RootSurface(surface, assets, manager)
    settings_surface = SettingsSurface(surface, assets, manager)
    manager.add_surface("root", root_surface)
    manager.add_surface("settings", settings_surface)
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
