import pygame
from typing import Optional, Callable, Any


class Button:
    """A declarative button component."""

    __slots__ = (
        "normal_image",
        "hover_image",
        "active_image",
        "position",
        "on_click",
        "sound_on_click",
        "on_draw",
        "is_hovered",
        "is_active",
        "current_image",
        "rect",
    )

    def __init__(
        self,
        normal_image: pygame.Surface,
        hover_image: pygame.Surface,
        active_image: pygame.Surface,
        position: tuple[int, int],
        on_click: Optional[Callable[["Button", pygame.event.Event], Any]] = None,
        sound_on_click: Optional[pygame.mixer.Sound] = None,
        on_draw: Optional[Callable[["Button", pygame.Surface], Any]] = None,
    ) -> None:
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.active_image = active_image
        self.position = position
        self.on_click = on_click
        self.sound_on_click = sound_on_click
        self.on_draw = on_draw
        self.is_hovered = False
        self.is_active = False
        self.current_image = normal_image
        self.rect = normal_image.get_rect(center=position)

    def __handle_click(self, event: pygame.event.Event) -> None:
        """Handle click events."""
        if self.is_active and self.is_hovered and self.on_click:
            if self.sound_on_click:
                self.sound_on_click.play()
            self.on_click(self, event)

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle events of interest."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.__handle_click(event)
            self.is_active = False

    def update(self) -> None:
        """Update the button's state."""
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.current_image = (
            self.active_image
            if self.is_active
            else self.hover_image
            if self.is_hovered
            else self.normal_image
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button."""
        surface.blit(self.current_image, self.rect)
        if self.on_draw:
            self.on_draw(self, surface)
