import pygame
from game.assets import Assets
from game.surface import Surface, SurfaceManager
from game.components.text import Text
from game.components.button import Button

class EndCreditsSurface(Surface):
    """End credits surface showing game completion."""
    
    __slots__ = (
        "surface",
        "assets",
        "manager",
        "info",
        "background",
        "credits_lines",
        "button_click_1",
        "back_button",
        "fade_alpha",
        "scroll_position",
        "scroll_speed",
        "font_size",
        "line_spacing"
    )
    
    def __init__(self, surface: pygame.Surface, assets: Assets, manager: SurfaceManager) -> None:
        super().__init__()
        self.surface = surface
        self.assets = assets
        self.manager = manager
        self.info = pygame.display.Info()
        self.fade_alpha = 255
        self.scroll_position = self.surface.get_height()
        self.scroll_speed = 50
        self.font_size = 50
        self.line_spacing = 60
        self.__setup_background()
        self.__setup_text()
        self.__setup_button()
        
    def __setup_background(self) -> None:
        """Initialize background surface."""
        self.background = pygame.transform.scale(
            self.assets.images.backgrounds.moon_sky(),
            (self.info.current_w, self.info.current_h)
        )
        
    def __wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        """Wrap text to fit within the specified width."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = font.render(word + " ", True, (255, 255, 255))
            word_width = word_surface.get_width()
            
            if current_width + word_width > max_width:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
                else:
                    lines.append(word)
                    current_line = []
                    current_width = 0
            else:
                current_line.append(word)
                current_width += word_width
        
        if current_line:
            lines.append(" ".join(current_line))
            
        return lines
        
    def __setup_text(self) -> None:
        """Initialize credits text with word wrapping."""
        with open("assets/Credits.md", "r", encoding="utf-8") as f:
            credits_content = f.read()
            
        font = self.assets.fonts.monogram_extended(self.font_size)
        max_width = int(self.surface.get_width() * 0.8)  # 80% of screen width
        
        # Split content into sections and wrap each section
        self.credits_lines = []
        sections = credits_content.split('\n\n')  # Split by double newline
        
        for section in sections:
            wrapped_lines = self.__wrap_text(section.strip(), font, max_width)
            self.credits_lines.extend(wrapped_lines)
            self.credits_lines.append('')  # Add spacing between sections
        
    def __setup_button(self) -> None:
        """Initialize back to menu button."""
        self.button_click_1 = pygame.mixer.Sound(self.assets.sounds.button_click_1())
        self.manager.sfx_objects.append(self.button_click_1)
        
        self.back_button = Button(
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
            on_click=lambda _, __: self.manager.set_active_surface_by_name("root"),
            sound_on_click=self.button_click_1
        )
    
    def hook(self) -> None:
        """Hook up necessary components for this surface."""
        pygame.mixer.music.load(self.assets.sounds.ambient_evening())
        pygame.mixer.music.play(-1)
        self.fade_alpha = 255
        self.scroll_position = self.surface.get_height()
        
    def on_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_active_surface_by_name("root")
            return
            
        self.back_button.on_event(event)
        
    def update(self, delta_time: float) -> None:
        """Update the state of components."""
        self.back_button.update()
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 2)
            
        # Update scroll position
        self.scroll_position -= self.scroll_speed * delta_time
        
        # Reset scroll when credits reach the top
        total_height = len(self.credits_lines) * self.line_spacing
        if self.scroll_position < -total_height:
            self.scroll_position = self.surface.get_height()
    
    def draw(self) -> None:
        """Draw the end credits screen."""
        self.surface.blit(self.background, (0, 0))
        
        # Create a temporary surface for the credits text
        credits_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        font = self.assets.fonts.monogram_extended(self.font_size)
        
        # Draw each line of text
        y_pos = self.scroll_position
        center_x = self.surface.get_width() // 2
        
        for line in self.credits_lines:
            if line.strip():  # Only render non-empty lines
                text = Text(
                    content=line,
                    font=font,
                    position=(center_x, int(y_pos)),
                    color=(255, 255, 255),
                    center=True
                )
                text.draw(credits_surface)
            y_pos += self.line_spacing
        
        self.surface.blit(credits_surface, (0, 0))
        self.back_button.draw(self.surface)
        
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(self.surface.get_size())
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            self.surface.blit(fade_surface, (0, 0)) 