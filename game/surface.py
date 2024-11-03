"""
Provide base classes for game surfaces, manage surfaces, scene dynamics and provide a type-safe interface to interact with them.
"""

import os
import re
import sys
import pygame
import importlib
from game.assets import Assets
from abc import ABC, abstractmethod
from game.components.text import Text
from typing import Optional, TypedDict, Callable
from game.components.choice_banner import ChoiceBanner
from game.components.dialogue_banner import DialogueBanner


class HistoryEntry(TypedDict):
    text: str
    is_choice: bool
    timestamp: int


class Surface(ABC):
    """Base class for all game surfaces."""

    __slots__ = "is_active"

    def __init__(self) -> None:
        """Initialize a new Surface instance."""
        self.is_active = False

    def activate(self) -> None:
        """Activate this surface, making it interactive."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate this surface, pausing its updates and rendering."""
        self.is_active = False

    def hook(self) -> None:
        """Run any necessary setup code for this surface. Called on activation."""
        pass

    @abstractmethod
    def on_event(self, event: pygame.event.Event) -> None:
        """Listen to and handle events specific to this surface."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Update the state of this surface."""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw elements onto the target display/blank surface."""
        pass


class SurfaceManager:
    """Manages different game surfaces, handling their activation and transitions."""

    __slots__ = (
        "surface",
        "assets",
        "scene",
        "surfaces",
        "last_active_surface_name",
        "active_surface",
        "active_surface_name",
        "current_global_sfx_volume",
        "sfx_objects",
    )

    def __init__(self, surface: pygame.Surface, assets: Assets) -> None:
        """Initialize the SurfaceManager with a target surface and assets."""
        self.surface = surface
        self.assets = assets
        self.scene = SceneDynamics(self.surface, self.assets)
        self.surfaces = {}
        self.last_active_surface_name = None
        self.active_surface = None
        self.active_surface_name = None
        self.current_global_sfx_volume = 1.0
        self.sfx_objects = []

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle events for the active surface."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.on_event(event)

    def update(self) -> None:
        """Update the active surface state."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.update()

    def draw(self) -> None:
        """Draw the active surface and update the display."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.draw()
            pygame.display.flip()

    def set_active_surface_by_name(self, name: str) -> None:
        """Set the active surface by its name."""
        if self.active_surface:
            self.active_surface.deactivate()
            self.last_active_surface_name = (
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.active_surface.__class__.__name__)
                .lower()
                .replace("_surface", "")
            )

        self.active_surface = self.surfaces.get(name)
        self.active_surface_name = name

        if self.active_surface:
            self.active_surface.hook()
            self.active_surface.activate()

    def reinitialize_surface_from_path(self, path: str) -> None:
        """Reinitialize a surface from a file path after changes."""
        print(f"[?] Detected change in {path}. Reloading module...")

        module_name = os.path.normpath(path).replace(os.path.sep, ".").rsplit(".", 1)[0]
        surface_name = re.sub(r"^_\d+_", "", os.path.basename(path).rsplit(".", 1)[0])

        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

        if surface_name.lower() in self.surfaces:
            class_name = "".join(part.title() for part in surface_name.split("_"))
            surface_class = getattr(sys.modules[module_name], f"{class_name}Surface")
            self.surfaces[surface_name] = surface_class(self.surface, self.assets, self)

            print(f"[?] Reinitialized {surface_class.__name__} surface.")

            if (
                self.active_surface
                and self.active_surface.__class__.__name__
                == self.surfaces[surface_name].__class__.__name__
            ):
                self.set_active_surface_by_name(surface_name)

    def set_global_sfx_volume(self, volume: float) -> None:
        """Set the global volume for all sound effects."""
        self.current_global_sfx_volume = volume
        for sound in self.sfx_objects:
            sound.set_volume(volume)


class SceneDynamics:
    """Handles core scene dynamics like choices, dialogue and transitions."""

    __slots__ = (
        "surface",
        "assets",
        "story",
        "choice_banners",
        "dialogue_banner",
        "character_sprite",
        "character_border",
        "button_click_1",
        "on_scene_complete",
        "history",
        "show_history",
        "history_scroll_position",
        "history_scroll_speed",
        "screen_width",
        "screen_height",
        "current_dialogue",
    )

    CHARACTER_SPRITES = {
        name: staticmethod(
            lambda assets, n=name: getattr(assets.images.characters, n.lower())()
        )
        for name in ["Aie", "Haruto", "Ryu", "Kaori", "Airi", "Kanae"]
    }

    def __init__(self, surface: pygame.Surface, assets: Assets) -> None:
        """Initialize SceneDynamics with a surface and assets."""
        self.surface = surface
        self.assets = assets
        self.story = assets.story
        self.choice_banners = []
        self.dialogue_banner = None
        self.character_sprite = None
        self.character_border = self.assets.images.ui.border_character_wood()
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        self.on_scene_complete: Optional[Callable[[str], None]] = None
        self.history = []
        self.show_history = False
        self.history_scroll_position = 0
        self.history_scroll_speed = 35
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()
        self.current_dialogue = None

    def get_next_dialogue(self) -> str:
        """Get the next dialogue text from the story."""
        while self.story.can_continue():
            if text := self.story.cont().strip():
                return text
        return ""

    def parse_dialogue(self, text: str) -> tuple[Optional[str], str]:
        """Parse dialogue text into character name and content."""
        if not text.startswith("@"):
            return None, text

        try:
            name, content = text[1:].split(":", 1)
            return name.strip(), content.strip()
        except ValueError:
            return None, text

    def create_dialogue_banner(
        self, text: str, char_name: Optional[str]
    ) -> DialogueBanner:
        """Create a new dialogue banner with the given text and character name."""
        return DialogueBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.border_dialogue_wood(),
            text_content=text,
            text_color=(255, 255, 255),
            font=self.assets.fonts.monogram_extended(50),
            character_name=char_name,
            character_name_color=(182, 160, 118),
            on_advance=self.button_click_1,
            x_offset=int(self.screen_width * 0.25),
            y_offset=int(self.screen_height * 0.07),
        )

    def should_show_next_dialogue_page(self) -> bool:
        """Check if there is a next dialogue page to show."""
        if not self.dialogue_banner:
            return False

        next_page_start = (self.dialogue_banner.current_page + 1) * (
            self.dialogue_banner.max_lines - 1
            if self.dialogue_banner.character_name
            else self.dialogue_banner.max_lines
        )
        return next_page_start < len(self.dialogue_banner.full_text_lines)

    def handle_dialogue_advance(self) -> None:
        """Handle advancing to the next dialogue."""
        if not self.story.can_continue():
            return

        if next_text := self.get_next_dialogue():
            next_text = next_text.strip()
            if next_text.startswith("$jump"):
                if self.on_scene_complete:
                    self.on_scene_complete(next_text.removeprefix("$jump").strip())
                return

            if self.dialogue_banner:
                char_name, dialogue_text = self.parse_dialogue(next_text)
                self.dialogue_banner.update_text(dialogue_text, char_name)
                self.update_character_sprite(char_name)
                self.current_dialogue = (char_name, dialogue_text)
                history_text = (
                    f"{char_name}: {dialogue_text}" if char_name else dialogue_text
                )
                self.add_to_history(history_text)
                self.add_to_history("")

        self.update_choices()

    def create_choice_banner(
        self, choice: str, index: int, y_offset: float
    ) -> ChoiceBanner:
        """Create a new choice banner with the given choice text and position."""
        return ChoiceBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.border_dialogue_wood(),
            text_content=f"{index+1}. {choice}",
            font=self.assets.fonts.monogram_extended(40),
            y_offset=y_offset,
            text_color=(182, 160, 118),
        )

    def update_choices(self) -> None:
        """Update the available choices."""
        self.choice_banners.clear()
        if not self.should_show_next_dialogue_page():
            choices = list(self.story.get_current_choices())  # type: ignore
            self.choice_banners.extend(
                (self.create_choice_banner(choice, i, 0.45 + (i * 0.08)), i)
                for i, choice in enumerate(choices)
            )

    def handle_choice_selection(self, choice_idx: int) -> None:
        """Handle the selection of a choice."""
        choices = self.story.get_current_choices()
        if choice_idx < len(choices):
            choice_text = choices[choice_idx]
            self.add_to_history(choice_text, True)
            self.add_to_history("")
            self.story.choose_choice_index(choice_idx)

            if next_text := self.get_next_dialogue():
                char_name, dialogue_text = self.parse_dialogue(next_text)
                if self.dialogue_banner:
                    self.dialogue_banner.update_text(dialogue_text, char_name)
                    self.update_character_sprite(char_name)
                    self.current_dialogue = (char_name, dialogue_text)
                    history_text = (
                        f"{char_name}: {dialogue_text}" if char_name else dialogue_text
                    )
                    self.add_to_history(history_text)
                    self.add_to_history("")
                    self.update_choices()

    def get_character_sprite(
        self, char_name: Optional[str]
    ) -> Optional[pygame.Surface]:
        """Get the character sprite surface for the given character name."""
        if not char_name:
            return None
        sprite_getter = self.CHARACTER_SPRITES.get(char_name)
        return sprite_getter(self.assets) if sprite_getter else None

    def update_character_sprite(self, char_name: Optional[str]) -> None:
        """Update the character sprite with the given character name."""
        if not (sprite := self.get_character_sprite(char_name)):
            self.character_sprite = None
            return

        border_width = int(self.screen_width * 0.18)
        border_height = int(self.screen_height * 0.4)
        border_surface = pygame.Surface((border_width, border_height), pygame.SRCALPHA)
        border_surface.blit(
            pygame.transform.scale(
                self.character_border, (border_width, border_height)
            ),
            (0, 0),
        )

        sprite_height = int(border_height * 0.8)
        sprite_width = int(sprite_height * sprite.get_width() / sprite.get_height())
        scaled_sprite = pygame.transform.scale(sprite, (sprite_width, sprite_height))

        sprite_x = int((border_width - sprite_width) / 1.6)
        sprite_y = int(border_height - sprite_height - (border_height * 0.175))
        border_surface.blit(scaled_sprite, (sprite_x, sprite_y))
        self.character_sprite = border_surface

    def setup(self) -> None:
        """Set up the initial scene state."""
        if initial_text := self.get_next_dialogue():
            char_name, dialogue_text = self.parse_dialogue(initial_text)
            self.dialogue_banner = self.create_dialogue_banner(dialogue_text, char_name)
            self.update_character_sprite(char_name)
            self.current_dialogue = (char_name, dialogue_text)
            history_text = (
                f"{char_name}: {dialogue_text}" if char_name else dialogue_text
            )
            self.add_to_history(history_text)
            self.add_to_history("")

    def add_to_history(self, text: str, is_choice: bool = False) -> None:
        """Add an entry to the scene history."""
        entry: HistoryEntry = {
            "text": text,
            "is_choice": is_choice,
            "timestamp": pygame.time.get_ticks(),
        }
        self.history.append(entry)

        if self.show_history:
            self.auto_scroll_history()

    def __setup_history_window(
        self, surface: pygame.Surface
    ) -> tuple[pygame.Surface, int, int, int]:
        """Set up the history window surface and return key dimensions."""
        width = surface.get_width()
        height = surface.get_height()
        padding = 40
        window_width = width - (padding * 2)
        window_height = height - (padding * 2)
        backdrop = pygame.Surface((width, height))
        backdrop.blit(surface, (0, 0))
        scale_factor = 0.05
        small = pygame.transform.scale(
            backdrop,
            (int(width * scale_factor), int(height * scale_factor)),
        )
        blurred = pygame.transform.scale(small, (width, height))
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        blurred.blit(overlay, (0, 0))
        surface.blit(blurred, (0, 0))
        window = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        window.fill((0, 0, 0, 25))

        gradient = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        for i in range(window_height):
            alpha = int(15 * (1 - i / window_height))
            gradient.fill((255, 255, 255, alpha), (0, i, window_width, 1))
        window.blit(gradient, (0, 0))

        return window, window_width, window_height, padding

    def __draw_history_title(self, window: pygame.Surface, width: int) -> None:
        """Draw the history title on the window."""
        title_height = 60
        title_surface = pygame.Surface((width, title_height), pygame.SRCALPHA)
        title_surface.fill((182, 160, 118, 25))
        window.blit(title_surface, (0, 0))

        title = Text(
            content="History",
            font=self.assets.fonts.monogram_extended(50),
            position=(width // 2, 20),
            color=(182, 160, 118),
            center=True,
        )
        title.draw(window)
        pygame.draw.line(
            window, (182, 160, 118), (20, title_height), (width - 20, title_height), 1
        )

    def __calculate_total_lines(
        self, font: pygame.font.Font, max_width: int, padding: int
    ) -> int:
        """Calculate total lines needed for history content."""
        total_lines = 0
        avg_char_width = font.size("M")[0]
        chars_per_line = max_width // avg_char_width

        for entry in self.history:
            if not entry["text"].strip():
                total_lines += 1
                continue

            text = entry["text"]
            if entry["is_choice"]:
                text = f"» {text}"
                text_lines = (len(text) // chars_per_line) + 1
                total_lines += text_lines
            else:
                if re.match(r"^[A-Za-z]+:", text.strip()):
                    char_name, dialogue = text.split(":", 1)
                    char_name_width = font.size(char_name + ":")[0]
                    remaining_width = max_width - char_name_width
                    chars_in_remaining = remaining_width // avg_char_width
                    dialogue_lines = (len(dialogue.strip()) // chars_in_remaining) + 1
                    total_lines += dialogue_lines
                else:
                    text_lines = (len(text) // chars_per_line) + 1
                    total_lines += text_lines

        return total_lines

    def __render_text_line(
        self,
        content: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        position: tuple[int, int],
        color: tuple[int, int, int],
    ) -> None:
        """Render a single line of text on the content surface."""
        text_surface = Text(
            content=text,
            font=font,
            position=position,
            color=color,
            center=False,
        )
        text_surface.draw(content)

    def render_history(self, surface: pygame.Surface) -> None:
        """Render the scene history on the given surface."""
        window, width, height, padding = self.__setup_history_window(surface)
        self.__draw_history_title(window, width)

        font = self.assets.fonts.monogram_extended(50)
        line_height = 35
        text_color = (255, 255, 255)
        choice_color = (182, 160, 118)
        max_width = width - (padding * 2)

        total_lines = self.__calculate_total_lines(font, max_width, padding)
        content_height = max(height, total_lines * line_height + 100)
        content = pygame.Surface((width, content_height + padding), pygame.SRCALPHA)
        y_offset = 80

        for entry in self.history:
            if not entry["text"].strip():
                y_offset += line_height
                continue

            text = entry["text"]
            color = choice_color if entry["is_choice"] else text_color

            if entry["is_choice"]:
                text = f"» {text}"
                words = text.split()
                current_line = []
                current_width = 0

                for word in words:
                    word_surface = font.render(word + " ", True, color)
                    word_width = word_surface.get_width()

                    if current_width + word_width <= max_width:
                        current_line.append(word)
                        current_width += word_width
                    else:
                        if current_line:
                            self.__render_text_line(
                                content,
                                " ".join(current_line),
                                font,
                                (padding, y_offset),
                                color,
                            )
                            y_offset += line_height
                            current_line = [word]
                            current_width = word_width

                if current_line:
                    self.__render_text_line(
                        content,
                        " ".join(current_line),
                        font,
                        (padding, y_offset),
                        color,
                    )
                    y_offset += line_height
            else:
                if re.match(r"^[A-Za-z]+:", text.strip()):
                    char_name, dialogue = text.split(":", 1)
                    self.__render_text_line(
                        content,
                        char_name + ":",
                        font,
                        (padding, y_offset),
                        choice_color,
                    )

                    char_name_width = font.size(char_name + ": ")[0]
                    remaining_width = max_width - char_name_width

                    words = dialogue.strip().split()
                    current_line = []
                    current_width = 0

                    for word in words:
                        word_surface = font.render(word + " ", True, text_color)
                        word_width = word_surface.get_width()

                        if current_width + word_width <= remaining_width:
                            current_line.append(word)
                            current_width += word_width
                        else:
                            if current_line:
                                self.__render_text_line(
                                    content,
                                    " ".join(current_line),
                                    font,
                                    (padding + char_name_width, y_offset),
                                    text_color,
                                )
                                y_offset += line_height
                                current_line = [word]
                                current_width = word_width

                    if current_line:
                        self.__render_text_line(
                            content,
                            " ".join(current_line),
                            font,
                            (padding + char_name_width, y_offset),
                            text_color,
                        )
                        y_offset += line_height
                else:
                    words = text.split()
                    current_line = []
                    current_width = 0

                    for word in words:
                        word_surface = font.render(word + " ", True, text_color)
                        word_width = word_surface.get_width()

                        if current_width + word_width <= max_width:
                            current_line.append(word)
                            current_width += word_width
                        else:
                            if current_line:
                                self.__render_text_line(
                                    content,
                                    " ".join(current_line),
                                    font,
                                    (padding, y_offset),
                                    text_color,
                                )
                                y_offset += line_height
                                current_line = [word]
                                current_width = word_width

                    if current_line:
                        self.__render_text_line(
                            content,
                            " ".join(current_line),
                            font,
                            (padding, y_offset),
                            text_color,
                        )
                        y_offset += line_height

        max_scroll = max(0, content_height - height + padding * 2)
        self.history_scroll_position = min(
            max_scroll, max(0, self.history_scroll_position)
        )

        window.blit(
            content, (0, 60), (0, self.history_scroll_position, width, height - 60)
        )
        surface.blit(window, (padding, padding))

    def auto_scroll_history(self) -> None:
        """Automatically scroll history to the latest entry."""
        if not self.show_history:
            return

        max_scroll = self.__calculate_history_scroll_height()
        self.history_scroll_position = max_scroll

    def handle_history_scroll(self, event: pygame.event.Event) -> None:
        """Handle scrolling events for the history view."""
        if not self.show_history or event.type != pygame.KEYDOWN:
            return

        max_scroll = self.__calculate_history_scroll_height()

        if event.key == pygame.K_UP:
            self.history_scroll_position = max(
                0, self.history_scroll_position - self.history_scroll_speed
            )
        elif event.key == pygame.K_DOWN:
            self.history_scroll_position = min(
                max_scroll, self.history_scroll_position + self.history_scroll_speed
            )

    def __calculate_history_scroll_height(self) -> int:
        """Calculate the maximum scroll height for history view."""
        line_height = 35
        padding = 40
        window_height = self.surface.get_height() - (padding * 2)
        window_width = self.surface.get_width() - (padding * 2)
        max_width = window_width - (padding * 2)

        total_lines = self.__count_history_lines(max_width)
        content_height = total_lines * line_height + 100 + padding
        return max(0, content_height - window_height + padding)

    def __count_history_lines(self, max_width: int) -> int:
        """Count total lines needed to display history entries."""
        total_lines = 0
        font = self.assets.fonts.monogram_extended(45)

        for entry in self.history:
            if not entry["text"].strip():
                total_lines += 1
                continue

            prefix = "» " if entry["is_choice"] else ""
            full_text = f"{prefix}{entry['text']}"
            total_lines += self.__count_text_lines(full_text, font, max_width)

        return total_lines

    def __count_text_lines(
        self, text: str, font: pygame.font.Font, max_width: int
    ) -> int:
        """Count lines needed for a text string."""
        words = text.split()
        current_width = 0
        line_count = 1

        for word in words:
            word_surface = font.render(word + " ", True, (255, 255, 255))
            word_width = word_surface.get_width()
            if current_width + word_width > max_width:
                line_count += 1
                current_width = word_width
            else:
                current_width += word_width

        return line_count
