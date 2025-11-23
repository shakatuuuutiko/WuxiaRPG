# --- SISTEMA DE TIEMPO Y HERENCIA ---
import math

# Vida Máxima por Grado (Realm)
LIFESPAN_TABLE = {
    0: 80,      # Mortal (Base)
    1: 120,     # Condensación de Qi
    3: 500,     # Núcleo Dorado
    6: 1500,    # Fusión
    10: 3000,   # Emperador Inmortal
    48: 9999999 # Dao Ancestor
}

def get_max_lifespan(realm_idx):
    """Retorna la longevidad máxima basada en el reino (G)."""
    for r in sorted(LIFESPAN_TABLE.keys(), reverse=True):
        if realm_idx >= r:
            return LIFESPAN_TABLE[r]
    return 80

class TimeSystem:
    def __init__(self):
        self.year = 1
        self.month = 1
        self.total_months = 0

    def pass_time(self, months):
        """Avanza el tiempo y retorna cuántos años pasaron."""
        self.month += months
        self.total_months += months
        
        years_passed = 0
        while self.month > 12:
            self.month -= 12
            self.year += 1
            years_passed += 1
            
        return years_passed

class AgeManager:
    def __init__(self, player_obj):
        self.player = player_obj
        self.current_age = 16 
        self.max_lifespan = get_max_lifespan(0) # Inicia como G0

    def check_death(self, years_added):
        """Verifica si el jugador muere por vejez."""
        self.current_age += years_added
        if self.current_age >= self.max_lifespan:
            return True # Muerte por vejez
        return False