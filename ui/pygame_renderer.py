import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CHUNK_SIZE

class PygameRenderer:
    def __init__(self, screen, map_mgr):
        self.screen = screen
        self.map_mgr = map_mgr
        self.tile_size = 24
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_title = pygame.font.SysFont("Arial", 20, bold=True)
        
        # Cargar fuente de iconos si es posible, sino usar default
        try:
            self.font_icon = pygame.font.SysFont("Segoe UI Symbol", 20)
        except:
            self.font_icon = self.font

    def draw_game_view(self, player_location, player):
        # ... (Lógica de mapa igual que antes) ...
        # COPIAR LA LOGICA DE DRAW_GAME_VIEW DEL MENSAJE ANTERIOR AQUÍ
        # O usar esta versión simplificada:
        
        gx, gy = player_location
        start_x = 300
        start_y = 50
        
        # Dibujar un área de 30x25 tiles alrededor
        view_w, view_h = 30, 25
        
        for y in range(view_h):
            for x in range(view_w):
                wx = gx - (view_w // 2) + x
                wy = gy - (view_h // 2) + y
                
                try:
                    tile = self.map_mgr.get_tile_info(wx, wy)
                except:
                    tile = "Vacío"
                    
                color = self._get_color(tile)
                pygame.draw.rect(self.screen, color, (start_x + x*self.tile_size, start_y + y*self.tile_size, self.tile_size, self.tile_size))

        # Jugador
        cx = start_x + (view_w // 2) * self.tile_size
        cy = start_y + (view_h // 2) * self.tile_size
        pygame.draw.circle(self.screen, (255, 255, 255), (cx + 10, cy + 10), 8)

    def draw_stats_panel(self, player):
        rect = pygame.Rect(0, 0, 280, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["panel"], rect)
        pygame.draw.line(self.screen, COLORS["gray"], (280, 0), (280, WINDOW_HEIGHT))
        
        self._draw_text(f"Nombre: {player.name}", (20, 20), COLORS["gold"])
        self._draw_text(f"Reino: {player.realm_name}", (20, 50), COLORS["text_light"])
        self._draw_text(f"HP: {player.stats['hp']}/{player.stats['max_hp']}", (20, 80), COLORS["danger_red"])
        self._draw_text(f"Qi: {player.stats['qi']}/{player.stats['max_qi']}", (20, 110), COLORS["qi_blue"])
        self._draw_text(f"Oro: {player.inventory.get('Oro', 0)}", (20, 140), COLORS["warning_yellow"])
        
        self._draw_text("CONTROLES:", (20, WINDOW_HEIGHT - 150), COLORS["gray"])
        self._draw_text("WASD: Mover", (20, WINDOW_HEIGHT - 120), COLORS["gray"])
        self._draw_text("ESPACIO: Explorar", (20, WINDOW_HEIGHT - 100), COLORS["gray"])
        self._draw_text("I: Inventario/Usar", (20, WINDOW_HEIGHT - 80), COLORS["gray"])
        self._draw_text("M: Meditar", (20, WINDOW_HEIGHT - 60), COLORS["gray"])

    def draw_combat_overlay(self, enemy, logs):
        # Panel semi-transparente
        s = pygame.Surface((WINDOW_WIDTH, 200))
        s.set_alpha(200)
        s.fill((50, 0, 0))
        self.screen.blit(s, (0, 0))
        
        self._draw_text(f"¡ENEMIGO: {enemy['name']}!", (400, 20), COLORS["danger_red"], font=self.font_title)
        self._draw_text(f"HP: {enemy['stats']['hp']}/{enemy['stats']['max_hp']}", (400, 60), COLORS["text_light"])
        
        self._draw_text("[1] ATACAR   [2] TÉCNICA   [3] CAPTURAR   [4] HUIR", (350, 120), COLORS["gold"])

    def draw_menu_overlay(self, title, items, selection_index, quantities=None):
        """Dibuja una lista seleccionable (Inventario/Crafting)"""
        # Fondo
        rect = pygame.Rect(350, 100, 600, 500)
        pygame.draw.rect(self.screen, COLORS["panel"], rect)
        pygame.draw.rect(self.screen, COLORS["gold"], rect, 2)
        
        self._draw_text(title, (370, 120), COLORS["gold"], font=self.font_title)
        
        start_y = 160
        for i, item in enumerate(items):
            color = COLORS["white"]
            prefix = "  "
            if i == selection_index:
                color = COLORS["warning_yellow"]
                prefix = "> "
            
            qty_text = f" (x{quantities[item]})" if quantities else ""
            self._draw_text(f"{prefix}{item}{qty_text}", (380, start_y + i*25), color)

    def draw_logs(self, logs):
        y = WINDOW_HEIGHT - 150
        for log in logs:
            self._draw_text(f"> {log}", (300, y), COLORS["text_light"])
            y += 20

    def _draw_text(self, text, pos, color, font=None):
        if not font: font = self.font
        surf = font.render(str(text), True, color)
        self.screen.blit(surf, pos)
        
    def _get_color(self, tile):
        # Mapeo rápido para ejemplo
        if "Bosque" in tile: return (0, 100, 0)
        if "Agua" in tile: return (0, 0, 200)
        if "Montaña" in tile: return (100, 100, 100)
        return (34, 139, 34) # Llanura