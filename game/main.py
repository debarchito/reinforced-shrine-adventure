import os
import pygame
from game.assets import Assets
from game.surface import SurfaceManager
from game.surfaces.root import RootSurface
from game.surfaces.pause import PauseSurface
from game.surfaces.settings import SettingsSurface
from game.surfaces.question import QuestionSurface
from game.surfaces._2_packing import PackingSurface
from game.surfaces._3_walk_to_gate import WalkToGateSurface
from game.surfaces._1_summer_break_choice import SummerBreakChoiceSurface
from game.surfaces.end_credits import EndCreditsSurface


def setup_surface_patcher() -> dict[str, float]:
    """Set up hmr patching by tracking file modifications in the game/surfaces directory."""
    last_modified = {}
    for root, _, files in os.walk("game/surfaces"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                last_modified[path] = os.path.getmtime(path)

    return last_modified


def patch_surface_on_hmr(
    manager: SurfaceManager, last_modified: dict[str, float]
) -> None:
    """Check for file changes in the game/surfaces directory and reinitialize modified surfaces."""
    for path, mtime in last_modified.items():
        current_mtime = os.path.getmtime(path)
        if current_mtime > mtime:
            manager.reinitialize_surface_from_path(path)
            last_modified[path] = current_mtime


def main() -> None:
    """Initialize and run the game loop."""
    pygame.init()
    assets = Assets()
    info = pygame.display.Info()
    surface = pygame.display.set_mode(
        (info.current_w, info.current_h),
        pygame.FULLSCREEN | pygame.SCALED
    )

    # Initialize the surface manager and surfaces
    manager = SurfaceManager(surface, assets)
    surfaces = {
        "root": RootSurface,
        "settings": SettingsSurface,
        "pause": PauseSurface,
        "summer_break_choice": SummerBreakChoiceSurface,
        "packing": PackingSurface,
        "walk_to_gate": WalkToGateSurface,
        "question": QuestionSurface,
        "end_credits": EndCreditsSurface,
    }

    # Initialize all surfaces at once
    manager.surfaces = {
        name: surface_class(surface, assets, manager)
        for name, surface_class in surfaces.items()
    }
    manager.set_active_surface_by_name("root")

    # Game loop variables
    running = True
    clock = pygame.time.Clock()
    last_modified = setup_surface_patcher()

    while running:
        patch_surface_on_hmr(manager, last_modified)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            manager.on_event(event)

        manager.update()
        manager.draw()
        clock.tick(60)

    pygame.quit()
