import pygame
from src.surface import Surface, SurfaceManager
from src.init import Assets
from src.components.text import Text
from src.components.button import Button
from src.components.slider import Slider


class SettingsSurface(Surface):
    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ):
        super().__init__(surface)
        self.info = pygame.display.Info()
        self.assets = assets
        self.manager = manager
        self.background = pygame.transform.scale(
            assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )

        # Heading for the settings page
        self.heading = Text(
            content="Settings",
            font=assets.fonts.monogram_extended(80),
            position=(300, 85),
        )

        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_sound_objects.append(self.button_click_1)
        self.back_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_arrow_left(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_arrow_left_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_arrow_left_active(), (100, 100)
            ),
            position=(90, 90),
            on_click=lambda _button, _event: manager.set_active_surface("root"),
            sound_on_click=self.button_click_1,
        )

        # SFX Slider and Label
        self.sfx_label = Text(
            content="SFX",
            font=assets.fonts.monogram_extended(40),  # Smaller font for the labels
            position=(self.surface.get_width() // 2 - 250, 200),  # Left side of slider
        )
        self.sfx_slider = Slider(
            rect=(self.surface.get_width() // 2 - 100, 200, 200, 20),
            min_value=0.0,
            max_value=1.0,
            start_value=self.manager.current_global_sfx_volume - 0.1,
            on_change=self.set_sfx_volume,
        )

        # Music Slider and Label
        self.music_label = Text(
            content="Background",
            font=assets.fonts.monogram_extended(40),
            position=(self.surface.get_width() // 2 - 250, 300),  # Left side of slider
        )
        self.music_slider = Slider(
            rect=(self.surface.get_width() // 2 - 100, 300, 200, 20),
            min_value=0.0,
            max_value=1.0,
            start_value=pygame.mixer.music.get_volume() - 0.1,
            on_change=self.set_music_volume,
        )

    def set_sfx_volume(self, volume):
        """Set global SFX volume."""
        self.manager.set_global_sfx_volume(volume)

    def set_music_volume(self, volume):
        """Set global music volume."""
        pygame.mixer.music.set_volume(volume)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.is_active:
            return

        self.back_button.handle_event(event)
        self.sfx_slider.handle_event(event)
        self.music_slider.handle_event(event)

    def update(self) -> None:
        if not self.is_active:
            return

        self.back_button.update()

    def draw(self) -> None:
        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
        self.back_button.draw(self.surface)

        # Draw sliders and labels
        self.sfx_label.draw(self.surface)
        self.sfx_slider.draw(self.surface)

        self.music_label.draw(self.surface)
        self.music_slider.draw(self.surface)
