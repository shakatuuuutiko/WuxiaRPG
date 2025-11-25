import random

ELEMENT_CHART = {
    "Fuego": "Metal", "Metal": "Madera", "Madera": "Tierra", 
    "Tierra": "Agua", "Agua": "Fuego", 
    "Rayo": "Agua", "Hielo": "Fuego"
}

class CombatEngine:
    def calculate_damage(self, attacker_obj, defender_stats, skill_data=None):
        """
        Calcula daño considerando el equipamiento del atacante.
        
        attacker_obj: Puede ser dict con stats O un objeto Player/NPC con equipment
        defender_stats: Dict con estadísticas de defensa
        skill_data: Skill opcional que modifica el cálculo
        """
        # 1. Daño Base (considerando equipamiento si existe)
        if hasattr(attacker_obj, 'get_total_atk'):
            # Es un Player u objeto con equipamiento
            atk = attacker_obj.get_total_atk()
        else:
            # Es un dict de stats
            atk = attacker_obj.get("atk", 10)
        
        skill_mult = skill_data.get("stats", {}).get("dmg_mult", 1.0) if skill_data else 1.0
        raw_dmg = atk * skill_mult
        
        # 2. Elementos
        if hasattr(attacker_obj, 'stats'):
            atk_elem = skill_data.get("element", "Neutro") if skill_data else attacker_obj.stats.get("element", "Neutro")
        else:
            atk_elem = skill_data.get("element", "Neutro") if skill_data else attacker_obj.get("element", "Neutro")
        
        def_elem = defender_stats.get("element", "Neutro")
        
        modifier = 1.0
        if ELEMENT_CHART.get(atk_elem) == def_elem: modifier = 1.5 
        elif ELEMENT_CHART.get(def_elem) == atk_elem: modifier = 0.75
            
        # 3. Defensa
        defense = defender_stats.get("def", 0)
        mitigation_percent = defense / (defense + 100) 
        
        damage_after_def = raw_dmg * modifier * (1 - mitigation_percent)
        
        # 4. Daño mínimo garantizado
        final_dmg = int(max(1, damage_after_def))
        
        # 5. Crítico
        is_crit = False
        crit_chance = skill_data.get("stats", {}).get("crit_chance", 0) if skill_data else 0.05
        if random.random() < (0.05 + crit_chance):
            final_dmg *= 2
            is_crit = True
            
        return final_dmg, is_crit, modifier > 1.0