import os
import pygame
from game.asset import Assets
from game.surface import SurfaceManager
from game.surfaces.root import RootSurface
from game.surfaces.settings import SettingsSurface


def main():
    pygame.init()
    assets = Assets()
    info = pygame.display.Info()
    surface = pygame.display.set_mode(
        (info.current_w, info.current_h), pygame.FULLSCREEN
    )

    manager = SurfaceManager(surface, assets)
    manager.add_surface("root", RootSurface(surface, assets, manager))
    manager.add_surface("settings", SettingsSurface(surface, assets, manager))
    manager.set_active_surface("root")

    clock = pygame.time.Clock()
    running = True

    last_modified = {}
    for root, _, files in os.walk("game/surfaces"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                last_modified[path] = os.path.getmtime(path)

    while running:
        for path, mtime in last_modified.items():
            if os.path.getmtime(path) > mtime:
                manager.reinitialize_surface(path)
                last_modified[path] = os.path.getmtime(path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update()
        manager.draw()
        clock.tick(60)

    pygame.quit()
