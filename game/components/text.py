import pygame
from typing import Optional, Callable, Any


class Text:
    """
    A declerative text component.
    """

    def __init__(
        self,
        content: str,
        font: pygame.font.Font,
        position: tuple[int, int],
        color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable[["Text", pygame.Surface], Any]] = None,
    ):
        self.content = content
        self.font = font
        self.position = position
        self.color = color
        self.on_draw = on_draw
        self.image = self.font.render(content, True, color)
        self.rect = self.image.get_rect(center=position)

    def update_content(self, new_content: str):
        """
        Update the content of the text component with new_content.
        """

        self.content = new_content
        self.image = self.font.render(new_content, True, self.color)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface: pygame.Surface):
        """
        Draw the text onto the given surface.
        """

        surface.blit(self.image, self.rect.topleft)
        if self.on_draw:
            self.on_draw(self, surface)
