import os
import pygame
from game.assets import Assets
from game.surface import SurfaceManager
from game.surfaces.root import RootSurface
from game.surfaces.pause import PauseSurface
from game.surfaces.settings import SettingsSurface
from game.surfaces._1_summer_break_choice import SummerBreakChoiceSurface


def setup_surface_patcher():
    """
    Set up hmr patching by tracking file modifications in the game/surfaces directory.
    """

    last_modified = {}
    for root, _, files in os.walk("game/surfaces"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                last_modified[path] = os.path.getmtime(path)
    return last_modified


def patch_surface_on_hmr(manager, last_modified):
    """
    Check for file changes in the game/surfaces directory and reinitialize modified surfaces.
    """

    for path, mtime in last_modified.items():
        if os.path.getmtime(path) > mtime:
            manager.reinitialize_surface_from_path(path)
            last_modified[path] = os.path.getmtime(path)


def main():
    pygame.init()
    assets = Assets()
    info = pygame.display.Info()
    surface = pygame.display.set_mode(
        (info.current_w, info.current_h), pygame.FULLSCREEN
    )

    manager = SurfaceManager(surface, assets)
    manager.surfaces["root"] = RootSurface(surface, assets, manager)
    manager.surfaces["settings"] = SettingsSurface(surface, assets, manager)
    manager.surfaces["pause"] = PauseSurface(surface, assets, manager)
    manager.surfaces["summer_break_choice"] = SummerBreakChoiceSurface(
        surface, assets, manager
    )
    manager.set_active_surface("root")

    running = True
    clock = pygame.time.Clock()
    last_modified = setup_surface_patcher()

    while running:
        patch_surface_on_hmr(manager, last_modified)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update()
        manager.draw()
        clock.tick(60)

    pygame.quit()
