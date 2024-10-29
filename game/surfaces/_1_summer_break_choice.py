import pygame
from game.components.dialogue_banner import DialogueBanner
from game.components.choice_banner import ChoiceBanner
from game.surface import Surface, SurfaceManager
from game.asset import Assets
from bink.story import Story


class SummerBreakChoiceSurface(Surface):
    def __init__(
        self,
        surface: pygame.Surface,
        assets: Assets,
        manager: SurfaceManager,
        story: Story,
    ):
        super().__init__(surface)
        self.assets = assets
        self.story = story
        self.manager = manager
        self.background_image = assets.images.backgrounds.empty_classroom()
        self.background_image = pygame.transform.scale(
            self.background_image,
            (pygame.display.Info().current_w, pygame.display.Info().current_h),
        )

        initial_text = ""
        while self.story.can_continue():
            next_text = self.story.cont()
            if next_text.strip():  # Only use non-empty text
                initial_text = next_text
                break

        self.dialogue_banner = DialogueBanner(
            surface=surface,
            banner_image=assets.images.ui.banner_dialogue_wood(),
            text_content=initial_text,
            text_color=(42, 0, 30),
            font=self.assets.fonts.monogram_extended(50),
        )

        self.choice_banners = []
        self.update_choices()

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

    def update_choices(self):
        """Update the choice banners based on current story choices"""
        self.choice_banners.clear()
        choices = self.story.get_current_choices()

        for i, choice in enumerate(choices):  # type: ignore
            y_offset = 0.55 + (i * 0.08)  # Start lower and stack more compactly
            banner = ChoiceBanner(
                surface=self.surface,
                banner_image=self.assets.images.ui.banner_choice_wood(),
                text_content=choice,
                font=self.assets.fonts.monogram_extended(40),
                y_offset=y_offset,
                text_color=(42, 0, 30),
            )
            self.choice_banners.append((banner, i))

    def handle_event(self, event: pygame.event.Event) -> None:
        self.dialogue_banner.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.story.can_continue():
                # Skip empty dialogues
                next_text = ""
                while self.story.can_continue():
                    text = self.story.cont()
                    if text.strip():  # Only use non-empty text
                        next_text = text
                        break
                if next_text:  # Only update if we found non-empty text
                    self.dialogue_banner.update_text(next_text)
                self.update_choices()
            else:
                # Handle choice selection
                for banner, choice_idx in self.choice_banners:
                    if banner.handle_event(event):
                        self.story.choose_choice_index(choice_idx)
                        if self.story.can_continue():
                            # Skip empty dialogues after choice
                            next_text = ""
                            while self.story.can_continue():
                                text = self.story.cont()
                                if text.strip():  # Only use non-empty text
                                    next_text = text
                                    break
                            if next_text:  # Only update if we found non-empty text
                                self.dialogue_banner.update_text(next_text)
                            self.update_choices()

    def update(self) -> None: ...

    def draw(self) -> None:
        self.surface.blit(self.background_image, (0, 0))
        self.dialogue_banner.draw(self.surface)
        for banner, _ in self.choice_banners:
            banner.draw(self.surface)
