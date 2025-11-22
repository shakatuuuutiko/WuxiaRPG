# --- MÓDULO: __init__.py ---
# Aquí pegarás el código correspondiente al sistema de __INIT__
def __init__(self, player, time_sys):
        # ... (código existente)
        
        # Inicializar Sistemas Locales
        self.map_mgr = MapManager()
        # ... (resto de sistemas)
        
        # === INICIALIZACIÓN DEL TORNEO ===
        self.ranking_sys = MockRankingSystem() # Usar el Mock o el RankingSystem real
        self.tournament_sys = TournamentSystem(self.player, self.ranking_sys)
        self.time.tournament_sys = self.tournament_sys # VINCULAR AL SISTEMA DE TIEMPO
        # =================================

        self.current_enemy = None
        # ... (resto de __init__)