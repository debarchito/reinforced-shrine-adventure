import pygame
from game.components.dialogue_banner import DialogueBanner
from game.surface import Surface, SurfaceManager
from game.asset import Assets


class SummerBreakChoiceSurface(Surface):
    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ):
        super().__init__(surface)
        self.manager = manager
        self.background_image = assets.images.backgrounds.empty_classroom()
        self.background_image = pygame.transform.scale(
            self.background_image,
            (pygame.display.Info().current_w, pygame.display.Info().current_h),
        )
        self.dialogue_banner = DialogueBanner(
            surface=surface,
            banner_image=assets.images.ui.banner_dialogue(),
            text_content="This is some text (not final)",
            text_color=(0, 0, 0),
            font=assets.fonts.monogram_extended(50),
            banner_width_percent=0.9,
            banner_height_percent=0.3,
            text_x_percent=0.4,
            text_y_percent=0.5,
        )

    def fade_transition(self, surface, color=(0, 0, 0), duration=1000):
        """Fades from the start menu to the game surface over a specified duration."""

        fade_surface = pygame.Surface(surface.get_size())
        fade_surface.fill(color)
        fade_surface.set_alpha(255)
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            alpha = max(0, 255 - (255 * elapsed_time // duration))
            fade_surface.set_alpha(alpha)
            surface.blit(self.background_image, (0, 0))
            surface.blit(fade_surface, (0, 0))
            pygame.display.flip()

            if alpha == 0:
                break

            clock.tick(60)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.surface.blit(self.background_image, (0, 0))
        self.dialogue_banner.draw(self.surface)
