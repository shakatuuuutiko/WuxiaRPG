import pygame
import sys
import random

from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from ui.pygame_utils import Button
from ui.pygame_renderer import PygameRenderer

# Importar Sistemas
from systems.map_core import MapManager
from systems.creature_gen import CreatureGenerator
from systems.cultivation import CultivationManager
from systems.combat import CombatEngine
from systems.resource_gen_v2 import ProceduralResourceGen
from systems.slave_mgmt import SlaveManager
from systems.crafting import AlchemySystem
from systems.manual_system import ManualManager
from ui.popups import PopupManager

class GameEngine:
    def __init__(self, screen, player, time_sys, map_mgr, clock):
        self.screen = screen
        self.player = player
        self.time = time_sys
        self.clock = clock
        self.running = True
        
        # Sistemas
        self.map_mgr = map_mgr
        self.beast_gen = CreatureGenerator()
        self.combat_sys = CombatEngine()
        self.cultivation = CultivationManager(self.player.stats)
        self.res_gen = ProceduralResourceGen()
        self.slave_mgr = SlaveManager(player)
        
        self.renderer = PygameRenderer(screen, map_mgr)
        
        # Estado
        self.state = "EXPLORING" 
        # Estados posibles: EXPLORING, COMBAT, MENU_SKILL, MENU_ITEM
        
        self.current_enemy = None
        self.logs = ["Bienvenido al Dao."]
        self.setup_ui()

    def setup_ui(self):
        # Botones Base (Exploración)
        self.btns_explore = [
            Button(20, 650, 100, 40, "Explorar", self.action_explore, COLORS["blue"]),
            Button(130, 650, 100, 40, "Meditar", self.action_meditate, COLORS["green"]),
            Button(240, 650, 100, 40, "Inventario", self.open_inv_popup, COLORS["gold"]), # Abre popup real
            Button(350, 650, 100, 40, "Secta", self.open_sect_popup, COLORS["gold"]),
            Button(460, 650, 100, 40, "Esclavos", self.open_slave_popup, COLORS["gold"]),
        ]
        
        # Botones Combate
        self.btns_combat = [
            Button(20, 650, 100, 40, "ATACAR", self.combat_attack_basic, COLORS["red"]),
            Button(130, 650, 100, 40, "TÉCNICA", self.open_skill_menu, COLORS["blue"]),
            Button(240, 650, 100, 40, "ITEM", self.open_item_menu, COLORS["green"]),
            Button(350, 650, 100, 40, "SOMETER", self.combat_capture, COLORS["gold"]),
            Button(460, 650, 100, 40, "HUIR", self.action_flee, COLORS["gray"]),
        ]

    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: self.running = False
            
            # Delegar eventos a botones según estado
            if self.state == "EXPLORING":
                for btn in self.btns_explore: btn.handle_event(event)
                
                # Movimiento
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_w: dy = -1
                    elif event.key == pygame.K_s: dy = 1
                    elif event.key == pygame.K_a: dx = -1
                    elif event.key == pygame.K_d: dx = 1
                    if dx or dy: self.move_player(dx, dy)

            elif self.state == "COMBAT":
                for btn in self.btns_combat: btn.handle_event(event)

            # Menús de Selección en Combate (Skills / Items)
            elif self.state in ["MENU_SKILL", "MENU_ITEM"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "COMBAT"
                    # Selección numérica 1-9
                    elif event.unicode.isdigit() and event.unicode != '0':
                        idx = int(event.unicode) - 1
                        self.handle_menu_selection(idx)

    def handle_menu_selection(self, idx):
        if self.state == "MENU_SKILL":
            skills = list(self.player.skills.keys())
            if idx < len(skills):
                s_name = skills[idx]
                data = self.player.skills[s_name]
                # Check Qi
                if self.player.stats["qi"] >= data["cost"]:
                    self.player.stats["qi"] -= data["cost"]
                    self.combat_execute_turn(s_name, data["mult"])
                    self.state = "COMBAT"
                else:
                    self.log("¡Falta Qi!")

        elif self.state == "MENU_ITEM":
            # Filtrar consumibles
            items = [k for k in self.player.inventory if "Píldora" in k]
            if idx < len(items):
                item = items[idx]
                self.player.inventory[item] -= 1
                if self.player.inventory[item] <= 0: del self.player.inventory[item]
                
                if "Curativa" in item:
                    self.player.stats["hp"] = min(self.player.stats["max_hp"], self.player.stats["hp"] + 50)
                    self.log("Usaste Píldora. +50 HP.")
                
                self.enemy_turn()
                self.state = "COMBAT"

    def update(self): pass

    def draw(self):
        self.screen.fill(COLORS["background"])
        
        # Mapa y UI
        map_rect = pygame.Rect(300, 50, WINDOW_WIDTH - 320, WINDOW_HEIGHT - 150)
        self.renderer.draw_map_view(self.player.location, self.player)
        self.renderer.draw_stats_panel(self.player)
        self.renderer.draw_logs(self.logs)

        # Botones
        if self.state == "EXPLORING":
            for btn in self.btns_explore: btn.draw(self.screen)
        elif self.state == "COMBAT":
            self.renderer.draw_combat_overlay(self.current_enemy, [])
            for btn in self.btns_combat: btn.draw(self.screen)

        # Menús Superpuestos
        if self.state == "MENU_SKILL":
            self.renderer.draw_menu_overlay("USAR TÉCNICA (1-9)", list(self.player.skills.keys()), -1)
        elif self.state == "MENU_ITEM":
            items = [k for k in self.player.inventory if "Píldora" in k]
            self.renderer.draw_menu_overlay("USAR OBJETO (1-9)", items, -1, self.player.inventory)

        pygame.display.flip()

    # --- LÓGICA ---
    def move_player(self, dx, dy):
        new_x = self.player.location[0] + dx
        new_y = self.player.location[1] + dy
        # Colisión
        try:
            tile = self.map_mgr.get_tile_info(new_x, new_y)
            if tile in ["Volcán", "ABISMO ESPACIAL"]: 
                self.log("Camino bloqueado.")
                return
        except: pass
        self.player.location = [new_x, new_y]
        if random.random() < 0.1: self.trigger_encounter()

    def action_explore(self):
        if random.random() < 0.4: self.trigger_encounter()
        else:
            res = self.res_gen.generate(self.player.realm_idx + 1)
            self.player.inventory[res["name"]] = self.player.inventory.get(res["name"], 0) + 1
            self.log(f"Recogiste: {res['name']}")

    def action_meditate(self):
        self.player.stats["qi"] = min(self.player.stats["max_qi"], self.player.stats["qi"] + 20)
        self.log("Meditando... +20 Qi")

    def trigger_encounter(self):
        rank = self.player.realm_idx + 1
        self.current_enemy = self.beast_gen.generate(rank)
        self.state = "COMBAT"
        self.log(f"¡ENEMIGO! {self.current_enemy['name']}")

    # --- COMBATE ---
    def combat_attack_basic(self):
        self.combat_execute_turn("Ataque Básico", 1.0)

    def open_skill_menu(self): self.state = "MENU_SKILL"
    def open_item_menu(self): self.state = "MENU_ITEM"

    def combat_capture(self):
        suc, msg = self.slave_mgr.attempt_capture(self.current_enemy)
        self.log(msg)
        if suc: 
            self.current_enemy = None
            self.state = "EXPLORING"
        else: self.enemy_turn()

    def action_flee(self):
        if random.random() < 0.5:
            self.log("Escapaste.")
            self.current_enemy = None
            self.state = "EXPLORING"
        else:
            self.log("Fallo al huir.")
            self.enemy_turn()

    def combat_execute_turn(self, atk_name, mult):
        dmg = int(self.player.stats["atk"] * mult)
        self.current_enemy["stats"]["hp"] -= dmg
        self.log(f"Usas {atk_name}: {dmg} daño.")
        
        if self.current_enemy["stats"]["hp"] <= 0:
            self.log("Victoria.")
            loot = self.current_enemy["loot"][0]
            self.player.inventory[loot] = self.player.inventory.get(loot, 0) + 1
            self.log(f"Obtuviste: {loot}")
            self.current_enemy = None
            self.state = "EXPLORING"
        else:
            self.enemy_turn()

    def enemy_turn(self):
        dmg = max(1, self.current_enemy["stats"]["atk"] - self.player.stats["def"])
        self.player.stats["hp"] -= dmg
        self.log(f"Recibes {dmg} daño.")
        if self.player.stats["hp"] <= 0:
            self.log("HAS MUERTO.")
            self.running = False

    # --- POPUPS ---
    def open_inv_popup(self): # Placeholder para usar el overlay o popup
        self.state = "INVENTORY" # Usamos overlay integrado de Pygame en lugar de popup
    
    def open_sect_popup(self): PopupManager.open_sect_ui(self.player, self.player.sect)
    def open_slave_popup(self): PopupManager.open_slave_ui(self.player)
    
    def log(self, msg):
        self.logs.append(msg)
        if len(self.logs) > 8: self.logs.pop(0)