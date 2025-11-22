import random
try:
    from data.origins_db import ORIGIN_PREFIXES, ORIGIN_ROLES, ORIGIN_SUFFIXES
except ImportError:
    # Fallback para evitar crash si falta la DB
    ORIGIN_PREFIXES = {"Común": {}}
    ORIGIN_ROLES = {"Aldeano": {"gold": 10}}
    ORIGIN_SUFFIXES = {"Normal": {}}

class OriginGenerator:
    def generate(self):
        prefix_name = random.choice(list(ORIGIN_PREFIXES.keys()))
        role_name = random.choice(list(ORIGIN_ROLES.keys()))
        suffix_name = random.choice(list(ORIGIN_SUFFIXES.keys()))
        
        prefix_data = ORIGIN_PREFIXES[prefix_name]
        role_data = ORIGIN_ROLES[role_name]
        suffix_data = ORIGIN_SUFFIXES[suffix_name]
        
        full_title = f"{prefix_name} {role_name} {suffix_name}".replace(" Común", "")
        
        # Fusionar
        final_inv = {}
        for source in [role_data, suffix_data]:
            for item, qty in source.get("inv", {}).items():
                final_inv[item] = final_inv.get(item, 0) + qty
        
        final_stats = {}
        base_gold = 0
        
        for source in [prefix_data, role_data, suffix_data]:
            base_gold += source.get("gold", 0)
            for k, v in source.get("stats", {}).items():
                final_stats[k] = final_stats.get(k, 0) + v
                
        flags = {}
        if suffix_data.get("force_bloodline"): flags["bloodline"] = True

        return {
            "title": full_title,
            "gold": base_gold,
            "inventory": final_inv,
            "stats_mod": final_stats,
            "flags": flags
        }