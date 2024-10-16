import pygame

def load_assets(asset_dict):
    loaded_assets = {}
    for key, path in asset_dict.items():
        if key.startswith("button_"):
            loaded_assets[key] = pygame.image.load(path)
        elif key == "font_monogram_extended":
            loaded_assets[key] = pygame.font.Font(path, 86)
        elif key == "sound_ambient_evening":
            loaded_assets[key] = path
    return loaded_assets

def render_text_with_effects(screen, text, font, pos, border_color, shadow_color, shadow_offset):
    text_surface = font.render(text, True, (255, 255, 255))
    border_surface = font.render(text, True, border_color)
    shadow_surface = font.render(text, True, shadow_color)

    screen.blit(shadow_surface, (pos[0] + shadow_offset, pos[1] + shadow_offset))
    screen.blit(border_surface, pos)
    screen.blit(text_surface, pos)

    underline_start = (pos[0], pos[1] + text_surface.get_height() + 5)
    underline_end = (pos[0] + text_surface.get_width(), underline_start[1])
    pygame.draw.line(screen, (255, 215, 0), underline_start, underline_end, 4)
