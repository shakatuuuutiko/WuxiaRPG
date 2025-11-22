import pygame
import sys
import random
from config import FPS, COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.map_render import PygameMapRenderer
from ui.pygame_utils import Button

# Sistemas
from systems.creature_gen import CreatureGenerator
from systems.cultivation import CultivationManager
from systems.combat import CombatEngine
from systems.resource_gen_v2 import ProceduralResourceGen
from systems.slave_mgmt import SlaveManager
from systems.crafting import AlchemySystem
from systems.sect_politics import Sect

class GameEngine:
    def __init__(self, screen, player, time_sys, map_mgr, clock):
        self.screen = screen
        self.player = player
        self.time = time_sys
        self.map_mgr = map_mgr
        self.clock = clock
        self.running = True
        
        # Lógica
        self.beast_gen = CreatureGenerator()
        self.combat_sys = CombatEngine()
        self.cultivation = CultivationManager(self.player.stats)
        self.res_gen = ProceduralResourceGen()
        self.slave_mgr = SlaveManager(self.player)
        self.alchemy = AlchemySystem()
        
        self.renderer = PygameMapRenderer(screen, map_mgr)
        
        # ESTADO DEL JUEGO
        self.state = "EXPLORING" 
        # Estados: EXPLORING, COMBAT, MENU_INVENTORY, MENU_SECT, MENU_SLAVES, MENU_CRAFT
        
        self.current_enemy = None
        self.logs = ["Inicio del Dao."]
        self.menu_items = [] 
        self.menu_selection = 0
        
        self.setup_buttons()

    def setup_buttons(self):
        # Botones inferiores
        y = WINDOW_HEIGHT - 50
        self.btns = {
            "Explorar": Button(10, y, 100, 30, "Explorar", self.act_explore, COLORS["blue"]),
            "Meditar": Button(120, y, 100, 30, "Meditar", self.act_meditate, COLORS["green"]),
            "Inv": Button(230, y, 80, 30, "Bolsa", lambda: self.set_menu("MENU_INVENTORY"), COLORS["gold"]),
            "Secta": Button(320, y, 80, 30, "Secta", lambda: self.set_menu("MENU_SECT"), COLORS["gold"]),
            "Esclavos": Button(410, y, 100, 30, "Esclavos", lambda: self.set_menu("MENU_SLAVES"), COLORS["gold"]),
            "Craft": Button(520, y, 80, 30, "Forja", lambda: self.set_menu("MENU_CRAFT"), COLORS["gold"]),
        }

    def run(self):
        while self.running:
            self.handle_input()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: self.running = False
            
            if self.state == "EXPLORING":
                # Mouse para botones
                for btn in self.btns.values(): btn.handle_event(event)
                
                # Teclado Movimiento
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_w: dy = -1
                    elif event.key == pygame.K_s: dy = 1
                    elif event.key == pygame.K_a: dx = -1
                    elif event.key == pygame.K_d: dx = 1
                    if dx or dy: self.move_player(dx, dy)
                    
                    if event.key == pygame.K_SPACE: self.act_explore_spot()

            elif self.state == "COMBAT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.combat_attack()
                    elif event.key == pygame.K_2: self.combat_capture()
                    elif event.key == pygame.K_3: self.combat_flee()

            elif "MENU" in self.state:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.state = "EXPLORING"
                    if event.key == pygame.K_w: self.menu_selection = max(0, self.menu_selection - 1)
                    if event.key == pygame.K_s: self.menu_selection = min(len(self.menu_items)-1, self.menu_selection + 1)
                    if event.key == pygame.K_RETURN: self.handle_menu_action()

    def draw(self):
        self.screen.fill(COLORS["background"])
        
        # 1. Mapa
        self.renderer.draw_game_view(self.player.location)
        # 2. HUD Lateral
        self.renderer.draw_hud(self.player)
        # 3. Logs
        self.renderer.draw_logs(self.logs)

        # 4. ESTADOS
        if self.state == "EXPLORING":
            for btn in self.btns.values(): btn.draw(self.screen)
            
        elif self.state == "COMBAT":
            self.renderer.draw_combat(self.current_enemy)

        elif "MENU" in self.state:
            self.renderer.draw_menu(self.state, self.menu_items, self.menu_selection)

        pygame.display.flip()

    # --- LÓGICA DE ESTADOS ---
    def set_menu(self, menu_type):
        self.state = menu_type
        self.menu_selection = 0
        
        if menu_type == "MENU_INVENTORY":
            self.menu_items = list(self.player.inventory.keys())
        elif menu_type == "MENU_SLAVES":
            self.menu_items = [f"{s.original_name} ({s.loyalty}%)" for s in self.player.slaves]
            if not self.menu_items: self.menu_items = ["(Vacío)"]
        elif menu_type == "MENU_SECT":
            if not self.player.sect: self.menu_items = ["Fundar Secta (1000 Oro)", "Buscar Secta"]
            else: self.menu_items = ["Cobrar Impuestos", "Ver Miembros", "Abandonar"]
        elif menu_type == "MENU_CRAFT":
            self.menu_items = ["Mezclar Poción (Curativa)", "Forjar Espada"]

    def handle_menu_action(self):
        sel = self.menu_items[self.menu_selection]
        
        if self.state == "MENU_INVENTORY":
            if "Píldora" in sel:
                if self.player.inventory[sel] > 0:
                    self.player.inventory[sel] -= 1
                    if "Curativa" in sel: 
                        self.player.stats["hp"] = min(self.player.stats["max_hp"], self.player.stats["hp"] + 50)
                        self.log("Curado 50 HP.")
            if "Cadáver" in sel:
                # Despiece automático
                loot = self.beast_gen.harvest_corpse(sel)
                self.player.inventory[sel] -= 1
                if self.player.inventory[sel] <= 0: del self.player.inventory[sel]
                for k, v in loot.items():
                    self.player.inventory[k] = self.player.inventory.get(k, 0) + v
                self.log("Despiezado con éxito.")
                self.set_menu("MENU_INVENTORY") # Recargar

        elif self.state == "MENU_SECT":
            if "Fundar" in sel:
                if self.player.inventory["Oro"] >= 1000:
                    self.player.inventory["Oro"] -= 1000
                    self.player.sect = Sect("Secta Celestial", True)
                    self.player.sect.recruit(self.player.name, "Patriarca")
                    self.log("¡Secta Fundada!")
                else: self.log("Falta Oro.")
            elif "Cobrar" in sel:
                log = self.player.sect.daily_tick()
                self.log(str(log))

    # --- LÓGICA DE JUEGO ---
    def move_player(self, dx, dy):
        new_x = self.player.location[0] + dx
        new_y = self.player.location[1] + dy
        # Colisión simple
        try:
            t = self.map_mgr.get_tile_info(new_x, new_y)
            if t in ["Volcán", "ABISMO ESPACIAL"]: return
        except: pass
        
        self.player.location = [new_x, new_y]
        if random.random() < 0.1: self.trigger_encounter()

    def act_explore(self):
        if random.random() < 0.4: self.trigger_encounter()
        else:
            r = self.res_gen.generate(self.player.realm_idx + 1)
            self.player.inventory[r["name"]] = self.player.inventory.get(r["name"], 0) + 1
            self.log(f"Hallado: {r['name']}")

    def act_explore_spot(self): self.act_explore() # Espacio hace lo mismo

    def act_meditate(self):
        gain = 20
        self.player.stats["qi"] = min(self.player.stats["max_qi"], self.player.stats["qi"] + gain)
        self.log("Meditando... +20 Qi")

    def trigger_encounter(self):
        self.state = "COMBAT"
        self.current_enemy = self.beast_gen.generate(self.player.realm_idx + 1)
        self.log(f"¡ENEMIGO! {self.current_enemy['name']}")

    # --- COMBATE ---
    def combat_attack(self):
        dmg = self.player.stats["atk"]
        self.current_enemy["stats"]["hp"] -= dmg
        self.log(f"Golpeas: {dmg}")
        
        if self.current_enemy["stats"]["hp"] <= 0:
            self.log("Victoria.")
            c = self.current_enemy["loot"][0]
            self.player.inventory[c] = self.player.inventory.get(c, 0) + 1
            self.current_enemy = None
            self.state = "EXPLORING"
        else:
            self.enemy_turn()

    def combat_capture(self):
        suc, msg = self.slave_mgr.attempt_capture(self.current_enemy)
        self.log(msg)
        if suc:
            self.current_enemy = None
            self.state = "EXPLORING"
        else: self.enemy_turn()

    def combat_flee(self):
        if random.random() < 0.5:
            self.state = "EXPLORING"
            self.current_enemy = None
            self.log("Escapaste.")
        else:
            self.log("Fallo huida.")
            self.enemy_turn()

    def enemy_turn(self):
        edmg = max(1, self.current_enemy["stats"]["atk"] - self.player.stats["def"])
        self.player.stats["hp"] -= edmg
        self.log(f"Recibes {edmg} daño.")
        if self.player.stats["hp"] <= 0:
            self.log("MUERTE.")
            self.running = False

    def log(self, msg):
        self.logs.append(msg)
        if len(self.logs) > 6: self.logs.pop(0)