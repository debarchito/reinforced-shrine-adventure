import pygame
from surface import Surface, SurfaceManager  # type: ignore
from init import Assets  # type: ignore
from components.text import Text  # type: ignore
from components.button import Button  # type: ignore


class SettingsSurface(Surface):
    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ):
        super().__init__(surface)
        self.info = pygame.display.Info()
        self.background = pygame.transform.scale(
            assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )
        self.surface = pygame.display.set_mode(
            self.background.get_size(), pygame.FULLSCREEN
        )
        self.heading = Text(
            content="Settings Page",
            font=assets.fonts.monogram_extended(130),
            position=(surface.get_width() // 2, int(surface.get_height() * 0.3)),
        )
        self.home_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_home(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_home_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_home_active(), (100, 100)
            ),
            position=(surface.get_width() // 2, int(surface.get_height() * 0.6)),
            on_click=lambda _button, _event: manager.set_active_surface("root"),
            sound_on_click=pygame.mixer.Sound(assets.sounds.button_click_1()),
        )
        pygame.mixer.music.load(assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.is_active:
            return

        self.home_button.handle_event(event)

    def update(self) -> None:
        if not self.is_active:
            return

        self.home_button.update()

    def draw(self) -> None:
        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
        self.home_button.draw(self.surface)
