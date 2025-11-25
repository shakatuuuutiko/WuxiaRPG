#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUIA DE INTEGRACION - Generador Procedural de Lugares
Como usar el sistema de ubicaciones procedurales en el juego
"""

# ============================================================================
# EJEMPLO 1: CARGAR UBICACIONES EN game_engine.py
# ============================================================================

def load_locations():
    """Cargar ubicaciones procedurales en el motor de juego."""
    import json
    import os
    
    # Cargar archivo de ubicaciones
    sistemas_dir = os.path.join(os.path.dirname(__file__), 'systems')
    locations_file = os.path.join(sistemas_dir, 'Lugares.json')
    
    with open(locations_file, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    # Ahora 'locations' contiene lista de 15 lugares procedurales
    return locations

# Uso en game_engine.py:
# 
# class GameEngine:
#     def __init__(self):
#         self.locations = load_locations()
#         self.location_map = {loc['Lugar']: loc for loc in self.locations}


# ============================================================================
# EJEMPLO 2: ACCEDER A UBICACIONES POR NOMBRE
# ============================================================================

def get_location_info(location_name, game_engine):
    """Obtener información de una ubicación."""
    
    if location_name in game_engine.location_map:
        location = game_engine.location_map[location_name]
        return {
            'nombre': location['Lugar'],
            'tipo': location['tipo'],
            'nivel': location['nivel'],
            'npcs': location['NPCs'],
            'descripcion': location['descripcion'],
            'coordenadas': location['coordenadas'],
        }
    else:
        return None

# Uso:
# info = get_location_info("Aldea Montañoso en el Valle", game_engine)
# if info:
#     print(f"Tipo: {info['tipo']}, Nivel: {info['nivel']}")


# ============================================================================
# EJEMPLO 3: FILTRAR UBICACIONES POR TIPO
# ============================================================================

def get_locations_by_type(location_type, game_engine):
    """Obtener todas las ubicaciones de un tipo específico."""
    return [loc for loc in game_engine.locations if loc['tipo'] == location_type]

# Uso:
# pueblos = get_locations_by_type('pueblo', game_engine)
# print(f"Hay {len(pueblos)} pueblos disponibles")
# 
# dungeons = get_locations_by_type('dungeon', game_engine)
# for dungeon in dungeons:
#     print(f"{dungeon['Lugar']} (Nivel {dungeon['nivel']})")


# ============================================================================
# EJEMPLO 4: OBTENER UBICACION CERCANA POR COORDENADAS
# ============================================================================

def find_nearest_location(x, y, game_engine, radius=500):
    """Encontrar ubicación más cercana dentro de radio."""
    import math
    
    nearest = None
    min_distance = float('inf')
    
    for location in game_engine.locations:
        loc_x, loc_y = location['coordenadas']
        distance = math.sqrt((loc_x - x) ** 2 + (loc_y - y) ** 2)
        
        if distance <= radius and distance < min_distance:
            min_distance = distance
            nearest = location
    
    return nearest

# Uso:
# player_x, player_y = 100, 200
# nearest = find_nearest_location(player_x, player_y, game_engine, radius=500)
# if nearest:
#     print(f"Ubicación cercana: {nearest['Lugar']} a {math.sqrt(...)} tiles")


# ============================================================================
# EJEMPLO 5: OBTENER NPCs DE UNA UBICACION
# ============================================================================

def get_npcs_at_location(location_name, game_engine):
    """Obtener lista de NPCs en una ubicación."""
    location = game_engine.location_map.get(location_name)
    if location:
        return location['NPCs']
    return []

# Uso:
# npcs = get_npcs_at_location("Santuario Dorado Bajo Tierra", game_engine)
# for npc in npcs:
#     print(f"NPC: {npc}")


# ============================================================================
# EJEMPLO 6: GENERAR NUEVAS UBICACIONES
# ============================================================================

def regenerate_world(seed=None):
    """Regenerar mundo con nuevas ubicaciones."""
    from systems.location_generator import LocationGenerator
    import json
    import os
    
    # Crear generador
    gen = LocationGenerator(seed=seed)
    
    # Generar ubicaciones
    locations = gen.generar_multiples(15)
    
    # Guardar
    sistemas_dir = os.path.join(os.path.dirname(__file__), 'systems')
    locations_file = os.path.join(sistemas_dir, 'Lugares.json')
    
    with open(locations_file, 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)
    
    print(f"Mundo regenerado: {len(locations)} ubicaciones")
    return locations

# Uso en menú:
# if menu_option == 'NEW_GAME':
#     new_world = regenerate_world(seed=None)  # Mundo aleatorio
# 
# if menu_option == 'LOAD_SPECIFIC_WORLD':
#     specific_world = regenerate_world(seed=12345)  # Mundo específico


# ============================================================================
# EJEMPLO 7: INTEGRACION CON MapManager
# ============================================================================

def update_mapmanager_with_locations(game_engine):
    """Actualizar MapManager con ubicaciones procedurales."""
    from systems.map_core import MapManager
    
    manager = MapManager()
    
    # Verificar que POIs están registrados
    print(f"POIs en registry: {len(manager.poi_registry)}")
    
    # Verificar específica
    for location in game_engine.locations[:5]:
        name = location['Lugar']
        if name in manager.poi_registry:
            coords = manager.poi_registry[name]
            print(f"✓ {name}: {coords}")
    
    return manager

# Uso:
# manager = update_mapmanager_with_locations(game_engine)
# tile_info = manager.get_tile_info(100, 200)


# ============================================================================
# EJEMPLO 8: MOSTRAR INFO DE UBICACION AL JUGADOR
# ============================================================================

def display_location_info(location):
    """Mostrar información de ubicación de forma amigable."""
    
    info = f"""
╔═════════════════════════════════════════════════════╗
║ {location['Lugar']:^45} ║
╠═════════════════════════════════════════════════════╣
║ Tipo:        {location['tipo']:<35} ║
║ Nivel:       {location['nivel']:<35} ║
║ Coordenadas: {str(location['coordenadas']):<35} ║
╠═════════════════════════════════════════════════════╣
║ Residentes:                                         ║
""" 
    for npc in location['NPCs']:
        info += f"║  • {npc:<43} ║\n"
    
    info += f"""╠═════════════════════════════════════════════════════╣
║ {location['descripcion']:<45} ║
╚═════════════════════════════════════════════════════╝
"""
    return info

# Uso:
# location = game_engine.location_map["Aldea Montañoso en el Valle"]
# print(display_location_info(location))


# ============================================================================
# EJEMPLO 9: ESTADISTICAS DE MUNDO
# ============================================================================

def get_world_statistics(game_engine):
    """Obtener estadísticas del mundo generado."""
    stats = {
        'total_locations': len(game_engine.locations),
        'by_type': {},
        'avg_level': 0,
        'total_npcs': 0,
    }
    
    for location in game_engine.locations:
        # Por tipo
        tipo = location['tipo']
        stats['by_type'][tipo] = stats['by_type'].get(tipo, 0) + 1
        
        # Promedio nivel
        stats['avg_level'] += location['nivel']
        
        # Total NPCs
        stats['total_npcs'] += len(location['NPCs'])
    
    stats['avg_level'] /= len(game_engine.locations)
    
    return stats

# Uso:
# stats = get_world_statistics(game_engine)
# print(f"Mundo: {stats['total_locations']} ubicaciones")
# print(f"Nivel promedio: {stats['avg_level']:.1f}")
# print(f"Total NPCs: {stats['total_npcs']}")
# for tipo, count in stats['by_type'].items():
#     print(f"  {tipo}: {count}")


# ============================================================================
# EJEMPLO 10: QUESTS PROCEDURALES BASADAS EN UBICACIONES
# ============================================================================

import random

def generate_location_quests(location, game_engine):
    """Generar quests procedurales basadas en ubicación."""
    
    quests = []
    
    # Quest 1: Resolver problema local
    problems = {
        'pueblo': [
            f"Bandidos atacan {location['Lugar']}",
            f"Cultivo arruinado en {location['Lugar']}",
            f"Bestias arengan {location['Lugar']}",
        ],
        'ciudad': [
            f"Crimen organizado en {location['Lugar']}",
            f"Corrupción en {location['Lugar']}",
            f"Intriga política en {location['Lugar']}",
        ],
        'secta': [
            f"Ritual prohibido en {location['Lugar']}",
            f"Traidor en {location['Lugar']}",
            f"Poder oscuro despierta en {location['Lugar']}",
        ],
        'templo': [
            f"Reliquia perdida en {location['Lugar']}",
            f"Sacrilegio en {location['Lugar']}",
            f"Bendición perdida en {location['Lugar']}",
        ],
        'dungeon': [
            f"Tesoro en {location['Lugar']}",
            f"Bestia ancestral en {location['Lugar']}",
            f"Maldición en {location['Lugar']}",
        ],
    }
    
    tipo = location['tipo']
    if tipo in problems:
        quest_name = random.choice(problems[tipo])
        reward = location['nivel'] * 10
        quests.append({
            'name': quest_name,
            'location': location['Lugar'],
            'level': location['nivel'],
            'reward': reward,
        })
    
    return quests

# Uso:
# for location in game_engine.locations:
#     quests = generate_location_quests(location, game_engine)
#     for quest in quests:
#         print(f"Quest: {quest['name']} (Nivel {quest['level']}, Recompensa: {quest['reward']})")


# ============================================================================
# INTEGRACION EN game_engine.py
# ============================================================================

"""
PASO A PASO DE INTEGRACION:

1. En __init__ de GameEngine:
   
   def __init__(self):
       self.locations = load_locations()
       self.location_map = {loc['Lugar']: loc for loc in self.locations}
       self.current_location = self.locations[0]

2. En métodos de movimiento:
   
   def move_to_location(self, location_name):
       if location_name in self.location_map:
           self.current_location = self.location_map[location_name]
           coords = self.current_location['coordenadas']
           self.map_manager.load_chunk(coords[0] // 32, coords[1] // 32)
           return True
       return False

3. En interface de juego:
   
   def show_current_location(self):
       print(display_location_info(self.current_location))

4. En menú de viaje:
   
   def show_locations_menu(self):
       for i, loc in enumerate(self.locations):
           print(f"{i}. {loc['Lugar']} (Nivel {loc['nivel']})")

5. En guardado de juego:
   
   def save_game(self, filename):
       game_data = {
           'player': self.player_data,
           'current_location': self.current_location['Lugar'],
           'world_seed': self.world_seed,  # Para persistencia
       }
       save_json(game_data, filename)
"""

if __name__ == "__main__":
    print("Este archivo es una guía de integración.")
    print("No ejecutar directamente. Incluir en game_engine.py")
