import pygame


from typing import Optional, Callable
from game.components.text import Text


class ChoiceBanner:
    """
    A choice banner component that displays on the right side of the screen
    above the dialogue banner. Contains choice text.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        banner_image: pygame.Surface,
        text_content: str,
        font: pygame.font.Font,
        y_offset: float = 0.7,  # Positioned just above dialogue banner
        text_color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable] = None,
    ):
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Banner dimensions - smaller than dialogue banner
        self.banner_width = int(screen_width * 0.3)
        self.banner_height = int(screen_height * 0.05)

        self.banner_image = pygame.transform.scale(
            banner_image, (self.banner_width, self.banner_height)
        )

        # Position banner on right side
        banner_x = screen_width - self.banner_width - 50  # 50px padding from right
        banner_y = int(screen_height * y_offset)
        self.position = (banner_x, banner_y)

        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.banner_width, self.banner_height
        )

        # Text positioning
        self.font = font
        self.text_color = text_color
        self.text = Text(
            content=text_content,
            font=self.font,
            position=(
                self.position[0] + (self.banner_width * 0.1),  # type: ignore
                self.position[1] + (self.banner_height * 0.15),
            ),
            color=self.text_color,
            center=False,
        )

        self.on_draw = on_draw

    def update_position(self, new_y_offset: float):
        """Update the vertical position of the banner."""
        screen_height = pygame.display.get_surface().get_height()
        new_y = int(screen_height * new_y_offset)
        self.position = (self.position[0], new_y)
        self.rect.topleft = self.position

        # Update text position
        self.text.position = (  # type: ignore
            self.position[0] + (self.banner_width * 0.1),
            self.position[1] + (self.banner_height * 0.15),
        )

    def update_text(self, new_text: str):
        """Update the choice text content."""
        self.text.content = new_text

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click on choice banner."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the banner and text onto the given surface."""
        surface.blit(self.banner_image, self.position)
        self.text.draw(surface)

        if self.on_draw:
            self.on_draw(self, surface)
