import os
import re
import sys
import pygame
import importlib
from abc import ABC, abstractmethod
from typing import Optional
from game.asset import Assets


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

    def __init__(self, display_surface: pygame.Surface, assets: Assets):
        self.display_surface = display_surface
        self.assets = assets
        self.surfaces: dict[str, Surface] = {}
        self.last_active_surface: Optional[Surface] = None
        self.active_surface: Optional[Surface] = None
        self.current_global_sfx_volume = 1.0
        self.sfx_sound_objects: list[pygame.mixer.Sound] = []

    def add_surface(self, name: str, surface: Surface) -> None:
        """Add a surface to the manager."""

        self.surfaces[name] = surface

    def set_active_surface(self, name: str) -> None:
        """Switch the active surface by name."""

        if self.active_surface:
            self.active_surface.deactivate()
            self.last_active_surface = self.active_surface
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

    def reinitialize_surfaces(self):
        """Reinitialize all surfaces."""

        for name, surface in self.surfaces.items():
            new_surface = surface.__class__(self.display_surface, self.assets, self)  # type: ignore
            self.surfaces[name] = new_surface

            if self.active_surface == surface:
                self.set_active_surface(name)

    def reinitialize_surface(self, path: str) -> None:
        """Reinitialize a specific surface based on the changed file path."""
        print(f"Detected change in {path}. Reloading module...")

        module_name = os.path.normpath(path).replace(os.path.sep, ".")
        module_name = module_name.rsplit(".", 1)[0]

        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

        surface_name = re.sub(r"^_\d+_", "", os.path.basename(path).rsplit(".", 1)[0])
        if surface_name.lower() in self.surfaces:
            class_name = "".join(part.title() for part in surface_name.split("_"))
            surface_class = getattr(sys.modules[module_name], f"{class_name}Surface")
            self.surfaces[surface_name] = surface_class(
                self.display_surface, self.assets, self
            )
            print(f"Reinitialized {surface_name} surface")

            if (
                self.active_surface.__class__.__name__
                == self.surfaces[surface_name].__class__.__name__
            ):
                self.set_active_surface(surface_name)

    def set_global_sfx_volume(self, volume: float) -> None:
        """Set the global volume for music."""

        self.current_global_sfx_volume = volume
        for sound in self.sfx_sound_objects:
            sound.set_volume(volume)
