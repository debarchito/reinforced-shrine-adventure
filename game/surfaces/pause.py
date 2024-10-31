import pygame
from game.assets import Assets
from game.surface import Surface
from game.surface import SurfaceManager
from game.components.button import Button
from game.components.text import Text


class PauseSurface(Surface):
    """
    Pause menu surface with frosted glass effect.
    """

    def __init__(
        self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager
    ):
        super().__init__(surface)
        self.manager = manager
        center_x = self.surface.get_width() // 2
        center_y = self.surface.get_height() // 2
        self.backdrop = pygame.Surface(surface.get_size())
        self.blur_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        manager.sfx_sound_objects.append(self.button_click_1)

        self.home_button = Button(
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
            on_click=self.__on_quit_click,
            sound_on_click=self.button_click_1,
        )

        self.quit_text = Text(
            content="Save & Return",
            center=False,
            font=assets.fonts.monogram_extended(70),
            position=(180, 60),
        )

        self.resume_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_play(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_play_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_play_active(), (100, 100)
            ),
            position=(center_x - 130, center_y),
            on_click=self.__on_resume_click,
            sound_on_click=self.button_click_1,
        )

        self.resume_text = Text(
            content="Continue",
            font=assets.fonts.monogram_extended(70),
            position=(center_x + 50, center_y),
        )

        self.exit_button = Button(
            normal_image=pygame.transform.scale(
                assets.images.ui.button_quit(), (100, 100)
            ),
            hover_image=pygame.transform.scale(
                assets.images.ui.button_quit_hover(), (100, 100)
            ),
            active_image=pygame.transform.scale(
                assets.images.ui.button_quit_active(), (100, 100)
            ),
            position=(center_x - 130, center_y + 120),
            on_click=self.__on_exit_click,
            sound_on_click=self.button_click_1,
        )

        self.exit_text = Text(
            content="Quit",
            font=assets.fonts.monogram_extended(70),
            position=(center_x, center_y + 120),
        )

    def __glass_overlay(self) -> None:
        """
        Create frosted glass effect over the current display
        """

        self.backdrop.blit(self.surface, (0, 0))
        self.blur_surface.fill((0, 0, 0, 180))
        scale_factor = 0.05
        small = pygame.transform.scale(
            self.backdrop,
            (
                int(self.surface.get_width() * scale_factor),
                int(self.surface.get_height() * scale_factor),
            ),
        )
        blurred = pygame.transform.scale(
            small, (self.surface.get_width(), self.surface.get_height())
        )
        self.backdrop = blurred
        self.backdrop.blit(self.blur_surface, (0, 0))

    def __on_resume_click(self, button: Button, event: pygame.event.Event) -> None:
        self.manager.set_active_surface(self.manager.last_active_surface)  # type: ignore

    def __on_quit_click(self, button: Button, event: pygame.event.Event) -> None:
        self.manager.set_active_surface("root")

    def __on_exit_click(self, button: Button, event: pygame.event.Event) -> None:
        pygame.quit()
        exit()

    def hook(self) -> None:
        pygame.mixer.music.stop()
        self.__glass_overlay()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle input events for the pause menu.
        """

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.__on_resume_click(self.resume_button, event)

        self.resume_button.handle_event(event)
        self.home_button.handle_event(event)
        self.exit_button.handle_event(event)

    def update(self) -> None:
        """
        Update the state of pause menu components.
        """

        self.resume_button.update()
        self.home_button.update()
        self.exit_button.update()

    def draw(self) -> None:
        """
        Draw the pause menu components.
        """

        self.surface.blit(self.backdrop, (0, 0))
        self.resume_button.draw(self.surface)
        self.resume_text.draw(self.surface)
        self.home_button.draw(self.surface)
        self.quit_text.draw(self.surface)
        self.exit_button.draw(self.surface)
        self.exit_text.draw(self.surface)
