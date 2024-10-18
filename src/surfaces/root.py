import pygame
from surface import Surface, SurfaceManager  # type: ignore
from init import Assets  # type: ignore
from components.button import Button  # type: ignore
from components.text import Text  # type: ignore


class RootSurface(Surface):
    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ):
        super().__init__(surface)
        self.manager = manager
        self.info = pygame.display.Info()
        self.background = pygame.transform.scale(
            assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )
        self.surface = pygame.display.set_mode(
            self.background.get_size(), pygame.FULLSCREEN
        )
        self.heading = Text(
            content="Reinforced Shrine Adventure",
            font=assets.fonts.monogram_extended(130),
            position=(surface.get_width() // 2, int(surface.get_height() * 0.3)),
        )
        self.start_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_start(), (200, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_start_hover(), (200, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_start_active(), (200, 100)
            ),
            position=(surface.get_width() // 2, int(surface.get_height() * 0.6)),
            on_click=lambda _button, _event: print("Button clicked x3!!!"),
            sound_on_click=pygame.mixer.Sound(assets.sounds.button_click_1()),
        )
        self.cog_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_cog(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_cog_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_cog_active(), (100, 100)
            ),
            position=(surface.get_width() // 2 - 50, int(surface.get_height() * 0.73)),
            on_click=lambda _button, _event: manager.set_active_surface("settings"),
            sound_on_click=pygame.mixer.Sound(assets.sounds.button_click_1()),
        )
        self.quit_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_quit(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_quit_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_quit_active(), (100, 100)
            ),
            position=(surface.get_width() // 2 + 50, int(surface.get_height() * 0.73)),
            on_click=lambda _button, _event: pygame.quit(),
            sound_on_click=pygame.mixer.Sound(assets.sounds.button_click_1()),
        )
        pygame.mixer.music.load(assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.is_active:
            return

        self.start_button.handle_event(event)
        self.cog_button.handle_event(event)
        self.quit_button.handle_event(event)

    def update(self) -> None:
        if not self.is_active:
            return

        self.start_button.update()
        self.cog_button.update()
        self.quit_button.update()

    def draw(self) -> None:
        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
        self.start_button.draw(self.surface)
        self.cog_button.draw(self.surface)
        self.quit_button.draw(self.surface)
