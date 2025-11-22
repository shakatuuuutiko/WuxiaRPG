import pygame
from config import COLORS

class Button:
    def __init__(self, x, y, width, height, text, callback, color=COLORS["panel_bg"]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255))
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def draw(self, surface):
        # Detectar hover
        mouse_pos = pygame.mouse.get_pos()
        curr_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Dibujar fondo y borde
        pygame.draw.rect(surface, curr_color, self.rect)
        pygame.draw.rect(surface, COLORS["white"], self.rect, 2)
        
        # Dibujar texto
        text_surf = self.font.render(self.text, True, COLORS["white"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback()