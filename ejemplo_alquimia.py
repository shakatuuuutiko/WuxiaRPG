"""
Ejemplos de Uso del Sistema de Alquimia Procedural
Demostraciones prácticas de cómo integrar alquimia en el juego
"""

from systems.crafting import AlchemySystem
import json
import os

# =============================================================================
# EJEMPLO 1: CRAFTEAR POCIONES ALEATORIAS
# =============================================================================
def ejemplo_craftear_pociones():
    """Crea pociones aleatorias - caso de uso típico en juego."""
    print("\n" + "="*70)
    print("EJEMPLO 1: CRAFTEAR POCIONES ALEATORIAS EN EL JUEGO")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\n🧪 Jugador entra a Laboratorio de Alquimia")
    print("   Ingredientes disponibles: 20 plantas")
    print("\n   [CREANDO POCIÓN #1...]")
    
    potion1 = alchemy.craft_potion(count=3)
    print(f"\n   ✓ Resultado: {potion1['name']}")
    print(f"   • Efecto: {potion1['effect']}")
    print(f"   • Potencia: {potion1['potency']}/100")
    print(f"   • Ingredientes: {', '.join(potion1['ingredients'])}")
    
    print("\n   [CREANDO POCIÓN #2...]")
    potion2 = alchemy.craft_potion(count=3)
    print(f"\n   ✓ Resultado: {potion2['name']}")
    print(f"   • Efecto: {potion2['effect']}")
    print(f"   • Potencia: {potion2['potency']}/100")
    
    print("\n   [CREANDO POCIÓN #3...]")
    potion3 = alchemy.craft_potion(count=3)
    print(f"\n   ✓ Resultado: {potion3['name']}")
    print(f"   • Efecto: {potion3['effect']}")
    print(f"   • Potencia: {potion3['potency']}/100")
    if not potion3['success']:
        print("   ⚠️  FALLÓ - Se creó incorrectamente")


# =============================================================================
# EJEMPLO 2: ALQUIMISTA NPC ENSEÑA RECETA
# =============================================================================
def ejemplo_descubrir_receta():
    """Un alquimista te enseña recetas específicas."""
    print("\n" + "="*70)
    print("EJEMPLO 2: ALQUIMISTA NPC ENSEÑA RECETA")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\n🧙 Alquimista Mayor: 'Joven aprendiz, aprende a crear pociones Yin'")
    print("   Me enseña los requisitos...\n")
    
    recipe = alchemy.discover_recipe(tag_name='Hielo', min_value=20)
    
    if recipe:
        print(f"   📜 Receta: '{recipe['recipe_name']}'")
        print(f"   └─ Necesitas:")
        for tag, valor in recipe['tags_needed'].items():
            print(f"      • {tag} ≥ {valor}")
        print(f"   └─ Efecto: {recipe['effect']}")
        print(f"   └─ Estilos posibles: {', '.join(recipe['descriptors'])}")
        print("\n   [Descubriste la receta: ENERGÍA YIN]")


# =============================================================================
# EJEMPLO 3: BATALLA - USAR POCIÓN DURANTE COMBATE
# =============================================================================
def ejemplo_usar_en_batalla():
    """Crear pociones y usarlas en combate."""
    print("\n" + "="*70)
    print("EJEMPLO 3: USAR POCIONES EN BATALLA")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\n⚔️  ¡COMBATE EN PROGRESO!")
    print("   Jugador: 50/100 HP")
    print("   Enemigo: 120/150 HP\n")
    
    # Crear poción de curacion
    print("   [CREANDO POCIÓN...]")
    potion = alchemy.craft_potion(count=2)
    
    print(f"\n   Nombre: {potion['name']}")
    print(f"   Efecto: {potion['effect']}")
    print(f"   Potencia: {potion['potency']}")
    
    if 'Restauración' in potion['effect'] or 'Defensa' in potion['effect']:
        print("\n   [BEBES LA POCIÓN]")
        heal = min(50, potion['potency'] * 2)  # Ejemplo de cálculo
        print(f"   ✓ Recuperaste {heal} HP")
        print(f"   Nueva salud: {50 + heal}/100 HP")
    else:
        print("\n   [BEBISTE LA POCIÓN]")
        print(f"   ✓ {potion['effect']}")


# =============================================================================
# EJEMPLO 4: CRAFTEAR EN LOTE (MODO MERCADER)
# =============================================================================
def ejemplo_craftear_lote():
    """Un mercader crea pociones en lote para vender."""
    print("\n" + "="*70)
    print("EJEMPLO 4: CRAFTEAR LOTE PARA VENDER")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\n🏪 Mercader de Pociones: 'Debo preparar el inventario de hoy'")
    print("   Preparando 10 pociones...\n")
    
    batch = alchemy.craft_batch(count=10)
    
    # Clasificar por tipo
    por_tipo = {}
    for potion in batch:
        effect = potion['effect']
        if effect not in por_tipo:
            por_tipo[effect] = []
        por_tipo[effect].append(potion)
    
    # Mostrar inventario
    print("   📦 INVENTARIO DE HOY:")
    for effect, pociones in por_tipo.items():
        count = len(pociones)
        potencia_promedio = sum(p['potency'] for p in pociones) // len(pociones)
        print(f"\n   • {effect} x{count}")
        print(f"     Potencia promedio: {potencia_promedio}")
        for p in pociones:
            status = "✓" if p['success'] else "✗"
            print(f"       {status} {p['name']}")
    
    # Cálculo de venta
    successful = sum(1 for p in batch if p['success'])
    print(f"\n   Tasa de éxito: {successful}/{len(batch)} ({successful*100//len(batch)}%)")
    print(f"   Precio total (estimado): {successful * 50} monedas")


# =============================================================================
# EJEMPLO 5: AVENTURERO BUSCANDO INGREDIENTES ESPECÍFICOS
# =============================================================================
def ejemplo_buscar_ingredientes():
    """Un aventurero busca plantas específicas para una receta."""
    print("\n" + "="*70)
    print("EJEMPLO 5: AVENTURERO BUSCA INGREDIENTES ESPECÍFICOS")
    print("="*70)
    
    # Cargar materiales
    MATERIALS_PATH = os.path.join(os.path.dirname(__file__), 'systems', 'Materiales.json')
    try:
        with open(MATERIALS_PATH, 'r', encoding='utf-8') as f:
            materials = json.load(f)
    except Exception:
        print("   Error cargando materiales")
        return
    
    plantas = materials.get('Plantas', [])
    alchemy = AlchemySystem()
    
    print("\n🗺️  Aventurero: 'Necesito crear una Píldora de Curacion'")
    print("   Requisito: Vida ≥ 20")
    print("\n   Buscando plantas con tag 'Vida'...\n")
    
    # Buscar plantas con alto valor de Vida
    plantas_vida = [p for p in plantas if p.get('tags', {}).get('Vida', 0) >= 15]
    
    print(f"   Encontré {len(plantas_vida)} plantas viables:")
    for i, planta in enumerate(plantas_vida[:5]):
        vida_value = planta.get('tags', {}).get('Vida', 0)
        print(f"     {i+1}. {planta['name']} (Vida: {vida_value}) - {planta['rarity']}")
    
    if plantas_vida:
        print(f"\n   [RECOLECTANDO 3 PLANTAS]")
        selected = plantas_vida[:3]
        
        # Mezclar
        print(f"   Ingredientes: {', '.join(p['name'] for p in selected)}")
        print(f"\n   [MEZCLANDO...]")
        
        name, success, effect, potency = alchemy.mix_ingredients(selected)
        print(f"\n   ✓ Resultado: {name}")
        print(f"   Efecto: {effect}")
        print(f"   Potencia: {potency}")
        print(f"   Éxito: {'Sí ✓' if success else 'No ✗'}")


# =============================================================================
# EJEMPLO 6: COMPARAR DIFERENTES MEZCLAS
# =============================================================================
def ejemplo_experimentar():
    """Un alquimista experimenta con diferentes ingredientes."""
    print("\n" + "="*70)
    print("EJEMPLO 6: EXPERIMENTACIÓN DE ALQUIMIA")
    print("="*70)
    
    MATERIALS_PATH = os.path.join(os.path.dirname(__file__), 'systems', 'Materiales.json')
    try:
        with open(MATERIALS_PATH, 'r', encoding='utf-8') as f:
            materials = json.load(f)
    except Exception:
        print("   Error cargando materiales")
        return
    
    plantas = materials.get('Plantas', [])
    alchemy = AlchemySystem()
    
    print("\n🔬 Alquimista Experimentador")
    print("   Probando diferentes combinaciones...")
    
    # Experimento 1: Pocas plantas
    print("\n   EXPERIMENTO 1: 2 plantas (mezcla simple)")
    if len(plantas) >= 2:
        result1 = alchemy.mix_ingredients(plantas[:2])
        print(f"   Resultado: {result1[0]} (Potencia: {result1[3]})")
    
    # Experimento 2: Muchas plantas
    print("\n   EXPERIMENTO 2: 5 plantas (mezcla compleja)")
    if len(plantas) >= 5:
        result2 = alchemy.mix_ingredients(plantas[:5])
        print(f"   Resultado: {result2[0]} (Potencia: {result2[3]})")
    
    # Experimento 3: Plantas específicas
    print("\n   EXPERIMENTO 3: Plantas de rareza Raro solo")
    rare_plants = [p for p in plantas if p.get('rarity') == 'Raro']
    if rare_plants:
        result3 = alchemy.mix_ingredients(rare_plants[:3])
        print(f"   Resultado: {result3[0]} (Potencia: {result3[3]})")
        print(f"   Éxito: {'Sí' if result3[1] else 'No'}")
    
    print("\n   Conclusión: La mezcla de pociones variadas produce resultados únicos cada vez")


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("\n" + "█"*70)
    print("█  EJEMPLOS PRÁCTICOS DE ALQUIMIA PROCEDURAL".center(70))
    print("█"*70)
    
    try:
        ejemplo_craftear_pociones()
        ejemplo_descubrir_receta()
        ejemplo_usar_en_batalla()
        ejemplo_craftear_lote()
        ejemplo_buscar_ingredientes()
        ejemplo_experimentar()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS".center(70))
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
