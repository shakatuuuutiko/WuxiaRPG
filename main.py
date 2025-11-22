# --- MAIN.PY: LANZADOR WUXIA PYGAME ---
import pygame
import sys
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE

# Importar Sistemas de Datos
try:
    from systems.cultivation import SpiritRoot
    from systems.bloodline import Bloodline
    from systems.time_system import TimeSystem, AgeManager
    from systems.origin_generator import OriginGenerator
    from systems.map_core import MapManager
    from ui.main_gui import GameEngine # El nuevo motor gráfico
except ImportError as e:
    print(f"FATAL: Faltan archivos de sistema ({e})")
    sys.exit()

class Player:
    def __init__(self):
        # 1. Origen y Nombre Real
        self.origin_gen = OriginGenerator()
        self.origin_data = self.origin_gen.generate()
        self.name = self._generate_name()
        self.title = self.origin_data["title"]
        
        # 2. Stats Reales
        self.stats = {
            "hp": 150, "max_hp": 150,
            "qi": 0, "max_qi": 100,
            "stamina": 100, "max_stamina": 100,
            "atk": 20, "def": 10,
            "comprension": 10, "suerte": 0,
            "dao_espacial": 0
        }
        # Aplicar mods de origen
        for k, v in self.origin_data.get("stats_mod", {}).items():
            if k in self.stats: self.stats[k] += v
            if k in ["hp", "stamina"]: self.stats[f"max_{k}"] += v

        self.realm_idx = 0
        self.realm_name = "Mortal"
        
        # 3. Misticismo
        self.spirit_root = SpiritRoot()
        self.bloodline = Bloodline()
        self.age_sys = AgeManager(self)
        
        # 4. Inventario Real
        self.inventory = {"Oro": self.origin_data.get("gold", 0)}
        for k, v in self.origin_data.get("inventory", {}).items():
            self.inventory[k] = self.inventory.get(k, 0) + v
            
        # Starter Kit
        self.inventory["Píldora Curativa"] = 3
        self.inventory["Píldora de Fundación"] = 1
        
        # Listas Vacías (Sin datos de prueba)
        self.slaves = []
        self.sect = None 
        self.skills = {
            "Golpe Básico": {"cost": 0, "mult": 1.0, "elem": "Neutro"},
            "Palma de Qi": {"cost": 10, "mult": 1.5, "elem": "Neutro"}
        }
        
        # Spawn Aleatorio
        rng = 1000
        self.location = [random.randint(-rng, rng), random.randint(-rng, rng)]

    def _generate_name(self):
        s = ["Li", "Wang", "Zhang", "Chen", "Ye", "Xiao", "Han", "Feng"]
        n = ["Wei", "Jie", "Fan", "Ying", "Hao", "Long", "Hua", "Shan"]
        return f"{random.choice(s)} {random.choice(n)}"

    @property
    def age(self): return self.age_sys.current_age
    @property
    def max_lifespan(self): return self.age_sys.max_lifespan

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(APP_TITLE)
    clock = pygame.time.Clock()
    
    # Instanciar Datos
    player = Player()
    time_sys = TimeSystem()
    map_mgr = MapManager()
    
    # Iniciar Motor
    engine = GameEngine(screen, player, time_sys, map_mgr, clock)
    engine.run()

if __name__ == "__main__":
    main()