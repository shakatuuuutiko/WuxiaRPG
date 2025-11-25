#!/usr/bin/env python
"""
Demo de uso del sistema de crafting mejorado.
Muestra:
  - Forja dinámica con nombres basados en materiales
  - Sistema de alquimia basado en tags
  - Lotes de crafting
"""

from systems.crafting import ForgeSystem, AlchemySystem, Materials

def demo_forja():
    print("=" * 60)
    print("DEMO: FORJA DINÁMICA")
    print("=" * 60)
    
    forge = ForgeSystem()
    
    # Ejemplo 1: Forja con moldes diferentes
    moldes = ["Sable", "Arco", "Espada", "Hacha", "Daga"]
    
    for molde in moldes:
        weapon = forge.forge_weapon(molde)
        print(f"\n{molde}:")
        print(f"  → Nombre: {weapon['name']}")
        print(f"  → Ataque: {weapon['atk']}")
        print(f"  → Velocidad: {weapon['speed']}")
        print(f"  → Madera: {weapon['components']['madera']}")
        print(f"  → Mineral: {weapon['components']['mineral']}")
    
    # Ejemplo 2: Lote de forja
    print("\n" + "=" * 60)
    print("LOTE: 5 Sables forjados")
    print("=" * 60)
    
    sables = forge.forge_batch("Sable", count=5)
    for i, sable in enumerate(sables, 1):
        print(f"\n{i}. {sable['name']}")
        print(f"   ATK: {sable['atk']} | Rareza: {sable['rarities']['overall']}")

def demo_alquimia():
    print("\n" + "=" * 60)
    print("DEMO: ALQUIMIA / HERBOLOGÍA")
    print("=" * 60)
    
    alchemy = AlchemySystem()
    
    for attempt in range(5):
        potion = alchemy.craft_potion(count=random.randint(2, 4))
        status = "✓ ÉXITO" if potion['success'] else "✗ FALLO"
        print(f"\n{attempt + 1}. {status}: {potion['name']}")
        print(f"   Potencia: {potion['potency']}")
        print(f"   Plantas usadas: {len(potion['ingredients'])}")

def demo_materiales():
    print("\n" + "=" * 60)
    print("DEMO: MATERIALES DISPONIBLES")
    print("=" * 60)
    
    print(f"\nTotal de Maderas: {len(Materials.get('Maderas', []))}")
    print(f"Total de Minerales: {len(Materials.get('Minerales', []))}")
    print(f"Total de Plantas: {len(Materials.get('Plantas', []))}")
    
    # Mostrar ejemplos
    if Materials['Maderas']:
        print(f"\n--- Maderas (ejemplos) ---")
        for wood in Materials['Maderas'][:3]:
            stats = wood.get('stats_forja', {})
            print(f"• {wood['name']} ({wood['rarity']})")
            print(f"  Dureza: {stats.get('dureza')}, Conductividad: {stats.get('conductividad')}, Peso: {stats.get('peso')}")
    
    if Materials['Plantas']:
        print(f"\n--- Plantas (ejemplos) ---")
        for plant in Materials['Plantas'][:3]:
            tags = plant.get('tags', {})
            print(f"• {plant['name']} ({plant['rarity']})")
            print(f"  Tags: {tags}")

if __name__ == '__main__':
    import random
    
    demo_forja()
    demo_alquimia()
    demo_materiales()
    
    print("\n" + "=" * 60)
    print("FIN DE LA DEMO")
    print("=" * 60)
