import random
import json
import os

# Cargar materiales generados por systems/resource_gen_v2.py
MATERIALS_PATH = os.path.join(os.path.dirname(__file__), 'Materiales.json')
try:
    with open(MATERIALS_PATH, 'r', encoding='utf-8') as _f:
        Materials = json.load(_f)
except Exception:
    Materials = {"Maderas": [], "Minerales": [], "Plantas": []}

# --- CONFIGURACIÓN DE MOLDES Y ESTRUCTURAS ---
WEAPON_MOLDS = {
    # Armas originales
    "Daga":         {"densidad": 1.5, "speed": 1.8, "atk_base": 25},
    "Espada":       {"densidad": 1.1, "speed": 1.0, "atk_base": 35},
    "Lanza":        {"densidad": 0.9, "speed": 1.2, "atk_base": 32},
    "Sable":        {"densidad": 1.0, "speed": 1.3, "atk_base": 30},
    "Arco":         {"densidad": 0.7, "speed": 1.5, "atk_base": 28},
    "Hacha":        {"densidad": 1.6, "speed": 0.9, "atk_base": 40},
    "Pico":         {"densidad": 1.8, "speed": 0.8, "atk_base": 38},
    # Nuevas armas (15 adicionales)
    "Catana":       {"densidad": 1.05, "speed": 1.4, "atk_base": 36},
    "Falcata":      {"densidad": 1.2, "speed": 1.1, "atk_base": 38},
    "Claymore":     {"densidad": 1.3, "speed": 0.85, "atk_base": 45},
    "Tridente":     {"densidad": 1.15, "speed": 1.25, "atk_base": 35},
    "Martillo":     {"densidad": 1.7, "speed": 0.7, "atk_base": 42},
    "Maza":         {"densidad": 1.55, "speed": 0.75, "atk_base": 39},
    "Mangual":      {"densidad": 1.4, "speed": 0.95, "atk_base": 41},
    "Guadaña":      {"densidad": 0.95, "speed": 1.3, "atk_base": 37},
    "Espada Ancha": {"densidad": 1.25, "speed": 0.95, "atk_base": 43},
    "Bastón":       {"densidad": 0.8, "speed": 1.6, "atk_base": 26},
    "Garras":       {"densidad": 1.2, "speed": 1.7, "atk_base": 28},
    "Horca":        {"densidad": 1.0, "speed": 1.15, "atk_base": 31},
    "Espada Corta": {"densidad": 1.1, "speed": 1.35, "atk_base": 27},
    "Alabarda":     {"densidad": 1.05, "speed": 1.1, "atk_base": 40}
}

# Sistema de herramientas
TOOL_MOLDS = {
    "Pico":        {"dureza_mod": 1.8, "speed": 0.8, "mining_power": 40},
    "Hacha":       {"dureza_mod": 1.6, "speed": 0.9, "chopping_power": 38},
    "Pala":        {"dureza_mod": 1.4, "speed": 1.0, "digging_power": 35},
    "Azada":       {"dureza_mod": 1.3, "speed": 1.1, "tilling_power": 32},
    "Hoz":         {"dureza_mod": 1.0, "speed": 1.5, "harvesting_power": 28},
    "Cuchillo":    {"dureza_mod": 0.9, "speed": 1.6, "cutting_power": 22},
    "Sierra":      {"dureza_mod": 1.45, "speed": 0.85, "sawing_power": 36}
}

# Sistema de armaduras (por parte del cuerpo)
ARMOR_PARTS = {
    "Casco":       {"def_base": 15, "weight": 8, "slots": 1},
    "Pechera":     {"def_base": 25, "weight": 15, "slots": 2},
    "Guantes":     {"def_base": 10, "weight": 4, "slots": 1},
    "Cintura":     {"def_base": 12, "weight": 5, "slots": 1},
    "Grebas":      {"def_base": 18, "weight": 10, "slots": 1},
    "Botas":       {"def_base": 8, "weight": 3, "slots": 1},
    "Escudo":      {"def_base": 20, "weight": 12, "slots": 1},
    "Cota de Malla":{"def_base": 22, "weight": 18, "slots": 2}
}

# Prefijos para armas y armaduras (modifican stats base)
WEAPON_PREFIXES = {
    "Fantasmal":    {"atk_mult": 0.95, "speed_mult": 1.15, "special": "Ignore Armor"},
    "Brutal":       {"atk_mult": 1.25, "speed_mult": 0.85, "special": "Bleed"},
    "Ágil":         {"atk_mult": 0.90, "speed_mult": 1.25, "special": "Extra Hit"},
    "Fiero":        {"atk_mult": 1.30, "speed_mult": 0.80, "special": "Crush"},
    "Maldito":      {"atk_mult": 1.10, "speed_mult": 0.95, "special": "Drain HP"},
    "Bendito":      {"atk_mult": 1.05, "speed_mult": 1.05, "special": "Heal on Hit"},
    "Glacial":      {"atk_mult": 1.00, "speed_mult": 1.10, "special": "Slow Enemy"},
    "Ígneo":        {"atk_mult": 1.15, "speed_mult": 0.95, "special": "Burn Damage"},
    "Venenoso":     {"atk_mult": 0.95, "speed_mult": 1.05, "special": "Poison"},
    "Eléctrico":    {"atk_mult": 1.05, "speed_mult": 1.20, "special": "Stun"},
}

# Sufijos para herramientas (modifican efectividad)
TOOL_SUFFIXES = {
    "Refinada":     {"power_mult": 1.10, "durability_mult": 0.95},
    "Robusta":      {"power_mult": 0.95, "durability_mult": 1.15},
    "Maestra":      {"power_mult": 1.20, "durability_mult": 1.05},
    "Perdurable":   {"power_mult": 0.90, "durability_mult": 1.25},
    "Experta":      {"power_mult": 1.15, "durability_mult": 1.00},
    "Imbuida":      {"power_mult": 1.25, "durability_mult": 0.90},
    "Afilada":      {"power_mult": 1.18, "durability_mult": 0.92},
    "Templada":     {"power_mult": 1.05, "durability_mult": 1.10}
}

# Sufijos de material (modifican defensa en armaduras)
MATERIAL_SUFFIXES = {
    "Común": ["Común", "Ordinaria", "Básica"],
    "Raro": ["Rara", "Refinada", "Bien Hecha"],
    "Épico": ["Épica", "Magistral", "Excelente"],
    "Legendario": ["Legendaria", "Divina", "Celestial"]
}

# Variable global para orden de rarezas
RARITY_ORDER = {"Común": 0, "Raro": 1, "Épico": 2, "Legendario": 3}

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
        rarity_list = []
        ingredient_names = []

        for item in ingredient_entries:
            tags = item.get('tags', {})
            ingredient_names.append(item.get('name', 'Desconocida'))
            
            for k, v in tags.items():
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
            
            # Crear nombre genérico
            main_tag = max(total_tags.items(), key=lambda x: x[1])[0] if total_tags else "Medicinal"
            generic_name = f"Polvo de {main_tag} Común"
            potency = sum(total_tags.values()) // max(len(total_tags), 1) if total_tags else 5
            
            return generic_name, True, "Efecto Menor", potency

    def get_random_plant(self):
        """Obtiene una planta aleatoria de los materiales."""
        if Materials.get('Plantas'):
            return random.choice(Materials['Plantas'])
        return None

    def craft_potion(self, count=3):
        """Crea una poción usando N plantas aleatorias.
        
        count: número de ingredientes a mezclar (default 3).
        Retorna dict con nombre, éxito, efecto, potencia e ingredientes usados.
        """
        ingredients = [self.get_random_plant() for _ in range(count)]
        ingredients = [i for i in ingredients if i is not None]
        
        if not ingredients:
            return {
                'name': 'Fallo total - sin ingredientes',
                'success': False,
                'effect': 'Nada',
                'potency': 0,
                'ingredients': []
            }

        potion_name, success, effect, potency = self.mix_ingredients(ingredients)
        
        return {
            'name': potion_name,
            'success': success,
            'effect': effect,
            'potency': potency,
            'ingredients': [i.get('name', 'Desconocida') for i in ingredients],
            'ingredient_count': len(ingredients)
        }
    
    def craft_batch(self, count=5):
        """Crea un lote de pociones.
        
        count: número de pociones a crear.
        Retorna lista de dicts de pociones.
        """
        return [self.craft_potion(random.randint(2, 4)) for _ in range(count)]
    
    def discover_recipe(self, tag_name, min_value=20):
        """Descubre una receta basada en un tag específico.
        
        Usado para gameplay: permitir al jugador buscar recetas específicas.
        """
        compatible_recipes = []
        
        for recipe_name, template in self.RECIPE_TEMPLATES.items():
            required = template['tags_requeridos']
            if tag_name in required and required[tag_name] <= min_value:
                compatible_recipes.append((recipe_name, template))
        
        if compatible_recipes:
            recipe_name, template = random.choice(compatible_recipes)
            return {
                'recipe_name': recipe_name,
                'tags_needed': template['tags_requeridos'],
                'effect': template['efecto'],
                'descriptors': template['descriptores']
            }
        
        return None

# --- SISTEMA DE FORJA DINÁMICO CON PREFIJOS Y SUFIJOS ---
class ForgeSystem:
    def _get_descriptive_name(self, material_entry):
        """Extrae un descriptor legible del nombre del material."""
        name = material_entry.get('name', '')
        rarity = material_entry.get('rarity', 'Común')
        
        # Buscar palabras descriptivas en el nombre
        descriptive_words = {
            'Espiritual', 'Eterno', 'Fénix', 'Negro', 'Estelar', 'Divino', 
            'Milenario', 'Sagrado', 'Universal', 'Sangre', 'Inmortal', 'Galáctico',
            'del Vacío', 'Primordial', 'Blanco', 'Venenoso', 'Fosforescente'
        }
        
        parts = name.split()
        for p in parts:
            if p in descriptive_words:
                return p
        
        # Si no hay descripción especial, devolver el primer sustantivo
        return parts[0] if parts else rarity

    def _get_weapon_prefix(self):
        """Selecciona un prefijo aleatorio para armas."""
        return random.choice(list(WEAPON_PREFIXES.items()))

    def _build_weapon_name(self, prefix_name, mold_type, wood_entry, mineral_entry):
        """Construye nombre dinámico: Prefijo + Molde + Descriptor Madera + 'de' + Mineral."""
        wood_desc = self._get_descriptive_name(wood_entry) if wood_entry else "Madera"
        mineral_name = mineral_entry.get('name', 'Metal') if mineral_entry else 'Metal'
        
        name = f"{prefix_name} {mold_type} {wood_desc} de {mineral_name}"
        return name

    def _get_quality_suffix(self, wood_rarity, mineral_rarity):
        """Retorna un sufijo de calidad basado en las rarezas."""
        rarities = [wood_rarity, mineral_rarity]
        
        # Determinar la rareza más alta
        max_rarity = max(rarities, key=lambda r: RARITY_ORDER.get(r, 0))
        
        suffixes = MATERIAL_SUFFIXES.get(max_rarity, ["Ordinaria"])
        return random.choice(suffixes)

    def get_random_wood(self):
        """Obtiene una madera aleatoria."""
        if Materials.get('Maderas'):
            return random.choice(Materials['Maderas'])
        return None

    def get_random_mineral(self):
        """Obtiene un mineral aleatorio."""
        if Materials.get('Minerales'):
            return random.choice(Materials['Minerales'])
        return None

    def forge_weapon(self, mold_type, wood_entry=None, mineral_entry=None, core_entry=None, prefix=None):
        """Forja un arma con sistema de prefijos.

        - `mold_type`: clave en `WEAPON_MOLDS` (ej. 'Sable', 'Arco')
        - `wood_entry`, `mineral_entry`: dicts de `Materials['Maderas']` y `Materials['Minerales']`.
        - `core_entry`: opcional, aporta bonificación elemental
        - `prefix`: opcional, prefijo específico; si None, selecciona uno aleatorio
        
        Retorna diccionario con nombre dinámico, daño, velocidad, efectos especiales y componentes.
        """
        # Si no se pasan materiales, elegir aleatorios
        if wood_entry is None:
            wood_entry = self.get_random_wood()
        if mineral_entry is None:
            mineral_entry = self.get_random_mineral()

        if wood_entry is None or mineral_entry is None:
            return {'name': 'Error: No hay materiales', 'atk': 0, 'error': True}

        mold = WEAPON_MOLDS.get(mold_type, WEAPON_MOLDS['Espada'])

        # Seleccionar prefijo
        if prefix is None:
            prefix_name, prefix_stats = self._get_weapon_prefix()
        else:
            prefix_name = prefix
            prefix_stats = WEAPON_PREFIXES.get(prefix, WEAPON_PREFIXES['Brutal'])

        # Obtener estadísticas de los materiales
        wood_stats = wood_entry.get('stats_forja', {}) or {}
        mineral_stats = mineral_entry.get('stats_forja', {}) or {}
        
        wood_dureza = wood_stats.get('dureza', 10)
        wood_peso = wood_stats.get('peso', 5)
        mineral_dureza = mineral_stats.get('dureza', 30)
        mineral_peso = mineral_stats.get('peso', 20)

        # Calcular daño base combinando dureza y peso
        # El mineral aporta más fuerza (~70%), la madera equilibrio (~30%)
        base_damage = mineral_dureza * 0.7 + wood_dureza * 0.3
        
        # Aplicar multiplicador del molde
        density = mold.get('densidad', 1.0)
        base_atk = mold.get('atk_base', 30)
        
        # Penalización/beneficio por peso promedio
        avg_peso = (wood_peso + mineral_peso) / 2.0
        peso_factor = max(0.85, 1.1 - (avg_peso / 100.0))
        
        # Bonificación del núcleo si existe
        core_bonus = 0
        if core_entry:
            core_bonus = int(core_entry.get('potency', 0) * 0.1)
        
        # Factor de calidad (variabilidad en la forja)
        quality_factor = random.uniform(0.95, 1.25)
        
        # Aplicar multiplicadores del prefijo
        atk_mult = prefix_stats.get('atk_mult', 1.0)
        speed_mult = prefix_stats.get('speed_mult', 1.0)
        
        final_atk = int((base_atk + base_damage * density + core_bonus) * peso_factor * quality_factor * atk_mult)
        final_speed = mold.get('speed', 1.0) * speed_mult

        # Construir nombre dinámico
        base_name = self._build_weapon_name(prefix_name, mold_type, wood_entry, mineral_entry)
        
        # Añadir sufijo de calidad
        wood_rarity = wood_entry.get('rarity', 'Común')
        mineral_rarity = mineral_entry.get('rarity', 'Común')
        quality_suffix = self._get_quality_suffix(wood_rarity, mineral_rarity)
        
        final_name = f"{base_name} ({quality_suffix})"

        result = {
            'name': final_name,
            'type': 'Arma',
            'mold': mold_type,
            'prefix': prefix_name,
            'atk': final_atk,
            'speed': round(final_speed, 2),
            'special_effect': prefix_stats.get('special', 'Normal'),
            'components': {
                'madera': wood_entry.get('name'),
                'mineral': mineral_entry.get('name'),
                'core': core_entry.get('name') if core_entry else None
            },
            'rarities': {
                'wood': wood_rarity,
                'mineral': mineral_rarity,
                'overall': wood_rarity if RARITY_ORDER.get(wood_rarity, 0) >= RARITY_ORDER.get(mineral_rarity, 0) else mineral_rarity
            }
        }

        return result

    def forge_batch(self, mold_type, count=5):
        """Forja múltiples armas del mismo molde usando materiales aleatorios."""
        results = []
        for _ in range(count):
            weapon = self.forge_weapon(mold_type)
            results.append(weapon)
        return results

# --- SISTEMA DE HERRAMIENTAS ---
class ToolSystem:
    def _get_tool_suffix(self):
        """Selecciona un sufijo aleatorio para herramientas."""
        return random.choice(list(TOOL_SUFFIXES.items()))

    def _get_descriptive_name(self, material_entry):
        """Extrae descriptor del material."""
        name = material_entry.get('name', '')
        parts = name.split()
        return parts[0] if parts else material_entry.get('rarity', 'Común')

    def _build_tool_name(self, tool_type, suffix_name, material_entry):
        """Construye nombre dinámico: Tipo + Descriptor Material + Sufijo."""
        mat_desc = self._get_descriptive_name(material_entry) if material_entry else "Básica"
        name = f"{tool_type} {mat_desc} {suffix_name}"
        return name

    def get_random_wood(self):
        """Obtiene una madera aleatoria."""
        if Materials.get('Maderas'):
            return random.choice(Materials['Maderas'])
        return None

    def get_random_mineral(self):
        """Obtiene un mineral aleatorio."""
        if Materials.get('Minerales'):
            return random.choice(Materials['Minerales'])
        return None

    def craft_tool(self, tool_type, wood_entry=None, mineral_entry=None, suffix=None):
        """Crea una herramienta con sistema de sufijos.

        - `tool_type`: clave en `TOOL_MOLDS` (ej. 'Pico', 'Hacha')
        - `wood_entry`, `mineral_entry`: materiales opcionales
        - `suffix`: sufijo específico; si None, selecciona uno aleatorio
        
        Retorna diccionario con nombre, potencia, durabilidad y componentes.
        """
        if tool_type not in TOOL_MOLDS:
            return {'name': 'Error: Herramienta desconocida', 'error': True}

        if wood_entry is None:
            wood_entry = self.get_random_wood()
        if mineral_entry is None:
            mineral_entry = self.get_random_mineral()

        if wood_entry is None or mineral_entry is None:
            return {'name': 'Error: No hay materiales', 'error': True}

        tool_spec = TOOL_MOLDS[tool_type]

        # Seleccionar sufijo
        if suffix is None:
            suffix_name, suffix_stats = self._get_tool_suffix()
        else:
            suffix_name = suffix
            suffix_stats = TOOL_SUFFIXES.get(suffix, TOOL_SUFFIXES['Refinada'])

        # Obtener estadísticas
        wood_stats = wood_entry.get('stats_forja', {}) or {}
        mineral_stats = mineral_entry.get('stats_forja', {}) or {}
        
        wood_dureza = wood_stats.get('dureza', 10)
        mineral_dureza = mineral_stats.get('dureza', 30)

        # Calcular potencia
        dureza_combined = mineral_dureza * 0.6 + wood_dureza * 0.4
        base_power = 25

        # Buscar el atributo de poder específico del tipo de herramienta
        for key in ['mining_power', 'chopping_power', 'digging_power', 'tilling_power', 
                   'harvesting_power', 'cutting_power', 'sawing_power']:
            if key in tool_spec:
                base_power = tool_spec[key]
                break

        power_mult = suffix_stats.get('power_mult', 1.0)
        durability_mult = suffix_stats.get('durability_mult', 1.0)

        final_power = int((base_power + dureza_combined) * power_mult)
        durability = int(100 * durability_mult)

        # Construir nombre
        base_name = self._build_tool_name(tool_type, suffix_name, wood_entry)
        
        rarity = max(
            [wood_entry.get('rarity', 'Común'), mineral_entry.get('rarity', 'Común')],
            key=lambda r: RARITY_ORDER.get(r, 0)
        )
        quality = MATERIAL_SUFFIXES.get(rarity, ["Ordinaria"])[0]
        
        final_name = f"{base_name} ({quality})"

        result = {
            'name': final_name,
            'type': 'Herramienta',
            'tool_type': tool_type,
            'suffix': suffix_name,
            'power': final_power,
            'durability': durability,
            'components': {
                'wood': wood_entry.get('name'),
                'mineral': mineral_entry.get('name')
            },
            'rarity': rarity
        }

        return result

    def craft_batch(self, tool_type, count=5):
        """Crea un lote de herramientas."""
        results = []
        for _ in range(count):
            tool = self.craft_tool(tool_type)
            results.append(tool)
        return results

# --- SISTEMA DE ARMADURAS ---
class ArmorSystem:
    def _get_armor_prefix(self):
        """Selecciona un prefijo para armaduras (basado en armas)."""
        return random.choice(list(WEAPON_PREFIXES.items()))

    def _get_descriptive_name(self, material_entry):
        """Extrae descriptor del material."""
        name = material_entry.get('name', '')
        parts = name.split()
        return parts[0] if parts else material_entry.get('rarity', 'Común')

    def _build_armor_name(self, armor_part, prefix_name, material_entry):
        """Construye nombre dinámico: Prefijo + Parte + Descriptor Material."""
        mat_desc = self._get_descriptive_name(material_entry) if material_entry else "Básica"
        name = f"{prefix_name} {armor_part} de {mat_desc}"
        return name

    def get_random_mineral(self):
        """Obtiene un mineral aleatorio."""
        if Materials.get('Minerales'):
            return random.choice(Materials['Minerales'])
        return None

    def forge_armor(self, armor_part, mineral_entry=None, prefix=None):
        """Forja una pieza de armadura con sistema de prefijos.

        - `armor_part`: clave en `ARMOR_PARTS` (ej. 'Casco', 'Pechera')
        - `mineral_entry`: material para la armadura
        - `prefix`: prefijo específico; si None, selecciona uno aleatorio
        
        Retorna diccionario con nombre, defensa, peso y componentes.
        """
        if armor_part not in ARMOR_PARTS:
            return {'name': 'Error: Armadura desconocida', 'error': True}

        if mineral_entry is None:
            mineral_entry = self.get_random_mineral()

        if mineral_entry is None:
            return {'name': 'Error: No hay minerales', 'error': True}

        armor_spec = ARMOR_PARTS[armor_part]

        # Seleccionar prefijo
        if prefix is None:
            prefix_name, prefix_stats = self._get_armor_prefix()
        else:
            prefix_name = prefix
            prefix_stats = WEAPON_PREFIXES.get(prefix, WEAPON_PREFIXES['Brutal'])

        # Obtener estadísticas del material
        mineral_stats = mineral_entry.get('stats_forja', {}) or {}
        mineral_dureza = mineral_stats.get('dureza', 30)

        # Calcular defensa
        base_def = armor_spec.get('def_base', 15)
        def_mult = prefix_stats.get('atk_mult', 1.0)  # Reutilizar como mult de defensa
        
        quality_factor = random.uniform(0.95, 1.15)
        final_def = int((base_def + mineral_dureza * 0.4) * def_mult * quality_factor)

        # Construir nombre
        base_name = self._build_armor_name(armor_part, prefix_name, mineral_entry)
        
        rarity = mineral_entry.get('rarity', 'Común')
        quality_suffix = random.choice(MATERIAL_SUFFIXES.get(rarity, ["Ordinaria"]))
        
        final_name = f"{base_name} ({quality_suffix})"

        result = {
            'name': final_name,
            'type': 'Armadura',
            'part': armor_part,
            'prefix': prefix_name,
            'defense': final_def,
            'weight': armor_spec.get('weight', 10),
            'slots': armor_spec.get('slots', 1),
            'special_effect': prefix_stats.get('special', 'Normal'),
            'component': mineral_entry.get('name'),
            'rarity': rarity
        }

        return result

    def forge_full_set(self, prefix=None):
        """Forja un conjunto completo de armadura (todas las partes)."""
        armor_set = []
        for armor_part in ARMOR_PARTS.keys():
            piece = self.forge_armor(armor_part, prefix=prefix)
            armor_set.append(piece)
        return armor_set

    def forge_batch(self, armor_part, count=5):
        """Crea múltiples piezas del mismo tipo de armadura."""
        results = []
        for _ in range(count):
            armor = self.forge_armor(armor_part)
            results.append(armor)
        return results


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
