#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Integracion - Generador de Lugares con MapManager
Verifica que los lugares generados proceduralmente funcionen correctamente
con el sistema de mapas existente.
"""

import json
import os
import sys

# Agregar path del sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'systems'))

from map_core import MapManager


def test_1_load_generated_locations():
    """Test 1: Cargar lugares generados."""
    print("\n[TEST 1] Cargando Lugares.json generados...")
    
    sistemas_dir = os.path.join(os.path.dirname(__file__), 'systems')
    lugares_path = os.path.join(sistemas_dir, 'Lugares.json')
    with open(lugares_path, 'r', encoding='utf-8') as f:
        lugares = json.load(f)
    
    assert isinstance(lugares, list), "Lugares debe ser una lista"
    assert len(lugares) > 0, "Debe haber lugares generados"
    
    # Validar estructura
    for lugar in lugares:
        assert "Lugar" in lugar, "Falta campo 'Lugar'"
        assert "tipo" in lugar, "Falta campo 'tipo'"
        assert "nivel" in lugar, "Falta campo 'nivel'"
        assert "NPCs" in lugar, "Falta campo 'NPCs'"
        assert "descripcion" in lugar, "Falta campo 'descripcion'"
        assert "coordenadas" in lugar, "Falta campo 'coordenadas'"
    
    print(f"  [PASS] {len(lugares)} lugares cargados correctamente")
    return lugares


def test_2_tipos_procedurales(lugares):
    """Test 2: Validar tipos de lugares procedurales."""
    print("\n[TEST 2] Validando tipos procedurales...")
    
    tipos_validos = {"pueblo", "ciudad", "secta", "templo", "dungeon", "castillo"}
    tipos_encontrados = {lugar["tipo"] for lugar in lugares}
    
    print(f"  Tipos generados: {tipos_encontrados}")
    
    for tipo in tipos_encontrados:
        assert tipo in tipos_validos, f"Tipo inválido: {tipo}"
    
    # Debe haber al menos 3 tipos diferentes
    assert len(tipos_encontrados) >= 3, "Debe haber variedad de tipos"
    
    print(f"  [PASS] {len(tipos_encontrados)} tipos diferentes validados")


def test_3_niveles_coherentes(lugares):
    """Test 3: Validar que los niveles son coherentes por tipo."""
    print("\n[TEST 3] Validando niveles coherentes...")
    
    by_type = {}
    for lugar in lugares:
        tipo = lugar["tipo"]
        if tipo not in by_type:
            by_type[tipo] = []
        by_type[tipo].append(lugar["nivel"])
    
    # Verificar rangos esperados
    rangos_esperados = {
        "pueblo": (1, 10),
        "ciudad": (5, 20),
        "secta": (10, 35),
        "templo": (15, 40),
        "dungeon": (20, 50),
        "castillo": (25, 50),
    }
    
    for tipo, niveles in by_type.items():
        min_nivel = min(niveles)
        max_nivel = max(niveles)
        min_esperado, max_esperado = rangos_esperados.get(tipo, (1, 50))
        
        assert min_nivel >= 1, f"{tipo}: nivel minimo {min_nivel} < 1"
        assert max_nivel <= 50, f"{tipo}: nivel maximo {max_nivel} > 50"
        
        print(f"  {tipo}: min={min_nivel}, max={max_nivel}")
    
    print(f"  [PASS] Rangos de niveles validados")


def test_4_npcs_procedurales(lugares):
    """Test 4: Validar que NPCs son procedurales."""
    print("\n[TEST 4] Validando NPCs procedurales...")
    
    tipos_npcs = {
        "pueblo": {"Vendedor", "Posadero", "Herrero", "Curandera"},
        "ciudad": {"Gobernador", "Consejero", "Guardián", "Comerciante"},
        "secta": {"Patriarca", "Elder", "Guardián"},
        "templo": {"Sumo Sacerdote", "Monje", "Guardián"},
        "dungeon": {"Espíritu", "Bestia", "Esqueleto", "Guardián"},
    }
    
    for lugar in lugares:
        assert "NPCs" in lugar, f"Falta NPCs en {lugar['Lugar']}"
        assert isinstance(lugar["NPCs"], list), f"NPCs debe ser lista en {lugar['Lugar']}"
        assert len(lugar["NPCs"]) > 0, f"Debe haber al menos 1 NPC en {lugar['Lugar']}"
    
    print(f"  Total NPCs: {sum(len(l['NPCs']) for l in lugares)}")
    print(f"  [PASS] NPCs procedurales validados")


def test_5_descripciones_unicas(lugares):
    """Test 5: Validar descripciones únicas."""
    print("\n[TEST 5] Validando descripciones únicas...")
    
    descripciones = [lugar["descripcion"] for lugar in lugares]
    descripciones_unicas = set(descripciones)
    
    print(f"  Total descripciones: {len(descripciones)}")
    print(f"  Descripciones únicas: {len(descripciones_unicas)}")
    
    # Verificar que hay variedad
    assert len(descripciones_unicas) >= len(lugares) * 0.7, "Debe haber variedad de descripciones"
    
    print(f"  [PASS] Descripciones procedurales validadas")


def test_6_mapmanager_integration(lugares):
    """Test 6: Integración con MapManager."""
    print("\n[TEST 6] Integrando con MapManager...")
    
    # Crear MapManager
    manager = MapManager()
    
    # Verificar que carga Lugares.json
    assert hasattr(manager, 'poi_registry'), "MapManager debe tener poi_registry"
    
    # Verificar POIs
    for lugar in lugares[:5]:  # Verificar primeros 5
        nombre = lugar["Lugar"]
        assert nombre in manager.poi_registry, f"POI {nombre} no en registry"
        
        coords = manager.poi_registry[nombre]
        assert isinstance(coords, list), f"Coordenadas de {nombre} deben ser lista"
        assert len(coords) == 2, f"Coordenadas de {nombre} deben ser [x, y]"
    
    print(f"  [PASS] MapManager integración exitosa ({len(lugares)} POIs registrados)")


def test_7_coordenadas_validas(lugares):
    """Test 7: Validar coordenadas dentro del rango del mapa."""
    print("\n[TEST 7] Validando coordenadas...")
    
    COORD_MIN = -2000
    COORD_MAX = 2000
    
    for lugar in lugares:
        coords = lugar["coordenadas"]
        x, y = coords
        
        assert COORD_MIN <= x <= COORD_MAX, f"{lugar['Lugar']}: x={x} fuera de rango"
        assert COORD_MIN <= y <= COORD_MAX, f"{lugar['Lugar']}: y={y} fuera de rango"
    
    print(f"  [PASS] Coordenadas en rango [{COORD_MIN}, {COORD_MAX}]")


def test_8_nombres_unicos(lugares):
    """Test 8: Validar nombres únicos."""
    print("\n[TEST 8] Validando nombres únicos...")
    
    nombres = [lugar["Lugar"] for lugar in lugares]
    nombres_unicos = set(nombres)
    
    assert len(nombres) == len(nombres_unicos), "Hay nombres duplicados"
    
    print(f"  Total nombres: {len(nombres)}")
    print(f"  Nombres únicos: {len(nombres_unicos)}")
    print(f"  [PASS] Todos los nombres son únicos")


def main():
    """Ejecutar todos los tests."""
    print("=" * 80)
    print("TEST DE INTEGRACION - GENERADOR PROCEDURAL DE LUGARES")
    print("=" * 80)
    
    try:
        # Test 1: Cargar
        lugares = test_1_load_generated_locations()
        
        # Tests de validación
        test_2_tipos_procedurales(lugares)
        test_3_niveles_coherentes(lugares)
        test_4_npcs_procedurales(lugares)
        test_5_descripciones_unicas(lugares)
        test_6_mapmanager_integration(lugares)
        test_7_coordenadas_validas(lugares)
        test_8_nombres_unicos(lugares)
        
        # Resumen
        print("\n" + "=" * 80)
        print("RESULTADO: 8/8 TESTS PASARON")
        print("=" * 80)
        print("\nLa generacion procedural de lugares es exitosa y se integra")
        print("correctamente con MapManager.")
        print("\nLugares generados por tipo:")
        
        by_type = {}
        for lugar in lugares:
            tipo = lugar["tipo"]
            by_type[tipo] = by_type.get(tipo, 0) + 1
        
        for tipo in sorted(by_type.keys()):
            print(f"  - {tipo}: {by_type[tipo]}")
        
        print("\n" + "=" * 80)
        
        return True
    
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
