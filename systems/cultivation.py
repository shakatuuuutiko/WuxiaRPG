# --- SISTEMA DE CULTIVO Y RAÍCES ESPIRITUALES ---
import random

# Configuración de Reinos (Los 48 Grados están contenidos en estas Eras)
REALMS_DATA = [
    {"id": 0, "name": "Mortal", "max_qi": 100, "lifespan": 80, "tribulation": False},
    {"id": 1, "name": "Condensación de Qi", "max_qi": 1000, "lifespan": 120, "tribulation": False},
    {"id": 2, "name": "Establecimiento de Fundación", "max_qi": 5000, "lifespan": 200, "tribulation": True},
    {"id": 3, "name": "Núcleo Dorado", "max_qi": 20000, "lifespan": 500, "tribulation": True},
    {"id": 4, "name": "Alma Naciente", "max_qi": 100000, "lifespan": 1000, "tribulation": True},
    {"id": 5, "name": "Transformación Divina", "max_qi": 500000, "lifespan": 2000, "tribulation": True},
    {"id": 6, "name": "Vacío", "max_qi": 2000000, "lifespan": 5000, "tribulation": True}
]

ROOT_TYPES = {
    "Celestial": {"elems": 1, "mult": 2.5},
    "Terrenal":  {"elems": 2, "mult": 1.5},
    "Verdadera": {"elems": 3, "mult": 1.0},
    "Pseudo":    {"elems": 4, "mult": 0.7},
    "Mortal":    {"elems": 5, "mult": 0.4}
}

ELEMENTS = ["Oro", "Madera", "Agua", "Fuego", "Tierra"]
MUTATED = ["Rayo", "Hielo", "Viento", "Vacío"]

class SpiritRoot:
    def __init__(self):
        self.tier = ""
        self.elements = []
        self.cultivation_mult = 0.0
        self.generate()

    def generate(self):
        # Lógica de generación de raíces (basada en probabilidad)
        roll = random.random()
        if roll < 0.01: self.tier = "Celestial"
        elif roll < 0.10: self.tier = "Terrenal"
        elif roll < 0.40: self.tier = "Verdadera"
        elif roll < 0.70: self.tier = "Pseudo"
        else: self.tier = "Mortal"

        data = ROOT_TYPES[self.tier]
        self.cultivation_mult = data["mult"]
        count = data["elems"]
        
        if count <= 2 and random.random() < 0.15:
            # Mutación
            self.elements = [random.choice(MUTATED)] if count == 1 else [random.choice(MUTATED), random.choice(ELEMENTS)]
            self.tier += " (Mutada)"
            self.cultivation_mult += 0.5
        else:
            self.elements = random.sample(ELEMENTS, count)

class CultivationManager:
    def __init__(self, player_stats):
        self.stats = player_stats

    def get_realm_info(self, realm_idx):
        if realm_idx >= len(REALMS_DATA): return REALMS_DATA[-1]
        return REALMS_DATA[realm_idx]

    def check_breakthrough(self, current_qi, realm_idx):
        """Verifica si el jugador está listo para intentar romper al siguiente reino."""
        info = self.get_realm_info(realm_idx)
        if current_qi < info["max_qi"]:
            return False, "Qi insuficiente para romper el cuello de botella.", 0
            
        next_idx = realm_idx + 1
        if next_idx >= len(REALMS_DATA):
            return False, "Has alcanzado la cima de este mundo.", 0
            
        next_info = self.get_realm_info(next_idx)
        
        # Daño de la tribulación (Si aplica)
        damage = 0
        if next_info["tribulation"]:
            damage = int(next_info["max_qi"] * 0.1)
            
        return True, f"¡Ruptura exitosa a {next_info['name']}!", damage