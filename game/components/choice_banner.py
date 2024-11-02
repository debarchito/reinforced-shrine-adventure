import pygame
from typing import Optional, Callable, Any
from game.components.text import Text


class ChoiceBanner:
    """A declarative choice banner component that displays choice text on the right side of the screen."""

    __slots__ = (
        "banner_width",
        "banner_height",
        "banner_image",
        "position",
        "rect",
        "font",
        "text_color",
        "text",
        "on_draw",
    )

    def __init__(
        self,
        surface: pygame.Surface,
        banner_image: pygame.Surface,
        text_content: str,
        font: pygame.font.Font,
        y_offset: float = 0.7,
        text_color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable[["ChoiceBanner", pygame.Surface], Any]] = None,
    ) -> None:
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        text_content = f" {text_content} "
        self.banner_width = self.__calculate_banner_width(text_content, font)
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
        self.on_draw = on_draw
        self.text = self.__create_text_object(text_content)

    def __calculate_banner_width(self, text: str, font: pygame.font.Font) -> int:
        """Calculate banner width based on text content."""
        avg_char_width = font.size("M")[0]  # Use M as average character width
        return len(text) * avg_char_width + 40  # Add 20px padding on each side

    def __create_text_object(self, content: str) -> Text:
        """Create text object with proper positioning."""
        return Text(
            content=content,
            font=self.font,
            position=(
                self.position[0] + 20,
                int(self.position[1] + (self.banner_height * 0.15)),
            ),
            color=self.text_color,
            center=False,
        )

    def on_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click events on the choice banner."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the banner and text onto the given surface."""
        surface.blit(self.banner_image, self.position)
        self.text.draw(surface)

        if self.on_draw:
            self.on_draw(self, surface)
