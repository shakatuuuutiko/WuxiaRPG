"""
Sistema de Compañeros (NPCs con inteligencia y equipamiento)
"""

import random
from systems.equipment import CharacterEquipment, Equipment, create_starter_weapon
from systems.creature_gen import CreatureGenerator


class Companion:
    """Representa un compañero (esclavo, aliado, NPC) equipable."""
    
    def __init__(self, name=None, rank=1):
        self.name = name or f"Compañero {random.randint(1000, 9999)}"
        self.rank = rank
        
        # Stats
        base_stat = 20 + (rank * 10)
        self.stats = {
            "hp": int(base_stat * 2.5 * random.uniform(0.8, 1.2)),
            "max_hp": int(base_stat * 2.5),
            "atk": int(base_stat * 0.5),
            "def": int(base_stat * 0.3),
            "qi": rank * 50,
            "element": random.choice(["Neutro", "Fuego", "Agua", "Metal", "Madera", "Tierra"])
        }
        
        # Equipamiento
        self.equipment = CharacterEquipment()
        self.loyalty = 50  # Lealtad al dueño (0-100)
        self.experience = 0
        self.level = 1
        
        # Personaje
        self.archetype = random.choice(["Guerrero", "Arquero", "Mago", "Tanque", "Sabio"])
        
    def get_total_atk(self):
        """Retorna el ataque total incluyendo equipamiento."""
        base_atk = self.stats.get("atk", 10)
        weapon_bonus = self.equipment.get_equipped_damage()
        return base_atk + weapon_bonus
    
    def get_attack_speed(self):
        """Retorna la velocidad de ataque."""
        return self.equipment.get_equipped_speed()
    
    def equip_weapon(self, equipment):
        """Equipa un arma."""
        self.equipment.equip_weapon(equipment)
    
    def gain_experience(self, amount):
        """Gana experiencia."""
        self.experience += amount
        # Nivel sube cada 100 exp
        new_level = 1 + (self.experience // 100)
        if new_level > self.level:
            self.level = new_level
            self.level_up()
    
    def level_up(self):
        """Aumenta stats al subir de nivel."""
        multiplier = 1.1
        self.stats["atk"] = int(self.stats["atk"] * multiplier)
        self.stats["def"] = int(self.stats["def"] * multiplier)
        self.stats["max_hp"] = int(self.stats["max_hp"] * multiplier)
        self.stats["hp"] = self.stats["max_hp"]
    
    def take_damage(self, damage):
        """Recibe daño."""
        self.stats["hp"] = max(0, self.stats["hp"] - damage)
    
    def heal(self, amount):
        """Se cura."""
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)
    
    def is_alive(self):
        return self.stats["hp"] > 0
    
    def to_dict(self):
        """Serializa el compañero."""
        return {
            'name': self.name,
            'rank': self.rank,
            'stats': self.stats.copy(),
            'loyalty': self.loyalty,
            'experience': self.experience,
            'level': self.level,
            'archetype': self.archetype,
            'equipment': self.equipment.to_dict()
        }
    
    @staticmethod
    def from_dict(data):
        """Reconstruye un compañero desde diccionario."""
        comp = Companion(data['name'], data['rank'])
        comp.stats = data.get('stats', comp.stats)
        comp.loyalty = data.get('loyalty', 50)
        comp.experience = data.get('experience', 0)
        comp.level = data.get('level', 1)
        comp.archetype = data.get('archetype', 'Guerrero')
        if 'equipment' in data:
            comp.equipment = CharacterEquipment.from_dict(data['equipment'])
        return comp


class CompanionParty:
    """Gestiona un grupo de compañeros."""
    
    def __init__(self, max_size=5):
        self.companions = []
        self.max_size = max_size
        self.active_combat_party = []  # Compañeros en combate
    
    def add_companion(self, companion):
        """Añade un compañero al grupo."""
        if len(self.companions) < self.max_size:
            self.companions.append(companion)
            return True
        return False
    
    def remove_companion(self, index):
        """Remueve un compañero."""
        if 0 <= index < len(self.companions):
            return self.companions.pop(index)
        return None
    
    def set_combat_party(self, indices):
        """Define qué compañeros irán a combate."""
        self.active_combat_party = [self.companions[i] for i in indices if i < len(self.companions)]
    
    def heal_all(self, amount):
        """Cura a todos los compañeros."""
        for comp in self.companions:
            comp.heal(amount)
    
    def get_total_power(self):
        """Calcula el poder combinado del grupo."""
        return sum(c.get_total_atk() for c in self.companions)
    
    def get_alive_count(self):
        """Cuenta cuántos compañeros están vivos."""
        return sum(1 for c in self.companions if c.is_alive())
    
    def to_dict(self):
        """Serializa el grupo."""
        return {
            'companions': [c.to_dict() for c in self.companions],
            'max_size': self.max_size
        }
    
    @staticmethod
    def from_dict(data):
        """Reconstruye un grupo desde diccionario."""
        party = CompanionParty(data.get('max_size', 5))
        for comp_data in data.get('companions', []):
            party.add_companion(Companion.from_dict(comp_data))
        return party


# --- GENERADOR DE COMPAÑEROS PROCEDURALES ---

class CompanionGenerator:
    """Genera compañeros aleatorios."""
    
    @staticmethod
    def generate(rank=1):
        """Genera un compañero aleatorio."""
        archetypes = ["Guerrero", "Arquero", "Mago", "Tanque", "Sabio", "Asesino"]
        comp = Companion(name=None, rank=rank)
        comp.archetype = random.choice(archetypes)
        
        # Modificar stats según arqueotipo
        if comp.archetype == "Tanque":
            comp.stats["def"] = int(comp.stats["def"] * 1.8)
            comp.stats["max_hp"] = int(comp.stats["max_hp"] * 1.5)
            comp.stats["hp"] = comp.stats["max_hp"]
        elif comp.archetype == "Guerrero":
            comp.stats["atk"] = int(comp.stats["atk"] * 1.5)
        elif comp.archetype == "Arquero":
            comp.stats["atk"] = int(comp.stats["atk"] * 1.3)
        elif comp.archetype == "Mago":
            comp.stats["qi"] = int(comp.stats["qi"] * 2)
        
        # Equipa con arma aleatoria
        from systems.crafting import ForgeSystem
        forge = ForgeSystem()
        weapon = Equipment(forge.forge_weapon(random.choice(["Espada", "Sable", "Arco", "Lanza"])))
        comp.equip_weapon(weapon)
        
        return comp


if __name__ == '__main__':
    print("=== SISTEMA DE COMPAÑEROS ===\n")
    
    # Test: Crear compañero
    comp1 = Companion("Xiao Ming", rank=3)
    print(f"Compañero: {comp1.name}")
    print(f"Stats: {comp1.stats}")
    print(f"Ataque Total: {comp1.get_total_atk()}\n")
    
    # Test: Generar grupo
    print("--- GENERANDO GRUPO DE 3 COMPAÑEROS ---")
    party = CompanionParty(max_size=3)
    for i in range(3):
        new_comp = CompanionGenerator.generate(rank=2)
        party.add_companion(new_comp)
        print(f"\n{i+1}. {new_comp.name} ({new_comp.archetype})")
        print(f"   Poder: {new_comp.get_total_atk()} | HP: {new_comp.stats['hp']}/{new_comp.stats['max_hp']}")
    
    print(f"\n--- PODER TOTAL DEL GRUPO: {party.get_total_power()} ---")
    
    # Test: Daño y sanación
    print("\n--- COMBATE SIMULADO ---")
    party.companions[0].take_damage(50)
    print(f"Compañero 1 recibe 50 daño: {party.companions[0].stats['hp']}/{party.companions[0].stats['max_hp']}")
    
    party.heal_all(20)
    print(f"Se cura a todos 20 HP:")
    for comp in party.companions:
        print(f"  {comp.name}: {comp.stats['hp']}/{comp.stats['max_hp']}")
