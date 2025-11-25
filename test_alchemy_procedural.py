"""
Test del Sistema de Alquimia Procedural
Demuestra cómo se generan recetas dinámicamente basadas en tags de plantas
"""

from systems.crafting import AlchemySystem
import json
import os

def test_basic_alchemy():
    """Test 1: Crear pociones y ver sus nombres generados proceduralmente."""
    print("\n" + "="*70)
    print("TEST 1: ALQUIMIA PROCEDURAL - NOMBRES DINÁMICOS")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\nCreando 5 pociones con ingredientes aleatorios...")
    for i in range(5):
        potion = alchemy.craft_potion(count=3)
        print(f"\n  Poción {i+1}:")
        print(f"    Nombre:      {potion['name']}")
        print(f"    Ingredientes: {', '.join(potion['ingredients'])}")
        print(f"    Efecto:      {potion['effect']}")
        print(f"    Potencia:    {potion['potency']}")
        print(f"    Éxito:       {'✓' if potion['success'] else '✗'}")


def test_recipe_discovery():
    """Test 2: Descubrir recetas por tag específico."""
    print("\n" + "="*70)
    print("TEST 2: DESCUBRIMIENTO DE RECETAS POR TAG")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    # Probar diferentes tags
    tags_to_test = ['Fuego', 'Hielo', 'Vida', 'Defensa', 'Velocidad', 'Sangre']
    
    for tag in tags_to_test:
        recipe = alchemy.discover_recipe(tag, min_value=20)
        if recipe:
            print(f"\n  📖 Receta de {tag}:")
            print(f"     Nombre: {recipe['recipe_name']}")
            print(f"     Requerimientos: {recipe['tags_needed']}")
            print(f"     Efecto: {recipe['effect']}")
            print(f"     Estilos: {', '.join(recipe['descriptors'])}")
        else:
            print(f"\n  ❌ No hay receta para {tag}")


def test_ingredients_analysis():
    """Test 3: Análisis detallado de ingredientes."""
    print("\n" + "="*70)
    print("TEST 3: ANÁLISIS DE INGREDIENTES")
    print("="*70)
    
    # Cargar materiales
    MATERIALS_PATH = os.path.join(os.path.dirname(__file__), 'systems', 'Materiales.json')
    try:
        with open(MATERIALS_PATH, 'r', encoding='utf-8') as f:
            materials = json.load(f)
    except Exception as e:
        print(f"Error cargando materiales: {e}")
        return
    
    plantas = materials.get('Plantas', [])
    
    print(f"\nTotal de plantas disponibles: {len(plantas)}")
    print("\nPrimeras 5 plantas y sus tags:")
    
    for i, planta in enumerate(plantas[:5]):
        print(f"\n  {i+1}. {planta['name']} ({planta['rarity']})")
        tags = planta.get('tags', {})
        if tags:
            for tag, valor in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"     • {tag}: {valor}")
        else:
            print("     • Sin tags")


def test_batch_crafting():
    """Test 4: Craftear lotes de pociones."""
    print("\n" + "="*70)
    print("TEST 4: CREACIÓN DE LOTES")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print("\nCreando lote de 5 pociones...")
    batch = alchemy.craft_batch(count=5)
    
    success_count = sum(1 for p in batch if p['success'])
    total_potency = sum(p['potency'] for p in batch)
    
    print(f"\n  Resultados del lote:")
    for i, potion in enumerate(batch):
        status = "✓" if potion['success'] else "✗"
        print(f"  {i+1}. {status} {potion['name']:<40} (Potencia: {potion['potency']})")
    
    print(f"\n  📊 Estadísticas:")
    print(f"     Éxitos: {success_count}/{len(batch)}")
    print(f"     Potencia total: {total_potency}")
    print(f"     Potencia promedio: {total_potency // len(batch)}")


def test_recipe_templates():
    """Test 5: Mostrar todas las recetas disponibles."""
    print("\n" + "="*70)
    print("TEST 5: CATÁLOGO DE RECETAS PROCEDURALES")
    print("="*70)
    
    alchemy = AlchemySystem()
    
    print(f"\nTotal de recetas: {len(alchemy.RECIPE_TEMPLATES)}\n")
    
    for recipe_name, template in sorted(alchemy.RECIPE_TEMPLATES.items()):
        print(f"  📜 {recipe_name}:")
        print(f"     Etiqueta: {template['etiqueta']}")
        print(f"     Requerimientos: {template['tags_requeridos']}")
        print(f"     Efecto: {template['efecto']}")
        print(f"     Estilos: {', '.join(template['descriptores'])}")
        print()


def test_pure_vs_impure():
    """Test 6: Comparar pociones puras vs impuras."""
    print("\n" + "="*70)
    print("TEST 6: PUREZA VS IMPUREZA EN POCIONES")
    print("="*70)
    
    # Cargar materiales
    MATERIALS_PATH = os.path.join(os.path.dirname(__file__), 'systems', 'Materiales.json')
    try:
        with open(MATERIALS_PATH, 'r', encoding='utf-8') as f:
            materials = json.load(f)
    except Exception as e:
        print(f"Error cargando materiales: {e}")
        return
    
    plantas = materials.get('Plantas', [])
    
    # Separar plantas con Pureza alta vs baja
    pure_plants = [p for p in plantas if p.get('tags', {}).get('Pureza', 0) > 15]
    impure_plants = [p for p in plantas if p.get('tags', {}).get('Pureza', 0) <= 5]
    
    print(f"\nPlantas puras disponibles: {len(pure_plants)}")
    print(f"Plantas impuras disponibles: {len(impure_plants)}")
    
    alchemy = AlchemySystem()
    
    if pure_plants and impure_plants:
        print("\n  Creando poción PURA (con ingredientes de alta pureza):")
        pure_potion = alchemy.mix_ingredients(pure_plants[:3])
        print(f"    Nombre: {pure_potion[0]}")
        print(f"    Éxito: {pure_potion[1]}")
        
        print("\n  Creando poción IMPURA (con ingredientes de baja pureza):")
        impure_potion = alchemy.mix_ingredients(impure_plants[:3])
        print(f"    Nombre: {impure_potion[0]}")
        print(f"    Éxito: {impure_potion[1]}")


if __name__ == "__main__":
    print("\n" + "█"*70)
    print("█  SISTEMA DE ALQUIMIA PROCEDURAL - SUITE DE TESTS".center(70))
    print("█"*70)
    
    try:
        test_recipe_templates()
        test_basic_alchemy()
        test_recipe_discovery()
        test_ingredients_analysis()
        test_batch_crafting()
        test_pure_vs_impure()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS COMPLETADOS".center(70))
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LOS TESTS: {e}")
        import traceback
        traceback.print_exc()
