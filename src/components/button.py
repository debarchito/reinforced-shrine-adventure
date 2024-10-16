import pygame
from typing import Optional, Callable


class Button:
    """
    A declarative button component.
    """

    def __init__(
        self,
        normal_image: pygame.Surface,
        hover_image: pygame.Surface,
        pressed_image: pygame.Surface,
        position: tuple[int, int],
        on_click: Optional[Callable] = None,
    ):
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.pressed_image = pressed_image
        self.position = position
        self.on_click = on_click
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect(center=position)
        self.is_hovered = False
        self.is_pressed = False

    def update(self) -> None:
        """
        Update the button's state.
        """

        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.is_pressed:
            self.current_image = self.pressed_image
        else:
            self.current_image = (
                self.hover_image if self.is_hovered else self.normal_image
            )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle events of interest.
        """

        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.is_hovered:
                if self.on_click:
                    self.on_click()
            self.is_pressed = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button.
        """

        screen.blit(self.current_image, self.rect)
