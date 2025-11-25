import json
import random
import os

# Recursos de base organizados por rareza
RESOURCES_DB = {
    "Maderas": {
        "Común": ["Roble", "Pino", "Rama", "Tronco", "Bambú"],
        "Raro": ["Madera de Hierro", "Bambú Espiritual", "Tronco Espiritual", "Roble Milenario"],
        "Épico": ["Madera de Fénix", "Raíz del Árbol del Mundo", "Tronco del Árbol del Mundo", "Raíz Universal"],
        "Legendario": ["Roble Eterno", "Raíz del Eterno Mundo"]
    },
    "Minerales": {
        "Común": ["Roca", "Cobre", "Hierro", "Granito", "Estaño"],
        "Raro": ["Plata", "Oro", "Cristal", "Titanio"],
        "Épico": ["Adamantita", "Mithril", "Oro Galáctico"],
        "Legendario": ["Adamantita Estelar", "Mithril del Vacío"]
    },
    "Plantas": {
        "Común": ["Hierba Medicinal", "Flor Silvestre", "Hongo Marrón"],
        "Raro": ["Ginseng de 100 años", "Loto de Nieve", "Hongo Espiritual"],
        "Épico": ["Ginseng de Sangre", "Fruto de la Inmortalidad"],
        "Legendario": ["Hierba de la Eternidad", "Loto de la Inmortalidad"]
    }
}


RARITY_WEIGHTS = {
    "Común": 60,
    "Raro": 25,
    "Épico": 10,
    "Legendario": 5
}


def _choose_rarity():
    rarities = list(RARITY_WEIGHTS.keys())
    weights = [RARITY_WEIGHTS[r] for r in rarities]
    return random.choices(rarities, weights=weights, k=1)[0]


class ProceduralResourceGen:
    def __init__(self, out_path=None):
        # Guardar en systems/Materiales.json por defecto
        base_dir = os.path.dirname(__file__)
        self.out_path = out_path or os.path.join(base_dir, 'Materiales.json')

    def _generate_material_entry(self, category, name, rarity):
        entry = {
            "name": name,
            "rarity": rarity,
            "type": category
        }

        # Atributos para forja (Maderas y Minerales)
        if category in ("Maderas", "Minerales"):
            # Ajustar rangos según rareza
            if rarity == "Común":
                dureza = random.randint(5, 30) if category == "Maderas" else random.randint(10, 40)
                conductividad = random.randint(10, 60) if category == "Maderas" else random.randint(5, 40)
                peso = round(random.uniform(1.0, 8.0), 2) if category == "Maderas" else round(random.uniform(6.0, 30.0), 2)
            elif rarity == "Raro":
                dureza = random.randint(20, 50) if category == "Maderas" else random.randint(30, 60)
                conductividad = random.randint(15, 80) if category == "Maderas" else random.randint(10, 60)
                peso = round(random.uniform(2.0, 9.0), 2) if category == "Maderas" else round(random.uniform(8.0, 40.0), 2)
            elif rarity == "Épico":
                dureza = random.randint(40, 70) if category == "Maderas" else random.randint(50, 80)
                conductividad = random.randint(20, 100) if category == "Maderas" else random.randint(20, 80)
                peso = round(random.uniform(3.0, 12.0), 2) if category == "Maderas" else round(random.uniform(10.0, 50.0), 2)
            else:  # Legendario
                dureza = random.randint(60, 100) if category == "Maderas" else random.randint(80, 120)
                conductividad = random.randint(30, 150) if category == "Maderas" else random.randint(30, 140)
                peso = round(random.uniform(4.0, 20.0), 2) if category == "Maderas" else round(random.uniform(12.0, 70.0), 2)

            entry.update({
                "stats_forja": {
                    "dureza": dureza,
                    "conductividad": conductividad,
                    "peso": peso
                }
            })

        # Atributos para plantas (tags usados por el sistema de alquimia)
        if category == "Plantas":
            # Posibles tags y su peso base
            possible_tags = ["Fuego", "Vida", "Madera", "Hielo", "Agua", "Pureza", "Yin", "Yang", "Sangre", "Estabilidad"]
            tags = {}
            # Número de tags según rareza
            tag_count = {"Común": 2, "Raro": 3, "Épico": 4, "Legendario": 5}[rarity]
            chosen = random.sample(possible_tags, tag_count)
            for t in chosen:
                # Valores mayores para rarezas altas
                base = {"Común": (5, 12), "Raro": (10, 25), "Épico": (20, 45), "Legendario": (40, 90)}[rarity]
                tags[t] = random.randint(*base)

            entry.update({
                "tags": tags,
                "potency": sum(tags.values())
            })

        return entry

    def generate(self, include_all=True, per_category_limit=None):
        """Genera materiales y guarda un JSON listo para usar en crafting.
        - include_all: si True incluirá todas las entradas de RESOURCES_DB.
        - per_category_limit: si especificado, limita el número por categoría (elige aleatoriamente).
        """
        materials = {"Maderas": [], "Minerales": [], "Plantas": []}

        for category, rarities in RESOURCES_DB.items():
            pool = []
            for rarity, names in rarities.items():
                for name in names:
                    pool.append((category, name, rarity))

            # Elegir ítems
            selected = pool
            if per_category_limit and per_category_limit > 0:
                selected = random.sample(pool, min(per_category_limit, len(pool)))

            for cat, name, rarity in selected:
                entry = self._generate_material_entry(cat, name, rarity)
                materials[cat].append(entry)

        # Guardar
        self.save_to_json(materials)
        return materials

    def save_to_json(self, materials):
        os.makedirs(os.path.dirname(self.out_path), exist_ok=True)
        with open(self.out_path, 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    gen = ProceduralResourceGen()
    mats = gen.generate()
    total = sum(len(v) for v in mats.values())
    print(f"Generados {total} materiales -> {gen.out_path}")