"""
Provide base classes for game surfaces, manage surfaces, scene dynamics and provide a type-safe interface to interact with them.
"""

import os
import re
import sys
import pygame
import importlib
from typing import Optional, Callable
from game.assets import Assets
from abc import ABC, abstractmethod
from game.components.choice_banner import ChoiceBanner
from game.components.dialogue_banner import DialogueBanner
from game.components.text import Text


class Surface(ABC):
    """Base class for all game surfaces."""

    __slots__ = "is_active"

    def __init__(self) -> None:
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
        self.surface = surface
        self.assets = assets
        self.scene = SceneDynamics(self.surface, self.assets)

        # Surface management
        self.surfaces: dict[str, Surface] = {}
        self.last_active_surface_name: Optional[str] = None
        self.active_surface: Optional[Surface] = None
        self.active_surface_name: Optional[str] = None

        # Audio management
        self.current_global_sfx_volume = 1.0
        self.sfx_objects: list[pygame.mixer.Sound] = []

    def on_event(self, event: pygame.event.Event) -> None:
        """Pass event handling to the active surface only."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.on_event(event)

    def update(self) -> None:
        """Update the active surface only."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.update()

    def draw(self) -> None:
        """Draw the active surface onto the display."""
        if self.active_surface and self.active_surface.is_active:
            self.active_surface.draw()
            pygame.display.flip()

    def set_active_surface_by_name(self, name: str) -> None:
        """Set the active surface by name while deactivating the previous one."""
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
        """Reinitialize a specific surface based on the changed file path."""
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
        """Set the global volume for sfx."""
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
        "scene_history",
        "show_history",
        "history_scroll_position",
        "history_scroll_speed",
        "screen_width",
        "screen_height",
    )

    CHARACTER_SPRITES = {
        name: staticmethod(
            lambda assets, n=name: getattr(assets.images.characters, n.lower())()
        )
        for name in ["Aie", "Haruto", "Ryu", "Kaori", "Airi", "Kanae"]
    }

    def __init__(self, surface: pygame.Surface, assets: Assets) -> None:
        self.surface = surface
        self.assets = assets
        self.story = assets.story
        self.choice_banners: list[tuple[ChoiceBanner, int]] = []
        self.dialogue_banner: Optional[DialogueBanner] = None
        self.character_sprite: Optional[pygame.Surface] = None
        self.character_border = self.assets.images.ui.border_character_wood()
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        self.on_scene_complete: Optional[Callable] = None
        self.scene_history: list[tuple[Optional[str], str]] = []
        self.show_history = False
        self.history_scroll_position = 0
        self.history_scroll_speed = 35
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

    def get_next_dialogue(self) -> str:
        """Get next line of dialogue from story."""
        while self.story.can_continue():
            if text := self.story.cont().strip():
                return text
        return ""

    def parse_dialogue(self, text: str) -> tuple[Optional[str], str]:
        """Parse dialogue text to extract character name and content."""
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
        """Create a dialogue banner with the given parameters."""
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
        """Check if there are more pages of dialogue to show."""
        if not self.dialogue_banner:
            return False

        next_page_start = (self.dialogue_banner.current_page + 1) * (
            self.dialogue_banner.max_lines - 1
            if self.dialogue_banner.character_name
            else self.dialogue_banner.max_lines
        )
        return next_page_start < len(self.dialogue_banner.full_text_lines)

    def handle_dialogue_advance(self) -> None:
        """Handle advancing to next dialogue line."""
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
                # Add to history
                history_text = (
                    f"{char_name}: {dialogue_text}" if char_name else dialogue_text
                )
                self.add_to_history(history_text)
                # Auto-scroll history
                self.auto_scroll_history()

        self.update_choices()

    def create_choice_banner(
        self, choice: str, index: int, y_offset: float
    ) -> ChoiceBanner:
        """Create a choice banner with the given parameters."""
        return ChoiceBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.border_dialogue_wood(),
            text_content=f"{index+1}. {choice}",
            font=self.assets.fonts.monogram_extended(40),
            y_offset=y_offset,
            text_color=(182, 160, 118),
        )

    def update_choices(self) -> None:
        """Update available choice banners."""
        self.choice_banners.clear()

        if self.should_show_next_dialogue_page():
            return

        choices = list(self.story.get_current_choices())  # type: ignore
        self.choice_banners.extend(
            (self.create_choice_banner(choice, i, 0.45 + (i * 0.08)), i)
            for i, choice in enumerate(choices)
        )

    def handle_choice_selection(self, choice_idx: int) -> None:
        """Handle selection of a choice option."""
        choices = self.story.get_current_choices()
        if choice_idx < len(choices):
            # Add choice to history
            self.add_to_history(choices[choice_idx], True)
            self.auto_scroll_history()

        self.story.choose_choice_index(choice_idx)
        if not self.story.can_continue():
            return

        if next_text := self.get_next_dialogue():
            char_name, dialogue_text = self.parse_dialogue(next_text)
            if self.dialogue_banner:
                self.dialogue_banner.update_text(dialogue_text, char_name)
                self.update_character_sprite(char_name)
                history_text = (
                    f"{char_name}: {dialogue_text}" if char_name else dialogue_text
                )
                self.add_to_history(history_text)
                self.auto_scroll_history()
                self.update_choices()

    def get_character_sprite(
        self, char_name: Optional[str]
    ) -> Optional[pygame.Surface]:
        """Get character sprite based on character name."""
        if not char_name:
            return None
        sprite_getter = self.CHARACTER_SPRITES.get(char_name)
        return sprite_getter(self.assets) if sprite_getter else None

    def update_character_sprite(self, char_name: Optional[str]) -> None:
        """Update the character sprite based on who is speaking."""
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
        """Set up initial dialogue and character sprite."""
        if initial_text := self.get_next_dialogue():
            char_name, dialogue_text = self.parse_dialogue(initial_text)
            self.dialogue_banner = self.create_dialogue_banner(dialogue_text, char_name)
            self.update_character_sprite(char_name)

    def add_to_history(self, text: str, is_choice: bool = False) -> None:
        """Add a new entry to the scene history."""
        if not text.strip():
            return

        entry = {
            "text": text,
            "is_choice": is_choice,
            "timestamp": pygame.time.get_ticks(),
        }
        self.scene_history.append(entry)

        # Add an empty line after choices
        if is_choice:
            empty_entry = {
                "text": " ",  # Empty line
                "is_choice": False,
                "timestamp": pygame.time.get_ticks(),
            }
            self.scene_history.append(empty_entry)

    def render_history(self, surface: pygame.Surface) -> None:
        """Render the scene history popup with scrolling."""
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        padding = 40
        width = surface.get_width() - (padding * 2)
        height = surface.get_height() - (padding * 2)
        window = pygame.Surface((width, height), pygame.SRCALPHA)
        window.fill((40, 40, 40, 255))
        pygame.draw.rect(window, (182, 160, 118), (0, 0, width, height), 2)

        font = self.assets.fonts.monogram_extended(30)
        line_height = 35
        text_color = (255, 255, 255)
        choice_color = (182, 160, 118)
        max_width = width - (padding * 2)
        content_height = max(height, len(self.scene_history) * line_height + 100)
        content = pygame.Surface((width, content_height), pygame.SRCALPHA)
        content.fill((0, 0, 0, 0))

        title = Text(
            content="Scene History",
            font=self.assets.fonts.monogram_extended(50),
            position=(width // 2, 20),
            color=(182, 160, 118),
            center=True,
        )
        title.draw(window)
        y_offset = 80

        for entry in self.scene_history:
            # Handle empty lines
            if not entry["text"].strip():
                y_offset += line_height
                continue

            color = choice_color if entry["is_choice"] else text_color
            prefix = "» " if entry["is_choice"] else ""
            full_text = f"{prefix}{entry['text']}"

            # Word wrap
            words = full_text.split()
            lines = []
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
                        lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width

            if current_line:
                lines.append(" ".join(current_line))

            # Render wrapped lines
            for line in lines:
                text = Text(
                    content=line,
                    font=font,
                    position=(padding, y_offset),
                    color=color,
                    center=False,
                )
                text.draw(content)
                y_offset += line_height

        # Calculate max scroll
        max_scroll = max(0, content_height - height + padding)
        self.history_scroll_position = min(
            max_scroll, max(0, self.history_scroll_position)
        )

        # Draw scrollable content below the title
        window.blit(
            content, (0, 60), (0, self.history_scroll_position, width, height - 60)
        )

        # Draw the final window
        surface.blit(window, (padding, padding))

    def auto_scroll_history(self) -> None:
        """Automatically scroll history to show newest content."""
        if not self.show_history:
            return

        # Calculate total content height
        line_height = 35
        content_height = (
            len(self.scene_history) * line_height + 100
        )  # Extra space for title

        # Calculate visible area height
        padding = 40
        window_height = self.surface.get_height() - (padding * 2)

        # Calculate maximum scroll position
        max_scroll = max(0, content_height - window_height)

        # Set scroll position to show current content
        self.history_scroll_position = max_scroll
