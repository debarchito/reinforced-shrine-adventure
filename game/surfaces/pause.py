import pygame
from game.assets import Assets
from game.surface import Surface
from game.surface import SurfaceManager
from game.components.button import Button
from game.components.text import Text


class PauseSurface(Surface):
    """Pause menu surface with frosted glass effect."""

    __slots__ = (
        "surface",
        "assets",
        "manager",
        "backdrop",
        "blur_surface",
        "button_click_1",
        "font",
        "home_button",
        "quit_text",
        "resume_button",
        "resume_text",
        "exit_button",
        "exit_text",
    )

    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ) -> None:
        super().__init__()
        self.surface = surface
        self.assets = assets
        self.manager = manager
        self.font = assets.fonts.monogram_extended(70)
        surface_size = surface.get_size()
        self.backdrop = pygame.Surface(surface_size)
        self.blur_surface = pygame.Surface(surface_size, pygame.SRCALPHA)
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        manager.sfx_objects.append(self.button_click_1)
        center_x = self.surface.get_width() // 2
        center_y = self.surface.get_height() // 2
        self.__setup_home_button()
        self.__setup_resume_button(center_x, center_y)
        self.__setup_exit_button(center_x, center_y)
        self.__setup_text_labels(center_x, center_y)

    def __setup_home_button(self) -> None:
        """Initialize home button."""
        self.home_button = Button(
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
            on_click=self.__on_quit_click,
            sound_on_click=self.button_click_1,
        )

        self.quit_text = Text(
            content="Save & Return",
            center=False,
            font=self.font,
            position=(180, 60),
        )

    def __setup_resume_button(self, center_x: int, center_y: int) -> None:
        """Initialize resume button."""
        self.resume_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_play(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_play_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_play_active(), (100, 100)
            ),
            position=(center_x - 130, center_y),
            on_click=self.__on_resume_click,
            sound_on_click=self.button_click_1,
        )

        self.resume_text = Text(
            content="Continue",
            font=self.font,
            position=(center_x + 50, center_y),
        )

    def __setup_exit_button(self, center_x: int, center_y: int) -> None:
        """Initialize exit button."""
        self.exit_button = Button(
            normal_image=pygame.transform.scale(
                self.assets.images.ui.button_quit(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                self.assets.images.ui.button_quit_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                self.assets.images.ui.button_quit_active(), (100, 100)
            ),
            position=(center_x - 130, center_y + 120),
            on_click=self.__on_exit_click,
            sound_on_click=self.button_click_1,
        )

        self.exit_text = Text(
            content="Quit",
            font=self.font,
            position=(center_x, center_y + 120),
        )

    def __setup_text_labels(self, center_x: int, center_y: int) -> None:
        """Initialize text labels."""
        self.quit_text = Text(
            content="Save & Return",
            center=False,
            font=self.font,
            position=(180, 60),
        )

        self.resume_text = Text(
            content="Continue",
            font=self.font,
            position=(center_x + 50, center_y),
        )

        self.exit_text = Text(
            content="Quit",
            font=self.font,
            position=(center_x, center_y + 120),
        )

    def __glass_overlay(self) -> None:
        """Create frosted glass effect over the current display."""
        width = self.surface.get_width()
        height = self.surface.get_height()
        scale_factor = 0.05

        self.backdrop.blit(self.surface, (0, 0))
        self.blur_surface.fill((0, 0, 0, 180))

        small = pygame.transform.scale(
            self.backdrop,
            (int(width * scale_factor), int(height * scale_factor)),
        )
        blurred = pygame.transform.scale(small, (width, height))
        self.backdrop = blurred
        self.backdrop.blit(self.blur_surface, (0, 0))

    def __on_resume_click(self, button: Button, event: pygame.event.Event) -> None:
        """Handle resume button click."""
        self.manager.set_active_surface_by_name(self.manager.last_active_surface_name)  # type: ignore

    def __on_quit_click(self, button: Button, event: pygame.event.Event) -> None:
        """Handle quit button click."""
        self.manager.set_active_surface_by_name("root")

    def __on_exit_click(self, button: Button, event: pygame.event.Event) -> None:
        """Handle exit button click."""
        pygame.quit()
        exit()

    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        pygame.mixer.music.stop()
        self.__glass_overlay()

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events for the pause menu."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.__on_resume_click(self.resume_button, event)

        self.resume_button.on_event(event)
        self.home_button.on_event(event)
        self.exit_button.on_event(event)

    def update(self) -> None:
        """Update the state of pause menu components."""
        self.resume_button.update()
        self.home_button.update()
        self.exit_button.update()

    def draw(self) -> None:
        """Draw the pause menu components."""
        self.surface.blit(self.backdrop, (0, 0))
        self.resume_button.draw(self.surface)
        self.resume_text.draw(self.surface)
        self.home_button.draw(self.surface)
        self.quit_text.draw(self.surface)
        self.exit_button.draw(self.surface)
        self.exit_text.draw(self.surface)
