import pygame
import re
from game.assets import Assets
from game.surface import Surface, SurfaceManager
from game.components.text import Text
from game.components.button import Button


class MarkdownRenderer:
    """Simple markdown renderer for credits display."""

    def __init__(self, font_regular: pygame.font.Font, font_italic: pygame.font.Font):
        self.font_regular = font_regular
        self.font_italic = font_italic

    def parse_line(self, line: str) -> tuple[str, dict]:
        """Parse a line of markdown and return text and style attributes."""
        styles = {
            "font": self.font_regular,
            "color": (255, 255, 255),
            "size_multiplier": 1.0,
            "add_newline": False,
            "indent": 0,
            "add_newline_before": False,
        }

        # Headers
        if line.startswith("# "):
            line = line[2:]
            styles["size_multiplier"] = 1.5
            styles["add_newline"] = True
            styles["add_newline_before"] = True
        elif line.startswith("## "):
            line = line[3:]
            styles["size_multiplier"] = 1.3
            styles["add_newline"] = True
            styles["add_newline_before"] = True
        elif line.startswith("### "):
            line = line[4:]
            styles["size_multiplier"] = 1.2
            styles["add_newline"] = True
            styles["add_newline_before"] = True

        # Bullets/Lists
        bullet_match = re.match(r"^(\s*)-\s+(.*)$", line)
        if bullet_match:
            indent_level = len(bullet_match.group(1)) // 2
            line = "• " + bullet_match.group(2)
            styles["indent"] = indent_level * 40  # 40 pixels per indent level

        # Emphasis
        if re.match(r"\*\*.*\*\*", line):
            line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            styles["color"] = (182, 160, 118)  # Gold color for emphasis

        # Italics
        if re.match(r"\*.*\*", line):
            line = re.sub(r"\*(.*?)\*", r"\1", line)
            styles["font"] = self.font_italic

        return line, styles


class EndCreditsSurface(Surface):
    """End credits surface showing game completion with markdown rendering."""

    __slots__ = (
        "surface",
        "assets",
        "manager",
        "info",
        "background",
        "credits_elements",
        "button_click_1",
        "back_button",
        "fade_alpha",
        "scroll_position",
        "scroll_speed",
        "base_font_size",
        "line_spacing",
        "markdown_renderer",
    )

    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ) -> None:
        super().__init__()
        self.surface = surface
        self.assets = assets
        self.manager = manager
        self.info = pygame.display.Info()
        self.fade_alpha = 255
        self.scroll_position = self.surface.get_height()
        self.scroll_speed = 50
        self.base_font_size = 50
        self.line_spacing = 60

        self.markdown_renderer = MarkdownRenderer(
            font_regular=self.assets.fonts.monogram_extended(self.base_font_size),
            font_italic=self.assets.fonts.monogram_extended_italic(self.base_font_size),
        )

        self.__setup_background()
        self.__setup_credits()
        self.__setup_button()

    def __setup_background(self) -> None:
        """Initialize background surface."""
        self.background = pygame.transform.scale(
            self.assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )

    def __setup_credits(self) -> None:
        """Parse and setup credits content with markdown rendering."""
        with open("assets/Credits.md", "r", encoding="utf-8") as f:
            credits_content = f.read()

        # max_width = int(self.surface.get_width() * 0.8)
        self.credits_elements = []

        # Process each line
        for line in credits_content.split("\n"):
            line = line.strip()
            if not line:
                continue

            text, styles = self.markdown_renderer.parse_line(line)

            # Add newline before headers if needed
            if styles["add_newline_before"]:
                self.credits_elements.append(None)

            # Create font with adjusted size
            adjusted_size = int(self.base_font_size * styles["size_multiplier"])
            if styles["font"] == self.markdown_renderer.font_regular:
                font = self.assets.fonts.monogram_extended(adjusted_size)
            else:
                font = self.assets.fonts.monogram_extended_italic(adjusted_size)

            # Create text component with indentation for bullets
            text_component = Text(
                content=text,
                font=font,
                position=(
                    self.surface.get_width() // 2 + styles["indent"],
                    0,
                ),  # Add indent to x position
                color=styles["color"],
                center=True,
            )

            self.credits_elements.append(text_component)

            # Add extra spacing after headers
            if styles["add_newline"]:
                self.credits_elements.append(None)  # None represents an empty line

    def __setup_button(self) -> None:
        """Initialize back to menu button."""
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_objects.append(self.button_click_1)

        self.back_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_arrow_left(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_arrow_left_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_arrow_left_active(), (100, 100)
            ),
            position=(90, 90),
            on_click=lambda _, __: self.manager.set_active_surface_by_name("root"),
            sound_on_click=self.button_click_1,
        )

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        pygame.mixer.music.load(self.assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)
        self.fade_alpha = 255
        self.scroll_position = self.surface.get_height()

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_active_surface_by_name("root")
            return

        self.back_button.on_event(event)

    def update(self, delta_time: float) -> None:
        """Update the state of components."""
        self.back_button.update()
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 2)

        # Update scroll position
        self.scroll_position -= self.scroll_speed * delta_time

        # Reset scroll when credits reach the top
        total_height = len(self.credits_elements) * self.line_spacing
        if self.scroll_position < -total_height:
            self.scroll_position = self.surface.get_height()

    def draw(self) -> None:
        """Draw the end credits screen with markdown rendering."""
        self.surface.blit(self.background, (0, 0))

        # Create a temporary surface for the credits text
        credits_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)

        # Draw each text element
        y_pos = self.scroll_position
        for text_element in self.credits_elements:
            if text_element is not None:
                # Update text position
                text_element.position = (text_element.position[0], int(y_pos))
                text_element.rect.center = text_element.position

                # Draw text
                text_element.draw(credits_surface)
            y_pos += self.line_spacing

        self.surface.blit(credits_surface, (0, 0))
        self.back_button.draw(self.surface)

        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(self.surface.get_size())
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            self.surface.blit(fade_surface, (0, 0))
