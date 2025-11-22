# --- SCRIPT MAESTRO: WUXIA RPG (PYGAME EDITION) ---
# Versión: 5.0 (Motor Gráfico Puro)

import pygame
import sys
import random

# --- CONFIGURACIÓN ---
# Asegúrate de que config.py tenga WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE, FPS
from config import WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE, FPS

# --- IMPORTACIONES DE SISTEMAS (LÓGICA DE DATOS) ---
try:
    from systems.cultivation import SpiritRoot
    from systems.bloodline import Bloodline
    from systems.time_system import TimeSystem, AgeManager
    from systems.origin_generator import OriginGenerator
    from systems.map_core import MapManager
except ImportError as e:
    print("FATAL ERROR: Faltan archivos de sistema.")
    print(f"Detalle: {e}")
    sys.exit()

# --- IMPORTACIÓN DEL MOTOR DE JUEGO (UI GRÁFICA) ---
try:
    from ui.game_engine import GameEngine
except ImportError as e:
    print("FATAL ERROR: Falta el motor gráfico (ui/game_engine.py).")
    print(f"Detalle: {e}")
    sys.exit()


# =====================================================
# 1. CLASE JUGADOR (MODELO DE DATOS)
# =====================================================
class Player:
    def __init__(self):
        print("--- Inicializando Alma del Jugador ---")
        
        # 1. Generar Origen Procedural
        self.origin_gen = OriginGenerator()
        self.origin_data = self.origin_gen.generate()
        
        self.name = self._generate_wuxia_name()
        self.title = self.origin_data["title"]
        
        # 2. Stats Base
        self.stats = {
            "hp": 150, "max_hp": 150,
            "qi": 0, "max_qi": 100,
            "stamina": 100, "max_stamina": 100,
            "atk": 20, "def": 10,
            "comprension": 10, "suerte": 0,
            "dao_espacial": 0, "dao_devorar": 0
        }
        
        # 3. Aplicar Modificadores del Origen
        mods = self.origin_data.get("stats_mod", {})
        for stat, value in mods.items():
            if stat in self.stats:
                self.stats[stat] += value
                if stat in ["hp", "stamina"]:
                    self.stats[f"max_{stat}"] += value
            elif stat == "qi":
                self.stats["qi"] = value

        if self.stats["max_hp"] < 50: self.stats["max_hp"] = 50
        self.stats["hp"] = self.stats["max_hp"]

        self.realm_idx = 0
        self.realm_name = "Mortal"
        
        # 4. Sistemas Místicos
        flags = self.origin_data.get("flags", {})
        
        self.spirit_root = SpiritRoot()
        if "root" in flags: 
            self.spirit_root.tier = flags["root"]
            self.spirit_root.cultivation_mult = 2.5 
            self.spirit_root.elements = ["Vacío"]

        self.bloodline = Bloodline()    
        if "bloodline" in flags: 
            self.bloodline.purity = 20.0 
            self.bloodline.ancestor = random.choice(["Dragón", "Fénix", "Tigre"])

        self.age_sys = AgeManager(self)
        
        # 5. Inventario
        self.inventory = {"Oro": self.origin_data.get("gold", 0)}
        origin_inv = self.origin_data.get("inventory", {})
        for item, qty in origin_inv.items():
            self.inventory[item] = self.inventory.get(item, 0) + qty
            
        # Kit Inicial
        self.inventory["Píldora Curativa"] = self.inventory.get("Píldora Curativa", 0) + 3
        self.inventory["Píldora de Fundación"] = self.inventory.get("Píldora de Fundación", 0) + 1
        
        self.slaves = []
        self.skills = {
            "Puño Básico": {"cost": 0, "mult": 1.0, "elem": "Neutro"},
            "Palma de Qi": {"cost": 10, "mult": 1.5, "elem": "Neutro"}
        }
        
        # 6. Ubicación (Spawn)
        start_range = 1000
        start_x = random.randint(-start_range, start_range)
        start_y = random.randint(-start_range, start_range)
        self.location = [start_x, start_y]

        print(f"Jugador Listo: {self.name} [{self.title}] en {self.location}")

    def _generate_wuxia_name(self):
        surnames = ["Li", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou", "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Lin", "Luo", "Jiang", "Fan", "Su", "Han", "Tang", "Feng", "Jin", "Wei", "Ye", "Bai"]
        given_names = ["Wei", "Jie", "Hao", "Yi", "Fan", "Lei", "Xin", "Ying", "Xiu", "Mei", "Lan", "Feng", "Long", "Hu", "Gui", "Chen", "Yun", "Tian", "Ming", "Hua", "Shan", "Ren", "Kai", "Jian", "Ping", "An", "Bo", "Cheng", "Dong", "Gang"]
        return f"{random.choice(surnames)} {random.choice(given_names)}"

    @property
    def age(self): return self.age_sys.current_age
    
    @property
    def max_lifespan(self): return self.age_sys.max_lifespan


# =====================================================
# 3. FUNCIÓN PRINCIPAL (BOOTSTRAP)
# =====================================================
def main():
    print("--- Inicializando Pygame ---")
    pygame.init()
    pygame.font.init()
    
    # Configurar Pantalla
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(APP_TITLE)
    
    # Reloj
    clock = pygame.time.Clock()
    
    # Crear Instancias de Datos
    player = Player()
    time_sys = TimeSystem()
    map_mgr = MapManager() # El gestor de chunks y archivos

    print("--- Lanzando Motor de Juego ---")
    
    # Iniciar el Bucle Principal (GameEngine maneja el while True)
    try:
        engine = GameEngine(screen, player, time_sys, map_mgr, clock)
        engine.run()
    except Exception as e:
        print(f"CRASH DEL MOTOR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()