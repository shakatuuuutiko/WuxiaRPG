import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CHUNK_SIZE

class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont("Arial", 20)
        self.font_title = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_icon = pygame.font.SysFont("Segoe UI Symbol", int(TILE_SIZE * 0.8))

    def draw_game(self, engine):
        self.screen.fill(COLORS["background"])
        
        # 1. DIBUJAR MAPA
        self._draw_map(engine)
        
        # 2. DIBUJAR HUD (Barras de vida, info)
        self._draw_hud(engine.player)
        
        # 3. DIBUJAR ESTADOS (Combate, Inventario)
        if engine.state == "COMBAT":
            self._draw_combat_overlay(engine)
        elif engine.state == "INVENTORY":
            self._draw_inventory_overlay(engine.player)
        elif engine.state == "LOG":
            self._draw_log_overlay(engine.logs)

        pygame.display.flip()

    def _draw_map(self, engine):
        player_x, player_y = engine.player.location
        
        # Calcular cuántos tiles caben en pantalla
        tiles_w = WINDOW_WIDTH // TILE_SIZE
        tiles_h = WINDOW_HEIGHT // TILE_SIZE
        
        start_x = player_x - (tiles_w // 2)
        start_y = player_y - (tiles_h // 2)

        for y in range(tiles_h):
            for x in range(tiles_w):
                world_x = start_x + x
                world_y = start_y + y
                
                # Obtener terreno real del sistema
                try:
                    tile_type = engine.map_mgr.get_tile_info(world_x, world_y)
                except:
                    tile_type = "Vacío"

                # Color
                color = COLORS.get(tile_type, (255, 0, 255))
                if tile_type == "ABISMO ESPACIAL": color = (0, 0, 0)
                
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Jugador (Centro)
                if world_x == player_x and world_y == player_y:
                    pygame.draw.circle(self.screen, (255, 255, 255), rect.center, TILE_SIZE//2 - 2)

    def _draw_hud(self, player):
        # Panel inferior semi-transparente
        s = pygame.Surface((WINDOW_WIDTH, 100))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s, (0, WINDOW_HEIGHT - 100))
        
        # Textos
        self._draw_text(f"{player.name} [{player.title}]", (20, WINDOW_HEIGHT - 90), COLORS["gold"])
        self._draw_text(f"Reino: {player.realm_name} (G{player.realm_idx})", (20, WINDOW_HEIGHT - 60), COLORS["text_light"])
        
        # Barras
        self._draw_bar(300, WINDOW_HEIGHT - 80, 200, 20, player.stats["hp"], player.stats["max_hp"], COLORS["danger_red"])
        self._draw_text(f"HP", (260, WINDOW_HEIGHT - 80), COLORS["text_light"])
        
        self._draw_bar(300, WINDOW_HEIGHT - 50, 200, 20, player.stats["qi"], player.stats["max_qi"], COLORS["qi_blue"])
        self._draw_text(f"Qi", (260, WINDOW_HEIGHT - 50), COLORS["text_light"])
        
        # Controles
        controls = "WASD: Mover | ESPACIO: Explorar/Interactuar | I: Inventario | C: Cultivar"
        self._draw_text(controls, (600, WINDOW_HEIGHT - 70), COLORS["gray"])

    def _draw_combat_overlay(self, engine):
        enemy = engine.current_enemy
        
        # Fondo Oscuro
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((20, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        # Info Enemigo
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self._draw_text(f"¡ENEMIGO: {enemy['name']}!", (cx - 150, cy - 100), COLORS["danger_red"], size=40)
        self._draw_text(f"Rango: {enemy['rank']} | Elemento: {enemy['element']}", (cx - 100, cy - 50), COLORS["text_light"])
        
        # Barra Vida Enemigo
        self._draw_bar(cx - 200, cy, 400, 30, enemy['stats']['hp'], enemy['stats']['max_hp'], COLORS["danger_red"])
        
        # Menú de Acción
        actions = "[1] Atacar Físico  [2] Usar Técnica  [3] Capturar (Someter)  [4] Huir"
        self._draw_text(actions, (cx - 250, cy + 100), COLORS["gold"])
        
        # Log de combate reciente
        if engine.logs:
            self._draw_text(f"> {engine.logs[-1]}", (cx - 250, cy + 150), COLORS["white"])

    def _draw_inventory_overlay(self, player):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((10, 10, 20))
        self.screen.blit(overlay, (0,0))
        
        self._draw_text("BOLSA ESPACIAL", (50, 50), COLORS["gold"], size=30)
        
        y = 100
        for item, qty in player.inventory.items():
            self._draw_text(f"- {item}: {qty}", (60, y), COLORS["text_light"])
            y += 30
            
        self._draw_text("[ESC] Cerrar", (50, WINDOW_HEIGHT - 50), COLORS["gray"])

    def _draw_log_overlay(self, logs):
        # Opcional: Mostrar historial completo
        pass

    def _draw_text(self, text, pos, color, size=20):
        font = self.font_main if size == 20 else pygame.font.SysFont("Arial", size, bold=True)
        surf = font.render(str(text), True, color)
        self.screen.blit(surf, pos)

    def _draw_bar(self, x, y, w, h, current, max_val, color):
        pct = max(0, min(1, current / max(1, max_val)))
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, w, h)) # Fondo
        pygame.draw.rect(self.screen, color, (x, y, int(w * pct), h)) # Relleno
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 1) # Borde
        
        # Texto numérico
        text = f"{int(current)}/{int(max_val)}"
        font = pygame.font.SysFont("Arial", 14)
        surf = font.render(text, True, (255, 255, 255))
        self.screen.blit(surf, (x + w//2 - surf.get_width()//2, y + 2))