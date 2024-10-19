import pygame
from src.surface import Surface, SurfaceManager
from src.init import Assets
from src.components.text import Text
from src.components.button import Button


class Slider:
    def __init__(self, rect, min_value, max_value, start_value, on_change):
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.on_change = on_change
        self.handle = pygame.Rect(self.rect.x, self.rect.y, 20, self.rect.height)
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle.x = max(self.rect.x, min(event.pos[0], self.rect.right - self.handle.width))
            self.value = self.min_value + (self.max_value - self.min_value) * ((self.handle.x - self.rect.x) / self.rect.width)
            self.on_change(self.value)

    def draw(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.handle)


class SettingsSurface(Surface):
    def __init__(self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager):
        super().__init__(surface)
        self.info = pygame.display.Info()
        self.assets = assets
        self.manager = manager
        self.background = pygame.transform.scale(
            assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h),
        )
        self.heading = Text(
            content="Settings",
            font=assets.fonts.monogram_extended(80),
            position=(300, 85),
        )
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_sound_objects.append(self.button_click_1)
        self.back_button = Button(
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
            on_click=lambda _button, _event: manager.set_active_surface("root"),
            sound_on_click=self.button_click_1,
        )

        # Add sliders for SFX and Music volume control
        self.sfx_slider = Slider(
            rect=(self.surface.get_width() // 2 - 100, 200, 200, 20),
            min_value=0.0,
            max_value=1.0,
            start_value=self.manager.current_global_sfx_volume,
            on_change=self.set_sfx_volume
        )

        self.music_slider = Slider(
            rect=(self.surface.get_width() // 2 - 100, 300, 200, 20),
            min_value=0.0,
            max_value=1.0,
            start_value=pygame.mixer.music.get_volume(),
            on_change=self.set_music_volume
        )

    def set_sfx_volume(self, volume):
        """Set global SFX volume."""
        self.manager.set_global_sfx_volume(volume)

    def set_music_volume(self, volume):
        """Set global music volume."""
        pygame.mixer.music.set_volume(volume)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.is_active:
            return

        self.back_button.handle_event(event)
        self.sfx_slider.handle_event(event)
        self.music_slider.handle_event(event)

    def update(self) -> None:
        if not self.is_active:
            return

        self.back_button.update()

    def draw(self) -> None:
        if not self.is_active:
            return

        self.surface.blit(self.background, (0, 0))
        self.heading.draw(self.surface)
        self.back_button.draw(self.surface)
        self.sfx_slider.draw(self.surface)
        self.music_slider.draw(self.surface)
