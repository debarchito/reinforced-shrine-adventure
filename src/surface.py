import pygame
from abc import ABC, abstractmethod
from typing import Optional
from src.init import Assets


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
        self.active_surface: Optional[Surface] = None

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
