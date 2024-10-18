import pygame
import logging
import traceback
import importlib

# import gc
from abc import ABC, abstractmethod
from typing import Optional
from watchdog.observers import Observer

# from watchdog.events import FileSystemEventHandler
from init import Assets


class Surface(ABC):
    """Abstract base class for all game surfaces."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.is_active = False

    def activate(self) -> None:
        """Activate this surface, making it visible and interactive."""

        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate this surface, pausing its updates and rendering."""

        self.is_active = False

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events specific to this surface."""

        pass

    @abstractmethod
    def update(self) -> None:
        """Update any necessary state for this surface."""

        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw all elements on this surface."""

        pass


class SurfaceManager:
    """Manages different game surfaces, handling their activation and transitions."""

    def __init__(
        self, display_surface: pygame.Surface, assets: Assets, enable_hmr: bool = False
    ):
        self.display_surface = display_surface
        self.assets = assets
        self.surfaces: dict[str, Surface] = {}
        self.active_surface: Optional[Surface] = None
        self.enable_hmr = enable_hmr
        self.observer: Optional[Observer] = None  # type: ignore

        # if enable_hmr:
        #     self.start_hmr()

    def load_surface(self, module_name: str):
        """Dynamically load or reload a surface by module name."""

        logging.info(f"Loading surface: {module_name}")

        try:
            new_module = importlib.import_module(f"surfaces.{module_name}")
            new_module = importlib.reload(new_module)

            surface_class_name = f"{module_name.capitalize()}Surface"
            surface_class = getattr(new_module, surface_class_name, None)

            if surface_class:
                new_surface = surface_class(self.display_surface, self.assets, self)
                self.add_surface(module_name, new_surface)
                logging.info(f"Surface '{module_name}' loaded successfully.")
                return new_surface
            else:
                logging.error(
                    f"No matching class '{surface_class_name}' found in {module_name}."
                )
        except Exception as e:
            logging.error(f"Error loading surface '{module_name}': {e}")
            traceback.print_exc()
            return None

    def add_surface(self, name: str, surface: Surface) -> None:
        """Add a surface to the manager."""

        self.surfaces[name] = surface

    def set_active_surface(self, name: str) -> None:
        """Switch the active surface by name."""

        if self.active_surface:
            self.active_surface.deactivate()
        self.active_surface = self.surfaces.get(name)
        if self.active_surface:
            self.active_surface.activate()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Pass event handling to the active surface only."""

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.handle_event(event)

    def update(self) -> None:
        """Update the active surface only."""

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.update()

    def draw(self) -> None:
        """Draw the active surface onto the display."""

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.draw()
            pygame.display.flip()

    # def start_hmr(self) -> None:
    #     """Start watching for changes in the surfaces folder."""

    #     event_handler = SurfaceHotModuleReplacement(self)
    #     self.observer = Observer()
    #     self.observer.schedule(event_handler, path='./src/surfaces', recursive=False)
    #     self.observer.start()
    #     logging.info("Hot Module Replacement enabled. Watching for file changes...")


# class SurfaceHotModuleReplacement(FileSystemEventHandler):
#     """Handle changes in surface files and reload dynamically."""

#     def __init__(self, surface_manager: SurfaceManager):
#         self.surface_manager = surface_manager
#         self.version_counter: dict[str, int] = {}

#     def on_modified(self, event):
#         if event.src_path.endswith(".py"):
#             module_name = event.src_path.split('/')[-1].replace('.py', '')
#             self.version_counter[module_name] = self.version_counter.get(module_name, 0) + 1
#             current_version = self.version_counter[module_name]
#             logging.info(f"Detected change in {module_name}. Reloading as {module_name}_{current_version}...")

#             new_surface = self.surface_manager.load_surface(module_name)

#             if new_surface:
#                 self.surface_manager.add_surface(f"{module_name}_{current_version}", new_surface)
#                 self.surface_manager.set_active_surface(f"{module_name}_{current_version}")
#                 # self.surface_manager.add_surface(module_name, new_surface)
#                 logging.info(f"Surface '{module_name}_{current_version}' reloaded successfully.")
#             else:
#                 logging.error(f"Failed to reload surface '{module_name}'.")

#             gc.collect()
