# game_surface.py
import pygame
from game.surface import Surface, SurfaceManager
from game.asset import Assets
from pygame.locals import *

class GameSurface(Surface):
    def __init__(self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager):
        super().__init__(surface)
        self.assets = assets
        self.manager = manager
        self.background_image = pygame.image.load("assets/images/backgrounds/afternoon_empty_classroom.jpeg")
        self.background_image = pygame.transform.scale(
            self.background_image,
            (pygame.display.Info().current_w, pygame.display.Info().current_h)
        )

    # Define the fade function
    def fade_transition(self, surface, color=(0, 0, 0), duration=1000):
        """Fades from the start menu to the game surface over a specified duration."""
        fade_surface = pygame.Surface(surface.get_size())
        fade_surface.fill(color)
        fade_surface.set_alpha(255)  # Start fully opaque
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        
        # Loop to gradually reduce the alpha of the fade surface
        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            # Calculate the alpha based on elapsed time and duration
            alpha = max(0, 255 - (255 * elapsed_time // duration))
            fade_surface.set_alpha(alpha)
            
            # Draw the fade surface on top
            surface.blit(self.background_image, (0, 0))
            surface.blit(fade_surface, (0, 0))
            pygame.display.flip()

            # Break once the fade is complete
            if alpha == 0:
                break

            clock.tick(60)  # Cap the frame rate to make the fade smoother

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Switch to the settings surface when Esc is pressed
            self.manager.set_active_surface("settings")

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.surface.blit(self.background_image, (0, 0))
