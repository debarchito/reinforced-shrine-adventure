import pygame
from game.assets import Assets
from game.surface import Surface, SurfaceManager
from game.components.choice_banner import ChoiceBanner
from game.components.dialogue_banner import DialogueBanner


class SummerBreakChoiceSurface(Surface):
    """
    First game scene surface that handles dialogue and choices.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        assets: Assets,
        manager: SurfaceManager,
    ):
        super().__init__(surface)
        self.assets = assets
        self.story = self.assets.story
        self.manager = manager
        self.info = pygame.display.Info()
        self.choice_banners = []
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_sound_objects.append(self.button_click_1)
        self.__setup_background()
        self.__setup_initial_dialogue()
        self.__update_choices()

    def __setup_background(self) -> None:
        self.background_image = pygame.transform.scale(
            self.assets.images.backgrounds.empty_classroom(),
            (self.info.current_w, self.info.current_h),
        )

    def __setup_initial_dialogue(self) -> None:
        initial_text = self.__get_next_dialogue()
        char_name, dialogue_text = self.__parse_dialogue(initial_text)
        self.dialogue_banner = DialogueBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.banner_dialogue_wood(),
            text_content=dialogue_text,
            text_color=(42, 0, 30),
            font=self.assets.fonts.monogram_extended(50),
            character_name=char_name,
            character_name_color=(255, 215, 0),
            on_advance=self.button_click_1,
        )

    def __get_next_dialogue(self) -> str:
        while self.story.can_continue():
            text = self.story.cont()
            if text.strip():
                return text

        return ""

    def __parse_dialogue(self, text: str) -> tuple[str | None, str]:
        if not text.startswith("@"):
            return None, text

        parts = text.split(":", 1)
        if len(parts) != 2:
            return None, text

        return parts[0][1:].strip(), parts[1].strip()

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

    def __update_choices(self) -> None:
        """Update available choice banners."""

        self.choice_banners.clear()

        next_page_start = (self.dialogue_banner.current_page + 1) * (
            self.dialogue_banner.max_lines - 1
            if self.dialogue_banner.character_name
            else self.dialogue_banner.max_lines
        )

        if next_page_start < len(self.dialogue_banner.full_text_lines):
            return

        choices = self.story.get_current_choices()
        for i, choice in enumerate(choices):  # type: ignore
            y_offset = 0.55 + (i * 0.08)
            banner = ChoiceBanner(
                surface=self.surface,
                banner_image=self.assets.images.ui.banner_choice_wood(),
                text_content=f"{i+1}. {choice}",
                font=self.assets.fonts.monogram_extended(40),
                y_offset=y_offset,
                text_color=(42, 0, 30),
            )
            self.choice_banners.append((banner, i))

    def __handle_choice_selection(self, choice_idx: int) -> None:
        """Handle selection of a choice option."""

        self.story.choose_choice_index(choice_idx)
        if not self.story.can_continue():
            return

        next_text = self.__get_next_dialogue()
        if not next_text:
            return

        char_name, dialogue_text = self.__parse_dialogue(next_text)
        self.dialogue_banner.update_text(dialogue_text, char_name)
        self.__update_choices()

    def hook(self) -> None:
        """
        Hook up any necessary components for this surface.
        """

        pygame.mixer.music.load(self.assets.sounds.empty_classroom())
        pygame.mixer.music.play(-1)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events for dialogue and choices."""

        if not self.is_active:
            return

        if self.dialogue_banner.handle_event(event):
            self.__update_choices()
            return

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):
            if self.story.can_continue():
                next_text = self.__get_next_dialogue()
                if next_text:
                    char_name, dialogue_text = self.__parse_dialogue(next_text)
                    self.dialogue_banner.update_text(dialogue_text, char_name)
                self.__update_choices()
                return

            next_page_start = (self.dialogue_banner.current_page + 1) * (
                self.dialogue_banner.max_lines - 1
                if self.dialogue_banner.character_name
                else self.dialogue_banner.max_lines
            )
            if next_page_start < len(self.dialogue_banner.full_text_lines):
                return

        if event.type == pygame.KEYDOWN:
            choice_num = None
            if pygame.K_1 <= event.key <= pygame.K_9:
                choice_num = event.key - pygame.K_1
            elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                choice_num = event.key - pygame.K_KP1
            elif event.key == pygame.K_ESCAPE:
                self.manager.set_active_surface("pause")

            if choice_num is not None and choice_num < len(self.choice_banners):
                self.__handle_choice_selection(choice_num)
                return

        for banner, choice_idx in self.choice_banners:
            if banner.handle_event(event):
                self.__handle_choice_selection(choice_idx)
                break

    def update(self) -> None:
        """Update the state of surface components."""

        ...

    def draw(self) -> None:
        """Render the surface components."""

        if not self.is_active:
            return

        self.surface.blit(self.background_image, (0, 0))
        self.dialogue_banner.draw(self.surface)
        for banner, _ in self.choice_banners:
            banner.draw(self.surface)
