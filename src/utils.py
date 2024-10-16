import pygame

def render_text_with_effects(
    screen: pygame.Surface, 
    text: str, 
    font: pygame.font.Font, 
    pos: tuple[int, int], 
    border_color: tuple[int, int, int], 
    shadow_color: tuple[int, int, int], 
    shadow_offset: int
) -> None:
    """
    Renders a text with border, shadow and underline effects on the given pygame screen.
    """

    text_surface = font.render(text, True, (255, 255, 255))
    border_surface = font.render(text, True, border_color)
    shadow_surface = font.render(text, True, shadow_color)

    screen.blit(shadow_surface, (pos[0] + shadow_offset, pos[1] + shadow_offset))
    screen.blit(border_surface, pos)
    screen.blit(text_surface, pos)

    underline_start = (pos[0], pos[1] + text_surface.get_height() + 5)
    underline_end = (pos[0] + text_surface.get_width(), underline_start[1])
    pygame.draw.line(screen, (255, 215, 0), underline_start, underline_end, 4)
