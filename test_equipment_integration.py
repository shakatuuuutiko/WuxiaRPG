#!/usr/bin/env python
"""
Test integral del sistema de equipamiento
Demuestra:
  - Player con equipo
  - Compañeros con equipo
  - Combate considerando equipamiento
  - Gestión de durabilidad
"""

from systems.crafting import ForgeSystem, Materials
from systems.equipment import Equipment, CharacterEquipment, create_starter_weapon
from systems.companion import Companion, CompanionParty, CompanionGenerator
from systems.combat import CombatEngine
from main import Player


def test_player_equipment():
    """Test del equipamiento del jugador."""
    print("=" * 60)
    print("TEST 1: EQUIPAMIENTO DEL JUGADOR")
    print("=" * 60)
    
    player = Player()
    print(f"\nJugador: {player.name}")
    print(f"Stats Base ATK: {player.stats['atk']}")
    print(f"ATK Total (con equipo): {player.get_total_atk()}")
    print(f"Velocidad de ataque: {player.get_attack_speed()}")
    
    # Mostrar arma equipada
    if player.equipment.equipped_weapon:
        print(f"\nArma equipada: {player.equipment.equipped_weapon.name}")
        print(f"  Daño base: {player.equipment.equipped_weapon.atk}")
        print(f"  Durabilidad: {player.equipment.equipped_weapon.durability}/{player.equipment.equipped_weapon.max_durability}")
        print(f"  Rareza: {player.equipment.equipped_weapon.rarities.get('overall', 'Desconocida')}")
    
    # Simular degradación del arma
    print("\n--- Simulando combate (5 golpes) ---")
    for i in range(5):
        player.equipment.equipped_weapon.take_damage(8)
        print(f"Golpe {i+1}: Durabilidad {player.equipment.equipped_weapon.durability}/{player.equipment.equipped_weapon.max_durability}, Daño efectivo: {player.equipment.equipped_weapon.get_effective_damage()}")


def test_companions():
    """Test de compañeros."""
    print("\n" + "=" * 60)
    print("TEST 2: COMPAÑEROS CON EQUIPAMIENTO")
    print("=" * 60)
    
    party = CompanionParty(max_size=3)
    
    for i in range(3):
        comp = CompanionGenerator.generate(rank=2 + i)
        party.add_companion(comp)
        print(f"\n{i+1}. {comp.name} ({comp.archetype}) - Rango G{comp.rank}")
        print(f"   ATK Base: {comp.stats['atk']} | ATK Total: {comp.get_total_atk()}")
        print(f"   DEF: {comp.stats['def']} | HP: {comp.stats['hp']}/{comp.stats['max_hp']}")
        if comp.equipment.equipped_weapon:
            print(f"   Arma: {comp.equipment.equipped_weapon.name} (ATK: {comp.equipment.equipped_weapon.atk})")
    
    print(f"\nPoderTotal del Grupo: {party.get_total_power()}")


def test_combat_with_equipment():
    """Test de combate considerando equipamiento."""
    print("\n" + "=" * 60)
    print("TEST 3: COMBATE CON EQUIPAMIENTO")
    print("=" * 60)
    
    player = Player()
    enemy = CompanionGenerator.generate(rank=2)
    
    print(f"\nJugador: {player.name}")
    print(f"  Ataque Total: {player.get_total_atk()}")
    print(f"  Defensa: {player.stats['def']}")
    
    print(f"\nEnemigo: {enemy.name}")
    print(f"  Ataque Total: {enemy.get_total_atk()}")
    print(f"  Defensa: {enemy.stats['def']}")
    
    # Simular intercambio de ataques
    engine = CombatEngine()
    
    print("\n--- RONDA 1 ---")
    dmg_player, crit_p, advantage_p = engine.calculate_damage(player, enemy.stats)
    print(f"Ataque del Jugador: {dmg_player} daño" + (" ¡CRÍTICO!" if crit_p else ""))
    enemy.take_damage(dmg_player)
    print(f"  Enemigo ahora tiene {enemy.stats['hp']}/{enemy.stats['max_hp']} HP")
    
    dmg_enemy, crit_e, advantage_e = engine.calculate_damage(enemy, player.stats)
    print(f"\nAtaque del Enemigo: {dmg_enemy} daño" + (" ¡CRÍTICO!" if crit_e else ""))
    player.stats["hp"] = max(0, player.stats["hp"] - dmg_enemy)
    print(f"  Jugador ahora tiene {player.stats['hp']}/{player.stats['max_hp']} HP")
    
    # Degradación del arma
    if player.equipment.equipped_weapon:
        player.equipment.equipped_weapon.take_damage(10)
        print(f"\nDurabilidad del arma del Jugador: {player.equipment.equipped_weapon.durability}/{player.equipment.equipped_weapon.max_durability}")


def test_equipment_management():
    """Test de gestión de equipamiento."""
    print("\n" + "=" * 60)
    print("TEST 4: GESTIÓN DE EQUIPAMIENTO")
    print("=" * 60)
    
    forge = ForgeSystem()
    eq = CharacterEquipment()
    
    # Crear múltiples armas
    weapons = []
    for mold in ["Espada", "Arco", "Sable", "Hacha"]:
        weapon = Equipment(forge.forge_weapon(mold))
        weapons.append(weapon)
    
    # Equipar la primera
    eq.equip_weapon(weapons[0])
    print(f"Arma equipada: {eq.equipped_weapon.name}")
    
    # Añadir al inventario
    for w in weapons[1:]:
        eq.add_to_inventory(w)
    
    print("\nInventario:")
    for line in eq.list_inventory():
        print(f"  {line}")
    
    # Cambiar arma
    print(f"\n--- Cambiando a Arco ---")
    eq.equip_weapon(eq.remove_from_inventory(0))  # El Arco es el primer inventario
    
    print("Nuevo inventario:")
    for line in eq.list_inventory():
        print(f"  {line}")
    
    # Reparar todo
    print(f"\n--- Reparando todas las armas ---")
    eq.repair_all()
    print("Inventario después de reparar:")
    for line in eq.list_inventory():
        print(f"  {line}")


def test_crafting_integration():
    """Test de integración con crafting."""
    print("\n" + "=" * 60)
    print("TEST 5: INTEGRACIÓN CON CRAFTING")
    print("=" * 60)
    
    forge = ForgeSystem()
    
    # Crear lotes de armas
    print("\nForjando 5 Sables...")
    batch = forge.forge_batch("Sable", count=5)
    
    for i, weapon_dict in enumerate(batch, 1):
        equip = Equipment(weapon_dict)
        print(f"{i}. {equip.name} - ATK: {equip.atk} ({equip.rarities.get('overall', 'N/A')})")
    
    # Crear grupo de compañeros y equiparlos
    print("\nEquipando compañeros con armas forjadas...")
    party = CompanionParty(max_size=len(batch))
    
    for i, weapon_dict in enumerate(batch):
        comp = CompanionGenerator.generate(rank=1)
        weapon = Equipment(weapon_dict)
        comp.equip_weapon(weapon)
        party.add_companion(comp)
        print(f"  {comp.name}: Equipado con {weapon.name}")
    
    print(f"\nPoderTotal del grupo: {party.get_total_power()}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SUITE DE TESTS - SISTEMA INTEGRADO DE EQUIPAMIENTO")
    print("=" * 60)
    
    try:
        test_player_equipment()
        test_companions()
        test_combat_with_equipment()
        test_equipment_management()
        test_crafting_integration()
        
        print("\n" + "=" * 60)
        print("✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
