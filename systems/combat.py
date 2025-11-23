import random

ELEMENT_CHART = {
    "Fuego": "Metal", "Metal": "Madera", "Madera": "Tierra", 
    "Tierra": "Agua", "Agua": "Fuego", 
    "Rayo": "Agua", "Hielo": "Fuego"
}

class CombatEngine:
    def calculate_damage(self, attacker_stats, defender_stats, skill_data=None):
        # 1. Daño Base
        atk = attacker_stats.get("atk", 10)
        skill_mult = skill_data["stats"]["dmg_mult"] if skill_data else 1.0
        raw_dmg = atk * skill_mult
        
        # 2. Elementos
        atk_elem = skill_data.get("element", "Neutro") if skill_data else attacker_stats.get("element", "Neutro")
        def_elem = defender_stats.get("element", "Neutro")
        
        modifier = 1.0
        if ELEMENT_CHART.get(atk_elem) == def_elem: modifier = 1.5 
        elif ELEMENT_CHART.get(def_elem) == atk_elem: modifier = 0.75
            
        # 3. Defensa (Corregido para Early Game)
        defense = defender_stats.get("def", 0)
        mitigation_percent = defense / (defense + 100) 
        
        damage_after_def = raw_dmg * modifier * (1 - mitigation_percent)
        
        # FIX: Daño mínimo garantizado de 1
        final_dmg = int(max(1, damage_after_def))
        
        # 4. Crítico
        is_crit = False
        crit_chance = 0.05 + skill_data["stats"].get("crit_chance", 0) if skill_data else 0.05
        if random.random() < crit_chance:
            final_dmg *= 2
            is_crit = True
            
        return final_dmg, is_crit, modifier > 1.0