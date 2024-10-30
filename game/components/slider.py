import pygame
from typing import Callable


class Slider:
    """
    A slider component for adjusting numeric values.
    """

    def __init__(
        self,
        rect: tuple[int, int, int, int],
        min_value: float,
        max_value: float,
        start_value: float,
        on_change: Callable[[float], None],
    ):
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.on_change = on_change
        handle_x = self.rect.x + (
            self.rect.width * ((start_value - min_value) / (max_value - min_value))
        )
        self.handle = pygame.Rect(handle_x, self.rect.y, 20, self.rect.height)
        self.dragging = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse events for dragging the slider handle.
        """

        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.handle.collidepoint(event.pos):
                    self.dragging = True
            case pygame.MOUSEBUTTONUP:
                self.dragging = False
            case pygame.MOUSEMOTION if self.dragging:
                self.handle.x = max(
                    self.rect.x, min(event.pos[0], self.rect.right - self.handle.width)
                )
                self.value = self.min_value + (self.max_value - self.min_value) * (
                    (self.handle.x - self.rect.x) / self.rect.width
                )
                self.on_change(self.value)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the slider background, filled portion and handle.
        """

        filled_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width
            * ((self.value - self.min_value) / (self.max_value - self.min_value)),
            self.rect.height,
        )

        pygame.draw.rect(surface, (41, 78, 103), self.rect, border_radius=2)
        pygame.draw.rect(surface, (70, 130, 180), filled_rect, border_radius=2)
        pygame.draw.rect(surface, (208, 239, 243), self.handle, border_radius=2)
