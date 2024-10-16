import pygame

class Button:
    def __init__(self, normal_image, hover_image, position, on_click=None):
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.position = position
        self.on_click = on_click
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect(center=position)
        self.is_hovered = False

    def update(self):
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.current_image = self.hover_image if self.is_hovered else self.normal_image

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            if self.on_click:
                self.on_click()

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)
