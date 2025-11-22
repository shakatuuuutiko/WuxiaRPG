import json
import os
import random
import math

# Constantes
CHUNK_SIZE = 32
VOID_TILE = "ABISMO ESPACIAL"

class MapManager:
    def __init__(self, world_name="Mundo_Mortal"):
        self.world_name = world_name
        self.loaded_chunks = {} # Cache en RAM
        
        # Crear carpeta de guardado si no existe
        self.save_path = f"saves/{world_name}"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def get_tile_info(self, gx, gy):
        """Obtiene datos de una casilla global"""
        cx, cy = gx // CHUNK_SIZE, gy // CHUNK_SIZE
        lx, ly = gx % CHUNK_SIZE, gy % CHUNK_SIZE
        
        chunk = self._load_chunk(cx, cy)
        return chunk["grid"][ly][lx] # Retorna tipo de terreno (string)

    def get_biome_at(self, chunk_x, chunk_y):
        """
        Retorna el bioma PREDOMINANTE de un chunk sin cargar todo el grid.
        Usado para el Mapa Mundi rápido.
        """
        # Reutilizamos la fórmula de ruido simple
        noise_val = math.sin(chunk_x * 0.1) + math.cos(chunk_y * 0.1)
        
        if noise_val < -1: return "Océano"
        elif noise_val < -0.5: return "Playa"
        elif noise_val < 0.5: return "Bosque"
        elif noise_val < 1.2: return "Montaña"
        else: return "Volcán"

    def set_tile(self, gx, gy, value):
        """Modifica el terreno (Dao Espacial / Construcción)"""
        cx, cy = gx // CHUNK_SIZE, gy // CHUNK_SIZE
        lx, ly = gx % CHUNK_SIZE, gy % CHUNK_SIZE
        
        chunk = self._load_chunk(cx, cy)
        chunk["grid"][ly][lx] = value
        self._save_chunk(cx, cy, chunk)

    def _load_chunk(self, cx, cy):
        if (cx, cy) in self.loaded_chunks:
            return self.loaded_chunks[(cx, cy)]
            
        filename = f"{self.save_path}/chunk_{cx}_{cy}.json"
        
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        else:
            data = self._generate_procedural(cx, cy)
            # Sparse Saving: No guardamos hasta que se modifique
            
        self.loaded_chunks[(cx, cy)] = data
        return data

    def _save_chunk(self, cx, cy, data):
        filename = f"{self.save_path}/chunk_{cx}_{cy}.json"
        with open(filename, "w") as f:
            json.dump(data, f)

    def _generate_procedural(self, cx, cy):
        """Generador determinista basado en coordenadas"""
        grid = []
        # Usamos semilla fija para que si vuelves al mismo lugar sea igual
        random.seed(f"{cx}_{cy}_wuxia_seed") 
        
        # Bioma base
        base_biome = self.get_biome_at(cx, cy)

        for y in range(CHUNK_SIZE):
            row = []
            for x in range(CHUNK_SIZE):
                # Variación local (ruido)
                roll = random.random()
                if roll < 0.05:
                    row.append("Roca" if base_biome != "Océano" else "Arrecife")
                elif roll < 0.02:
                    row.append("Agua" if base_biome != "Volcán" else "Lava")
                else:
                    row.append(base_biome)
            grid.append(row)
            
        return {"grid": grid, "biome": base_biome}

class SpatialDao:
    def __init__(self, map_manager):
        self.map = map_manager

    def devour_area(self, player, radius=1):
        """
        Técnica Prohibida: Convierte el área en Abismo Espacial.
        """
        # Requisito de Cultivo (Simulado: Dao > 0)
        if player.stats.get("dao_espacial", 0) <= 0 and player.stats["qi"] < 1000:
            return False, "Tu comprensión espacial es insuficiente."

        px, py = player.location # [x, y]
        
        count = 0
        for y in range(py - radius, py + radius + 1):
            for x in range(px - radius, px + radius + 1):
                current = self.map.get_tile_info(x, y)
                if current != VOID_TILE:
                    self.map.set_tile(x, y, VOID_TILE)
                    count += 1
                    
        return True, f"Has devorado {count} casillas de realidad. El vacío se abre."

    def teleport(self, player, tx, ty):
        # Distancia Euclídea
        dist = math.sqrt((tx - player.location[0])**2 + (ty - player.location[1])**2)
        cost = int(dist * 2) # 2 Qi por metro
        
        if player.stats["qi"] >= cost:
            player.stats["qi"] -= cost
            player.location = [tx, ty]
            return True, f"Saltaste a {tx}, {ty}. (-{cost} Qi)"
        return False, f"Qi insuficiente. Costo: {cost}"

class PortalManager:
    def __init__(self):
        self.active_portals = []

    def create_dungeon_portal(self, x, y, rank):
        portal = {
            "type": "Dungeon",
            "location": (x, y),
            "name": f"Tumba Antigua G{rank}",
            "ttl": 24, # Horas de vida
            "reward_mult": 2.0
        }
        self.active_portals.append(portal)
        return portal