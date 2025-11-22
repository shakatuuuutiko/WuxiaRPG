import json
import os
import random
import math
from config import CHUNK_SIZE, VOID_TILE

class MapManager:
    def __init__(self, world_name="Mundo_Mortal"):
        self.world_name = world_name
        self.loaded_chunks = {} 
        self.save_path = f"saves/{world_name}"
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)
            
        # REGISTRO DE LUGARES (Coordenadas Globales)
        self.poi_registry = {
            "Pueblo Inicio": [0, 0],
            "Secta Nube": [200, 200],
            "Secta Sangre": [-300, 450],
            "Ruinas": [500, -100]
        }

    def get_tile_info(self, gx, gy):
        cx, cy = gx // CHUNK_SIZE, gy // CHUNK_SIZE
        lx, ly = gx % CHUNK_SIZE, gy % CHUNK_SIZE
        chunk = self._load_chunk(cx, cy)
        return chunk["grid"][ly][lx]

    def get_biome_at(self, chunk_x, chunk_y):
        # Ruido determinista para Mapa Global
        val = math.sin(chunk_x * 0.1) + math.cos(chunk_y * 0.1)
        if val < -1.2: return "Océano"
        elif val < -0.8: return "Agua"
        elif val < -0.6: return "Playa"
        elif val < 0.3: return "Llanura"
        elif val < 0.8: return "Bosque"
        elif val < 1.3: return "Montaña"
        return "Volcán"

    def _load_chunk(self, cx, cy):
        if (cx, cy) in self.loaded_chunks: return self.loaded_chunks[(cx, cy)]
        # Generación simple sin guardado en disco por ahora para velocidad
        return self._generate_procedural(cx, cy)

    def _generate_procedural(self, cx, cy):
        grid = []
        random.seed(f"{cx}_{cy}") 
        base_biome = self.get_biome_at(cx, cy)
        for y in range(CHUNK_SIZE):
            row = []
            for x in range(CHUNK_SIZE):
                roll = random.random()
                if roll < 0.05: row.append("Roca" if base_biome != "Océano" else "Arrecife")
                else: row.append(base_biome)
            grid.append(row)
        return {"grid": grid, "biome": base_biome}