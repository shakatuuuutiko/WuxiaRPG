import random
from data.items_db import ITEMS_DB
# Nota: La clase Soul y ArtifactSpirit deberían estar en systems/artifact_spirit.py
# Aquí asumimos que la clase existe y se importa correctamente.

# --- CONFIGURACIÓN DE MOLDES Y ESTRUCTURAS ---
WEAPON_MOLDS = {
    "Daga":   {"densidad": 1.5, "speed": 1.8},
    "Espada": {"densidad": 1.0, "speed": 1.0},
    "Lanza":  {"densidad": 0.9, "speed": 1.2}
}

BUILDINGS = {
    "Pared": {"char": "■", "cost": {"Madera": 5}},
    "Suelo": {"char": ".", "cost": {"Paja": 2}},
    "Cama":  {"char": "H", "cost": {"Madera": 20}, "effect": "Regen HP"},
    "Horno": {"char": "O", "cost": {"Hierro": 50}, "effect": "Alquimia"}
}

# Sufijos de calidad por rareza
QUALITY_SUFFIXES = {
    "Común": ["Común", "Ordinario"],
    "Raro": ["Raro", "Refinado"],
    "Épico": ["Épico", "Magistral"],
    "Legendario": ["Legendario", "Divino", "Eterno"]
}

# Variable global para orden de rarezas
RARITY_ORDER = {"Común": 0, "Raro": 1, "Épico": 2, "Legendario": 3}

# --- SISTEMA DE ALQUIMIA PROCEDURAL ---
class AlchemySystem:
    """Sistema de alquimia que genera recetas dinámicamente basadas en tags de plantas."""
    
    # Catálogo de recetas procedurales (plantilla)
    RECIPE_TEMPLATES = {
        # Recetas de daño/ofensiva
        'Fuego': {
            'tags_requeridos': {'Fuego': 25},
            'etiqueta': 'Incineración',
            'efecto': 'Daño por Fuego',
            'descriptores': ['Abrasador', 'Ígneo', 'Infernal']
        },
        'Hielo': {
            'tags_requeridos': {'Hielo': 25},
            'etiqueta': 'Congelación',
            'efecto': 'Daño por Hielo',
            'descriptores': ['Glacial', 'Congelante', 'Helado']
        },
        'Veneno': {
            'tags_requeridos': {'Veneno': 20},
            'etiqueta': 'Envenenamiento',
            'efecto': 'Daño por Veneno',
            'descriptores': ['Tóxico', 'Venenoso', 'Mortal']
        },
        'Electricidad': {
            'tags_requeridos': {'Electricidad': 25},
            'etiqueta': 'Electrocución',
            'efecto': 'Daño por Electricidad',
            'descriptores': ['Voltaico', 'Fulminante', 'Chispeante']
        },
        # Recetas de soporte/sanación
        'Vida': {
            'tags_requeridos': {'Vida': 20},
            'etiqueta': 'Regeneración',
            'efecto': 'Restauración de Salud',
            'descriptores': ['Vital', 'Curativa', 'Sanadora']
        },
        'Defensa': {
            'tags_requeridos': {'Defensa': 20},
            'etiqueta': 'Protección',
            'efecto': 'Aumento de Defensa',
            'descriptores': ['Protectora', 'Defensiva', 'Blindaje']
        },
        'Velocidad': {
            'tags_requeridos': {'Velocidad': 20},
            'etiqueta': 'Aceleración',
            'efecto': 'Aumento de Velocidad',
            'descriptores': ['Veloz', 'Rápida', 'Fugaz']
        },
        'Sabiduría': {
            'tags_requeridos': {'Sabiduría': 20},
            'etiqueta': 'Iluminación',
            'efecto': 'Aumento de Mana/Energía',
            'descriptores': ['Mística', 'Sagrada', 'Iluminada']
        },
        # Recetas complejas (combinaciones)
        'Yang': {
            'tags_requeridos': {'Fuego': 20, 'Estabilidad': 15},
            'etiqueta': 'Energía Yang',
            'efecto': 'Poder Ofensivo Aumentado',
            'descriptores': ['Yang', 'Ardiente', 'Expansiva']
        },
        'Yin': {
            'tags_requeridos': {'Hielo': 20, 'Agua': 15},
            'etiqueta': 'Energía Yin',
            'efecto': 'Defensa y Regeneración',
            'descriptores': ['Yin', 'Lunar', 'Tranquila']
        },
        'Sangre': {
            'tags_requeridos': {'Sangre': 20},
            'etiqueta': 'Vitalidad Salvaje',
            'efecto': 'Daño Crítico Aumentado',
            'descriptores': ['Sangrienta', 'Salvaje', 'Feroz']
        },
    }

    def _analyze_ingredients(self, ingredient_entries):
        """Analiza ingredientes y retorna tags totales, impureza, rareza."""
        total_tags = {}
        total_impurity = 0
        
        for item in ingredients:
            data = ITEMS_DB.get(item, {}).get("tags", {})
            for k, v in data.items():
                total_tags[k] = total_tags.get(k, 0) + v

            # Calcular impureza (falta de Pureza)
            if 'Pureza' not in tags:
                total_impurity += 10
            else:
                total_impurity -= item.get('tags', {}).get('Pureza', 0) // 5

            rarity_list.append(item.get('rarity', 'Común'))

        total_impurity = max(0, total_impurity)
        return total_tags, total_impurity, rarity_list, ingredient_names

    def _get_best_recipe(self, total_tags):
        """Encuentra la mejor receta que encaja con los tags disponibles.
        
        Retorna (nombre_receta, template_dict) si encuentra, sino (None, None)
        """
        best_match = None
        best_score = 0

        for recipe_name, template in self.RECIPE_TEMPLATES.items():
            required = template['tags_requeridos']
            score = 0

            # Calcular score: suma de tags que cumplen el requisito
            match = True
            for tag, min_value in required.items():
                if total_tags.get(tag, 0) >= min_value:
                    score += total_tags.get(tag, 0)
                else:
                    match = False
                    break

            if match and score > best_score:
                best_score = score
                best_match = (recipe_name, template)

        return best_match if best_match else (None, None)

    def _generate_potion_name(self, recipe_name, template, total_impurity, total_tags):
        """Genera nombre dinámico para la poción basado en template y tags."""
        descriptor = random.choice(template['descriptores'])
        etiqueta = template['etiqueta']
        
        # Modificar nombre según pureza
        if total_impurity > 40:
            quality = "Impura"
        elif total_impurity > 20:
            quality = "Tosca"
        else:
            quality = "Pura"

        # Nombre procedural
        potion_name = f"Píldora de {etiqueta} {quality} ({descriptor})"
        return potion_name

    def mix_ingredients(self, ingredient_entries):
        """Suma los tags de una lista de plantas y genera receta proceduralmente.

        ingredient_entries: list de material dicts (de Materials['Plantas']).
        Devuelve (resultado_nombre, success_bool, efecto, potencia).
        """
        if not ingredient_entries:
            return "Sin ingredientes", False, "Nada", 0

        total_tags, total_impurity, rarity_list, ingredient_names = self._analyze_ingredients(ingredient_entries)

        # Buscar mejor receta que encaje
        recipe_name, template = self._get_best_recipe(total_tags)

        if recipe_name:
            # Éxito: generar nombre dinámico
            potion_name = self._generate_potion_name(recipe_name, template, total_impurity, total_tags)
            
            # Calcular potencia
            potency = sum(total_tags.values()) // len(total_tags) if total_tags else 10
            
            # Chance de fallo por impureza
            success = random.random() > (total_impurity / 200.0)
            
            return potion_name, success, template['efecto'], potency
        else:
            # No hay receta: polvo genérico o tóxico
            if total_impurity > 50 or random.random() < 0.15:
                return "Escoria Tóxica", False, "Daño al usuario", 5
            
        return "Polvo Medicinal Genérico", True

# --- SISTEMA DE FORJA (Densidad) ---
class ForgeSystem:
    def forge_weapon(self, metal_name, core_name, mold_type):
        metal = ITEMS_DB.get(metal_name, {})
        mold = WEAPON_MOLDS.get(mold_type, WEAPON_MOLDS["Espada"])
        
        # Stats base por densidad
        base_atk = metal.get("stats_forja", {}).get("dureza", 10) * mold["densidad"]
        
        # Bonus por Núcleo (Simulado)
        elem_dmg = 0
        if core_name: elem_dmg = 20 
        
        # Factor Caos
        quality = random.uniform(0.9, 1.2)
        final_atk = int((base_atk + elem_dmg) * quality)
        
        name = f"{mold_type} de {metal_name.split(' ')[0]}"
        if final_atk > 50: name = f"{name} Divina"
        
        return {"name": name, "type": "Arma", "atk": final_atk}

# --- SISTEMA DE CONSTRUCCIÓN DE CASAS (Housing) ---
class HouseSystem:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.resources = {"Madera": 100, "Roca": 100, "Paja": 100}

    def build(self, x, y, structure):
        data = BUILDINGS.get(structure)
        if not data:
            return False, f"Estructura desconocida: {structure}"
        
        cost = data.get("cost", {})
        
        # Verificar recursos
        for res, qty in cost.items():
            if self.resources.get(res, 0) < qty:
                return False, f"Falta {res}. Necesitas {qty}, tienes {self.resources.get(res, 0)}."
        
        # Consumir recursos
        for res, qty in cost.items():
            self.resources[res] -= qty
            
        self.grid[y][x] = structure
        return True, f"Construido: {structure}"

    def get_resources(self):
        return self.resources.copy()



# --- MAIN DE PRUEBA ---
if __name__ == '__main__':
    print("=" * 80)
    print("SISTEMA DE CRAFTING AVANZADO - WuxiaRPG")
    print("=" * 80)
    
    # ===== PRUEBA DE FORJA DE ARMAS CON PREFIJOS =====
    print("\n" + "─" * 80)
    print("FORJA DE ARMAS (Con Sistema de Prefijos)")
    print("─" * 80)
    
    forge = ForgeSystem()
    
    # Arma individual con prefijo aleatorio
    print("\n>>> Arma Forjada Aleatorias:")
    weapon1 = forge.forge_weapon("Sable")
    print(f"  Nombre: {weapon1.get('name')}")
    print(f"  Ataque: {weapon1.get('atk')} | Velocidad: {weapon1.get('speed')}")
    print(f"  Prefijo: {weapon1.get('prefix')} | Efecto: {weapon1.get('special_effect')}")
    print(f"  Componentes: Madera={weapon1.get('components')['madera']}, "
          f"Mineral={weapon1.get('components')['mineral']}")
    
    # Arma con prefijo específico
    print("\n>>> Arma con Prefijo Específico (Brutal):")
    weapon2 = forge.forge_weapon("Claymore", prefix="Brutal")
    print(f"  Nombre: {weapon2.get('name')}")
    print(f"  Ataque: {weapon2.get('atk')} | Velocidad: {weapon2.get('speed')}")
    print(f"  Prefijo: {weapon2.get('prefix')} | Efecto: {weapon2.get('special_effect')}")
    
    # Lote de armas variadas
    print("\n>>> Lote de Arcos (diferentes prefijos):")
    bows = forge.forge_batch("Arco", count=3)
    for i, bow in enumerate(bows, 1):
        print(f"  {i}. {bow['name']}")
        print(f"     ATK: {bow['atk']} | SPD: {bow['speed']} | Efecto: {bow['special_effect']}")
    
    # ===== PRUEBA DE HERRAMIENTAS =====
    print("\n" + "─" * 80)
    print("CRAFTEO DE HERRAMIENTAS (Con Sistema de Sufijos)")
    print("─" * 80)
    
    tools = ToolSystem()
    
    print("\n>>> Herramientas Artesanales:")
    for tool_type in ["Pico", "Hacha", "Azada", "Hoz"]:
        tool = tools.craft_tool(tool_type)
        print(f"  {tool['name']}")
        print(f"    Potencia: {tool['power']} | Durabilidad: {tool['durability']} | Sufijo: {tool['suffix']}")
    
    # Lote de picos
    print("\n>>> Lote de Picos para Minería:")
    picos = tools.craft_batch("Pico", count=3)
    for i, pico in enumerate(picos, 1):
        print(f"  {i}. {pico['name']} - Potencia: {pico['power']}, Durabilidad: {pico['durability']}")
    
    # ===== PRUEBA DE ARMADURAS =====
    print("\n" + "─" * 80)
    print("FORJA DE ARMADURAS (Con Sistema de Prefijos)")
    print("─" * 80)
    
    armor = ArmorSystem()
    
    print("\n>>> Piezas de Armadura Individuales:")
    for part in ["Casco", "Pechera", "Guantes", "Botas"]:
        piece = armor.forge_armor(part)
        print(f"  {piece['name']}")
        print(f"    Defensa: {piece['defense']} | Peso: {piece['weight']} | Efecto: {piece['special_effect']}")
    
    # Conjunto completo con prefijo específico
    print("\n>>> Conjunto Completo de Armadura (Bendito):")
    full_set = armor.forge_full_set(prefix="Bendito")
    total_def = 0
    for piece in full_set:
        print(f"  ✓ {piece['name']} - Defensa: {piece['defense']}")
        total_def += piece['defense']
    print(f"  >>> DEFENSA TOTAL DEL CONJUNTO: {total_def}")
    
    # ===== COMPARATIVA DE ARMAS (15 NUEVAS) =====
    print("\n" + "─" * 80)
    print("COMPARATIVA DE TODAS LAS ARMAS DISPONIBLES (22 total)")
    print("─" * 80)
    
    print("\nArmas Originales (7):")
    original_weapons = ["Daga", "Espada", "Lanza", "Sable", "Arco", "Hacha", "Pico"]
    for weapon_name in original_weapons:
        w = forge.forge_weapon(weapon_name)
        print(f"  • {weapon_name:15} ATK: {w['atk']:3} SPD: {w['speed']:.2f}")
    
    print("\nArmas Nuevas (15):")
    new_weapons = ["Catana", "Falcata", "Claymore", "Tridente", "Martillo", "Maza", 
                   "Mangual", "Guadaña", "Espada Ancha", "Bastón", "Garras", "Horca", 
                   "Espada Corta", "Alabarda"]
    for weapon_name in new_weapons:
        w = forge.forge_weapon(weapon_name)
        print(f"  • {weapon_name:15} ATK: {w['atk']:3} SPD: {w['speed']:.2f}")
    
    # ===== PRUEBA DE ALQUIMIA =====
    print("\n" + "─" * 80)
    print("MEZCLA ALQUÍMICA")
    print("─" * 80)
    
    alchemy = AlchemySystem()
    print("\n>>> Pociones Creadas:")
    potions = alchemy.craft_batch(count=3)
    for i, potion in enumerate(potions, 1):
        status = "✓ ÉXITO" if potion['success'] else "✗ FALLO"
        print(f"  {i}. {potion['name']} [{status}]")
        print(f"     Efecto: {potion['effect']} | Potencia: {potion['potency']}")
        print(f"     Ingredientes: {', '.join(potion['ingredients'])}")
    
    # ===== ESTADÍSTICAS DEL SISTEMA =====
    print("\n" + "═" * 80)
    print("ESTADÍSTICAS DEL SISTEMA DE CRAFTING")
    print("═" * 80)
    
    print(f"\n✓ Armas disponibles: {len(WEAPON_MOLDS)} (7 originales + 15 nuevas)")
    print(f"✓ Herramientas disponibles: {len(TOOL_MOLDS)}")
    print(f"✓ Partes de armadura disponibles: {len(ARMOR_PARTS)}")
    print(f"✓ Prefijos para armas/armaduras: {len(WEAPON_PREFIXES)}")
    print(f"✓ Sufijos para herramientas: {len(TOOL_SUFFIXES)}")
    print(f"✓ Recetas alquímicas: {len(AlchemySystem.RECIPE_TEMPLATES)}")
    
    print("\n" + "═" * 80)
