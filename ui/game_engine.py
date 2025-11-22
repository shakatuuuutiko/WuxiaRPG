import pygame
import sys
import random

# Configuración
from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT

# Sistemas Reales
from systems.map_core import MapManager
from systems.creature_gen import CreatureGenerator
from systems.cultivation import CultivationManager
from systems.combat import CombatEngine
from systems.resource_gen_v2 import ProceduralResourceGen
from systems.slave_mgmt import SlaveManager

# Renderizador
from ui.pygame_renderer import PygameRenderer

class GameEngine:
    def __init__(self, screen, player, time_sys):
        self.screen = screen
        self.player = player
        self.time = time_sys
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicializar Lógica
        self.map_mgr = MapManager()
        self.beast_gen = CreatureGenerator()
        self.combat = CombatEngine()
        self.cultivation = CultivationManager(self.player.stats)
        self.res_gen = ProceduralResourceGen()
        self.slave_mgr = SlaveManager(self.player)
        
        # Renderizador
        self.renderer = PygameRenderer(screen)
        
        # Estado del Juego
        self.state = "EXPLORING" # EXPLORING, COMBAT, INVENTORY
        self.current_enemy = None
        self.logs = ["Inicio del Dao."]

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # --- CONTROLES DE EXPLORACIÓN ---
                if self.state == "EXPLORING":
                    if event.key == pygame.K_w: self.move(0, -1)
                    elif event.key == pygame.K_s: self.move(0, 1)
                    elif event.key == pygame.K_a: self.move(-1, 0)
                    elif event.key == pygame.K_d: self.move(1, 0)
                    elif event.key == pygame.K_i: self.state = "INVENTORY"
                    elif event.key == pygame.K_c: self.action_meditate()
                    elif event.key == pygame.K_SPACE: self.action_explore_spot()

                # --- CONTROLES DE COMBATE ---
                elif self.state == "COMBAT":
                    if event.key == pygame.K_1: self.combat_attack()
                    elif event.key == pygame.K_2: self.log("¡Técnica! (WIP)") # Placeholder para skills
                    elif event.key == pygame.K_3: self.combat_capture()
                    elif event.key == pygame.K_4: self.action_flee()

                # --- CONTROLES DE MENÚ ---
                elif self.state == "INVENTORY":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                        self.state = "EXPLORING"

    def update(self):
        pass # Aquí irían animaciones o tiempo real

    def draw(self):
        self.renderer.draw_game(self)

    # ================= LÓGICA DE JUEGO =================

    def move(self, dx, dy):
        new_x = self.player.location[0] + dx
        new_y = self.player.location[1] + dy
        
        # Colisión simple
        try:
            tile = self.map_mgr.get_tile_info(new_x, new_y)
            if tile in ["Volcán", "Océano", "ABISMO ESPACIAL"]:
                self.log(f"Bloqueado: {tile}")
                return
        except: pass
        
        self.player.location = [new_x, new_y]
        
        # Encuentro aleatorio al caminar
        if random.random() < 0.10:
            self.trigger_encounter()

    def action_explore_spot(self):
        self.time.pass_time(1) # Pasa tiempo
        if random.random() < 0.4:
            self.trigger_encounter()
        else:
            # Recolección
            res = self.res_gen.generate(self.player.realm_idx + 1)
            name = res["name"]
            self.player.inventory[name] = self.player.inventory.get(name, 0) + 1
            self.log(f"Recolectado: {name}")

    def action_meditate(self):
        # Lógica de Cultivo
        realm_info = self.cultivation.get_realm_info(self.player.realm_idx)
        max_qi = realm_info["max_qi"]
        
        if self.player.stats["qi"] >= max_qi:
            self.log("Qi Lleno. Necesitas romper el cuello de botella (Usa item).")
            # Aquí podrías abrir un menú de ruptura
            return
            
        gain = 20
        self.player.stats["qi"] = min(max_qi, self.player.stats["qi"] + gain)
        self.log(f"Meditas... +{gain} Qi")

    def trigger_encounter(self):
        rank = self.player.realm_idx + 1
        self.current_enemy = self.beast_gen.generate(rank)
        self.state = "COMBAT"
        self.log(f"¡COMBATE! {self.current_enemy['name']}")

    # --- COMBATE ---
    def combat_attack(self):
        # Tu ataque
        dmg = self.player.stats["atk"]
        self.current_enemy["stats"]["hp"] -= dmg
        self.log(f"Golpeas por {dmg}.")
        
        if self.current_enemy["stats"]["hp"] <= 0:
            self.log("¡Victoria!")
            self.get_loot()
            self.state = "EXPLORING"
            self.current_enemy = None
        else:
            self.enemy_turn()

    def enemy_turn(self):
        # Ataque enemigo
        e_dmg = max(1, self.current_enemy["stats"]["atk"] - self.player.stats["def"])
        self.player.stats["hp"] -= e_dmg
        self.log(f"Recibes {e_dmg} daño.")
        
        if self.player.stats["hp"] <= 0:
            self.player.stats["hp"] = 0
            self.log("HAS MUERTO. (Reinicia el juego)")
            self.running = False # Game Over

    def combat_capture(self):
        success, msg = self.slave_mgr.attempt_capture(self.current_enemy, "Siervo")
        self.log(msg)
        if success:
            self.state = "EXPLORING"
            self.current_enemy = None
        else:
            self.enemy_turn()

    def action_flee(self):
        if random.random() < 0.5:
            self.log("Escapaste.")
            self.state = "EXPLORING"
            self.current_enemy = None
        else:
            self.log("Fallo al huir.")
            self.enemy_turn()

    def get_loot(self):
        corpse = self.current_enemy["loot"][0]
        self.player.inventory[corpse] = self.player.inventory.get(corpse, 0) + 1
        self.log(f"Botín: {corpse}")

    def log(self, msg):
        print(msg) # También a consola
        self.logs.append(msg)
        if len(self.logs) > 5: self.logs.pop(0)