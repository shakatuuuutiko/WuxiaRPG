import random

class Soul:
    """Representa el alma capturada de una entidad."""
    def __init__(self, source_entity):
        self.origin_name = source_entity["name"]
        self.type = source_entity.get("family_root", "Humano") # Tipo de base (Mamífero, Dragón, Humano)
        self.rank = source_entity["rank"] # G-level de la entidad
        
        # El poder multiplicador es exponencial por rango
        self.power_mult = 5.0 + (self.rank * 10) 
        
        # Personalidad (Para interacción social y consejos)
        self.personality = random.choice(["Arrogante", "Sabio", "Sanguinario", "Servicial", "Cínico"])
        
    def get_power_level(self):
        return self.power_mult

class ArtifactSpirit:
    """El ser inteligente que reside en el Artefacto Espiritual."""
    def __init__(self, base_weapon, soul_obj):
        self.name = f"Espíritu de {base_weapon['name']}"
        self.soul = soul_obj
        self.loyalty = 50 # Lealtad al maestro (puede traicionar)
        self.level = 1
        
        # Stats masivos heredados: Multiplicamos por el poder del alma
        self.base_weapon = base_weapon
        self.multiplier = self.soul.get_power_level() / 10 # 10x - 100x
        
        # Efecto: Drenaje pasivo de Qi/Vida (El precio de su poder)
        self.upkeep_cost = int(self.multiplier * 0.5)

    def calculate_attack_bonus(self):
        """Retorna el daño base del espíritu."""
        return int(self.base_weapon.get("atk", 1) * self.multiplier)

    def get_advice(self):
        """Retorna un diálogo basado en su personalidad."""
        if self.soul.personality == "Arrogante":
            return "¡Te he dado un poder inmerecido, inútil! Usa más Qi."
        elif self.soul.personality == "Sabio":
            return "El enemigo tiene una debilidad en el hígado. Golpea con Metal."
        elif self.soul.personality == "Sanguinario":
            return "¡Más sangre! ¡Mi sed solo se calma con la matanza!"
        return "El camino del Dao es largo. Sigue cultivando."