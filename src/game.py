import pygame
from src.init import Assets
from src.surface import SurfaceManager
from src.surfaces.root import RootSurface
from src.surfaces.settings import SettingsSurface


def main():
    assets = Assets()
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    manager = SurfaceManager(surface, assets)
    manager.add_surface("root", RootSurface(surface, assets, manager))
    manager.add_surface("settings", SettingsSurface(surface, assets, manager))
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
