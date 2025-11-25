#!/usr/bin/env python
"""Verificación final de integración"""

from main import Player
from systems.equipment import Equipment
from systems.crafting import ForgeSystem
from systems.companion import CompanionGenerator
from systems.combat import CombatEngine

print('=== VERIFICACIÓN FINAL DE INTEGRACIÓN ===\n')

# Test 1: Player con equipo
print('1. PLAYER CON EQUIPAMIENTO')
player = Player()
print(f'   Nombre: {player.name}')
print(f'   ATK Base: {player.stats["atk"]}')
print(f'   ATK Total (con equipo): {player.get_total_atk()}')
print(f'   Velocidad: {player.get_attack_speed()}')
print(f'   Arma: {player.equipment.equipped_weapon.name}')

# Test 2: Cambiar arma
print('\n2. CAMBIANDO ARMA')
forge = ForgeSystem()
new_weapon = Equipment(forge.forge_weapon('Sable'))
player.equipment.equip_weapon(new_weapon)
print(f'   Nueva arma: {player.equipment.equipped_weapon.name}')
print(f'   Nuevo ATK Total: {player.get_total_atk()}')

# Test 3: Compañero equipable
print('\n3. COMPAÑERO EQUIPABLE')
comp = CompanionGenerator.generate(rank=2)
print(f'   Nombre: {comp.name}')
print(f'   Arqueotipo: {comp.archetype}')
print(f'   ATK Total: {comp.get_total_atk()}')
print(f'   Arma: {comp.equipment.equipped_weapon.name}')

# Test 4: Combate
print('\n4. SIMULACIÓN DE COMBATE')
engine = CombatEngine()
damage = engine.calculate_damage(player, comp.stats)[0]
print(f'   Daño del jugador: {damage}')
print(f'   Considerando: ATK total ({player.get_total_atk()}) + elementos + defensa')

print('\n✅ INTEGRACIÓN COMPLETA Y FUNCIONAL')
