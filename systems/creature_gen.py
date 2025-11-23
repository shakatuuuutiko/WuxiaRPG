import random
from data.beast_db_massive import ROOT_CREATURES, FAMILY_PREFIXES, VARIANTS, ANATOMY

class CreatureGenerator:
    def generate(self, target_rank=1):
        # 1. Construir Nombre
        root = random.choice(ROOT_CREATURES)
        prefix = random.choice(FAMILY_PREFIXES)
        
        if random.random() < 0.6:
            family_name = f"{prefix}{root.lower()}".title()
        else:
            family_name = f"{root} {prefix}"
        
        tier_key = "Baja"
        if target_rank > 3: tier_key = "Media"
        if target_rank > 6: tier_key = "Alta"
        if target_rank > 9: tier_key = "Mítica"
        
        variant = random.choice(VARIANTS[tier_key])
        full_name = f"{family_name} {variant}"
        
        # 2. Elemento y Stats
        element = self._deduce_element(prefix)
        base_stat = 20 + (target_rank * 15)
        final_hp = int(base_stat * 3.0 * random.uniform(0.8, 1.2))
        
        stats = {
            "hp": final_hp, "max_hp": final_hp,
            "atk": int(base_stat * 0.6), "def": int(base_stat * 0.3),
            "qi": target_rank * 100
        }
        
        # 3. LOOT DEFINITIVO: Solo devolvemos el Cadáver
        corpse_item = f"Cadáver de {full_name}"

        return {
            "name": full_name,
            "rank": f"G{target_rank}",
            "element": element,
            "stats": stats,
            "loot": [corpse_item], # <--- ESTO ES EL FIX: SOLO EL CUERPO
            "family_root": root    # Guardamos el root para la lógica de despiece
        }

    # --- LÓGICA DE DESPIECE MANUAL (HARVEST) ---
    def harvest_corpse(self, corpse_name):
        """
        Genera el loot real con abundancia y cantidades al desmantelar el cuerpo.
        Retorna: { Item: Cantidad }
        """
        clean_name = corpse_name.replace("Cadáver de ", "")
        
        # 1. Detección de Categoría y Elemento
        category = self._guess_category(clean_name)
        parts = ANATOMY.get(category, ANATOMY["Mamífero"])
        element = self._deduce_element(clean_name)
        
        # 2. Deducir Rango (para calcular la abundancia)
        rank_mult = 1
        if "Rey" in clean_name or "Alta" in clean_name: rank_mult = 3
        if "Mítica" in clean_name or "Dios" in clean_name: rank_mult = 6
        
        loot_dict = {}

        # 3. Loot ABUNDANTE POR CATEGORÍA
        
        # 3.1. Carne/Material Blando (Garantizado y Abundante)
        # Asumimos que la carne está en la anatomía, si no usamos 'Carne Cruda'
        item = f"Carne Cruda de {clean_name}"
        qty = random.randint(5, 10) * rank_mult
        loot_dict[item] = qty

        # 3.2. Piel/Cubierta (Material de Crafting)
        skin_types = [p for p in parts if p in ["Piel", "Escama", "Caparazón", "Corteza"]]
        if skin_types:
            item = f"{skin_types[0]} de {clean_name}"
            qty = random.randint(1, 2) * rank_mult
            loot_dict[item] = qty

        # 3.3. Partes Duras/Especiales (Aleatorio)
        special_parts = [p for p in parts if p not in ["Carne", "Piel", "Escama", "Caparazón"]]
        if special_parts:
            for _ in range(random.randint(1, 3)):
                part = random.choice(special_parts)
                item = f"{part} de {clean_name}"
                loot_dict[item] = random.randint(1, 2)

        # 3.4. NÚCLEO (Chance 30% + Rango)
        if random.random() < (0.3 + (rank_mult * 0.05)):
            core_name = f"Núcleo de Bestia ({element}) G{rank_mult}"
            loot_dict[core_name] = 1
            
        return loot_dict

    # --- MÉTODOS DE ANÁLISIS (Sintaxis Verificada) ---
    def _guess_category(self, name):
        """Adivina la categoría anatómica basada en el nombre (Sintaxis OK)"""
        n = name.lower()
        if any(x in n for x in ["lobo", "oso", "tigre", "león", "rata", "zorro", "ciervo"]): return "Mamífero"
        if any(x in n for x in ["sierpe", "dragón", "vibora", "lagarto", "reptil"]): return "Reptil"
        if any(x in n for x in ["águila", "ave", "pájaro", "fénix", "cuervo"]): return "Ave"
        if any(x in n for x in ["pez", "tiburón", "ballena", "kraken", "acuático"]): return "Acuático"
        if any(x in n for x in ["araña", "insecto", "escarabajo", "hormiga"]): return "Insecto"
        if any(x in n for x in ["ent", "planta", "hongo", "flor"]): return "Planta"
        if any(x in n for x in ["demonio", "gólem", "sombra", "espectro"]): return "Mítico"
        return "Mamífero"

    def _deduce_element(self, prefix):
        p = prefix.lower()
        if any(x in p for x in ["piro", "magma", "fuego", "solar", "infernal"]): return "Fuego"
        if any(x in p for x in ["crio", "hielo", "hidro", "agua", "mar"]): return "Agua"
        if any(x in p for x in ["electro", "trueno", "rayo"]): return "Rayo"
        if any(x in p for x in ["necro", "sombra", "vacío", "oscuro"]): return "Oscuridad"
        if any(x in p for x in ["ferro", "oro", "acero", "metal"]): return "Metal"
        return "Neutro"