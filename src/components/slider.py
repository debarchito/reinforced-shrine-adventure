import pygame


class Slider:
    def __init__(self, rect, min_value, max_value, start_value, on_change):
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.on_change = on_change
        self.handle = pygame.Rect(
            self.rect.x
            + (self.rect.width * ((start_value - min_value) / (max_value - min_value))),
            self.rect.y,
            20,
            self.rect.height,
        )
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle.x = max(
                self.rect.x, min(event.pos[0], self.rect.right - self.handle.width)
            )
            self.value = self.min_value + (self.max_value - self.min_value) * (
                (self.handle.x - self.rect.x) / self.rect.width
            )
            self.on_change(self.value)

    def draw(self, surface):
        pygame.draw.rect(
            surface, (41, 78, 103), self.rect, border_radius=2
        )  # Background bar
        pygame.draw.rect(
            surface, (208, 239, 243), self.handle, border_radius=2
        )  # Handle
