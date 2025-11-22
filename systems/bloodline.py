# --- SISTEMA DE LÍNEA DE SANGRE ---
import random

ANCESTRAL_LEGACIES = {
    "Tortuga": {"name": "Xuanwu", "buff": {"def": 3.0}, "passive": "Defensa Absoluta"},
    "Ave":     {"name": "Fénix Inmortal", "buff": {"qi": 2.0}, "passive": "Renacimiento"},
    "Pez":     {"name": "Kun Peng", "buff": {"vel": 5.0}, "passive": "Viaje Vacío"},
    "Tigre":   {"name": "Baihu", "buff": {"atk": 2.5}, "passive": "Aura Matanza"},
    "Dragón":  {"name": "Dragón Azure", "buff": {"all": 1.5}, "passive": "Control Clima"},
    "Humano":  {"name": "Sabio Taoísta", "buff": {"comprension": 2.0}, "passive": "Iluminación Rápida"}
}

class Bloodline:
    def __init__(self):
        self.ancestor = "Humano"
        self.purity = 0.0 # 0 - 100%
        self.active = False
        self.generate()

    def generate(self):
        keys = list(ANCESTRAL_LEGACIES.keys())
        if random.random() < 0.6:
            self.ancestor = "Humano"
            self.purity = random.uniform(1.0, 10.0)
        else:
            self.ancestor = random.choice(keys)
            self.purity = random.uniform(0.5, 5.0)

    def get_transform_data(self):
        data = ANCESTRAL_LEGACIES.get(self.ancestor, ANCESTRAL_LEGACIES["Humano"])
        return data

    def toggle_transform(self):
        if self.purity < 10:
            return False, "Tu sangre es demasiado débil para manifestarse."
        
        self.active = not self.active
        state = "ANCESTRAL" if self.active else "HUMANA"
        data = self.get_transform_data()
        return True, f"Has cambiado a forma {state} ({data['name']})."

    def get_stats_mult(self):
        """Retorna el multiplicador de stats basado en pureza activa."""
        if not self.active: return {}
        
        data = self.get_transform_data()
        base_buffs = data["buff"]
        factor = self.purity / 100.0
        final_buffs = {}
        
        for stat, val in base_buffs.items():
            if stat == "all":
                final_buffs["hp"] = 1 + (val * factor)
                final_buffs["atk"] = 1 + (val * factor)
                final_buffs["def"] = 1 + (val * factor)
            else:
                final_buffs[stat] = 1 + (val * factor)
                
        return final_buffs