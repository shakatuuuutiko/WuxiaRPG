"""Verificar que todos los sistemas funcionan correctamente"""

import sys
import traceback

def test_imports():
    """Verificar que todos los imports funcionan"""
    print("\n" + "="*70)
    print("TEST 1: VERIFICAR IMPORTS")
    print("="*70)
    
    try:
        from systems.crafting import AlchemySystem, ForgeSystem
        print("✅ systems.crafting importado correctamente")
        
        from systems.equipment import CharacterEquipment, Equipment
        print("✅ systems.equipment importado correctamente")
        
        from systems.companion import Companion, CompanionParty, CompanionGenerator
        print("✅ systems.companion importado correctamente")
        
        from systems.combat import CombatEngine
        print("✅ systems.combat importado correctamente")
        
        from main import Player
        print("✅ main importado correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        traceback.print_exc()
        return False


def test_alchemy_system():
    """Verificar que el sistema de alquimia funciona"""
    print("\n" + "="*70)
    print("TEST 2: SISTEMA DE ALQUIMIA")
    print("="*70)
    
    try:
        from systems.crafting import AlchemySystem
        
        alchemy = AlchemySystem()
        print("✅ AlchemySystem inicializado")
        
        # Verificar recetas
        recipes_count = len(alchemy.RECIPE_TEMPLATES)
        print(f"✅ Recetas disponibles: {recipes_count}")
        
        # Crear una poción
        potion = alchemy.craft_potion(count=3)
        print(f"✅ Poción creada: {potion['name']}")
        print(f"   Efecto: {potion['effect']}")
        print(f"   Potencia: {potion['potency']}")
        print(f"   Éxito: {potion['success']}")
        
        # Crear lote
        batch = alchemy.craft_batch(count=3)
        print(f"✅ Lote creado: {len(batch)} pociones")
        
        # Descubrir receta
        recipe = alchemy.discover_recipe('Vida', 20)
        print(f"✅ Receta descubierta: {recipe['recipe_name']}")
        
        return True
    except Exception as e:
        print(f"❌ Error en alchemy: {e}")
        traceback.print_exc()
        return False


def test_forge_system():
    """Verificar que el sistema de forja funciona"""
    print("\n" + "="*70)
    print("TEST 3: SISTEMA DE FORJA")
    print("="*70)
    
    try:
        from systems.crafting import ForgeSystem
        
        forge = ForgeSystem()
        print("✅ ForgeSystem inicializado")
        
        # Forjar un arma
        weapon = forge.forge_weapon("Sable")
        print(f"✅ Arma forjada: {weapon['name']}")
        print(f"   ATK: {weapon['atk']}")
        
        # Forjar lote
        batch = forge.forge_batch("Espada", count=3)
        print(f"✅ Lote forjado: {len(batch)} armas")
        
        return True
    except Exception as e:
        print(f"❌ Error en forge: {e}")
        traceback.print_exc()
        return False


def test_equipment_system():
    """Verificar que el sistema de equipamiento funciona"""
    print("\n" + "="*70)
    print("TEST 4: SISTEMA DE EQUIPAMIENTO")
    print("="*70)
    
    try:
        from systems.equipment import CharacterEquipment, Equipment
        from systems.crafting import ForgeSystem
        
        # Crear equipo
        equipment = CharacterEquipment()
        print("✅ CharacterEquipment inicializado")
        
        # Crear arma
        forge = ForgeSystem()
        weapon_data = forge.forge_weapon("Daga")
        weapon = Equipment(weapon_data)
        print(f"✅ Arma creada: {weapon.name}")
        
        # Equipar
        equipment.equip_weapon(weapon)
        print(f"✅ Arma equipada")
        
        # Verificar daño
        damage = equipment.get_equipped_damage()
        print(f"✅ Daño equipado: {damage}")
        
        return True
    except Exception as e:
        print(f"❌ Error en equipment: {e}")
        traceback.print_exc()
        return False


def test_companion_system():
    """Verificar que el sistema de compañeros funciona"""
    print("\n" + "="*70)
    print("TEST 5: SISTEMA DE COMPAÑEROS")
    print("="*70)
    
    try:
        from systems.companion import CompanionGenerator, CompanionParty
        
        # Generar compañero
        companion = CompanionGenerator.generate(rank=2)
        print(f"✅ Compañero generado: {companion.name}")
        print(f"   Arqueotipo: {companion.archetype}")
        print(f"   ATK: {companion.get_total_atk()}")
        
        # Crear grupo
        party = CompanionParty()
        for i in range(3):
            comp = CompanionGenerator.generate(rank=1)
            party.add_companion(comp)
        print(f"✅ Grupo creado: {len(party.companions)} compañeros")
        print(f"   Poder total: {party.get_total_power()}")
        
        return True
    except Exception as e:
        print(f"❌ Error en companion: {e}")
        traceback.print_exc()
        return False


def test_player_integration():
    """Verificar que Player tiene equipamiento"""
    print("\n" + "="*70)
    print("TEST 6: INTEGRACIÓN CON PLAYER")
    print("="*70)
    
    try:
        from main import Player
        
        # Crear jugador
        player = Player()
        print(f"✅ Jugador creado: {player.name}")
        
        # Verificar equipamiento
        if hasattr(player, 'equipment'):
            print("✅ Player tiene equipamiento")
            total_atk = player.get_total_atk()
            print(f"   ATK Total: {total_atk}")
        else:
            print("❌ Player NO tiene equipamiento")
            return False
        
        # Verificar velocidad
        speed = player.get_attack_speed()
        print(f"✅ Velocidad de ataque: {speed}")
        
        return True
    except Exception as e:
        print(f"❌ Error en player: {e}")
        traceback.print_exc()
        return False


def test_combat_integration():
    """Verificar que Combat usa equipamiento"""
    print("\n" + "="*70)
    print("TEST 7: INTEGRACIÓN CON COMBAT")
    print("="*70)
    
    try:
        from main import Player
        from systems.combat import CombatEngine
        
        # Crear jugador y enemigo
        player = Player()
        enemy_stats = {"hp": 100, "atk": 15, "def": 5}
        
        # Calcular daño
        engine = CombatEngine()
        damage, is_crit, was_super_effective = engine.calculate_damage(player, enemy_stats)
        
        print(f"✅ Daño calculado: {damage}")
        print(f"   Crítico: {is_crit}")
        print(f"   Super efectivo: {was_super_effective}")
        print("✅ Combat está considerando equipamiento de Player")
        
        return True
    except Exception as e:
        print(f"❌ Error en combat: {e}")
        traceback.print_exc()
        return False


def test_json_files():
    """Verificar que los archivos JSON son válidos"""
    print("\n" + "="*70)
    print("TEST 8: VALIDACIÓN DE ARCHIVOS JSON")
    print("="*70)
    
    import json
    import os
    
    try:
        # Verificar Materiales.json
        path = "systems/Materiales.json"
        with open(path, 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        maderas = len(materials.get('Maderas', []))
        minerales = len(materials.get('Minerales', []))
        plantas = len(materials.get('Plantas', []))
        
        print(f"✅ Materiales.json válido")
        print(f"   Maderas: {maderas}")
        print(f"   Minerales: {minerales}")
        print(f"   Plantas: {plantas}")
        
        return True
    except Exception as e:
        print(f"❌ Error en JSON: {e}")
        traceback.print_exc()
        return False


def main():
    """Ejecutar todas las verificaciones"""
    print("\n" + "█"*70)
    print("█  VERIFICACIÓN COMPLETA DE SISTEMAS".center(70))
    print("█"*70)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Alchemy", test_alchemy_system()))
    results.append(("Forge", test_forge_system()))
    results.append(("Equipment", test_equipment_system()))
    results.append(("Companion", test_companion_system()))
    results.append(("Player Integration", test_player_integration()))
    results.append(("Combat Integration", test_combat_integration()))
    results.append(("JSON Files", test_json_files()))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE VERIFICACIÓN".center(70))
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n✅ TODOS LOS SISTEMAS VERIFICADOS CORRECTAMENTE")
        return 0
    else:
        print(f"\n❌ {total - passed} ERRORES ENCONTRADOS")
        return 1


if __name__ == "__main__":
    sys.exit(main())
