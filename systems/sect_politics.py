# --- MÓDULO: sect_politics.py ---
# Aquí pegarás el código correspondiente al sistema de SECT_POLITICS
import random

# Configuración de Rangos y Costos
RANKS = {
    "Patriarca":          {"salary": 0,    "authority": 100, "limit": 1},
    "Gran Anciano":       {"salary": 500,  "authority": 80,  "limit": 3},
    "Anciano":            {"salary": 200,  "authority": 60,  "limit": 10},
    "Discípulo Legado":   {"salary": 100,  "authority": 40,  "limit": 10},
    "Discípulo Interior": {"salary": 50,   "authority": 20,  "limit": 500},
    "Discípulo Exterior": {"salary": 10,   "authority": 10,  "limit": 10000}
}

class Sect:
    def __init__(self, name, is_player_owned=False):
        self.name = name
        self.is_player_owned = is_player_owned
        
        # Tesoro
        self.treasury = {"Oro": 10000, "Píldoras": 100, "Hierbas": 500}
        self.territories = [] # ["Mina de Hierro", "Veta Espiritual"]
        
        # Miembros: {id_entidad: rango}
        self.members = {}
        self.morale = 80 # 0-100
        self.relations = {} # Diplomacia

    def recruit(self, entity_id, rank="Discípulo Exterior"):
        self.members[entity_id] = rank

    def promote(self, entity_id, new_rank):
        # Verificar cupo
        current = list(self.members.values()).count(new_rank)
        limit = RANKS[new_rank]["limit"]
        
        if current >= limit:
            return False, f"No hay vacantes para {new_rank}."
            
        self.members[entity_id] = new_rank
        return True, f"{entity_id} ascendido a {new_rank}."

    def daily_tick(self):
        """Ciclo económico diario"""
        logs = []
        
        # 1. Ingresos
        income = len(self.territories) * 500 + (len(self.members) * 5)
        self.treasury["Oro"] += income
        
        # 2. Gastos (Salarios)
        expenses = sum([RANKS[r]["salary"] for r in self.members.values()])
        
        if self.treasury["Oro"] >= expenses:
            self.treasury["Oro"] -= expenses
            logs.append(f"Finanzas: +{income} Ingresos | -{expenses} Salarios.")
            self.morale = min(100, self.morale + 1)
        else:
            self.treasury["Oro"] = 0
            self.morale -= 10
            logs.append("¡CRISIS! No hay oro para salarios. La moral cae.")
            
        return logs

class WarEngine:
    def simulate_war(self, attacker, defender):
        # Poder de combate (Simulado basado en número de miembros)
        # En el juego real, iterarías los objetos reales para sumar su ATK
        pow_a = len(attacker.members) * 100 * (attacker.morale / 100)
        pow_b = len(defender.members) * 100 * (defender.morale / 100)
        
        # Factor Estrategia (RNG)
        final_a = pow_a * random.uniform(0.8, 1.2)
        final_b = pow_b * random.uniform(0.8, 1.2)
        
        winner = attacker if final_a > final_b else defender
        loser = defender if final_a > final_b else attacker
        
        # Saqueo
        loot = int(loser.treasury["Oro"] * 0.5)
        loser.treasury["Oro"] -= loot
        winner.treasury["Oro"] += loot
        
        # Bajas
        casualties = int(len(loser.members) * 0.1)
        
        return {
            "winner": winner.name,
            "loot": loot,
            "casualties": casualties
        }