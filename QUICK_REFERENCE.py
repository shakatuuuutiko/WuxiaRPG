#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUICK_REFERENCE.py - Referencia Rápida del Sistema de Crafting

Use este archivo como referencia rápida para todas las funciones disponibles.
"""

from systems.crafting import (
    ForgeSystem, ToolSystem, ArmorSystem, AlchemySystem,
    WEAPON_MOLDS, TOOL_MOLDS, ARMOR_PARTS,
    WEAPON_PREFIXES, TOOL_SUFFIXES, MATERIAL_SUFFIXES,
    RARITY_ORDER
)

print("""
================================================================================
SISTEMA DE CRAFTING - REFERENCIA RÁPIDA
================================================================================

1. FORJA DE ARMAS
================================================================================

Clases:
  • ForgeSystem - Sistema principal de forja

Métodos principales:
  • forge_weapon(tipo, prefix=None) - Forjar arma individual
  • forge_batch(tipo, count) - Forjar múltiples armas

Ejemplo:
  from systems.crafting import ForgeSystem
  forge = ForgeSystem()
  
  # Arma con prefijo aleatorio
  weapon = forge.forge_weapon("Espada")
  print(weapon['name'])      # Nombre dinámico
  print(weapon['atk'])       # Ataque
  print(weapon['speed'])     # Velocidad
  print(weapon['special_effect'])  # Efecto especial
  
  # Arma con prefijo específico
  brutal_sword = forge.forge_weapon("Espada", prefix="Brutal")
  
  # Lote de armas
  swords = forge.forge_batch("Espada", count=5)

Armas disponibles (21):
  Originales (7): Daga, Espada, Lanza, Sable, Arco, Hacha, Pico
  Nuevas (14): Catana, Falcata, Claymore, Tridente, Martillo, Maza,
               Mangual, Guadaña, Espada Ancha, Bastón, Garras, Horca,
               Espada Corta, Alabarda

Prefijos disponibles (10):
  Brutal → ATK ×1.25, SPD ×0.85, Efecto: Bleed
  Ágil → ATK ×0.90, SPD ×1.25, Efecto: Extra Hit
  Fiero → ATK ×1.30, SPD ×0.80, Efecto: Crush
  Maldito → ATK ×1.10, SPD ×0.95, Efecto: Drain HP
  Bendito → ATK ×1.05, SPD ×1.05, Efecto: Heal on Hit
  Fantasmal → ATK ×0.95, SPD ×1.15, Efecto: Ignore Armor
  Glacial → ATK ×1.00, SPD ×1.10, Efecto: Slow Enemy
  Ígneo → ATK ×1.15, SPD ×0.95, Efecto: Burn Damage
  Venenoso → ATK ×0.95, SPD ×1.05, Efecto: Poison
  Eléctrico → ATK ×1.05, SPD ×1.20, Efecto: Stun

Atributos retornados:
  'name': str - Nombre dinámico
  'atk': int - Daño de ataque
  'speed': float - Velocidad de ataque
  'prefix': str - Nombre del prefijo
  'special_effect': str - Efecto especial
  'components': dict - {'madera': str, 'mineral': str}
  'rarities': dict - Rareza de los materiales

================================================================================

2. CREACIÓN DE HERRAMIENTAS
================================================================================

Clases:
  • ToolSystem - Sistema de herramientas

Métodos principales:
  • craft_tool(tipo, suffix=None) - Crear herramienta
  • craft_batch(tipo, count) - Crear múltiples herramientas

Ejemplo:
  from systems.crafting import ToolSystem
  tools = ToolSystem()
  
  # Herramienta con sufijo aleatorio
  tool = tools.craft_tool("Pico")
  print(tool['name'])        # Nombre dinámico
  print(tool['power'])       # Potencia
  print(tool['durability'])  # Durabilidad
  print(tool['suffix'])      # Nombre del sufijo
  
  # Herramienta con sufijo específico
  strong_axe = tools.craft_tool("Hacha", suffix="Robusta")
  
  # Lote de herramientas
  picos = tools.craft_batch("Pico", count=10)

Herramientas disponibles (7):
  Pico, Hacha, Pala, Azada, Hoz, Cuchillo, Sierra

Sufijos disponibles (8):
  Refinada → Potencia ×1.10, Durabilidad ×0.95
  Robusta → Potencia ×0.95, Durabilidad ×1.15
  Maestra → Potencia ×1.20, Durabilidad ×1.05
  Perdurable → Potencia ×0.90, Durabilidad ×1.25
  Experta → Potencia ×1.15, Durabilidad ×1.00
  Imbuida → Potencia ×1.25, Durabilidad ×0.90
  Afilada → Potencia ×1.18, Durabilidad ×0.92
  Templada → Potencia ×1.05, Durabilidad ×1.10

Atributos retornados:
  'name': str - Nombre dinámico
  'power': int - Potencia de la herramienta
  'durability': int - Durabilidad
  'suffix': str - Nombre del sufijo
  'tool_type': str - Tipo de herramienta
  'components': dict - {'wood': str, 'mineral': str}
  'rarity': str - Rareza general

================================================================================

3. FORJA DE ARMADURAS
================================================================================

Clases:
  • ArmorSystem - Sistema de armaduras

Métodos principales:
  • forge_armor(parte, prefix=None) - Forjar pieza individual
  • forge_full_set(prefix=None) - Forjar conjunto completo (8 piezas)
  • forge_batch(parte, count) - Forjar múltiples piezas del mismo tipo

Ejemplo:
  from systems.crafting import ArmorSystem
  armor = ArmorSystem()
  
  # Pieza individual
  casco = armor.forge_armor("Casco")
  print(casco['name'])       # Nombre dinámico
  print(casco['defense'])    # Defensa
  print(casco['weight'])     # Peso
  print(casco['special_effect'])  # Efecto especial
  
  # Con prefijo específico
  brutal_armor = armor.forge_armor("Pechera", prefix="Brutal")
  
  # Conjunto completo
  full_set = armor.forge_full_set(prefix="Bendito")
  total_def = sum(p['defense'] for p in full_set)
  
  # Lote de piezas
  cascos = armor.forge_batch("Casco", count=5)

Partes de armadura (8):
  Casco, Pechera, Guantes, Cintura, Grebas, Botas, Escudo, Cota de Malla

Prefijos disponibles (10):
  (Mismo que armas - ver arriba)

Atributos retornados:
  'name': str - Nombre dinámico
  'defense': int - Defensa
  'weight': int - Peso
  'slots': int - Espacios para encantamientos
  'prefix': str - Nombre del prefijo
  'special_effect': str - Efecto especial
  'component': str - Material principal
  'rarity': str - Rareza

================================================================================

4. ALQUIMIA
================================================================================

Clases:
  • AlchemySystem - Sistema de alquimia

Métodos principales:
  • craft_potion(count=3) - Crear poción con N ingredientes
  • craft_batch(count=5) - Crear múltiples pócimas
  • discover_recipe(tag, min_value=20) - Descubrir receta

Ejemplo:
  from systems.crafting import AlchemySystem
  alchemy = AlchemySystem()
  
  # Poción individual
  potion = alchemy.craft_potion(count=3)
  print(potion['name'])      # Nombre dinámico
  print(potion['success'])   # True/False
  print(potion['effect'])    # Efecto de la poción
  print(potion['potency'])   # Poder
  
  # Lote de pócimas
  potions = alchemy.craft_batch(count=10)
  
  # Descubrir receta
  recipe = alchemy.discover_recipe("Fuego")
  if recipe:
      print(recipe['recipe_name'])  # Nombre de receta
      print(recipe['tags_needed'])  # Tags necesarios
      print(recipe['effect'])       # Efecto

Recetas disponibles (11):
  Fuego, Hielo, Veneno, Electricidad, Vida, Defensa, Velocidad,
  Sabiduría, Yang, Yin, Sangre

Atributos retornados:
  'name': str - Nombre dinámico
  'success': bool - Éxito del crafteo
  'effect': str - Efecto de la poción
  'potency': int - Poder de la poción
  'ingredients': list - Ingredientes usados
  'ingredient_count': int - Número de ingredientes

================================================================================

5. CONSTANTES DISPONIBLES
================================================================================

Armas:
  WEAPON_MOLDS - Dict de 21 armas con specs

Herramientas:
  TOOL_MOLDS - Dict de 7 herramientas con specs

Armaduras:
  ARMOR_PARTS - Dict de 8 partes de armadura

Modificadores:
  WEAPON_PREFIXES - Dict de 10 prefijos para armas/armaduras
  TOOL_SUFFIXES - Dict de 8 sufijos para herramientas
  MATERIAL_SUFFIXES - Dict de sufijos por rareza
  RARITY_ORDER - Dict con orden de rarezas

Ejemplo de acceso:
  from systems.crafting import WEAPON_MOLDS
  print(WEAPON_MOLDS.keys())  # Lista todas las armas
  
  for arma, specs in WEAPON_MOLDS.items():
      print(f"{arma}: ATK {specs['atk_base']}, SPD {specs['speed']}")

================================================================================

6. EJEMPLOS COMPLETOS
================================================================================

Ejemplo 1: Equipar completamente a un guerrero
  from systems.crafting import ForgeSystem, ArmorSystem
  
  forge = ForgeSystem()
  armor = ArmorSystem()
  
  # Arma de combate
  weapon = forge.forge_weapon("Claymore", prefix="Brutal")
  
  # Armadura completa
  armadura = armor.forge_full_set(prefix="Brutal")
  
  # Mostrar equipo
  print(f"Arma: {weapon['name']} (ATK: {weapon['atk']})")
  total_def = sum(p['defense'] for p in armadura)
  print(f"Armadura: Defensa total {total_def}")

Ejemplo 2: Crear inventario de comerciante
  from systems.crafting import ForgeSystem, RARITY_ORDER
  
  forge = ForgeSystem()
  
  # Forjar lotes de diferentes armas
  tienda = {}
  for arma_tipo in ["Espada", "Arco", "Hacha"]:
      tienda[arma_tipo] = forge.forge_batch(arma_tipo, count=5)
  
  # Calcular valor total
  valor_total = 0
  for tipo, armas in tienda.items():
      for arma in armas:
          rareza = arma['rarities']['overall']
          precio = 100 * (RARITY_ORDER.get(rareza, 0) + 1)
          valor_total += precio

Ejemplo 3: Crear tesoro para mazmorra
  from systems.crafting import ForgeSystem, ToolSystem, ArmorSystem, AlchemySystem
  import random
  
  forge = ForgeSystem()
  tools = ToolSystem()
  armor = ArmorSystem()
  alchemy = AlchemySystem()
  
  tesoro = {
      'armas': forge.forge_batch(random.choice(["Espada", "Arco"]), count=2),
      'herramientas': [tools.craft_tool("Pico") for _ in range(2)],
      'armaduras': [armor.forge_armor("Casco") for _ in range(2)],
      'pociones': alchemy.craft_batch(count=5)
  }
  
  print(f"Tesoro generado con {sum(len(v) for v in tesoro.values())} items")

================================================================================

7. TIPS Y TRUCOS
================================================================================

• Para máximo daño: usa armas con prefijo "Brutal" o "Fiero"
• Para máxima velocidad: usa armas con prefijo "Ágil" o "Eléctrico"
• Para máxima defensa: forja armadura con prefijo "Brutal" o "Fiero"
• Para herramientas minería: usa sufijo "Imbuida" (máxima potencia)
• Para herramientas duraderas: usa sufijo "Perdurable"
• Las pócimas Legendarias valen 5× más que las Comunes
• Los nombres dinámicos se generan cada vez - no son iguales

================================================================================

8. ATRIBUTOS RETORNADOS POR CATEGORÍA
================================================================================

ARMAS retornan:
  {'name', 'type', 'mold', 'prefix', 'atk', 'speed', 'special_effect',
   'components', 'rarities'}

HERRAMIENTAS retornan:
  {'name', 'type', 'tool_type', 'suffix', 'power', 'durability',
   'components', 'rarity'}

ARMADURAS retornan:
  {'name', 'type', 'part', 'prefix', 'defense', 'weight', 'slots',
   'special_effect', 'component', 'rarity'}

POCIONES retornan:
  {'name', 'success', 'effect', 'potency', 'ingredients', 'ingredient_count'}

================================================================================

9. INTEGRACIÓN EN game_engine.py
================================================================================

# En __init__
self.forge = ForgeSystem()
self.tools = ToolSystem()
self.armor = ArmorSystem()
self.alchemy = AlchemySystem()

# En comandos de jugador
cmd_forjar_arma = lambda tipo, prefijo: self.forge.forge_weapon(tipo, prefix=prefijo)
cmd_craftar_tool = lambda tipo: self.tools.craft_tool(tipo)
cmd_forjar_armadura = lambda parte: self.armor.forge_armor(parte)
cmd_mezclar_pocion = lambda ingredientes: self.alchemy.craft_potion(count=ingredientes)

================================================================================

Para documentación completa, ver: CRAFTING_SYSTEM_DOCUMENTATION.md
Para ejemplos ejecutables, ver: CRAFTEO_EJEMPLOS.py
Para código fuente, ver: systems/crafting.py

================================================================================
""")
