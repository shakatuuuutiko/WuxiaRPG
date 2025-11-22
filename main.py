# --- SCRIPT MAESTRO: WUXIA RPG (PYGAME EDITION) ---
# Versión: 6.0 (Nombres Reales y Sistemas Finales)

import pygame
import sys
import random

# --- CONFIGURACIÓN ---
try:
    from config import WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE, FPS
except ImportError:
    print("ERROR: Falta el archivo config.py")
    sys.exit()

# --- IMPORTACIONES DE SISTEMAS ---
try:
    from systems.cultivation import SpiritRoot
    from systems.bloodline import Bloodline
    from systems.time_system import TimeSystem, AgeManager
    from systems.origin_generator import OriginGenerator
    from systems.map_core import MapManager
    from ui.game_engine import GameEngine
    from ui.main_menu import MainMenu
except ImportError as e:
    print(f"FATAL ERROR: Faltan archivos. {e}")
    sys.exit()

# =====================================================
# CLASE JUGADOR
# =====================================================
class Player:
    def __init__(self):
        # 1. Generar Origen
        self.origin_gen = OriginGenerator()
        self.origin_data = self.origin_gen.generate()
        
        # --- FIX: GENERACIÓN DE NOMBRE REAL ---
        self.name = self._generate_wuxia_name()
        self.title = self.origin_data["title"]
        
        # 2. Stats
        self.stats = {
            "hp": 150, "max_hp": 150,
            "qi": 0, "max_qi": 100,
            "stamina": 100, "max_stamina": 100,
            "atk": 20, "def": 10,
            "comprension": 10, "suerte": 0,
            "dao_espacial": 0, "dao_devorar": 0
        }
        
        # Mods
        mods = self.origin_data.get("stats_mod", {})
        for stat, value in mods.items():
            if stat in self.stats:
                self.stats[stat] += value
                if stat in ["hp", "stamina"]: self.stats[f"max_{stat}"] += value
            elif stat == "qi": self.stats["qi"] = value

        if self.stats["max_hp"] < 50: self.stats["max_hp"] = 50
        self.stats["hp"] = self.stats["max_hp"]

        self.realm_idx = 0
        self.realm_name = "Mortal"
        
        # 3. Misticismo
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
        
        # 4. Inventario
        self.inventory = {"Oro": self.origin_data.get("gold", 0)}
        for k, v in self.origin_data.get("inventory", {}).items():
            self.inventory[k] = self.inventory.get(k, 0) + v
            
        self.inventory["Píldora Curativa"] = 3
        self.inventory["Píldora de Fundación"] = 1
        
        self.slaves = []
        self.sect = None 
        self.skills = {
            "Puño Básico": {"cost": 0, "mult": 1.0, "elem": "Neutro"},
            "Palma de Qi": {"cost": 10, "mult": 1.5, "elem": "Neutro"}
        }
        
        start_range = 1000
        self.location = [random.randint(-start_range, start_range), random.randint(-start_range, start_range)]

    def _generate_wuxia_name(self):
        """Genera un nombre chino auténtico."""
        surnames = ["Li", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou", "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Lin", "Luo", "Jiang", "Fan", "Su", "Han", "Tang", "Feng", "Jin", "Wei", "Ye", "Bai"]
        given_names = ["Wei", "Jie", "Hao", "Yi", "Fan", "Lei", "Xin", "Ying", "Xiu", "Mei", "Lan", "Feng", "Long", "Hu", "Gui", "Chen", "Yun", "Tian", "Ming", "Hua", "Shan", "Ren", "Kai", "Jian", "Ping", "An", "Bo", "Cheng", "Dong", "Gang", "Zian", "Yan"]
        return f"{random.choice(surnames)} {random.choice(given_names)}"

    @property
    def age(self): return self.age_sys.current_age
    @property
    def max_lifespan(self): return self.age_sys.max_lifespan


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(APP_TITLE)
    clock = pygame.time.Clock()
    
    app_running = True
    
    while app_running:
        # 1. MOSTRAR MENÚ
        menu = MainMenu(screen)
        choice = menu.run()
        
        if choice == "SALIR" or choice == "EXIT":
            app_running = False
            break
            
        # 2. INICIAR NUEVA PARTIDA
        elif choice == "NUEVA REENCARNACIÓN" or choice == "CONTINUAR CAMINO":
            
            # Crear Instancias
            player = Player()
            time_sys = TimeSystem()
            map_mgr = MapManager()
            
            # Iniciar Motor
            engine = GameEngine(screen, player, time_sys, map_mgr, clock)
            
            try:
                engine.run()
            except Exception as e:
                print(f"CRASH: {e}")
                import traceback
                traceback.print_exc()
                app_running = False # Volver al menú o salir si es grave

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()