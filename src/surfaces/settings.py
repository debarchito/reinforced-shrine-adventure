import pygame
from surface import Surface  # type: ignore
from init import Assets  # type: ignore
from components.text import Text  # type: ignore


class SettingsSurface(Surface):
    def __init__(self, surface: pygame.Surface, assets: Assets):
        super().__init__(surface)
        self.info = pygame.display.Info()
        self.background = pygame.transform.scale(
            assets.images.backgrounds.moon_sky(), (self.info.current_w, self.info.current_h)
        )
        self.surface = pygame.display.set_mode(self.background.get_size(), pygame.FULLSCREEN)
        self.heading = Text(
            content="Settings Page",
            font=assets.fonts.monogram_extended(80),
            position=(surface.get_width() // 2, int(surface.get_height() * 0.3)),
        )
        pygame.mixer.music.load(assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
