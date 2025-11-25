import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, APP_TITLE

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("Times New Roman", 60, bold=True)
        self.font_option = pygame.font.SysFont("Arial", 30)
        self.font_small = pygame.font.SysFont("Arial", 16)
        
        self.options = ["NUEVA REENCARNACIÓN", "CONTINUAR CAMINO", "SALIR"]
        self.selected_index = 0

    def run(self):
        """Ejecuta el bucle del menú. Retorna la opción elegida."""
        running = True
        while running:
            self.screen.fill(COLORS["background"])
            
            # 1. Dibujar Título
            title_surf = self.font_title.render("LEYENDAS DE WUXIA", True, COLORS["gold"])
            title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title_surf, title_rect)
            
            sub_surf = self.font_small.render("v5.0 - Pygame Edition", True, COLORS["text_light"])
            self.screen.blit(sub_surf, (WINDOW_WIDTH // 2 - sub_surf.get_width() // 2, 200))

            # 2. Dibujar Opciones
            mouse_pos = pygame.mouse.get_pos()
            
            for i, option in enumerate(self.options):
                color = COLORS["text_light"]
                prefix = ""
                
                # Lógica de Selección (Teclado)
                if i == self.selected_index:
                    color = COLORS["warning_yellow"]
                    prefix = "> "
                
                # Lógica de Mouse (Hover)
                opt_surf = self.font_option.render(prefix + option, True, color)
                opt_rect = opt_surf.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 60))
                
                if opt_rect.collidepoint(mouse_pos):
                    self.selected_index = i # Actualizar selección si el mouse está encima
                    color = COLORS["gold"]
                    opt_surf = self.font_option.render(f"> {option} <", True, color)
                    opt_rect = opt_surf.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 60))

                self.screen.blit(opt_surf, opt_rect)

            pygame.display.flip()

            # 3. Inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected_index]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic izquierdo
                        # Verificar si hizo clic en alguna opción
                        for i, option in enumerate(self.options):
                            rect = self.font_option.render(option, True, (0,0,0)).get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 60))
                            # Expandir un poco el hitbox
                            rect.inflate_ip(100, 20)
                            if rect.collidepoint(event.pos):
                                return self.options[i]

            self.clock.tick(30)