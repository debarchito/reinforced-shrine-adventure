import pygame
from typing import cast
from game.assets import Assets
from game.surface import Surface, SurfaceManager
from game.surfaces._3_walk_to_gate import WalkToGateSurface


class PackingSurface(Surface):
    """Second game scene surface that handles dialogue and choices."""

    __slots__ = ("surface", "assets", "manager", "info", "scene", "background_image")

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
        self.scene = self.manager.scene
        self.manager.sfx_objects.append(self.scene.button_click_1)
        self.__setup_background()

    def __setup_background(self) -> None:
        """Initialize and scale background image."""
        self.background_image = pygame.transform.scale(
            self.assets.images.backgrounds.bedroom(),
            (self.info.current_w, self.info.current_h),
        )

    def __next_scene(self) -> None:
        """Transition to the walk to gate scene."""
        walk_to_gate_surface = cast(
            WalkToGateSurface, self.manager.surfaces["walk_to_gate"]
        )
        walk_to_gate_surface.fade_transition(self.surface)
        self.manager.set_active_surface_by_name("walk_to_gate")

    def fade_transition(
        self,
        surface: pygame.Surface,
        color: tuple[int, int, int] = (0, 0, 0),
        duration: int = 1000,
    ) -> None:
        """Fade transition between surfaces."""
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

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        self.scene.setup()
        self.scene.update_choices()
        self.scene.on_scene_complete = self.__next_scene
        pygame.mixer.music.load(self.assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)

    def __handle_choice_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard/mouse input for choices."""
        choice_num = None
        if pygame.K_1 <= event.key <= pygame.K_9:
            choice_num = event.key - pygame.K_1
        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
            choice_num = event.key - pygame.K_KP1
        elif event.key == pygame.K_ESCAPE:
            self.manager.set_active_surface_by_name("pause")
            return

        if choice_num is not None and choice_num < len(self.scene.choice_banners):
            self.scene.handle_choice_selection(choice_num)

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events for dialogue and choices."""
        if not self.is_active or not self.scene.dialogue_banner:
            return

        if self.scene.dialogue_banner.on_event(event):
            self.scene.update_choices()
            return

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):
            self.scene.handle_dialogue_advance()
            if self.scene.should_show_next_dialogue_page():
                return

        if event.type == pygame.KEYDOWN:
            self.__handle_choice_input(event)
            return

        for banner, choice_idx in self.scene.choice_banners:
            if banner.on_event(event):
                self.scene.handle_choice_selection(choice_idx)
                break

    def update(self) -> None:
        """Update the state of surface components."""
        pass

    def draw(self) -> None:
        """Render the surface components."""
        if not self.is_active:
            return

        self.surface.blit(self.background_image, (0, 0))

        if self.scene.dialogue_banner:
            self.scene.dialogue_banner.draw(self.surface)

        if self.scene.character_sprite:
            sprite_x = int(self.surface.get_width() * 0.05)
            sprite_y = int(self.surface.get_height() * 0.58)
            self.surface.blit(self.scene.character_sprite, (sprite_x - 45, sprite_y))

        for banner, _ in self.scene.choice_banners:
            banner.draw(self.surface)
