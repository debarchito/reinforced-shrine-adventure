import pygame
from game.assets import Assets
from game.surface import Surface
from game.surface import SurfaceManager
from game.components.button import Button
from game.components.text import Text


class QuestionSurface(Surface):
    """Help menu surface showing game controls."""

    __slots__ = (
        "surface",
        "assets",
        "manager",
        "backdrop",
        "blur_surface",
        "button_click_1",
        "font",
        "back_button",
        "back_text",
        "help_texts",
        "title_text",
    )

    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ) -> None:
        super().__init__()
        self.surface = surface
        self.assets = assets
        self.manager = manager
        self.font = assets.fonts.monogram_extended(70)
        surface_size = surface.get_size()
        self.backdrop = pygame.Surface(surface_size)
        self.blur_surface = pygame.Surface(surface_size, pygame.SRCALPHA)
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        manager.sfx_objects.append(self.button_click_1)
        self.__setup_home_button()
        self.__setup_help_texts()

    def __setup_home_button(self) -> None:
        """Initialize back button."""
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
            on_click=self.__on_back,
            sound_on_click=self.button_click_1,
        )

        self.back_text = Text(
            content="Let's go!",
            center=False,
            font=self.font,
            position=(180, 60),
        )

    def __setup_help_texts(self) -> None:
        """Initialize help text content."""
        center_x = self.surface.get_width() // 2
        base_y = int(self.surface.get_height() * 0.185)
        line_height = int(self.surface.get_height() * 0.111)
        title_color = (182, 160, 118)
        text_color = (255, 255, 255)
        key_offset = int(self.surface.get_width() * 0.156)
        desc_offset = int(self.surface.get_width() * -0.052)
        self.help_texts = [
            Text(
                content="ESC",
                font=self.font,
                position=(center_x - key_offset, base_y + line_height + 30),
                center=True,
                color=title_color,
            ),
            Text(
                content="Pause Toggle",
                font=self.font,
                position=(center_x + desc_offset, base_y + line_height),
                center=False,
                color=text_color,
            ),
            Text(
                content="H",
                font=self.font,
                position=(center_x - key_offset, base_y + line_height * 2 + 30),
                center=True,
                color=title_color,
            ),
            Text(
                content="Dialogue History Toggle",
                font=self.font,
                position=(center_x + desc_offset, base_y + line_height * 2),
                center=False,
                color=text_color,
            ),
            Text(
                content="SPACE",
                font=self.font,
                position=(center_x - key_offset, base_y + line_height * 3 + 30),
                center=True,
                color=title_color,
            ),
            Text(
                content="Dialogue Advance",
                font=self.font,
                position=(center_x + desc_offset, base_y + line_height * 3),
                center=False,
                color=text_color,
            ),
            Text(
                content="1-9",
                font=self.font,
                position=(center_x - key_offset, base_y + line_height * 4 + 30),
                center=True,
                color=title_color,
            ),
            Text(
                content="Choice Selection",
                font=self.font,
                position=(center_x + desc_offset, base_y + line_height * 4),
                center=False,
                color=text_color,
            ),
        ]

    def __glass_overlay(self) -> None:
        """Create frosted glass effect over the current display."""
        width = self.surface.get_width()
        height = self.surface.get_height()
        scale_factor = 0.05

        self.backdrop.blit(self.surface, (0, 0))
        self.blur_surface.fill((0, 0, 0, 215))

        small = pygame.transform.scale(
            self.backdrop,
            (int(width * scale_factor), int(height * scale_factor)),
        )
        blurred = pygame.transform.scale(small, (width, height))
        self.backdrop = blurred
        self.backdrop.blit(self.blur_surface, (0, 0))

    def __on_back(self, button: Button, event: pygame.event.Event) -> None:
        """Handle back button click."""
        self.manager.set_active_surface_by_name(self.manager.last_active_surface_name)  # type: ignore

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        pygame.mixer.music.stop()
        self.__glass_overlay()

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events for the help menu."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.__on_back(self.back_button, event)

        self.back_button.on_event(event)

    def update(self) -> None:
        """Update the state of help menu components."""
        self.back_button.update()

    def draw(self) -> None:
        """Draw the help menu components."""
        self.surface.blit(self.backdrop, (0, 0))
        self.back_button.draw(self.surface)
        self.back_text.draw(self.surface)
        for text in self.help_texts:
            text.draw(self.surface)
