import pygame
from typing import Callable, Any


class Slider:
    """A declarative slider component for adjusting numeric values."""

    __slots__ = (
        "rect",
        "min_value",
        "max_value",
        "value",
        "on_change",
        "handle",
        "dragging",
    )

    def __init__(
        self,
        rect: tuple[int, int, int, int],
        min_value: float,
        max_value: float,
        start_value: float,
        on_change: Callable[[float], Any],
    ) -> None:
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.on_change = on_change
        self.handle = pygame.Rect(
            self.__calculate_handle_x(start_value), self.rect.y, 20, self.rect.height
        )
        self.dragging = False

    def __calculate_handle_x(self, value: float) -> int:
        """Calculate x position of handle based on value."""

        return self.rect.x + int(
            self.rect.width
            * ((value - self.min_value) / (self.max_value - self.min_value))
        )

    def __update_value_from_handle(self) -> None:
        """Update slider value based on handle position."""

        self.value = self.min_value + (self.max_value - self.min_value) * (
            (self.handle.x - self.rect.x) / self.rect.width
        )
        self.on_change(self.value)

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle mouse events for dragging the slider handle."""

        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.handle.x = max(
                        self.rect.x, min(event.pos[0] - self.handle.width // 2, 
                        self.rect.right - self.handle.width)
                    )
                    self.__update_value_from_handle()
            case pygame.MOUSEBUTTONUP:
                self.dragging = False
            case pygame.MOUSEMOTION if self.dragging:
                self.handle.x = max(
                    self.rect.x, min(event.pos[0] - self.handle.width // 2, 
                    self.rect.right - self.handle.width)
                )
                self.__update_value_from_handle()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the slider background, filled portion and handle."""
        
        filled_width = int(
            self.rect.width
            * ((self.value - self.min_value) / (self.max_value - self.min_value))
        )
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, filled_width, self.rect.height
        )

        pygame.draw.rect(surface, (41, 78, 103), self.rect, border_radius=2)
        pygame.draw.rect(surface, (70, 130, 180), filled_rect, border_radius=2)
        pygame.draw.rect(surface, (208, 239, 243), self.handle, border_radius=2)
