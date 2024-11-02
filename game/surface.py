"""
Provide base classes for game surfaces, manage surfaces, and provide a type-safe interface to interact with them.
"""

import os
import re
import sys
import pygame
import importlib
from typing import Optional
from game.assets import Assets
from abc import ABC, abstractmethod
from game.utils import SceneDynamics


class Surface(ABC):
    """
    Base class for all game surfaces.
    """

    def __init__(self):
        self.is_active = False

    def activate(self) -> None:
        """
        Activate this surface, making it interactive.
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deactivate this surface, pausing its updates and rendering.
        """

        self.is_active = False

    def hook(self) -> None:
        """
        Run any necessary setup code for this surface. This method is called every time the surface is activated.
        """

        ...

    @abstractmethod
    def on_event(self, event: pygame.event.Event) -> None:
        """
        Listen to and handle events specific to this surface.
        """

        ...

    @abstractmethod
    def update(self) -> None:
        """
        Update the state of this surface.
        """

        ...

    @abstractmethod
    def draw(self) -> None:
        """
        Draw elements onto the target display/blank surface.
        """

        ...


class SurfaceManager:
    """
    Manages different game surfaces, handling their activation and transitions.
    """

    def __init__(self, surface: pygame.Surface, assets: Assets):
        self.surface = surface
        self.assets = assets
        self.scene = SceneDynamics(self.surface, self.assets)

        # Surface management stuff
        self.surfaces: dict[str, Surface] = {}
        self.last_active_surface_name: Optional[str] = None
        self.active_surface: Optional[Surface] = None
        self.active_surface_name: Optional[str] = None

        # Audio (SFX) management stuff
        self.current_global_sfx_volume = 1.0
        self.sfx_objects: list[pygame.mixer.Sound] = []

    def on_event(self, event: pygame.event.Event) -> None:
        """
        Pass event handling to the active surface only.
        """

        if self.active_surface and self.active_surface.is_active:
            self.active_surface.on_event(event)

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

    def set_active_surface_by_name(self, name: str) -> None:
        """
        Set the active surface by name. Also handles deactivation and recording of the last active surface.
        """

        if self.active_surface:
            self.active_surface.deactivate()
            self.last_active_surface_name = (
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.active_surface.__class__.__name__)
                .lower()
                .replace("_surface", "")
            )

        self.active_surface = self.surfaces.get(name)
        self.active_surface_name = name

        if self.active_surface:
            self.active_surface.hook()
            self.active_surface.activate()

    def reinitialize_surface_from_path(self, path: str) -> None:
        """
        Reinitialize a specific surface based on the changed file path.
        """

        print(f"[?] Detected change in {path}. Reloading module...")

        module_name = os.path.normpath(path).replace(os.path.sep, ".")
        module_name = module_name.rsplit(".", 1)[0]

        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

        # HMR hot-patching class resolution rules:
        # 1. Converts snake_case to PascalCase (e.g. _1_my_custom -> _1_MyCustom)
        # 2. Removes leading _<number>_; good for order (e.g. _1_my_custom -> MyCustom)
        # 3. Appends "Surface" to the class name (e.g. _1_my_custom -> MyCustomSurface)
        # 4. Looks for the class "MyCustomSurface" to patch.
        # So, name your surfaces like this: _<number>_<snake_case>.py and leave the rest to the parser magic.
        surface_name = re.sub(r"^_\d+_", "", os.path.basename(path).rsplit(".", 1)[0])

        if surface_name.lower() in self.surfaces:
            class_name = "".join(part.title() for part in surface_name.split("_"))
            surface_class = getattr(sys.modules[module_name], f"{class_name}Surface")
            self.surfaces[surface_name] = surface_class(self.surface, self.assets, self)

            print(f"[?] Reinitialized {surface_class.__name__} surface.")

            if (
                self.active_surface.__class__.__name__
                == self.surfaces[surface_name].__class__.__name__
            ):
                self.set_active_surface_by_name(surface_name)

    def set_global_sfx_volume(self, volume: float) -> None:
        """
        Set the global volume for sfx.
        """

        self.current_global_sfx_volume = volume

        for sound in self.sfx_objects:
            sound.set_volume(volume)
