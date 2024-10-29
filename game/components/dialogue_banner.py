import pygame
from typing import Optional, Callable
from game.components.text import Text


class DialogueBanner:
    """
    A dialogue banner component that displays at the bottom of the screen
    with text content. By default takes up bottom 30% of screen height
    and 90% of screen width, with configurable text positioning.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        banner_image: pygame.Surface,
        text_content: str,
        font: pygame.font.Font,
        banner_width_percent: float = 0.9,
        banner_height_percent: float = 0.3,
        text_x_percent: float = 0.05,
        text_y_percent: float = 0.1,
        text_color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable] = None,
    ):
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        self.banner_width = int(screen_width * banner_width_percent)
        self.banner_height = int(screen_height * banner_height_percent)

        self.banner_image = pygame.transform.scale(
            banner_image, (self.banner_width, self.banner_height)
        )

        # Center horizontally and position at bottom
        banner_x = (screen_width - self.banner_width) // 2
        banner_y = screen_height - self.banner_height
        self.position = (banner_x, banner_y)

        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.banner_width, self.banner_height
        )

        # Calculate text position relative to banner
        text_x = self.position[0] + int(self.banner_width * text_x_percent)
        text_y = self.position[1] + int(self.banner_height * text_y_percent)

        self.text = Text(
            content=text_content, font=font, position=(text_x, text_y), color=text_color
        )

        self.on_draw = on_draw

    def update_text(self, new_text: str):
        """Update the dialogue text content."""
        self.text.update_content(new_text)

    def draw(self, surface: pygame.Surface):
        """Draw the banner and text onto the given surface."""
        surface.blit(self.banner_image, self.position)
        self.text.draw(surface)

        if self.on_draw:
            self.on_draw(self, surface)
