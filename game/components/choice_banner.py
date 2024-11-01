import pygame
from typing import Optional, Callable, Any
from game.components.text import Text


class ChoiceBanner:
    """
    A declarative choice banner component that displays choice text on the right side of the screen.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        banner_image: pygame.Surface,
        text_content: str,
        font: pygame.font.Font,
        y_offset: float = 0.7,
        text_color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable[["ChoiceBanner", pygame.Surface], Any]] = None,
    ):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        text_content = f" {text_content} "
        average_char_width = font.size("M")[
            0
        ]  # Assuming 'M' as an average character width
        self.banner_width = (
            len(text_content) * average_char_width + 40
        )  # Adding padding of 20 on each side
        self.banner_height = int(screen_height * 0.05)
        self.banner_image = pygame.transform.scale(
            banner_image, (self.banner_width, self.banner_height)
        )
        banner_x = screen_width - self.banner_width - 50
        banner_y = int(screen_height * y_offset)
        self.position = (banner_x, banner_y)
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.banner_width, self.banner_height
        )
        self.font = font
        self.text_color = text_color
        self.text = Text(
            content=text_content,
            font=self.font,
            position=(
                self.position[0] + 20,
                self.position[1] + (self.banner_height * 0.15),  # type: ignore
            ),
            color=self.text_color,
            center=False,
        )
        self.on_draw = on_draw

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse click events on the choice banner.
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the banner and text onto the given surface.
        """

        surface.blit(self.banner_image, self.position)
        self.text.draw(surface)

        if self.on_draw:
            self.on_draw(self, surface)
