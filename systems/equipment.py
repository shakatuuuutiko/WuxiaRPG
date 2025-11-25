"""
Sistema de Equipamiento para Personajes y NPCs
Permite equipar armas forjadas del sistema de crafting
"""

from systems.crafting import Materials, ForgeSystem


class Equipment:
    """Representa un equipo (arma) que puede ser equipado."""
    def __init__(self, weapon_dict):
        """
        Inicializa equipamiento desde un dict de arma forjada.
        weapon_dict: salida de ForgeSystem.forge_weapon()
        """
        self.name = weapon_dict.get('name', 'Arma Genérica')
        self.type = weapon_dict.get('type', 'Arma')
        self.mold = weapon_dict.get('mold', 'Espada')
        self.atk = weapon_dict.get('atk', 0)
        self.speed = weapon_dict.get('speed', 1.0)
        self.components = weapon_dict.get('components', {})
        self.rarities = weapon_dict.get('rarities', {})
        
        # Durabilidad (puede deteriorarse)
        self.max_durability = 100 + (self.atk // 5)
        self.durability = self.max_durability
        
    def take_damage(self, amount=1):
        """Reduce la durabilidad del arma."""
        self.durability = max(0, self.durability - amount)
        
    def repair(self, amount=None):
        """Repara el arma."""
        if amount is None:
            self.durability = self.max_durability
        else:
            self.durability = min(self.max_durability, self.durability + amount)
    
    def get_effective_damage(self):
        """Retorna el daño efectivo considerando durabilidad."""
        durability_mult = self.durability / self.max_durability
        return int(self.atk * durability_mult)
    
    def is_broken(self):
        return self.durability <= 0
    
    def to_dict(self):
        """Convierte el equipamiento a diccionario para guardado."""
        return {
            'name': self.name,
            'type': self.type,
            'mold': self.mold,
            'atk': self.atk,
            'speed': self.speed,
            'durability': self.durability,
            'max_durability': self.max_durability,
            'components': self.components,
            'rarities': self.rarities
        }
    
    @staticmethod
    def from_dict(data):
        """Reconstruye un Equipment desde un diccionario."""
        equip = Equipment({'name': data['name'], 'type': data['type'], 'mold': data['mold'],
                          'atk': data['atk'], 'speed': data['speed']})
        equip.durability = data.get('durability', equip.max_durability)
        equip.max_durability = data.get('max_durability', 100)
        return equip


class CharacterEquipment:
    """Gestiona el equipamiento de un personaje."""
    def __init__(self):
        self.equipped_weapon = None
        self.backup_weapon = None
        self.inventory = []  # Lista de armas disponibles
    
    def equip_weapon(self, equipment):
        """Equipa un arma, guardando la anterior como backup."""
        if self.equipped_weapon is not None:
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = equipment
    
    def unequip_weapon(self):
        """Desequipa el arma actual."""
        if self.equipped_weapon is not None:
            self.inventory.append(self.equipped_weapon)
            self.equipped_weapon = None
    
    def add_to_inventory(self, equipment):
        """Añade un arma al inventario."""
        self.inventory.append(equipment)
    
    def remove_from_inventory(self, index):
        """Remueve un arma del inventario por índice."""
        if 0 <= index < len(self.inventory):
            return self.inventory.pop(index)
        return None
    
    def get_equipped_damage(self):
        """Retorna el daño del arma equipada."""
        if self.equipped_weapon is None:
            return 10  # Daño de puños sin arma
        return self.equipped_weapon.get_effective_damage()
    
    def get_equipped_speed(self):
        """Retorna la velocidad del arma equipada."""
        if self.equipped_weapon is None:
            return 1.0
        return self.equipped_weapon.speed
    
    def repair_equipped(self):
        """Repara completamente el arma equipada."""
        if self.equipped_weapon is not None:
            self.equipped_weapon.repair()
            return True
        return False
    
    def repair_all(self):
        """Repara todas las armas del inventario."""
        if self.equipped_weapon is not None:
            self.equipped_weapon.repair()
        for weapon in self.inventory:
            weapon.repair()
    
    def list_inventory(self):
        """Retorna una lista formateada del inventario."""
        result = []
        if self.equipped_weapon:
            result.append(f"[EQUIPADA] {self.equipped_weapon.name} (ATK: {self.equipped_weapon.atk}, Durabilidad: {self.equipped_weapon.durability}/{self.equipped_weapon.max_durability})")
        
        for i, weapon in enumerate(self.inventory):
            effective_dmg = weapon.get_effective_damage()
            result.append(f"{i+1}. {weapon.name} (ATK: {weapon.atk}, Efectivo: {effective_dmg}, Durabilidad: {weapon.durability}/{weapon.max_durability})")
        
        return result
    
    def to_dict(self):
        """Serializa el equipamiento."""
        return {
            'equipped': self.equipped_weapon.to_dict() if self.equipped_weapon else None,
            'inventory': [w.to_dict() for w in self.inventory]
        }
    
    @staticmethod
    def from_dict(data):
        """Reconstruye desde diccionario."""
        eq = CharacterEquipment()
        if data.get('equipped'):
            eq.equipped_weapon = Equipment.from_dict(data['equipped'])
        for item_data in data.get('inventory', []):
            eq.inventory.append(Equipment.from_dict(item_data))
        return eq


# --- INTEGRACIÓN CON PLAYER Y NPCS ---

def add_equipment_to_player(player_obj):
    """Añade sistema de equipamiento al Player."""
    if not hasattr(player_obj, 'equipment'):
        player_obj.equipment = CharacterEquipment()
    return player_obj.equipment


def add_equipment_to_npc(npc_obj):
    """Añade sistema de equipamiento a un NPC."""
    if not hasattr(npc_obj, 'equipment'):
        npc_obj.equipment = CharacterEquipment()
    return npc_obj.equipment


# --- HELPER PARA CREAR ARMAS DE PRUEBA ---

def create_starter_weapon(player_name="Aventurero"):
    """Crea un arma inicial para el jugador."""
    forge = ForgeSystem()
    weapon_dict = forge.forge_weapon("Espada")
    return Equipment(weapon_dict)


if __name__ == '__main__':
    print("=== SISTEMA DE EQUIPAMIENTO ===\n")
    
    # Test: Crear equipamiento
    forge = ForgeSystem()
    weapon1 = Equipment(forge.forge_weapon("Sable"))
    weapon2 = Equipment(forge.forge_weapon("Arco"))
    weapon3 = Equipment(forge.forge_weapon("Hacha"))
    
    # Test: Gestionar inventario
    eq = CharacterEquipment()
    eq.equip_weapon(weapon1)
    eq.add_to_inventory(weapon2)
    eq.add_to_inventory(weapon3)
    
    print("INVENTARIO INICIAL:")
    for line in eq.list_inventory():
        print(line)
    
    print(f"\n--- DAÑO EQUIPADO: {eq.get_equipped_damage()} ---")
    print(f"--- VELOCIDAD: {eq.get_equipped_speed()} ---")
    
    # Test: Degradación
    weapon1.take_damage(30)
    print(f"\nDESPUÉS DE DAÑO:")
    for line in eq.list_inventory():
        print(line)
    
    # Test: Cambiar arma
    eq.equip_weapon(eq.remove_from_inventory(0))
    print(f"\nAMES DE CAMBIAR A ARCO:")
    for line in eq.list_inventory():
        print(line)
