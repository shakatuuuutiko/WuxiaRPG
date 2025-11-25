# --- MÓDULO: slave_mgmt.py ---
# Aquí pegarás el código correspondiente al sistema de SLAVE_MGMT
import random

CONTRACTS = {
    "Siervo": {
        "cost": 50, "loyalty": 10, "fear": 50, "efficiency": 1.2,
        "desc": "Mantiene conciencia. Riesgo de rebelión."
    },
    "Marioneta": {
        "cost": 200, "loyalty": 100, "fear": 0, "efficiency": 0.7,
        "desc": "Sin mente. Lealtad absoluta pero torpe."
    }
}

class Slave:
    def __init__(self, entity_data, contract_type):
        self.original_name = entity_data["name"]
        self.stats = entity_data["stats"]
        self.contract = contract_type
        
        data = CONTRACTS[contract_type]
        self.loyalty = data["loyalty"]
        self.fear = data["fear"]
        self.task = "Nada" # Nada, Cultivo, Minería, Guardaespaldas

    def work_tick(self):
        """Genera recursos basado en la tarea"""
        if self.task == "Nada": return None
        
        eff = CONTRACTS[self.contract]["efficiency"]
        # Si es Siervo, su estado emocional afecta
        if self.contract == "Siervo":
            eff *= (0.5 + (self.loyalty + self.fear) / 200.0)
            # Desgaste
            if random.random() < 0.05: self.loyalty -= 1

        roll = random.random()
        output = None
        
        if self.task == "Cultivo" and roll < (0.3 * eff):
            output = ("Hierba Espiritual", 1)
        elif self.task == "Minería" and roll < (0.2 * eff):
            output = ("Hierro Negro", 1)
            
        return output

    def check_rebellion(self, master_hp_percent):
        """Intento de asesinato si el maestro está débil"""
        if self.contract == "Marioneta": return False
        
        hate = 100 - self.loyalty
        opportunity = (1.0 - master_hp_percent) * 100
        
        risk = hate - self.fear + opportunity
        return risk > 100

class SlaveManager:
    def __init__(self, player):
        self.player = player
        if not hasattr(player, "slaves"): player.slaves = []

    def attempt_capture(self, enemy_entity, contract="Siervo"):
        # 1. Check HP
        hp_perc = enemy_entity["stats"]["hp"] / enemy_entity["stats"]["max_hp"]
        if hp_perc > 0.15: return False, "Enemigo muy fuerte. Debilita a <15% HP."
        
        # 2. Check Qi
        cost = CONTRACTS[contract]["cost"]
        if self.player.stats["qi"] < cost: return False, "Falta Qi para el sello."
        
        # 3. Probabilidad
        my_soul = self.player.stats["max_qi"]
        enemy_soul = enemy_entity["stats"].get("qi", 100)
        chance = 0.5 + ((my_soul - enemy_soul) / 1000.0)
        
        self.player.stats["qi"] -= cost
        
        if random.random() < chance:
            new_slave = Slave(enemy_entity, contract)
            self.player.slaves.append(new_slave)
            return True, f"¡Captura exitosa! {enemy_entity['name']} es tuyo."
        else:
            self.player.stats["hp"] -= int(self.player.stats["max_hp"] * 0.1)
            return False, "Fallo. Sufriste contragolpe."

    def interact(self, slave_idx, action):
        slave = self.player.slaves[slave_idx]
        
        if action == "Torturar":
            slave.fear = min(100, slave.fear + 20)
            slave.loyalty = max(0, slave.loyalty - 10)
            return "Miedo aumentado. Odio aumentado."
        elif action == "Premiar":
            slave.loyalty = min(100, slave.loyalty + 15)
            slave.fear = max(0, slave.fear - 5)
            return "Lealtad aumentada."