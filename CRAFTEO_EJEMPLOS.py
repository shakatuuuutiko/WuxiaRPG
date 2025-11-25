#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRAFTEO_EJEMPLOS.py - Ejemplos prácticos del sistema de crafting mejorado

Este archivo demuestra cómo usar todas las funcionalidades del sistema de
crafting mejorado para jugadores, NPCs y el sistema de juego.

Autor: Sistema de Crafting WuxiaRPG
"""

import random
from systems.crafting import ForgeSystem, ToolSystem, ArmorSystem, AlchemySystem

# ============================================================================
# EJEMPLOS PRÁCTICOS - SISTEMA DE FORJA
# ============================================================================

def ejemplo_1_forjar_arma_aleatoria():
    """Forja un arma con prefijo y materiales aleatorios"""
    forge = ForgeSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 1: Forjar Arma Aleatoria")
    print("="*70)
    
    # Seleccionar arma aleatoria
    armas_disponibles = list(forge.forge_weapon.__code__.co_consts)
    arma_tipo = random.choice(["Espada", "Arco", "Sable", "Claymore", "Martillo"])
    
    # Forjar
    arma = forge.forge_weapon(arma_tipo)
    
    print(f"\n✓ Arma Forjada:")
    print(f"  Nombre: {arma['name']}")
    print(f"  Tipo: {arma['mold']}")
    print(f"  Ataque: {arma['atk']} | Velocidad: {arma['speed']}")
    print(f"  Prefijo: {arma['prefix']} → Efecto: {arma['special_effect']}")
    print(f"  Rareza: {arma['rarities']['overall']}")
    print(f"  Componentes:")
    print(f"    • Madera: {arma['components']['madera']}")
    print(f"    • Mineral: {arma['components']['mineral']}")
    
    return arma


def ejemplo_2_forjar_arma_especifica():
    """Forja un arma con prefijo específico elegido por el jugador"""
    forge = ForgeSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 2: Forjar Arma con Prefijo Específico")
    print("="*70)
    
    # Jugador elige: crear una espada brutal
    arma = forge.forge_weapon("Espada", prefix="Brutal")
    
    print(f"\n✓ Espada Brutal Forjada:")
    print(f"  {arma['name']}")
    print(f"  ATK Base: 35 × Multiplicador: 1.25 = {arma['atk']}")
    print(f"  SPD Base: 1.0 × Multiplicador: 0.85 = {arma['speed']}")
    print(f"  Efecto: {arma['special_effect']} (Causa sangrado)")
    
    return arma


def ejemplo_3_lote_armas_comerciante():
    """Un comerciante forja un lote de armas para vender"""
    forge = ForgeSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 3: Lote de Armas para Comerciante")
    print("="*70)
    
    # Comerciante forja 8 espadas de calidad
    print("\n✓ Comerciante forjando 8 espadas...")
    espadas = forge.forge_batch("Espada", count=8)
    
    print(f"\nInventario de Comerciante:")
    precio_base = 100
    for i, espada in enumerate(espadas, 1):
        rareza = espada['rarities']['overall']
        multiplicador = {"Común": 1.0, "Raro": 1.5, "Épico": 2.5, "Legendario": 5.0}[rareza]
        precio = int(precio_base * multiplicador)
        print(f"  {i}. {espada['name']:40} | ATK: {espada['atk']:3} | Precio: {precio} oro")
    
    return espadas


def ejemplo_4_armas_nuevas_disponibles():
    """Muestra todas las 15 armas nuevas disponibles"""
    forge = ForgeSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 4: Listado de Armas Nuevas (15 tipos)")
    print("="*70)
    
    armas_nuevas = [
        "Catana", "Falcata", "Claymore", "Tridente", "Martillo",
        "Maza", "Mangual", "Guadaña", "Espada Ancha", "Bastón",
        "Garras", "Horca", "Espada Corta", "Alabarda"
    ]
    
    print("\n  Arma               ATK Aprox.    SPD Aprox.    Tipo")
    print("  " + "-"*60)
    
    for arma_nombre in armas_nuevas:
        arma = forge.forge_weapon(arma_nombre)
        atk = arma['atk']
        spd = arma['speed']
        
        # Categoría
        if spd > 1.5:
            tipo = "Rápida"
        elif spd < 0.85:
            tipo = "Lenta/Pesada"
        else:
            tipo = "Equilibrada"
        
        print(f"  {arma_nombre:18} {atk:3}         {spd:5.2f}       {tipo}")
    
    return armas_nuevas


# ============================================================================
# EJEMPLOS PRÁCTICOS - HERRAMIENTAS
# ============================================================================

def ejemplo_5_crear_herramientas():
    """Crear diferentes herramientas para minería y agricultura"""
    tools = ToolSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 5: Crear Herramientas Especializadas")
    print("="*70)
    
    tipos_herramientas = ["Pico", "Hacha", "Azada", "Hoz"]
    
    print("\n✓ Herramientas Creadas:")
    herramientas = {}
    
    for herramienta_tipo in tipos_herramientas:
        tool = tools.craft_tool(herramienta_tipo)
        herramientas[herramienta_tipo] = tool
        
        print(f"\n  {tool['name']}")
        print(f"    Potencia: {tool['power']}")
        print(f"    Durabilidad: {tool['durability']}")
        print(f"    Sufijo: {tool['suffix']}")
        print(f"    Rareza: {tool['rarity']}")
    
    return herramientas


def ejemplo_6_herramientas_especificas():
    """Crear herramientas con sufijos específicos para diferentes trabajos"""
    tools = ToolSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 6: Herramientas con Sufijos Optimizados")
    print("="*70)
    
    print("\n✓ Herramientas Optimizadas para Tareas Específicas:")
    
    # Para minería: queremos máxima potencia
    pico_mineria = tools.craft_tool("Pico", suffix="Imbuida")
    print(f"\n  Para Minería (máxima potencia):")
    print(f"    {pico_mineria['name']}")
    print(f"    Potencia: {pico_mineria['power']} (mejorada)")
    
    # Para leña: queremos durabilidad
    hacha_lena = tools.craft_tool("Hacha", suffix="Perdurable")
    print(f"\n  Para Leña (máxima durabilidad):")
    print(f"    {hacha_lena['name']}")
    print(f"    Durabilidad: {hacha_lena['durability']} (mejorada)")
    
    # Para agricultura: balance
    azada_agricultura = tools.craft_tool("Azada", suffix="Templada")
    print(f"\n  Para Agricultura (balance):")
    print(f"    {azada_agricultura['name']}")
    print(f"    Potencia: {azada_agricultura['power']} | Durabilidad: {azada_agricultura['durability']}")
    
    return [pico_mineria, hacha_lena, azada_agricultura]


# ============================================================================
# EJEMPLOS PRÁCTICOS - ARMADURAS
# ============================================================================

def ejemplo_7_armar_guerrero():
    """Armar completamente a un guerrero con conjunto de armadura"""
    armor = ArmorSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 7: Equipar Guerrero Completo")
    print("="*70)
    
    # Crear conjunto con prefijo específico
    print("\n✓ Creando armadura Brutal para guerrero...")
    armadura_brutal = armor.forge_full_set(prefix="Brutal")
    
    print(f"\nEquipo Completo del Guerrero:")
    print(f"  (Prefijo: Brutal - Ataque aumentado, Efecto: Bleed)")
    print()
    
    total_def = 0
    peso_total = 0
    slots_total = 0
    
    for piece in armadura_brutal:
        total_def += piece['defense']
        peso_total += piece['weight']
        slots_total += piece['slots']
        print(f"  • {piece['part']:15} DEF: {piece['defense']:3} | PESO: {piece['weight']:2} | SLOTS: {piece['slots']}")
    
    print(f"\n  TOTAL: Defensa {total_def} | Peso {peso_total} | Slots {slots_total}")
    print(f"  Efecto: {armadura_brutal[0]['special_effect']}")
    
    return armadura_brutal


def ejemplo_8_diferentes_estilos_armadura():
    """Mostrar diferentes estilos de armadura según prefijo"""
    armor = ArmorSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 8: Diferentes Estilos de Armadura")
    print("="*70)
    
    estilos = ["Brutal", "Ágil", "Bendito", "Glacial"]
    
    print("\n✓ Comparativa de Estilos de Armadura:\n")
    
    for estilo in estilos:
        # Crear solo pechera para comparación
        pechera = armor.forge_armor("Pechera", prefix=estilo)
        
        print(f"  Estilo: {estilo}")
        print(f"    {pechera['name']}")
        print(f"    Defensa: {pechera['defense']} | Efecto: {pechera['special_effect']}")
        print()
    
    return estilos


# ============================================================================
# EJEMPLOS PRÁCTICOS - ALQUIMIA
# ============================================================================

def ejemplo_9_mezclar_pociones():
    """Mezclar diferentes pociones alquímicas"""
    alchemy = AlchemySystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 9: Mezcla de Pócimas Alquímicas")
    print("="*70)
    
    print("\n✓ Creando 5 pociones...")
    pociones = alchemy.craft_batch(count=5)
    
    exitos = 0
    for i, pocion in enumerate(pociones, 1):
        status = "✓" if pocion['success'] else "✗"
        exitos += pocion['success']
        
        print(f"\n  {i}. {pocion['name']} [{status}]")
        print(f"     Efecto: {pocion['effect']}")
        print(f"     Potencia: {pocion['potency']}")
        if pocion['success']:
            print(f"     Vendible: {pocion['potency'] * 10} monedas")
    
    tasa_exito = (exitos / len(pociones)) * 100
    print(f"\n  Tasa de Éxito: {tasa_exito:.1f}% ({exitos}/{len(pociones)})")
    
    return pociones


def ejemplo_10_alquimista_especializado():
    """Un alquimista intenta perfeccionar una receta"""
    alchemy = AlchemySystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 10: Alquimista Perfeccionando Receta")
    print("="*70)
    
    print("\n✓ Descubriendo receta con tag 'Fuego'...")
    receta = alchemy.discover_recipe("Fuego", min_value=25)
    
    if receta:
        print(f"\n  Receta Descubierta: {receta['recipe_name']}")
        print(f"  Efecto: {receta['effect']}")
        print(f"  Tags Necesarios: {receta['tags_needed']}")
        print(f"  Descriptores: {', '.join(receta['descriptors'][:3])}")
        
        print(f"\n  Intentando crear 10 pociones con esta receta...")
        exitos = 0
        for _ in range(10):
            potion = alchemy.craft_potion(count=3)
            if potion['success'] and potion['effect'] == receta['effect']:
                exitos += 1
        
        print(f"  Pócimas exitosas de esta receta: {exitos}/10")
    
    return receta


# ============================================================================
# EJEMPLOS PRÁCTICOS - CASOS COMPLEJOS
# ============================================================================

def ejemplo_11_nvpc_equipo_basico():
    """Un NPC obtiene su equipo básico"""
    forge = ForgeSystem()
    tools = ToolSystem()
    armor = ArmorSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 11: NPC Recibe Equipo Básico (Campesino)")
    print("="*70)
    
    print("\n✓ Equipando a campesino con herramientas básicas...")
    
    # Herramientas para trabajar
    azada = tools.craft_tool("Azada", suffix="Robusta")
    hoz = tools.craft_tool("Hoz", suffix="Afilada")
    
    print(f"\n  Herramientas:")
    print(f"    • {azada['name']} (Potencia: {azada['power']})")
    print(f"    • {hoz['name']} (Potencia: {hoz['power']})")
    
    # Armadura ligera
    armadura_campesino = armor.forge_full_set(prefix="Ágil")
    total_def = sum(p['defense'] for p in armadura_campesino)
    
    print(f"\n  Armadura Ligera (Defensa total: {total_def}):")
    for piece in armadura_campesino[:3]:  # Mostrar las primeras 3
        print(f"    • {piece['part']}: {piece['defense']} defensa")
    
    return {"herramientas": [azada, hoz], "armadura": armadura_campesino}


def ejemplo_12_nvpc_equipo_guerrero():
    """Un NPC guerrero recibe equipo de combate"""
    forge = ForgeSystem()
    armor = ArmorSystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 12: NPC Recibe Equipo de Combate (Guerrero)")
    print("="*70)
    
    print("\n✓ Equipando guerrero con arma y armadura...")
    
    # Arma de combate
    arma = forge.forge_weapon("Espada", prefix="Brutal")
    print(f"\n  Arma:")
    print(f"    {arma['name']}")
    print(f"    ATK: {arma['atk']} | SPD: {arma['speed']}")
    
    # Armadura de combate
    armadura_guerrero = armor.forge_full_set(prefix="Fiero")
    total_def = sum(p['defense'] for p in armadura_guerrero)
    
    print(f"\n  Armadura de Combate:")
    print(f"    Defensa Total: {total_def}")
    print(f"    Prefijo: Fiero (Ataque muy aumentado, Efecto: Crush)")
    print(f"    Piezas: {len(armadura_guerrero)}")
    
    return {"arma": arma, "armadura": armadura_guerrero}


def ejemplo_13_generador_tesoro():
    """Generar un tesoro variado para una mazmorra"""
    forge = ForgeSystem()
    tools = ToolSystem()
    armor = ArmorSystem()
    alchemy = AlchemySystem()
    
    print("\n" + "="*70)
    print("EJEMPLO 13: Generar Tesoro de Mazmorra")
    print("="*70)
    
    print("\n✓ Generando tesoro...")
    
    tesoro = {
        "armas": forge.forge_batch(random.choice(["Espada", "Arco", "Martillo"]), count=2),
        "herramientas": [tools.craft_tool(random.choice(["Pico", "Hacha"])) for _ in range(2)],
        "armaduras": [armor.forge_armor(random.choice(list(armor.forge_armor.__code__.co_consts or ["Casco"]))) for _ in range(2)],
        "pociones": alchemy.craft_batch(count=3)
    }
    
    print(f"\n  Armas ({len(tesoro['armas'])}):")
    for arma in tesoro['armas']:
        print(f"    • {arma['name']} - ATK: {arma['atk']}")
    
    print(f"\n  Herramientas ({len(tesoro['herramientas'])}):")
    for tool in tesoro['herramientas']:
        print(f"    • {tool['name']} - Potencia: {tool['power']}")
    
    print(f"\n  Pociones ({len(tesoro['pociones'])}):")
    for pocion in tesoro['pociones']:
        print(f"    • {pocion['name']} - Efecto: {pocion['effect']}")
    
    return tesoro


# ============================================================================
# FUNCIÓN MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  EJEMPLOS PRÁCTICOS - SISTEMA DE CRAFTING AVANZADO".center(68) + "#")
    print("#" + "  WuxiaRPG".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    # Ejecutar todos los ejemplos
    ejemplo_1_forjar_arma_aleatoria()
    ejemplo_2_forjar_arma_especifica()
    ejemplo_3_lote_armas_comerciante()
    ejemplo_4_armas_nuevas_disponibles()
    
    ejemplo_5_crear_herramientas()
    ejemplo_6_herramientas_especificas()
    
    ejemplo_7_armar_guerrero()
    ejemplo_8_diferentes_estilos_armadura()
    
    ejemplo_9_mezclar_pociones()
    ejemplo_10_alquimista_especializado()
    
    ejemplo_11_nvpc_equipo_basico()
    ejemplo_12_nvpc_equipo_guerrero()
    ejemplo_13_generador_tesoro()
    
    print("\n" + "#"*70)
    print("#" + "  Ejemplos Completados OK".center(68) + "#")
    print("#"*70 + "\n")
