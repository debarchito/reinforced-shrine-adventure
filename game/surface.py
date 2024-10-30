"""
Provide base classes for game surfaces, manage surfaces, and provide a type-safe interface to interact with them.
"""

import os
import re
import sys
import pygame
import importlib
from game.assets import Assets
from typing import Optional, cast
from abc import ABC, abstractmethod


class Surface(ABC):
    """
    Base class for all game surfaces.
    """

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.is_active = False

    def activate(self) -> None:
        """
        Activate this surface, making it visible and interactive.
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deactivate this surface, pausing its updates and rendering.
        """

        self.is_active = False

    def hook(self) -> None:
        """
        Hook up any necessary components for this surface.
        """

        ...

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle events specific to this surface.
        """

        ...

    @abstractmethod
    def update(self) -> None:
        """
        Update any necessary state for this surface.
        """

        ...

    @abstractmethod
    def draw(self) -> None:
        """
        Draw elements on this surface.
        """

        ...


class SurfaceManager:
    """
    Manages different game surfaces, handling their activation and transitions.
    """

    def __init__(self, display_surface: pygame.Surface, assets: Assets):
        self.display_surface = display_surface
        self.assets = assets
        self.surfaces: dict[str, Surface] = {}
        self.last_active_surface: Optional[str] = None
        self.active_surface: Optional[Surface] = None
        self.current_global_sfx_volume = 1.0
        self.sfx_sound_objects: list[pygame.mixer.Sound] = []

    def set_active_surface(self, name: str) -> None:
        """
        Switch the active surface by name.
        """

        if self.active_surface:
            self.active_surface.deactivate()
            self.last_active_surface = (
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.active_surface.__class__.__name__)
                .lower()
                .replace("_surface", "")
            )
        self.active_surface = self.surfaces.get(name)
        surface = cast(Surface, self.active_surface)
        surface.hook()
        surface.activate()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Pass event handling to the active surface only.
        """

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.handle_event(event)

    def update(self) -> None:
        """
        Update the active surface only.
        """

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.update()

    def draw(self) -> None:
        """
        Draw the active surface onto the display.
        """

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.draw()
            pygame.display.flip()

    def reinitialize_surface_from_path(self, path: str) -> None:
        """
        Reinitialize a specific surface based on the changed file path.
        """

        print(f"[?] Detected change in {path}. Reloading module...")

        module_name = os.path.normpath(path).replace(os.path.sep, ".")
        module_name = module_name.rsplit(".", 1)[0]

        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

        # Class resolution rules from file path:
        # 1. Converts snake_case to PascalCase (e.g. summer_break_choice -> SummerBreakChoice)
        # 2. Removes leading _<number>_; good for order (e.g. _1_summer_break_choice -> SummerBreakChoice)
        # 3. Appends "Surface" to the class name (e.g. _1_summer_break_choice -> SummerBreakChoiceSurface)
        surface_name = re.sub(r"^_\d+_", "", os.path.basename(path).rsplit(".", 1)[0])

        if surface_name.lower() in self.surfaces:
            class_name = "".join(part.title() for part in surface_name.split("_"))
            surface_class = getattr(sys.modules[module_name], f"{class_name}Surface")

            self.surfaces[surface_name] = surface_class(
                self.display_surface, self.assets, self
            )
            print(f"[?] Reinitialized {surface_class.__name__} surface")

            if (
                self.active_surface.__class__.__name__
                == self.surfaces[surface_name].__class__.__name__
            ):
                self.set_active_surface(surface_name)

    def set_global_sfx_volume(self, volume: float) -> None:
        """
        Set the global volume for sfx.
        """

        self.current_global_sfx_volume = volume
        for sound in self.sfx_sound_objects:
            sound.set_volume(volume)
