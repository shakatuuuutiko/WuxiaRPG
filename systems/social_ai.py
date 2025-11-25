# --- MÓDULO: social_ai.py ---
# Aquí pegarás el código correspondiente al sistema de SOCIAL_AI
import random

# ARQUETIPOS DE PERSONALIDAD
PERSONALITIES = {
    "Justo":      {"aggro": 0.1, "greed": 0.2, "honor": 1.0, "fear": 0.5, "likes": "Justo", "hates": "Demoníaco"},
    "Demoníaco":  {"aggro": 0.9, "greed": 0.9, "honor": 0.0, "fear": 0.3, "likes": "Demoníaco", "hates": "Justo"},
    "Arrogante":  {"aggro": 0.8, "greed": 0.6, "honor": 0.5, "fear": 0.0, "likes": "Fuerte", "hates": "Débil"},
    "Cauto":      {"aggro": 0.0, "greed": 0.4, "honor": 0.6, "fear": 0.9, "likes": "Pacífico", "hates": "Agresivo"},
    "Hedonista":  {"aggro": 0.3, "greed": 0.5, "honor": 0.5, "fear": 0.5, "likes": "Cualquiera", "hates": "Aburrido"}
}

DISGUISES = {
    "Pañuelo Negro": {"stealth": 30, "durability": 2},
    "Máscara de Madera": {"stealth": 60, "durability": 10},
    "Piel de las Mil Caras": {"stealth": 95, "durability": 50}
}

class SocialEngine:
    def __init__(self):
        self.relations = {} # {id_a: {id_b: score}}
        self.news_feed = []
        self.wanted_list = {} # {name: bounty}

    def get_relation(self, id_a, id_b):
        return self.relations.get(id_a, {}).get(id_b, 0)

    def modify_relation(self, id_a, id_b, amount):
        if id_a not in self.relations: self.relations[id_a] = {}
        current = self.relations[id_a].get(id_b, 0)
        self.relations[id_a][id_b] = max(-100, min(100, current + amount))

    def interact(self, actor, target):
        """Simula encuentro NPC-NPC o NPC-Player"""
        p_actor = PERSONALITIES.get(actor.archetype, PERSONALITIES["Cauto"])
        rel = self.get_relation(actor.name, target.name)
        
        # Factor RNG + Relación
        roll = random.randint(-50, 50) + rel
        
        # Lógica de Acción
        if roll > 50: # Amistad/Romance
            self.modify_relation(actor.name, target.name, 10)
            self.modify_relation(target.name, actor.name, 10)
            return "FRIENDLY", f"{actor.name} y {target.name} compartieron té y dao."
            
        elif roll < -30 or (p_actor["greed"] > 0.8 and target.inventory): # Conflicto
            # Si es agresivo, ataca
            if p_actor["aggro"] > 0.5:
                return "ATTACK", f"{actor.name} intentó robar a {target.name}."
            else:
                self.modify_relation(actor.name, target.name, -5)
                return "INSULT", f"{actor.name} miró con desprecio a {target.name}."
        
        return "NEUTRAL", f"{actor.name} ignoró a {target.name}."

class IdentityManager:
    def __init__(self, real_name):
        self.real_name = real_name
        self.current_disguise = None
        self.fake_name = None
        self.reputation_db = {real_name: 0} # Reputación por identidad

    def equip_mask(self, item_name, alias):
        if item_name in DISGUISES:
            self.current_disguise = item_name
            self.fake_name = alias
            if alias not in self.reputation_db: self.reputation_db[alias] = 0
            return True, f"Ahora eres '{alias}'."
        return False, "Disfraz inválido."

    def unequip(self):
        self.current_disguise = None
        self.fake_name = None

    def get_visible_name(self):
        return self.fake_name if self.current_disguise else self.real_name

    def check_leak(self, observer_perception):
        """Verifica si te descubren"""
        if not self.current_disguise: return True, "Sin máscara."
        
        data = DISGUISES[self.current_disguise]
        chance = data["stealth"] - (observer_perception * 0.5)
        
        if random.randint(0, 100) > chance:
            self.unequip()
            return True, f"¡Tu {self.current_disguise} falló! Saben que eres {self.real_name}."
        return False, "Identidad segura."

class CrimeSystem:
    def __init__(self, social_engine):
        self.social = social_engine

    def report_crime(self, culprit_identity, victim_name, witnesses, location):
        culprit_name = culprit_identity.get_visible_name()
        
        if not witnesses:
            self.social.news_feed.append(f"MISTERIO: Cuerpo de {victim_name} hallado en {location}.")
            return "Crimen perfecto."
        else:
            # Bajar reputación de la identidad actual
            culprit_identity.reputation_db[culprit_name] -= 50
            
            news = f"BUSCADO: {culprit_name} asesinó a {victim_name} en {location}."
            self.social.news_feed.append(news)
            self.social.wanted_list[culprit_name] = 1000 # Recompensa
            
            return f"¡Testigos escaparon! Se busca a: {culprit_name}"