# --- CONFIGURACIÓN GLOBAL DEL JUEGO ---

# 1. Configuración de Ventana y Gráficos (Base para Pygame/Tkinter)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
APP_TITLE = "WUXIA: ETERNIDAD INFINITA - Final Build"
FPS = 30 # Velocidad de refresco del juego

# 2. Configuración de Tiempos y Archivos
TICK_SPEED_MS = 1000 # 1 segundo real = 1 ciclo de juego (para automatización de tareas)
SAVE_FOLDER = "saves"

# 3. Constantes del Mundo
CHUNK_SIZE = 32 # Tamaño de cada trozo de mapa (32x32)
VOID_TILE = "ABISMO ESPACIAL" # Nombre del terreno borrado por Dao Espacial

# 4. Paleta de Colores (Usada en Pygame/Tkinter)
COLORS = {
    "background": "#050505",    # Negro oscuro
    "panel": "#101010",         
    "text_light": "#dddddd",    
    "highlight_gold": "#d4aa00",# Dorado
    "danger_red": "#ff5555",    # Rojo (HP)
    "qi_blue": "#4fa4ff",       # Azul (Qi)
    "success_green": "#55ff55", # Verde
    "warning_yellow": "#ffff00" # Amarillo
}