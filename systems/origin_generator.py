import random
from data.origins_db_massive import ORIGIN_PREFIXES, ORIGIN_ROLES, ORIGIN_SUFFIXES

class OriginGenerator:
    def generate(self):
        # 1. Elegir piezas
        prefix_name = random.choice(list(ORIGIN_PREFIXES.keys()))
        role_name = random.choice(list(ORIGIN_ROLES.keys()))
        suffix_name = random.choice(list(ORIGIN_SUFFIXES.keys()))
        
        prefix_data = ORIGIN_PREFIXES[prefix_name]
        role_data = ORIGIN_ROLES[role_name]
        suffix_data = ORIGIN_SUFFIXES[suffix_name]
        
        # 2. Construir Nombre
        # Ej: "Maldito Príncipe con un Anillo"
        full_title = f"{prefix_name} {role_name}"
        if suffix_name != "Común":
            full_title += f" {suffix_name}"
            
        # 3. Fusionar Inventarios
        final_inv = {}
        for source in [role_data, suffix_data]:
            if "inv" in source:
                for item, qty in source["inv"].items():
                    final_inv[item] = final_inv.get(item, 0) + qty
        
        # 4. Fusionar Stats
        final_stats = {"hp": 0, "qi": 0, "atk": 0, "def": 0, "stamina": 0, "comprension": 0, "luck": 0}
        base_gold = 0
        
        for source in [prefix_data, role_data, suffix_data]:
            base_gold += source.get("gold", 0)
            mods = source.get("stats", {}) # Algunos usan 'stats', otros claves directas en prefix
            
            # Normalizar datos (Prefix usa claves directas, Role usa sub-diccionario)
            data_to_merge = mods if mods else source
            
            for k, v in data_to_merge.items():
                if k in final_stats:
                    final_stats[k] += v

        # 5. Flags Especiales
        special_flags = {}
        if suffix_data.get("force_bloodline"): special_flags["bloodline"] = "Random_Strong"
        if suffix_data.get("force_root"): special_flags["root"] = suffix_data["force_root"]

        # 6. Generar Descripción
        desc = f"{prefix_data.get('desc', '')} Eras un {role_name.lower()}."
        
        return {
            "title": full_title,
            "description": desc,
            "gold": base_gold,
            "inventory": final_inv,
            "stats_mod": final_stats,
            "flags": special_flags
        }

# Test rápido
if __name__ == "__main__":
    gen = OriginGenerator()
    for _ in range(5):
        print(gen.generate()["title"])