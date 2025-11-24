import random
import json
from data import Materials

# Nota: La clase Soul y ArtifactSpirit deberían estar en systems/artifact_spirit.py
# Aquí asumimos que la clase existe y se importa correctamente.

# --- CONFIGURACIÓN DE MOULDES Y ESTRUCTURAS ---
WEAPON_MOLDS = {
    "Daga":   {"densidad": 1.5, "speed": 1.8},
    "Espada": {"densidad": 1.1, "speed": 1.0},
    "Lanza":  {"densidad": 0.9, "speed": 1.2},
    "Sable":  {"densidad": 1.0, "speed": 1.3},
    "Hacha":  {"densidad": 1.6, "speed": 0.9},
    "Pico":  {"densidad": 1.8, "speed": 0.9}
}

BUILDINGS = {
    "Pared": {"char": "■", "cost": {"Madera": 5}},
    "Suelo": {"char": ".", "cost": {"Paja": 2}},
    "Cama":  {"char": "H", "cost": {"Madera": 20}, "effect": "Regen HP"},
    "Horno": {"char": "O", "cost": {"Hierro": 50}, "effect": "Alquimia"}
}

# --- SISTEMA DE ALQUIMIA POR ATRIBUTOS ---
class AlchemySystem:
    def mix_ingredients(self, ingredients):
        """Suma los atributos (tags) de los ingredientes seleccionados."""
        total_tags = {}
        total_impurity = 0
        
        for item in ingredients:
            data = Materials.get("Plantas", {}).get("tags", {})
            for k, v in data.items():
                total_tags[k] = total_tags.get(k, 0) + v
                
            if "Pureza" not in data: total_impurity += 10

        # Lógica de Recetas
        if total_tags.get("Fuego", 0) > 30 and total_tags.get("Estabilidad", 0) > 10:
            quality = "Alta" if total_impurity < 20 else "Baja"
            return f"Píldora Yang ({quality})", True
            
        if total_tags.get("Vida", 0) > 20:
            return "Píldora Curativa Mayor", True
            
        # Fallo si la mezcla es muy sucia o inestable
        if total_impurity > 50 or random.random() < 0.2:
            return "Escoria Tóxica", False
            
        return "Polvo Medicinal Genérico", True
    def get_random_material(self, category):
        """Obtenga un material aleatorio de la categoría especificada."""
        materials = Materials.get(category, ["Plantas"])
        return random.choice(materials) if materials else None
# --- SISTEMA DE FORJA (Densidad) ---
class ForgeSystem:
    def get_random_material(self, category):
        """Obtenga un material aleatorio de la categoría especificada."""
        Materials = Materials.get(category, ["Minerales"])
        return random.choice(Materials) if Materials else None
    def get_random_material(self, category):
        """Obtenga un material aleatorio de la categoría especificada."""
        Materials = Materials.get(category, ["Maderas"])
        return random.choice(Materials) if Materials else None
    def forge_weapon(self, metal_name, core_name, mold_type):
        Minerales = Materials.get(Materials, {})
        Maderas = Materials.get(Materials, {})
        mold = WEAPON_MOLDS.get(mold_type, WEAPON_MOLDS["Espada"])
        
        # Stats base por densidad
        base_atk = Minerales.get("stats_forja", {}).get("dureza", 10) * mold["densidad"], Maderas.get("stats_forja", {}).get("dureza", 10) * mold["densidad"]
        
        # Bonus por Núcleo (Simulado)
        elem_dmg = 0
        if core_name: elem_dmg = 20 
        
        # Factor Caos
        quality = random.uniform(0.9, 1.2)
        final_atk = int((base_atk + elem_dmg) * quality)
        
        name = f"{mold_type} de {metal_name.split(' ')[0]}"
        if final_atk > 50: name = f"{name} Divina"
        
        return {"name": name, "type": "Arma", "atk": final_atk}

# --- SISTEMA DE CONSTRUCCIÓN DE CASAS (Housing) ---
class HouseSystem:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.resources = {"Madera": 100, "Roca": 100, "Paja": 100}

    def build(self, x, y, structure):
        data = BUILDINGS.get(structure)
        cost = data["cost"]
        
        # Verificar recursos y construir
        for res, qty in cost.items():
            if self.resources.get(res, 0) < qty:
                return False, f"Falta {res}."
        
        for res, qty in cost.items():
            self.resources[res] -= qty
            
        self.grid[y][x] = structure
        return True, f"Construido: {structure}"