import pygame
from game.assets import Assets
from game.components.text import Text
from game.components.button import Button
from game.components.slider import Slider
from game.surface import Surface, SurfaceManager


class SettingsSurface(Surface):
    """
    Settings menu surface that handles game settings like audio volumes.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        assets: Assets,
        manager: SurfaceManager,
    ):
        super().__init__(surface)
        self.assets = assets
        self.manager = manager
        self.info = pygame.display.Info()
        self.__setup_background()
        self.__setup_heading()
        self.__setup_buttons()
        self.__setup_sliders()
        self.__setup_labels()

    def __setup_background(self) -> None:
        self.background = pygame.transform.scale(
            self.assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )

    def __setup_heading(self) -> None:
        self.heading = Text(
            content="Settings",
            font=self.assets.fonts.monogram_extended(80),
            position=(300, 85),
        )

    def __setup_buttons(self) -> None:
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_sound_objects.append(self.button_click_1)
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
            on_click=lambda _, __: self.manager.set_active_surface("root"),
            sound_on_click=self.button_click_1,
        )

    def __setup_sliders(self) -> None:
        self.sfx_slider = Slider(
            rect=(
                self.surface.get_width() // 2,
                int(self.surface.get_height() // 2 - self.surface.get_height() // 3.83),
                480,
                30,
            ),
            min_value=0.0,
            max_value=1.0,
            start_value=self.manager.current_global_sfx_volume - 0.1,
            on_change=self.manager.set_global_sfx_volume,
        )
        self.music_slider = Slider(
            rect=(
                self.surface.get_width() // 2,
                int(
                    self.surface.get_height() // 2
                    - self.surface.get_height() // 3.83
                    + 120
                ),
                480,
                30,
            ),
            min_value=0.0,
            max_value=1.0,
            start_value=pygame.mixer.music.get_volume() - 0.1,
            on_change=pygame.mixer.music.set_volume,
        )

    def __setup_labels(self) -> None:
        self.sfx_label = Text(
            content="SFX",
            font=self.assets.fonts.monogram_extended(50),
            position=(
                self.surface.get_width() // 2 - self.surface.get_width() // 9 - 55,
                self.surface.get_height() // 2 - self.surface.get_height() // 4,
            ),
        )
        self.music_label = Text(
            content="Background Music",
            font=self.assets.fonts.monogram_extended(50),
            position=(
                self.surface.get_width() // 2 - self.surface.get_width() // 9 - 55,
                self.surface.get_height() // 2 - self.surface.get_height() // 4 + 120,
            ),
        )
        self.number_font = self.assets.fonts.monogram_extended(30)

    def __draw_slider_numbers(self, slider: Slider, y_position: int) -> None:
        """
        Helper method to draw '0' and '100' at the start and end of each slider.
        """

        zero_text = self.number_font.render("0", True, (255, 255, 255))
        hundred_text = self.number_font.render("100", True, (255, 255, 255))

        self.surface.blit(
            zero_text,
            (
                slider.rect.x - (zero_text.get_width() * 2),
                y_position - (zero_text.get_height() / 8),
            ),
        )
        self.surface.blit(
            hundred_text,
            (
                slider.rect.right + (zero_text.get_width() / 1.1),
                y_position - (zero_text.get_height() / 8),
            ),
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle input events for the settings menu.
        """
        if not self.is_active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_active_surface("root")
            return

        self.back_button.handle_event(event)
        self.sfx_slider.handle_event(event)
        self.music_slider.handle_event(event)

    def update(self) -> None:
        """
        Update the state of settings components.
        """

        if not self.is_active:
            return

        self.back_button.update()

    def draw(self) -> None:
        """
        Render the settings components to the surface.
        """

        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
        self.back_button.draw(self.surface)
        self.sfx_label.draw(self.surface)
        self.sfx_slider.draw(self.surface)
        self.music_label.draw(self.surface)
        self.music_slider.draw(self.surface)
        self.__draw_slider_numbers(
            self.sfx_slider,
            int(self.surface.get_height() // 2 - self.surface.get_height() // 3.83 + 5),
        )
        self.__draw_slider_numbers(
            self.music_slider,
            int(
                self.surface.get_height() // 2 - self.surface.get_height() // 3.83 + 125
            ),
        )
