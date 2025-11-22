import tkinter as tk

# Colores de Fondo
BIOME_COLORS = {
    "Llanura": "#228B22",   # Verde
    "Bosque":  "#006400",   # Verde Oscuro
    "Montaña": "#696969",   # Gris
    "Volcán":  "#8B0000",   # Rojo
    "Tundra":  "#F0FFFF",   # Blanco Hielo
    "Océano":  "#00008B",   # Azul Profundo
    "Playa":   "#F4A460",   # Arena
    "Roca":    "#555555",   # Gris Roca
    "Arrecife":"#00CED1",   # Turquesa
    "Agua":    "#1E90FF",   # Azul Claro
    "ABISMO ESPACIAL": "#000000" # Negro
}

# Iconos / Sprites de Texto
BIOME_ICONS = {
    "Llanura": " . ", "Bosque":  "♣", "Montaña": "▲", "Volcán":  "🔥", "Tundra":  "❄",
    "Océano":  "~", "Playa":   "∴", "Roca":    "▓", "Arrecife":"#", "Agua":    "≈",
    "ABISMO ESPACIAL": "🌀"
}

class MapWidget(tk.Canvas):
    def __init__(self, parent, width=400, height=300, cell_size=20):
        super().__init__(parent, width=width, height=height, bg="#000000", highlightthickness=0)
        self.cell_size = cell_size

    def draw_chunk(self, chunk_data, player_local_x, player_local_y):
        self.delete("all")
        
        grid = chunk_data["grid"]
        rows = len(grid)
        cols = len(grid[0])
        
        offset_x = (int(self['width']) - (cols * self.cell_size)) // 2
        offset_y = (int(self['height']) - (rows * self.cell_size)) // 2
        
        for y in range(rows):
            for x in range(cols):
                tile_type = grid[y][x]
                color = BIOME_COLORS.get(tile_type, "#FF00FF") 
                
                x1 = offset_x + (x * self.cell_size)
                y1 = offset_y + (y * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                icon = BIOME_ICONS.get(tile_type, "")
                if icon.strip():
                    # FIX: Usamos un font genérico para evitar cuadrados blancos
                    self.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, 
                                     text=icon, font=("TkFixedFont", 10), fill="white")

        # Dibujar Jugador
        px = offset_x + (player_local_x * self.cell_size)
        py = offset_y + (player_local_y * self.cell_size)
        
        self.create_oval(px+2, py+2, px+self.cell_size-2, py+self.cell_size-2, 
                         fill="#FF0000", outline="white", width=2)
        self.create_text(px + self.cell_size/2, py + self.cell_size/2, text="🧘", 
                         font=("TkFixedFont", 10))