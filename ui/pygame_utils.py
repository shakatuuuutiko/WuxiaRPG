import pygame
from config import COLORS

class Button:
    def __init__(self, x, y, width, height, text, callback, color=COLORS["panel"]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        r, g, b = color
        self.hover_color = (min(r+40, 255), min(g+40, 255), min(b+40, 255))
        
        if not pygame.font.get_init(): pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 14, bold=True)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        curr_color = self.hover_color if is_hovered else self.color
        pygame.draw.rect(surface, curr_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, COLORS["white"], self.rect, 1, border_radius=4)
        
        text_surf = self.font.render(self.text, True, COLORS["white"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback()