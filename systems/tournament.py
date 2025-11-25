import random
import math

# Dependencias (Asumidas: Asumimos que CombatEngine existe y funciona)
try:
    from systems.combat import CombatEngine
    # Nota: Asumimos que RankingSystem tiene el método get_top_ranked_cultivators(tier)
except ImportError:
    # Mock para asegurar la ejecución si CombatEngine no existe.
    class CombatEngine:
        def simple_fight(self, entity1_stats, entity2_stats):
            """Simulación de combate simple (poder = HP + ATK)"""
            power1 = entity1_stats.get('hp', 1) + entity1_stats.get('atk', 1)
            power2 = entity2_stats.get('hp', 1) + entity2_stats.get('atk', 1)
            
            # Devolver las stats del ganador (simple)
            if power1 > power2: return entity1_stats
            else: return entity2_stats

class TournamentSystem:
    def __init__(self, player, ranking_system):
        self.player = player
        self.ranking_system = ranking_system
        self.combat_engine = CombatEngine()
        self.current_bracket = []
        self.is_active = False

    def check_and_start_tournament(self, year):
        """Verifica si es un año de torneo (cada 5 años)"""
        # Se activa el torneo cada 5 años de juego (Año 5, 10, 15, etc.)
        if year % 5 == 0 and year > 0 and not self.is_active:
            self.start_new_tournament(tier=1)
            return True
        return False

    def start_new_tournament(self, tier):
        """Prepara y arranca el Torneo del Dao para un Tier específico."""
        self.is_active = True
        
        # 1. Obtener Participantes (Top 7 NPCs + Jugador)
        try:
            npcs = self.ranking_system.get_top_ranked_cultivators(tier)
        except:
            npcs = self._mock_npcs(tier) # Usar Mock si el RankingSystem falla
            
        participants = [self.player.to_dict()] + npcs
        random.shuffle(participants)
        
        # Asegurar que siempre haya 8 participantes (Bracket 8)
        if len(participants) < 8:
            participants += self._mock_npcs(tier, 8 - len(participants))
        participants = participants[:8]
        
        self.current_bracket = participants
        
        log = f"--- COMIENZA EL GRAN TORNEO DEL DAO (Tier {tier}) ---"
        self.player.log(log, "special")
        
        self.run_tournament(tier)
        
        return log

    def run_tournament(self, tier):
        """Simula las rondas de un torneo de 8 personas."""
        
        # 1. Ronda 1 (Cuartos de Final)
        self.current_bracket = self._run_round(self.current_bracket, "Cuartos de Final")
        if len(self.current_bracket) == 1:
            self.end_tournament(tier, self.current_bracket[0])
            return

        # 2. Ronda 2 (Semifinales)
        self.current_bracket = self._run_round(self.current_bracket, "Semifinales")
        if len(self.current_bracket) == 1:
            self.end_tournament(tier, self.current_bracket[0])
            return

        # 3. Ronda 3 (FINAL)
        self.current_bracket = self._run_round(self.current_bracket, "FINAL")
        
        self.end_tournament(tier, self.current_bracket[0])

    def _run_round(self, fighters, round_name):
        """Ejecuta una ronda de combates y devuelve a los ganadores."""
        winners = []
        self.player.log(f"\n--- RONDA: {round_name} ---", "special")
        
        for i in range(0, len(fighters), 2):
            fighter1 = fighters[i]
            fighter2 = fighters[i+1]
            
            winner, loser = self._fight_match(fighter1, fighter2)
            winners.append(winner)

            # Log para el jugador
            p_name = self.player.name
            if winner['name'] == p_name:
                self.player.log(f"✅ {p_name} vence a {loser['name']}.", "gain")
            elif loser['name'] == p_name:
                self.player.log(f"❌ {p_name} es derrotado por {winner['name']}.", "alert")
            else:
                 self.player.log(f"Resultado: {winner['name']} vence a {loser['name']}", "info")
                 
        return winners

    def _fight_match(self, entity1, entity2):
        """Simula un combate uno a uno usando el CombatEngine (o la simulación simple)"""
        
        # Stats del Jugador (si está participando)
        stats1 = self.player.stats if entity1['name'] == self.player.name else entity1['stats']
        stats2 = self.player.stats if entity2['name'] == self.player.name else entity2['stats']
        
        # Simulación de combate (El más fuerte gana, con algo de azar si son similares)
        power1 = stats1.get('hp', 1) + stats1.get('atk', 1) + (stats1.get('qi', 0) / 5)
        power2 = stats2.get('hp', 1) + stats2.get('atk', 1) + (stats2.get('qi', 0) / 5)
        
        if power1 > power2 * 1.15: # Victoria clara
            winner = entity1
            loser = entity2
        elif power2 > power1 * 1.15: # Derrota clara
            winner = entity2
            loser = entity1
        elif random.random() < 0.5: # 50/50 si el poder es similar
            winner = entity1
            loser = entity2
        else:
            winner = entity2
            loser = entity1
            
        return winner, loser


    def end_tournament(self, tier, winner):
        """Asigna premios y limpia el estado del torneo."""
        self.is_active = False
        
        self.player.log(f"\n--- ¡{winner['name']} GANA EL TORNEO DEL DAO TIER {tier}! ---", "special")
        
        if winner['name'] == self.player.name:
            self.award_prizes(tier)
        
        self.current_bracket = []

    def award_prizes(self, tier):
        """Entrega premios al jugador si ganó."""
        prize_gold = 100 * (tier ** 2)
        prize_item = f"Manual de Arte Secreto (Tier {tier})"
        
        self.player.inventory['Oro'] = self.player.inventory.get('Oro', 0) + prize_gold
        self.player.inventory[prize_item] = self.player.inventory.get(prize_item, 0) + 1
        
        self.player.log(f"🏆 ¡Recompensas por la victoria! +{prize_gold} Oro, +1 {prize_item}", "gain")


    def _mock_npcs(self, tier, count=7):
        """Genera NPCs de relleno para la simulación si no hay RankingSystem."""
        mock_npcs = []
        names = ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao"]
        
        for i in range(count):
            name = random.choice(names) + f" el Cultivador #{i + 1}"
            stats = {
                'hp': random.randint(100, 150) * tier,
                'max_hp': random.randint(100, 150) * tier,
                'atk': random.randint(15, 25) * tier,
                'def': random.randint(5, 10) * tier,
            }
            mock_npcs.append({'name': name, 'stats': stats, 'rank': tier})
            
        return mock_npcs