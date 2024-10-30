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
        center: bool = True,
        on_draw: Optional[Callable[["Text", pygame.Surface], Any]] = None,
    ):
        self.content = content
        self.font = font
        self.position = position
        self.color = color
        self.center = center
        self.on_draw = on_draw
        self.__update_image()

    def __update_image(self) -> None:
        """
        Update the rendered text image and rect.
        """

        self.image = self.font.render(self.content, True, self.color)
        if self.center:
            self.rect = self.image.get_rect(center=self.position)
        else:
            self.rect = self.image.get_rect(topleft=self.position)

    def update_content(self, new_content: str) -> None:
        """
        Update the content of the text component with new_content.
        """

        if self.content == new_content:
            return
        self.content = new_content
        self.__update_image()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the text onto the given surface.
        """

        surface.blit(self.image, self.rect)
        if self.on_draw:
            self.on_draw(self, surface)
