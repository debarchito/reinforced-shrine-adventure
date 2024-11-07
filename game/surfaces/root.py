import pygame
from typing import cast
from game.assets import Assets
from game.components.button import Button
from game.surface import Surface, SurfaceManager
from game.surfaces._1_summer_break_choice import SummerBreakChoiceSurface


class RootSurface(Surface):
    """Main menu surface that handles the game's initial screen."""

    __slots__ = (
        "surface",
        "assets",
        "manager",
        "info",
        "background",
        "logo",
        "button_click_1",
        "start_button",
        "cog_button",
        "quit_button",
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
        self.__setup_logo()
        self.__setup_buttons()

    def __setup_background(self) -> None:
        """Initialize background surface."""
        self.background = pygame.transform.scale(
            self.assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )

    def __setup_logo(self) -> None:
        """Initialize logo image."""
        logo_surface = pygame.transform.scale(
            self.assets.logo(),
            (int(self.surface.get_width() * 0.8), int(self.surface.get_height() * 1.2)),
        )
        logo_rect = logo_surface.get_rect()
        logo_rect.center = (
            self.surface.get_width() // 1.92,  # type: ignore
            int(self.surface.get_height() * 0.2),
        )
        self.logo = (logo_surface, logo_rect)

    def __setup_buttons(self) -> None:
        """Initialize menu buttons and sound effects."""
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_objects.append(self.button_click_1)

        width = self.surface.get_width()
        height = self.surface.get_height()

        self.start_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_start(), (200, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_start_hover(), (200, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_start_active(), (200, 100)
            ),
            position=(width // 2, int(height * 0.6)),
            on_click=lambda _, __: self.__start_game(),
            sound_on_click=self.button_click_1,
        )

        self.cog_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_cog(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_cog_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_cog_active(), (100, 100)
            ),
            position=(width // 2 - 50, int(height * 0.73)),
            on_click=lambda _, __: self.manager.set_active_surface_by_name("settings"),
            sound_on_click=self.button_click_1,
        )

        self.quit_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_quit(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_quit_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_quit_active(), (100, 100)
            ),
            position=(width // 2 + 50, int(height * 0.73)),
            on_click=lambda _, __: pygame.quit(),
            sound_on_click=self.button_click_1,
        )

    def __start_game(self) -> None:
        """Transition to the first game scene."""
        summer_break_surface = cast(
            SummerBreakChoiceSurface,
            self.manager.surfaces[self.manager.last_active_scene_name],
        )
        summer_break_surface.fade_transition(self.surface)
        self.manager.set_active_surface_by_name(self.manager.last_active_scene_name)

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        current_music = pygame.mixer.music.get_busy()
        if not current_music or pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.load(self.assets.sounds.ambient_evening())
            pygame.mixer.music.play(-1)

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events for the main menu."""
        self.start_button.on_event(event)
        self.cog_button.on_event(event)
        self.quit_button.on_event(event)

    def update(self, delta_time: float) -> None:
        """Update the state of menu components."""
        self.start_button.update()
        self.cog_button.update()
        self.quit_button.update()

    def draw(self) -> None:
        """Render the menu components to the surface."""
        self.surface.blit(self.background, (0, 0))
        logo_surface, logo_rect = self.logo
        self.surface.blit(logo_surface, logo_rect)
        self.start_button.draw(self.surface)
        self.cog_button.draw(self.surface)
        self.quit_button.draw(self.surface)
