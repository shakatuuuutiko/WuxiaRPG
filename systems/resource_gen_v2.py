import random

# Base de datos de recursos por categoría y rareza
RESOURCES_DB = {
    "Madera": {
        "Común": ["Roble", "Pino", "Rama"],
        "Raro": ["Madera de Hierro", "Bambú Espiritual"],
        "Épico": ["Madera de Fénix", "Raíz del Árbol Mundo"]
    },
    "Mineral": {
        "Común": ["Roca", "Cobre", "Hierro"],
        "Raro": ["Plata", "Oro", "Jade", "Hierro Negro"],
        "Épico": ["Adamantita", "Mithril", "Plata Estelar"]
    },
    "Planta": {
        "Común": ["Hierba Medicinal", "Flor Silvestre", "Hongo Marrón"],
        "Raro": ["Ginseng de 100 años", "Loto de Nieve", "Hongo Espiritual"],
        "Épico": ["Ginseng de Sangre", "Fruto de la Inmortalidad"]
    }
}

SUFFIX_TIERS = {
    "Mortal": {"range": (1, 3), "suffixes": ["Común", "Seco", "Simple"], "origin": "Mundo Mortal"},
    "Espiritual": {"range": (4, 6), "suffixes": ["de Jade", "Luminoso", "Rúnico"], "origin": "Reino Espiritual"},
    "Inmortal": {"range": (7, 9), "suffixes": ["Divino", "Volador", "Sagrado"], "origin": "Reino Inmortal"},
    "Divino": {"range": (10, 50), "suffixes": ["del Caos", "del Vacío", "Primordial"], "origin": "El Vacío / Reino de Dioses"}
}

class ProceduralResourceGen:
    def generate(self, target_rank=1, force_type=None):
        """
        Genera un recurso y retorna un diccionario {name, rank, origin_world, potency}.
        """
        
        # 1. Determinar Tipo de Material
        if force_type:
            mat_type = force_type
        else:
            mat_type = random.choice(list(RESOURCES_DB.keys()))
            
        root_name = random.choice(RESOURCES_DB[mat_type]["Común"]) # Solo usamos comunes como base
        
        # 2. Determinar Tier
        tier_data = self._get_tier_data(target_rank)
        suffix = random.choice(tier_data["suffixes"])
        origin = tier_data["origin"]
        
        # 3. Construir Nombre
        full_name = f"{root_name} {suffix}"
        
        # 4. Calcular Propiedades
        potency = target_rank * 10 * random.uniform(0.8, 1.2)
        
        return {
            "name": full_name,
            "type": mat_type,
            "rank": f"G{target_rank}",
            "origin_world": origin,
            "potency": int(potency)
        }

    def _get_tier_data(self, rank):
        for tier, data in SUFFIX_TIERS.items():
            min_r, max_r = data["range"]
            if min_r <= rank <= max_r:
                return data
        return SUFFIX_TIERS["Divino"]