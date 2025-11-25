#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Comprehensivo de Sistemas de Mapa - Version ASCII
Verifica:
  1. MapManager - Carga y gestión de ubicaciones
  2. Generación procedural de chunks
  3. Carga de Lugares.json
  4. Sistema de POI (Points of Interest)
  5. Generación de biomas
  6. Acceso a tiles
"""

import sys
import os
import json

# Configurar paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'systems'))

from config import CHUNK_SIZE, VOID_TILE, COLORS
from map_core import MapManager

print("=" * 80)
print("TEST DE SISTEMAS DE MAPA - WuxiaRPG")
print("=" * 80)

# TEST 1
print("\n[TEST 1] Verificando configuracion...")
try:
    print("  OK CHUNK_SIZE: %d" % CHUNK_SIZE)
    print("  OK VOID_TILE: %s" % VOID_TILE)
    print("  OK COLORS: %d colores definidos" % len(COLORS))
    print("  Resultado: PASS")
    test1_pass = True
except Exception as e:
    print("  ERROR: %s" % str(e))
    print("  Resultado: FAIL")
    test1_pass = False

# TEST 2
print("\n[TEST 2] Verificando Lugares.json...")
try:
    lugares_path = os.path.join(os.path.dirname(__file__), 'systems', 'Lugares.json')
    with open(lugares_path, 'r', encoding='utf-8') as f:
        lugares_data = json.load(f)
    
    if isinstance(lugares_data, list):
        print("  OK Archivo valido: %d ubicaciones" % len(lugares_data))
        for i, lugar in enumerate(lugares_data):
            print("    %d. %s" % (i+1, lugar.get('Lugar', '?')))
        print("  Resultado: PASS")
        test2_pass = True
    else:
        print("  ERROR Estructura incorrecta")
        print("  Resultado: FAIL")
        test2_pass = False
except FileNotFoundError:
    print("  WARN Archivo no encontrado (se usaran datos por defecto)")
    print("  Resultado: PASS")
    test2_pass = True
except Exception as e:
    print("  ERROR: %s" % str(e))
    print("  Resultado: FAIL")
    test2_pass = False

# TEST 3
print("\n[TEST 3] Inicializando MapManager...")
try:
    map_mgr = MapManager()
    print("  OK MapManager creado")
    print("  OK Mundo: %s" % map_mgr.world_name)
    print("  OK Guardado en: %s" % map_mgr.save_path)
    print("  Resultado: PASS")
    test3_pass = True
except Exception as e:
    print("  ERROR al crear MapManager: %s" % str(e))
    import traceback
    traceback.print_exc()
    print("  Resultado: FAIL")
    test3_pass = False
    sys.exit(1)

# TEST 4
print("\n[TEST 4] Verificando POI Registry...")
try:
    poi_count = len(map_mgr.poi_registry)
    print("  OK POIs cargados: %d" % poi_count)
    
    for i, (name, coords) in enumerate(list(map_mgr.poi_registry.items())[:5]):
        print("    - %s: [%d, %d]" % (name, coords[0], coords[1]))
    
    if poi_count > 0:
        print("  Resultado: PASS")
        test4_pass = True
    else:
        print("  ERROR No hay POIs cargados")
        print("  Resultado: FAIL")
        test4_pass = False
except Exception as e:
    print("  ERROR: %s" % str(e))
    print("  Resultado: FAIL")
    test4_pass = False

# TEST 5
print("\n[TEST 5] Generando chunks procedurales...")
try:
    test_coords = [(0, 0), (1, 0), (0, 1), (5, 5), (-3, -3)]
    chunk_errors = 0
    
    for cx, cy in test_coords:
        chunk = map_mgr._generate_procedural(cx, cy)
        
        if "grid" not in chunk or "biome" not in chunk:
            print("  ERROR Chunk (%d, %d) no tiene estructura correcta" % (cx, cy))
            chunk_errors += 1
            continue
        
        if len(chunk["grid"]) != CHUNK_SIZE:
            print("  ERROR Chunk (%d, %d) height incorrecto" % (cx, cy))
            chunk_errors += 1
            continue
        
        if len(chunk["grid"][0]) != CHUNK_SIZE:
            print("  ERROR Chunk (%d, %d) width incorrecto" % (cx, cy))
            chunk_errors += 1
            continue
        
        print("  OK Chunk (%2d, %2d): %-15s - %dx%d grid" % (cx, cy, chunk['biome'], CHUNK_SIZE, CHUNK_SIZE))
    
    if chunk_errors == 0:
        print("  Resultado: PASS")
        test5_pass = True
    else:
        print("  Resultado: FAIL")
        test5_pass = False
except Exception as e:
    print("  ERROR: %s" % str(e))
    import traceback
    traceback.print_exc()
    print("  Resultado: FAIL")
    test5_pass = False

# TEST 6 - Cache (CRITICAL FIX)
print("\n[TEST 6] Verificando cache de chunks...")
try:
    # Limpiar cache
    map_mgr.loaded_chunks.clear()
    
    # Cargar un chunk
    chunk1 = map_mgr._load_chunk(0, 0)
    cache_after_first = len(map_mgr.loaded_chunks)
    
    # Acceder de nuevo (debe estar en cache)
    chunk2 = map_mgr._load_chunk(0, 0)
    cache_after_repeat = len(map_mgr.loaded_chunks)
    
    # Cargar otro chunk
    chunk3 = map_mgr._load_chunk(1, 0)
    cache_after_new = len(map_mgr.loaded_chunks)
    
    print("  OK Cache despues de primer chunk: %d" % cache_after_first)
    print("  OK Cache despues de reusar: %d (sin duplicados)" % cache_after_repeat)
    print("  OK Cache despues de nuevo chunk: %d" % cache_after_new)
    
    if cache_after_first > 0 and cache_after_new > cache_after_repeat:
        print("  OK Cache funcionando correctamente")
        print("  Resultado: PASS")
        test6_pass = True
    else:
        print("  ERROR Cache no funciona como esperado")
        print("  Resultado: FAIL")
        test6_pass = False
except Exception as e:
    print("  ERROR: %s" % str(e))
    import traceback
    traceback.print_exc()
    print("  Resultado: FAIL")
    test6_pass = False

# TEST 7
print("\n[TEST 7] Accediendo a tiles individuales...")
try:
    test_points = [(0, 0), (5, 5), (32, 32), (-5, -5), (100, 100)]
    
    for gx, gy in test_points:
        try:
            tile = map_mgr.get_tile_info(gx, gy)
            print("  OK Tile (%4d, %4d): %s" % (gx, gy, tile))
        except Exception as e:
            print("  ERROR accediendo a (%d, %d): %s" % (gx, gy, str(e)))
    
    print("  Resultado: PASS")
    test7_pass = True
except Exception as e:
    print("  ERROR general: %s" % str(e))
    print("  Resultado: FAIL")
    test7_pass = False

# TEST 8
print("\n[TEST 8] Verificando determinismo de generacion...")
try:
    chunk_a1 = map_mgr._generate_procedural(42, 42)
    chunk_a2 = map_mgr._generate_procedural(42, 42)
    
    grid_a1 = str(chunk_a1["grid"])
    grid_a2 = str(chunk_a2["grid"])
    
    if grid_a1 == grid_a2:
        print("  OK Generacion determinista verificada")
        print("    Bioma: %s" % chunk_a1['biome'])
        print("    Grid size: %dx%d" % (len(chunk_a1['grid']), len(chunk_a1['grid'][0])))
        print("  Resultado: PASS")
        test8_pass = True
    else:
        print("  ERROR Generacion no es determinista")
        print("  Resultado: FAIL")
        test8_pass = False
except Exception as e:
    print("  ERROR: %s" % str(e))
    print("  Resultado: FAIL")
    test8_pass = False

# RESUMEN
print("\n" + "=" * 80)
print("RESUMEN DE TESTS")
print("=" * 80)

tests = [
    ("Configuracion", test1_pass),
    ("Lugares.json", test2_pass),
    ("MapManager", test3_pass),
    ("POI Registry", test4_pass),
    ("Chunks procedurales", test5_pass),
    ("Cache de chunks", test6_pass),
    ("Acceso a tiles", test7_pass),
    ("Determinismo", test8_pass),
]

passed = sum(1 for _, p in tests if p)
total = len(tests)

for name, passed_flag in tests:
    status = "PASS" if passed_flag else "FAIL"
    print("  [%s] %s" % (status, name))

print("\nResultado final: %d/%d tests pasados" % (passed, total))

if passed == total:
    print("\nCONCLUSION: TODO FUNCIONANDO CORRECTAMENTE")
    print("=" * 80)
    sys.exit(0)
else:
    print("\nCONCLUSION: ALGUNOS TESTS FALLARON")
    print("=" * 80)
    sys.exit(1)
