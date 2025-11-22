import pygame
import sys
import random
from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from ui.pygame_utils import Button
from ui.pygame_renderer import PygameRenderer
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
        self.slave_mgr = SlaveManager(player)
        self.alchemy = AlchemySystem()
        
        self.renderer = PygameRenderer(screen, map_mgr)
        
        self.state = "EXPLORING"
        self.current_enemy = None
        self.logs = ["Inicio del Dao."]
        self.menu_items = []
        self.menu_selection = 0
        self.hover_info = "" # FIX: Inicializado
        
        self.setup_buttons()

    def setup_buttons(self):
        w, h = self.screen.get_size()
        y_base = h - 50 
        
        self.btns_explore = [
            Button(10, y_base, 100, 35, "EXPLORAR", self.act_explore, COLORS["blue"]),
            Button(120, y_base, 100, 35, "MEDITAR", self.act_meditate, COLORS["green"]),
            Button(230, y_base, 100, 35, "PASAR MES", self.action_wait, COLORS["gray"]),
        ]
        
        rx = w - 120
        sy = 100
        gap = 40
        self.btns_explore.append(Button(rx, sy, 110, 30, "INVENTARIO", lambda: self.set_menu("MENU_INVENTORY"), COLORS["gold"]))
        self.btns_explore.append(Button(rx, sy+gap, 110, 30, "SECTA", lambda: self.set_menu("MENU_SECT"), COLORS["gold"]))
        self.btns_explore.append(Button(rx, sy+gap*2, 110, 30, "CRAFTING", lambda: self.set_menu("MENU_CRAFT"), COLORS["gold"]))
        self.btns_explore.append(Button(rx, sy+gap*3, 110, 30, "ESCLAVOS", lambda: self.set_menu("MENU_SLAVES"), COLORS["gold"]))
        self.btns_explore.append(Button(rx, sy+gap*4, 110, 30, "MAPA MUNDI", self.open_global_map, COLORS["qi_blue"]))

        cx = w // 2
        cy = h - 100
        self.btns_combat = [
            Button(cx-200, cy, 100, 40, "ATACAR [1]", self.combat_attack, COLORS["red"]),
            Button(cx-90, cy, 100, 40, "TÉCNICA [2]", lambda: self.set_menu("MENU_SKILL"), COLORS["blue"]),
            Button(cx+20, cy, 100, 40, "SOMETER [3]", self.combat_capture, COLORS["gold"]),
            Button(cx+130, cy, 100, 40, "HUIR [4]", self.action_flee, COLORS["gray"])
        ]

    def run(self):
        while self.running:
            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

    def handle_input(self):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.renderer.screen = self.screen
                self.setup_buttons()

            if self.state == "EXPLORING":
                for btn in self.btns_explore: btn.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_w: dy = -1
                    elif event.key == pygame.K_s: dy = 1
                    elif event.key == pygame.K_a: dx = -1
                    elif event.key == pygame.K_d: dx = 1
                    if dx or dy: self.move_player(dx, dy)
                    if event.key == pygame.K_SPACE: self.act_explore_spot()
                    if event.key == pygame.K_m: self.open_global_map()

            elif self.state == "GLOBAL_MAP":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE: self.state = "EXPLORING"
                self.update_global_hover(mouse_pos)

            elif self.state == "COMBAT":
                for btn in self.btns_combat: btn.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.combat_attack()
                    elif event.key == pygame.K_3: self.combat_capture()
                    elif event.key == pygame.K_4: self.action_flee()

            elif "MENU" in self.state:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.state = "COMBAT" if self.current_enemy else "EXPLORING"
                    if event.key == pygame.K_w: self.menu_selection = max(0, self.menu_selection - 1)
                    if event.key == pygame.K_s: self.menu_selection = min(len(self.menu_items)-1, self.menu_selection + 1)
                    if event.key == pygame.K_RETURN: self.handle_menu_action()

    def draw(self):
        self.renderer.draw_game(self)
        if self.state == "EXPLORING":
            for btn in self.btns_explore: btn.draw(self.screen)
        elif self.state == "COMBAT":
            for btn in self.btns_combat: btn.draw(self.screen)
        pygame.display.flip()

    # --- LÓGICA ---
    def open_global_map(self):
        self.state = "GLOBAL_MAP"
        self.hover_info = "Moviendo vista..."

    def update_global_hover(self, pos):
        mx, my = pos
        w, h = self.screen.get_size()
        cell = 60
        start_x = (w - (9*cell))//2
        start_y = (h - (9*cell))//2
        
        dx = (mx - start_x)//cell
        dy = (my - start_y)//cell
        
        if 0 <= dx < 9 and 0 <= dy < 9:
            ctx = (self.player.location[0]//32) + (dx-4)
            cty = (self.player.location[1]//32) + (dy-4)
            biome = self.map_mgr.get_biome_at(ctx, cty)
            
            poi_txt = ""
            for name, c in self.map_mgr.poi_registry.items():
                if c[0]//32 == ctx and c[1]//32 == cty: poi_txt = f" | 🏛️ {name}"
            
            self.hover_info = f"[{ctx}, {cty}] {biome}{poi_txt}"
        else: self.hover_info = ""

    def set_menu(self, menu_type):
        self.state = menu_type
        self.menu_selection = 0
        if menu_type == "MENU_INVENTORY":
            self.menu_items = list(self.player.inventory.keys())
        elif menu_type == "MENU_SECT":
            self.menu_items = ["Fundar Secta (1000 Oro)", "Buscar"] if not self.player.sect else ["Cobrar", "Ver"]
        elif menu_type == "MENU_SLAVES":
            self.menu_items = [s.original_name for s in self.player.slaves] or ["(Vacío)"]
        elif menu_type == "MENU_CRAFT":
            self.menu_items = ["Pocion Curativa", "Forjar Espada"]
        elif menu_type == "MENU_SKILL":
            self.menu_items = list(self.player.skills.keys())
        elif menu_type == "MENU_BREAKTHROUGH":
            self.menu_items = ["ROMPER CUELLO DE BOTELLA", "CANCELAR"]

    def handle_menu_action(self):
        if not self.menu_items: return
        sel = self.menu_items[self.menu_selection]
        
        if self.state == "MENU_INVENTORY":
            if "Píldora" in sel and self.player.inventory[sel] > 0:
                self.player.inventory[sel] -= 1
                if "Curativa" in sel: self.player.stats["hp"] += 50
                if self.player.inventory[sel] == 0: del self.player.inventory[sel]
                self.set_menu("MENU_INVENTORY")
            elif "Cadáver" in sel:
                loot = self.beast_gen.harvest_corpse(sel)
                del self.player.inventory[sel]
                for k, v in loot.items(): self.player.inventory[k] = self.player.inventory.get(k,0)+v
                self.log("Despiezado.")
                self.set_menu("MENU_INVENTORY")
        
        elif self.state == "MENU_SKILL":
            data = self.player.skills[sel]
            if self.player.stats["qi"] >= data["cost"]:
                self.player.stats["qi"] -= data["cost"]
                self.combat_execute(sel, data["mult"])
            else: self.log("Falta Qi")
            
        elif self.state == "MENU_BREAKTHROUGH":
            if sel == "ROMPER CUELLO DE BOTELLA":
                self.do_breakthrough()
            self.state = "EXPLORING"

    # ... (Resto de métodos move, explore, combat igual) ...
    # COPIAR LOS MÉTODOS RESTANTES QUE YA TIENES FUNCIONANDO
    def move_player(self, dx, dy):
        try:
            t = self.map_mgr.get_tile_info(self.player.location[0]+dx, self.player.location[1]+dy)
            if t in ["Volcán", "ABISMO ESPACIAL"]: return
        except: pass
        self.player.location[0] += dx
        self.player.location[1] += dy
        if random.random() < 0.1: self.trigger_encounter()

    def act_explore(self):
        if random.random() < 0.4: self.trigger_encounter()
        else:
            r = self.res_gen.generate(self.player.realm_idx + 1)
            name = r["name"]
            self.player.inventory[name] = self.player.inventory.get(name, 0) + 1
            self.log(f"Hallado: {name}")

    def act_explore_spot(self): self.act_explore()

    def act_meditate(self):
        if self.player.stats["qi"] >= self.player.stats["max_qi"]:
            self.set_menu("MENU_BREAKTHROUGH")
            return
        gain = 20
        self.player.stats["qi"] = min(self.player.stats["max_qi"], self.player.stats["qi"] + gain)
        self.log(f"Meditas... +{gain} Qi")
        
    def do_breakthrough(self):
        self.player.realm_idx += 1
        info = self.cultivation.get_realm_info(self.player.realm_idx)
        self.player.stats["max_qi"] = info["max_qi"]
        self.player.stats["qi"] = 0
        self.player.realm_name = info["name"]
        self.player.stats["max_hp"] += 100
        self.log(f"¡AVANCE! {info['name']}")

    def action_wait(self):
        self.time.pass_time(1)
        self.log("Pasa un mes...")

    def trigger_encounter(self):
        self.state = "COMBAT"
        self.current_enemy = self.beast_gen.generate(self.player.realm_idx + 1)
        self.log(f"¡ENEMIGO! {self.current_enemy['name']}")

    def combat_attack(self):
        self.combat_execute("Ataque Básico", 1.0)

    def combat_execute(self, name, mult):
        dmg = int(self.player.stats["atk"] * mult)
        self.current_enemy["stats"]["hp"] -= dmg
        self.log(f"{name}: {dmg}")
        if self.current_enemy["stats"]["hp"] <= 0:
            l = self.current_enemy["loot"][0]
            self.player.inventory[l] = self.player.inventory.get(l, 0) + 1
            self.current_enemy = None
            self.state = "EXPLORING"
        else: self.enemy_turn()

    def combat_capture(self):
        suc, msg = self.slave_mgr.attempt_capture(self.current_enemy)
        self.log(msg)
        if suc:
            self.current_enemy = None
            self.state = "EXPLORING"
        else: self.enemy_turn()

    def action_flee(self):
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