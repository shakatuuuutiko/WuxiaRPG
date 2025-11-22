import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CHUNK_SIZE

class PygameRenderer:
    def __init__(self, screen, map_mgr):
        self.screen = screen
        self.map_mgr = map_mgr
        self.tile_size = 24
        
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_title = pygame.font.SysFont("Arial", 20, bold=True)
        
        # Fuente para iconos (Unicode seguro)
        try: self.font_icon = pygame.font.SysFont("Segoe UI Symbol", 20)
        except: self.font_icon = self.font

    def draw_game(self, engine):
        self.screen.fill(COLORS["background"])
        
        # 1. DIBUJAR CAPA BASE (Juego o Mapa Global)
        if engine.state == "GLOBAL_MAP":
            self._draw_global_map(engine.player, engine.hover_info)
        else:
            # Juego Normal
            self.draw_game_view(engine.player.location, engine.player)
            self.draw_stats_panel(engine.player)
            self.draw_logs(engine.logs)

        # 2. DIBUJAR OVERLAYS (Menús encima del juego)
        if engine.state == "COMBAT":
            self._draw_combat_overlay(engine.current_enemy)
            
        elif "MENU" in engine.state:
            titles = {
                "MENU_INVENTORY": "BOLSA ESPACIAL",
                "MENU_SECT": "GESTIÓN DE SECTA",
                "MENU_SLAVES": "MAZMORRA DE ALMAS",
                "MENU_CRAFT": "PABELLÓN DE ARTESANÍA",
                "MENU_SKILL": "TÉCNICAS MARCIALES",
                "MENU_BREAKTHROUGH": "CUELLO DE BOTELLA"
            }
            title = titles.get(engine.state, "MENÚ")
            qtys = engine.player.inventory if engine.state == "MENU_INVENTORY" else None
            
            self._draw_menu_overlay(title, engine.menu_items, engine.menu_selection, qtys)

    # --- MAPA GLOBAL ---
    def _draw_global_map(self, player, hover_info):
        cell_size = 60
        center_gx, center_gy = player.location
        center_cx = center_gx // CHUNK_SIZE
        center_cy = center_gy // CHUNK_SIZE
        view_range = 4 # 9x9
        
        # Centrar
        start_x = (WINDOW_WIDTH - (9 * cell_size)) // 2
        start_y = (WINDOW_HEIGHT - (9 * cell_size)) // 2
        
        self._txt_centered("MAPA GLOBAL (M para salir)", (WINDOW_WIDTH//2, 40), COLORS["gold"], size=30)

        for dy in range(-view_range, view_range + 1):
            for dx in range(-view_range, view_range + 1):
                cx = center_cx + dx
                cy = center_cy + dy
                
                biome = self.map_mgr.get_biome_at(cx, cy)
                col = self._get_col(biome)
                
                rect_x = start_x + (dx + view_range) * cell_size
                rect_y = start_y + (dy + view_range) * cell_size
                
                pygame.draw.rect(self.screen, col, (rect_x, rect_y, cell_size, cell_size))
                pygame.draw.rect(self.screen, (0,0,0), (rect_x, rect_y, cell_size, cell_size), 1)
                
                # Jugador
                if dx == 0 and dy == 0:
                    pygame.draw.circle(self.screen, (255,0,0), (rect_x + cell_size//2, rect_y + cell_size//2), 8)

                # POIs
                for name, coords in self.map_mgr.poi_registry.items():
                    pcx = coords[0] // CHUNK_SIZE
                    pcy = coords[1] // CHUNK_SIZE
                    if pcx == cx and pcy == cy:
                         pygame.draw.circle(self.screen, COLORS["gold"], (rect_x + 10, rect_y + 10), 5)
                         # Nombre pequeño si cabe
                         if dy == 0: self._txt(name, (rect_x, rect_y+20), COLORS["white"])

        if hover_info:
            self._txt_centered(hover_info, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 50), COLORS["white"], size=20)

    # --- MAPA LOCAL ---
    def draw_game_view(self, player_location, player):
        gx, gy = player_location
        start_x, start_y = 300, 50
        w_tiles, h_tiles = 30, 25
        
        for y in range(h_tiles):
            for x in range(w_tiles):
                wx = gx - (w_tiles//2) + x
                wy = gy - (h_tiles//2) + y
                try: tile = self.map_mgr.get_tile_info(wx, wy)
                except: tile = "Vacío"
                col = self._get_col(tile)
                rect = (start_x + x*self.tile_size, start_y + y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, col, rect)
                
                # Iconos simples
                icon = self._get_icon(tile)
                if icon:
                    txt = self.font_icon.render(icon, True, (255,255,255))
                    self.screen.blit(txt, (rect[0]+2, rect[1]+2))

        # Jugador
        cx = start_x + (w_tiles//2)*self.tile_size + 12
        cy = start_y + (h_tiles//2)*self.tile_size + 12
        pygame.draw.circle(self.screen, (255,0,0), (cx, cy), 8)

    # --- MENÚS Y HUD ---
    def draw_stats_panel(self, player):
        pygame.draw.rect(self.screen, COLORS["panel"], (0,0,280,WINDOW_HEIGHT))
        self._txt(f"{player.name}", (20,20), COLORS["gold"])
        self._txt(f"Reino: {player.realm_name}", (20,50), COLORS["text_light"])
        self._txt(f"HP: {int(player.stats['hp'])}", (20,80), COLORS["danger_red"])
        self._txt(f"Qi: {int(player.stats['qi'])}/{player.stats['max_qi']}", (20,110), COLORS["qi_blue"])
        self._txt(f"Oro: {player.inventory.get('Oro', 0)}", (20,140), COLORS["warning_yellow"])

    def _draw_menu_overlay(self, title, items, sel_idx, qtys=None):
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)); s.set_alpha(230); s.fill((0,0,0))
        self.screen.blit(s, (0,0))
        self._txt_centered(title, (WINDOW_WIDTH//2, 100), COLORS["gold"], size=40)
        
        start_y = 180
        if not items: self._txt_centered("(Vacío)", (WINDOW_WIDTH//2, start_y), COLORS["gray"])
        
        for i, item in enumerate(items):
            if start_y + i*30 > WINDOW_HEIGHT - 50: break
            col = COLORS["warning_yellow"] if i == sel_idx else COLORS["text_light"]
            pre = "> " if i == sel_idx else "  "
            q = f" (x{qtys[item]})" if qtys and item in qtys else ""
            self._txt(f"{pre}{item}{q}", (400, start_y + i*30), col)

    def _draw_combat_overlay(self, enemy):
        s = pygame.Surface((WINDOW_WIDTH, 250)); s.set_alpha(220); s.fill((50,0,0))
        self.screen.blit(s, (0,0))
        if enemy:
            self._txt_centered(f"¡ENEMIGO: {enemy['name']}!", (WINDOW_WIDTH//2, 50), COLORS["danger_red"], size=30)
            self._txt_centered(f"HP: {enemy['stats']['hp']}", (WINDOW_WIDTH//2, 90), COLORS["text_light"])

    def draw_logs(self, logs):
        y = WINDOW_HEIGHT - 160
        for l in logs:
            self._txt(f"> {l}", (300, y), COLORS["text_light"])
            y += 22

    # Helpers
    def _txt(self, t, p, c, size=None):
        f = self.font if not size else pygame.font.SysFont("Arial", size, bold=True)
        self.screen.blit(f.render(str(t), True, c), p)
    def _txt_centered(self, t, p, c, size=None):
        f = self.font if not size else pygame.font.SysFont("Arial", size, bold=True)
        s = f.render(str(t), True, c)
        self.screen.blit(s, s.get_rect(center=p))
    def _get_col(self, t): 
        return COLORS.get(t, COLORS["Llanura"])
    def _get_icon(self, t):
        if "Bosque" in t: return "♣"
        if "Montaña" in t: return "▲"
        if "Volcán" in t: return "🌋"
        if "Agua" in t: return "≈"
        return ""