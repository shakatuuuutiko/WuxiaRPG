#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('systems/Lugares.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)

print("\n" + "=" * 80)
print("UBICACIONES PROCEDURALES GENERADAS - RESUMEN FINAL")
print("=" * 80)

by_type = {}
for loc in locations:
    tipo = loc['tipo']
    if tipo not in by_type:
        by_type[tipo] = []
    by_type[tipo].append(loc)

for tipo in sorted(by_type.keys()):
    locs = by_type[tipo]
    print(f"\n{tipo.upper()} ({len(locs)}):")
    for loc in locs:
        npcs_str = ", ".join(loc['NPCs'][:2])
        if len(loc['NPCs']) > 2:
            npcs_str += f"... (+{len(loc['NPCs']) - 2})"
        print(f"  • {loc['Lugar']} (Nivel {loc['nivel']})")
        print(f"    NPCs: {npcs_str}")
        print(f"    Coordenadas: {loc['coordenadas']}")

print("\n" + "=" * 80)
print(f"TOTAL: {len(locations)} ubicaciones generadas proceduralmente")
print("=" * 80 + "\n")
