import pygame
from typing import Optional, Callable, Any
from game.components.text import Text


class DialogueBanner:
    """
    A declarative dialogue banner component that displays text content at the bottom of the screen.
    Supports text buffering and pagination.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        banner_image: pygame.Surface,
        text_content: str,
        font: pygame.font.Font,
        text_color: tuple[int, int, int] = (255, 255, 255),
        character_name: Optional[str] = None,
        character_name_color: tuple[int, int, int] = (255, 255, 255),
        on_draw: Optional[Callable[["DialogueBanner", pygame.Surface], Any]] = None,
        on_advance: Optional[pygame.mixer.Sound] = None,
        x_offset: int = 0,
        y_offset: int = 0,
    ):
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Add equal padding on all sides
        padding = 50
        self.banner_width = min(
            int(screen_width * 0.9), screen_width - x_offset - padding * 2
        )
        self.banner_height = int(screen_height * 0.3)

        # Scale banner image to full width
        self.banner_image = pygame.transform.scale(
            banner_image, (self.banner_width, self.banner_height)
        )

        banner_x = x_offset
        banner_y = screen_height - self.banner_height - y_offset
        self.position = (banner_x, banner_y)
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.banner_width, self.banner_height
        )
        self.font = font
        self.text_color = text_color
        self.character_name_color = character_name_color
        self.text_padding = int(self.banner_width * 0.08)
        self.text_start_x = x_offset + self.text_padding
        self.text_start_y = banner_y + self.text_padding - 27
        self.text_end_x = x_offset + self.banner_width - self.text_padding
        self.line_spacing = 10
        self.max_lines = 3
        self.character_name = character_name
        self.full_text_lines = self.__wrap_text(text_content)
        self.current_page = 0
        self.texts = []
        self.on_draw = on_draw
        self.on_advance = on_advance
        self.__update_visible_texts()

    def __wrap_text(self, text_content: str) -> list[str]:
        """
        Wrap text to fit within the dialogue banner width.
        """

        words = text_content.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = self.font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()

            if current_width + word_width <= self.text_end_x - self.text_start_x:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def __update_visible_texts(self) -> None:
        """
        Update the visible text objects based on current page.
        """

        start_idx = self.current_page * (
            self.max_lines - 1 if self.character_name else self.max_lines
        )
        visible_lines = self.full_text_lines[
            start_idx : start_idx
            + (self.max_lines - 1 if self.character_name else self.max_lines)
        ]
        self.texts = []

        if self.character_name:
            self.texts.append(
                Text(
                    content=self.character_name,
                    font=self.font,
                    position=(
                        self.text_start_x + (self.text_end_x - self.text_start_x) / 2,  # type: ignore
                        self.text_start_y,
                    ),
                    color=self.character_name_color,
                    center=True,
                )
            )

        for i, line in enumerate(visible_lines):
            if self.current_page > 0 and i == 0:
                line = "..." + line

            next_page_start = (self.current_page + 1) * (
                self.max_lines - 1 if self.character_name else self.max_lines
            )
            if (
                next_page_start < len(self.full_text_lines)
                and i == len(visible_lines) - 1
            ):
                line = line + "..."

            y_offset = 1 if self.character_name else 0
            self.texts.append(
                Text(
                    content=line,
                    font=self.font,
                    position=(
                        self.text_start_x,
                        self.text_start_y
                        + (i + y_offset)
                        * (self.font.get_height() + self.line_spacing / 2),  # type: ignore
                    ),
                    color=self.text_color,
                    center=False,
                )
            )

    def on_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse click or spacebar to advance text.
        """

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):
            if self.on_advance:
                self.on_advance.play()
            next_page_start = (self.current_page + 1) * (
                self.max_lines - 1 if self.character_name else self.max_lines
            )
            if next_page_start < len(self.full_text_lines):
                self.current_page += 1
                self.__update_visible_texts()
                return True

        return False

    def update_text(self, new_text: str, character_name: Optional[str] = None) -> None:
        """
        Update the dialogue text content.
        """

        self.character_name = character_name
        self.full_text_lines = self.__wrap_text(new_text)
        self.current_page = 0
        self.__update_visible_texts()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the banner and text onto the given surface.
        """

        surface.blit(self.banner_image, self.position)
        for text in self.texts:
            text.draw(surface)

        if self.on_draw:
            self.on_draw(self, surface)
