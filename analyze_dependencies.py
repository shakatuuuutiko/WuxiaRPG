#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Exhaustivo de Vinculaciones Entre Archivos
Mapea qué archivo usa qué y detecta problemas
"""

import os
import re
from collections import defaultdict

# Directorio del proyecto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Archivos a analizar
PYTHON_FILES = []
for root, dirs, files in os.walk(PROJECT_ROOT):
    # Excluir __pycache__ y otros directorios innecesarios
    dirs[:] = [d for d in dirs if d != '__pycache__' and d not in ['.git', '.venv', 'env']]
    
    for file in files:
        if file.endswith('.py') and not file.startswith('test_'):
            path = os.path.join(root, file)
            PYTHON_FILES.append(path)

print("=" * 80)
print("ANÁLISIS DE VINCULACIONES ENTRE ARCHIVOS - WuxiaRPG")
print("=" * 80)
print(f"\nArchivos encontrados: {len(PYTHON_FILES)}\n")

# Mapas de dependencias
imports_map = defaultdict(list)  # archivo -> lista de imports
imported_by = defaultdict(list)  # módulo -> lista de archivos que lo importan

# Procesar cada archivo
for file_path in sorted(PYTHON_FILES):
    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        continue
    
    # Extraer todos los imports
    # Patrón: from X import Y o import X
    import_patterns = [
        r'^from\s+([\w\.]+)\s+import',
        r'^import\s+([\w\.]+)'
    ]
    
    imports_found = set()
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            continue
        
        for pattern in import_patterns:
            match = re.match(pattern, line)
            if match:
                module = match.group(1)
                imports_found.add(module)
    
    if imports_found:
        imports_map[rel_path] = sorted(list(imports_found))

# Crear mapa de quién importa a quién (solo archivos internos)
internal_modules = {
    'config': 'config.py',
    'systems.map_core': 'systems/map_core.py',
    'systems.crafting': 'systems/crafting.py',
    'systems.equipment': 'systems/equipment.py',
    'systems.combat': 'systems/combat.py',
    'systems.companion': 'systems/companion.py',
    'systems.creature_gen': 'systems/creature_gen.py',
    'systems.time_system': 'systems/time_system.py',
    'systems.cultivation': 'systems/cultivation.py',
    'systems.bloodline': 'systems/bloodline.py',
    'systems.origin_generator': 'systems/origin_generator.py',
    'systems.artifact_spirit': 'systems/artifact_spirit.py',
    'systems.manual_system': 'systems/manual_system.py',
    'systems.resource_gen_v2': 'systems/resource_gen_v2.py',
    'systems.slave_mgmt': 'systems/slave_mgmt.py',
    'systems.social_ai': 'systems/social_ai.py',
    'systems.sect_politics': 'systems/sect_politics.py',
    'systems.tournament': 'systems/tournament.py',
    'ui.game_engine': 'ui/game_engine.py',
    'ui.main_menu': 'ui/main_menu.py',
    'ui.pygame_renderer': 'ui/pygame_renderer.py',
    'ui.pygame_utils': 'ui/pygame_utils.py',
    'ui.map_render': 'ui/map_render.py',
    'ui.panels': 'ui/panels.py',
    'ui.popups': 'ui/popups.py',
    'data.beast_db_massive': 'data/beast_db_massive.py',
    'data.items_db': 'data/items_db.py',
    'main': 'main.py'
}

# Mapear imports
for file_path, imports in imports_map.items():
    for imp in imports:
        # Buscar módulos internos
        for mod_key, mod_file in internal_modules.items():
            if imp == mod_key or imp.startswith(mod_key + '.'):
                imported_by[mod_key].append(file_path)
                break

print("=" * 80)
print("DEPENDENCIAS INTERNAS (Imports entre archivos del proyecto)")
print("=" * 80)

# Mostrar cada archivo y sus dependencias
print("\n[ARCHIVO] → [Depende de]\n")
for file_path in sorted(imports_map.keys()):
    imports = imports_map[file_path]
    
    # Filtrar solo imports internos
    internal_imports = []
    for imp in imports:
        for mod_key in internal_modules.keys():
            if imp == mod_key or imp.startswith(mod_key + '.'):
                internal_imports.append(imp)
                break
    
    if internal_imports:
        print(f"{file_path}")
        for imp in sorted(internal_imports):
            target_file = internal_modules.get(imp, '?')
            status = "✓" if target_file in [os.path.relpath(p, PROJECT_ROOT) for p in PYTHON_FILES] else "✗"
            print(f"  {status} → {imp:40} ({target_file})")
        print()

print("\n" + "=" * 80)
print("IMPORTADO POR (Qué archivos usan cada módulo)")
print("=" * 80)

print("\n[MÓDULO] ← [Usado por]\n")
for mod_key in sorted(internal_modules.keys()):
    users = imported_by.get(mod_key, [])
    if users:
        print(f"{mod_key}")
        for user in sorted(set(users)):
            print(f"  ← {user}")
        print()

print("\n" + "=" * 80)
print("ANÁLISIS DE PROBLEMAS")
print("=" * 80)

# Detectar circular dependencies
print("\n[BUSCANDO CIRCULAR DEPENDENCIES]\n")

def has_circular_dependency(start_file, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    if start_file in visited:
        return path + [start_file]
    
    visited.add(start_file)
    path.append(start_file)
    
    # Obtener imports del archivo
    imports = imports_map.get(start_file, [])
    
    for imp in imports:
        # Buscar archivo que corresponde a este import
        for mod_key, mod_file in internal_modules.items():
            if imp == mod_key or imp.startswith(mod_key + '.'):
                mod_rel_path = os.path.relpath(os.path.join(PROJECT_ROOT, mod_file), PROJECT_ROOT)
                
                if mod_rel_path in visited:
                    cycle = path + [mod_rel_path]
                    return cycle
    
    visited.remove(start_file)
    path.pop()
    return None

circular_deps = []
for file_path in imports_map.keys():
    cycle = has_circular_dependency(file_path)
    if cycle:
        circular_deps.append(cycle)

if circular_deps:
    print("⚠ CIRCULAR DEPENDENCIES DETECTADAS:\n")
    for cycle in circular_deps:
        print(f"  {' → '.join(cycle)} → {cycle[0]}")
else:
    print("✓ No hay circular dependencies detectadas")

# Detectar imports rotos
print("\n\n[BUSCANDO IMPORTS ROTOS]\n")

broken_imports = []
for file_path, imports in imports_map.items():
    for imp in imports:
        # Revisar si es un import interno roto
        found = False
        for mod_key in internal_modules.keys():
            if imp == mod_key or imp.startswith(mod_key + '.'):
                found = True
                target_file = internal_modules[mod_key]
                full_path = os.path.join(PROJECT_ROOT, target_file)
                if not os.path.exists(full_path):
                    broken_imports.append((file_path, imp, target_file))
                break

if broken_imports:
    print("✗ IMPORTS ROTOS ENCONTRADOS:\n")
    for file_path, imp, target in broken_imports:
        print(f"  {file_path}")
        print(f"    → intenta importar: {imp}")
        print(f"    → esperaría archivo: {target}")
        print()
else:
    print("✓ Todos los imports internos apuntan a archivos que existen")

# Archivos no importados
print("\n[ARCHIVOS NO USADOS]")
print("\nArchivos que NO son importados por nadie (orphans):\n")

for file_path in sorted(imports_map.keys()):
    # Buscar si este archivo es importado por alguien
    is_imported = False
    for users in imported_by.values():
        if file_path in users:
            is_imported = True
            break
    
    # También verificar si es main.py o test
    if file_path == 'main.py' or 'test_' in file_path:
        is_imported = True
    
    if not is_imported:
        print(f"  ⚠ {file_path}")

print("\n" + "=" * 80)
print("ESTADÍSTICAS")
print("=" * 80)

total_files = len(imports_map)
files_with_internal_deps = len([f for f in imports_map.values() if any(
    any(imp == mod_key or imp.startswith(mod_key + '.') for mod_key in internal_modules.keys())
    for imp in f
)])

print(f"""
Total archivos Python (excluye tests): {total_files}
Archivos con dependencias internas: {files_with_internal_deps}
Módulos internos definidos: {len(internal_modules)}
Circular dependencies: {len(circular_deps)}
Imports rotos: {len(broken_imports)}
""")

print("=" * 80)
print("FIN DEL ANÁLISIS")
print("=" * 80)
