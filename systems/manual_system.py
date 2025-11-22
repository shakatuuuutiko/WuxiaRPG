import random

KEYWORDS = {
    "NOUNS": ["Palma", "Puño", "Dedo", "Espada", "Sable", "Rugido", "Corte", "Aguja", "Paso"],
    "ADJECTIVES": ["Divino", "Infernal", "Vasto", "Eterno", "Rápido", "Pesado", "Oculto"],
    "ELEMENTS": {
        "Fuego": ["del Sol", "Abrasador"], "Agua": ["del Océano", "de Escarcha"],
        "Tierra": ["de la Montaña", "Sismico"], "Viento": ["de la Tormenta", "Invisible"],
        "Rayo": ["del Trueno", "Relámpago"],
        "Neutro": ["de la Fuerza", "del Guerrero", "Básico"]
    }
}

class ManualGenerator:
    def generate(self, target_rank="Mortal"):
        # 1. Tipo y Elemento
        skill_type = random.choice(["Ataque", "Defensa", "Movimiento"])
        elem = random.choice(list(KEYWORDS["ELEMENTS"].keys()))
        
        # 2. Nombre Procedural
        noun = random.choice(KEYWORDS["NOUNS"])
        adj = random.choice(KEYWORDS["ADJECTIVES"])
        suffix = random.choice(KEYWORDS["ELEMENTS"][elem])
        name = f"{noun} {adj} {suffix}"

        # 3. Stats
        mult_base = {"Mortal": 1.5, "Tierra": 2.5, "Cielo": 4.0, "Divino": 8.0}
        mult = mult_base.get(target_rank, 1.5) * random.uniform(0.8, 1.2)
        
        stats = {
            "dmg_mult": round(mult, 1),
            "qi_cost": int(10 * mult),
            "difficulty": int(10 * mult)
        }
        
        if elem == "Fuego": stats["burn_chance"] = 0.3
        
        return {
            "name": name,
            "type": "Manual",
            "rank": target_rank,
            "element": elem,
            "skill_type": skill_type,
            "stats": stats,
            "value": int(mult * 100)
        }

class ManualManager:
    def __init__(self, player):
        self.player = player
        if not hasattr(player, "skills"): 
            self.player.skills = {}

    def study_manual(self, item_name):
        # Lógica de estudio (Simplificada)
        tech_name = item_name.replace("Manual: ", "").replace(" (Fragmento)", "")
        
        difficulty = 20
        if "Divino" in tech_name: difficulty = 80
        
        comprension = self.player.stats.get("comprension", 10)
        root_affinity = 1.0
        
        gain = 5 + ((comprension * root_affinity * 5) / (difficulty / 10))
        gain = max(1.0, gain)
        
        current = self.player.skills.get(tech_name, 0.0)
        new_val = min(100.0, current + gain)
        self.player.skills[tech_name] = new_val
        
        msg = f"Estudiaste '{tech_name}'.\nProgreso: {new_val:.1f}%"
        return gain, msg, new_val >= 100.0

    def fuse_fragments(self, item_name, qty):
        if qty < 3: return False, "Necesitas 3 fragmentos."
        
        chance = 0.3 + (self.player.stats["comprension"] * 0.02)
        if random.random() < chance:
            new_name = item_name.replace(" (Fragmento)", "")
            return True, new_name
        else:
            return False, "Fallaste la deducción. Perdiste un fragmento."