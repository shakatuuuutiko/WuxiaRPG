import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CHUNK_SIZE

class PygameMapRenderer:
    def __init__(self, screen, map_mgr):
        self.screen = screen
        self.map_mgr = map_mgr
        try:
            self.font = pygame.font.SysFont("Arial", 16)
            self.font_icon = pygame.font.SysFont("Segoe UI Symbol", 20)
        except: pass

    def draw_game_view(self, loc):
        # Centro
        gx, gy = loc
        start_x = 300
        start_y = 50
        w, h = 30, 25
        
        for y in range(h):
            for x in range(w):
                wx = gx - (w//2) + x
                wy = gy - (h//2) + y
                
                try: tile = self.map_mgr.get_tile_info(wx, wy)
                except: tile = "Vacío"
                
                col = self._get_col(tile)
                icon = self._get_icon(tile)
                
                rect = (start_x + x*24, start_y + y*24, 24, 24)
                pygame.draw.rect(self.screen, col, rect)
                
                if icon:
                    txt = self.font_icon.render(icon, True, (255,255,255))
                    self.screen.blit(txt, rect)
        
        # Jugador
        cx = start_x + (w//2)*24 + 12
        cy = start_y + (h//2)*24 + 12
        pygame.draw.circle(self.screen, (255,0,0), (cx, cy), 8)

    def draw_hud(self, player):
        # Panel Izq
        pygame.draw.rect(self.screen, COLORS["panel"], (0,0,280,WINDOW_HEIGHT))
        self._txt(f"{player.name}", (20,20), COLORS["gold"])
        self._txt(f"HP: {player.stats['hp']}/{player.stats['max_hp']}", (20,50), COLORS["danger_red"])
        self._txt(f"Qi: {player.stats['qi']}/{player.stats['max_qi']}", (20,80), COLORS["qi_blue"])
        
    def draw_menu(self, title, items, sel_idx):
        # Overlay
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(200); s.fill((0,0,0))
        self.screen.blit(s, (0,0))
        
        # Caja
        rect = pygame.Rect(300, 100, 600, 500)
        pygame.draw.rect(self.screen, COLORS["panel"], rect)
        pygame.draw.rect(self.screen, COLORS["gold"], rect, 2)
        
        self._txt(title, (320, 120), COLORS["gold"])
        
        y = 160
        for i, item in enumerate(items):
            col = COLORS["warning_yellow"] if i == sel_idx else COLORS["text_light"]
            pre = "> " if i == sel_idx else "  "
            self._txt(f"{pre}{item}", (330, y), col)
            y += 25

    def draw_combat(self, enemy):
        s = pygame.Surface((WINDOW_WIDTH, 200))
        s.set_alpha(200); s.fill((50,0,0))
        self.screen.blit(s, (0,0))
        self._txt(f"¡ENEMIGO: {enemy['name']}!", (400, 50), COLORS["danger_red"])
        self._txt(f"HP: {enemy['stats']['hp']}", (400, 80), COLORS["text_light"])
        self._txt("[1] ATACAR  [2] CAPTURAR  [3] HUIR", (350, 130), COLORS["gold"])

    def draw_logs(self, logs):
        y = WINDOW_HEIGHT - 130
        for l in logs:
            self._txt(f"> {l}", (300, y), COLORS["text_light"])
            y += 20

    def _txt(self, t, p, c):
        surf = self.font.render(str(t), True, c)
        self.screen.blit(surf, p)

    def _get_col(self, t):
        if "Bosque" in t: return (34,100,34)
        if "Montaña" in t: return (100,100,100)
        if "Agua" in t: return (0,0,200)
        return (50,150,50)

    def _get_icon(self, t):
        if "Bosque" in t: return "🌳"
        if "Montaña" in t: return "🏔️"
        if "Océano" in t: return "🌊"
        if "Agua" in t: return "💦"
        if "Playa" in t: return "🌴"
        if "Llanura" in t: return "🌿"
        if "volcán" in t: return "⛰️"+"🔥"
        if "Desierto" in t: return "🌴"
        return ""