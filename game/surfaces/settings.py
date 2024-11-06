import pygame
from game.assets import Assets
from game.components.text import Text
from game.components.button import Button
from game.components.slider import Slider
from game.surface import Surface, SurfaceManager


class SettingsSurface(Surface):
    """Settings menu surface that handles game settings like audio volumes."""

    __slots__ = (
        "surface",
        "assets",
        "manager",
        "info",
        "backdrop",
        "blur_surface",
        "heading",
        "button_click_1",
        "back_button",
        "sfx_slider",
        "music_slider",
        "sfx_label",
        "music_label",
        "number_font",
    )

    def __init__(
        self,
        surface: pygame.Surface,
        assets: Assets,
        manager: SurfaceManager,
    ) -> None:
        super().__init__()
        self.surface = surface
        self.assets = assets
        self.manager = manager
        self.info = pygame.display.Info()
        self.__setup_background()
        self.__setup_heading()
        self.__setup_buttons()
        self.__setup_sliders()
        self.__setup_labels()

    def __setup_background(self) -> None:
        """Initialize background surfaces."""
        surface_size = self.surface.get_size()
        self.backdrop = pygame.Surface(surface_size)
        self.blur_surface = pygame.Surface(surface_size, pygame.SRCALPHA)

    def __glass_overlay(self) -> None:
        """Create frosted glass effect over the current display."""
        width = self.surface.get_width()
        height = self.surface.get_height()

        self.backdrop.blit(self.surface, (0, 0))
        self.blur_surface.fill((0, 0, 0, 215))

        scale_factor = 0.05
        small = pygame.transform.scale(
            self.backdrop, (int(width * scale_factor), int(height * scale_factor))
        )
        self.backdrop = pygame.transform.scale(small, (width, height))
        self.backdrop.blit(self.blur_surface, (0, 0))

    def __setup_heading(self) -> None:
        """Initialize heading text."""
        self.heading = Text(
            content="Settings",
            font=self.assets.fonts.monogram_extended(80),
            position=(300, 85),
        )

    def __setup_buttons(self) -> None:
        """Initialize back button and sound effects."""
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

    def __setup_sliders(self) -> None:
        """Initialize volume control sliders."""
        width = self.surface.get_width()
        height = self.surface.get_height()
        base_y = int(height // 2 - height // 3.83)

        self.sfx_slider = Slider(
            rect=(width // 2, base_y, 480, 30),
            min_value=0.0,
            max_value=1.0,
            start_value=self.manager.current_global_sfx_volume - 0.04,
            on_change=self.manager.set_global_sfx_volume,
        )

        self.music_slider = Slider(
            rect=(width // 2, base_y + 120, 480, 30),
            min_value=0.0,
            max_value=1.0,
            start_value=pygame.mixer.music.get_volume() - 0.03,
            on_change=pygame.mixer.music.set_volume,
        )

    def __setup_labels(self) -> None:
        """Initialize text labels."""
        width = self.surface.get_width()
        height = self.surface.get_height()
        base_x = width // 2 - width // 9 - 55
        base_y = height // 2 - height // 4

        font = self.assets.fonts.monogram_extended(50)
        self.sfx_label = Text(content="SFX", font=font, position=(base_x, base_y))
        self.music_label = Text(
            content="Background Music", font=font, position=(base_x, base_y + 120)
        )
        self.number_font = self.assets.fonts.monogram_extended(30)

    def __draw_slider_numbers(self, slider: Slider, y_position: int) -> None:
        """Draw '0' and '100' at the start and end of each slider."""
        zero_text = self.number_font.render("0", True, (255, 255, 255))
        hundred_text = self.number_font.render("100%", True, (255, 255, 255))
        zero_width = zero_text.get_width()
        zero_height = zero_text.get_height()

        self.surface.blit(
            zero_text,
            (slider.rect.x - (zero_width * 2), y_position - (zero_height / 8)),
        )
        self.surface.blit(
            hundred_text,
            (slider.rect.right + (zero_width / 1.1), y_position - (zero_height / 8)),
        )

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        self.__glass_overlay()

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events for the settings menu."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_active_surface_by_name("root")
            return

        self.back_button.on_event(event)
        self.sfx_slider.on_event(event)
        self.music_slider.on_event(event)

    def update(self, delta_time: float) -> None:
        """Update the state of components."""
        self.back_button.update()

    def draw(self) -> None:
        """Render the settings components to the surface."""
        self.surface.blit(self.backdrop, (0, 0))
        self.heading.draw(self.surface)
        self.back_button.draw(self.surface)
        self.sfx_label.draw(self.surface)
        self.sfx_slider.draw(self.surface)
        self.music_label.draw(self.surface)
        self.music_slider.draw(self.surface)

        height = self.surface.get_height()
        base_y = int(height // 2 - height // 3.83)
        self.__draw_slider_numbers(self.sfx_slider, base_y + 5)
        self.__draw_slider_numbers(self.music_slider, base_y + 125)
