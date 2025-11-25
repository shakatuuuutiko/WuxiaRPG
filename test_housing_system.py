#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Completo del Sistema de Housing
Verifica construcción, compra, materiales y efectos
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'systems'))

from housing_system import (
    HousingSystem, HousingType, HousingStatus,
    obtener_materiales_disponibles, obtener_requisitos_casa,
    listar_tipos_casas, HOUSING_REQUIREMENTS
)


def test_1_sistema_inicializa():
    """Test 1: Sistema se inicializa correctamente."""
    print("\n[TEST 1] Inicializando sistema de housing...")
    
    system = HousingSystem("systems")
    assert system is not None, "Sistema no se inicializó"
    assert len(system.materiales) > 0, "No se cargaron materiales"
    
    print(f"  ✓ Sistema inicializado")
    print(f"  ✓ {len(system.materiales)} materiales cargados")
    
    return system


def test_2_construir_casa(system):
    """Test 2: Construir una casa."""
    print("\n[TEST 2] Construyendo casa pequeña...")
    
    success, result = system.construir_casa("player_1", HousingType.PEQUEÑA, [100, 200])
    assert success, "No se pudo construir la casa"
    assert "house_id" in result, "No se retornó ID de casa"
    
    house_id = result["house_id"]
    print(f"  ✓ Casa creada: {house_id}")
    print(f"  ✓ Ubicación: {result['ubicacion']}")
    print(f"  ✓ Materiales requeridos: {list(result['materiales_requeridos'].keys())}")
    
    return house_id


def test_3_agregar_materiales(system, house_id):
    """Test 3: Agregar materiales a la construcción."""
    print("\n[TEST 3] Agregando materiales...")
    
    casa = system.casas[house_id]
    materiales_req = casa.materiales_requeridos
    
    for material, cantidad in materiales_req.items():
        success, msg = system.agregar_material_construccion(house_id, material, cantidad)
        assert success, f"Error agregando {material}: {msg}"
        print(f"  ✓ {cantidad}x {material} agregado")
    
    # Verificar progreso
    casa_info = system.obtener_casa(house_id)
    assert casa_info["progreso_construccion"] >= 99, "Progreso incompleto"
    print(f"  ✓ Progreso de construcción: {casa_info['progreso_construccion']:.1f}%")


def test_4_completar_construccion(system, house_id):
    """Test 4: Completar construcción."""
    print("\n[TEST 4] Completando construcción...")
    
    casa = system.casas[house_id]
    success, msg = casa.completar_construccion()
    assert success, f"Error completando construcción: {msg}"
    
    casa_info = system.obtener_casa(house_id)
    assert casa_info["estado"] == "completa", "Casa no está completa"
    print(f"  ✓ Casa completada")
    print(f"  ✓ Estado: {casa_info['estado']}")


def test_5_comprar_casa_ciudad(system):
    """Test 5: Comprar casa en ciudad."""
    print("\n[TEST 5] Comprando casa en ciudad...")
    
    success, result = system.comprar_casa(
        "player_2",
        "Metrópolis Maldita en el Bosque",
        HousingType.MEDIANA
    )
    assert success, "No se pudo comprar la casa"
    assert "costo" in result, "No se retornó costo"
    
    house_id = result["house_id"]
    casa_info = system.obtener_casa(house_id)
    assert casa_info["estado"] == "completa", "Casa comprada no está completa"
    
    print(f"  ✓ Casa comprada: {house_id}")
    print(f"  ✓ Costo: {result['costo']} oro")
    print(f"  ✓ Estado: {casa_info['estado']}")
    print(f"  ✓ Ubicación: {casa_info['ubicacion']}")
    
    return house_id


def test_6_efectos_casa(system, house_id):
    """Test 6: Verificar efectos de la casa."""
    print("\n[TEST 6] Verificando efectos de la casa...")
    
    casa_info = system.obtener_casa(house_id)
    efectos = casa_info["efectos"]
    
    assert len(efectos) > 0, "No hay efectos definidos"
    print(f"  ✓ Efectos activos: {len(efectos)}")
    for efecto, valor in efectos.items():
        print(f"    • {efecto}: {valor}x (+ {(valor-1)*100:.0f}%)")


def test_7_storage_casa(system, house_id):
    """Test 7: Probar storage de la casa."""
    print("\n[TEST 7] Probando storage de la casa...")
    
    casa = system.casas[house_id]
    capacidad = casa.capacidad_storage
    
    # Agregar items
    success, msg = casa.agregar_item_storage("Hierro Negro", 50)
    assert success, f"Error agregando item: {msg}"
    print(f"  ✓ Item agregado al storage")
    
    # Verificar
    assert "Hierro Negro" in casa.inventario, "Item no se guardó"
    assert casa.inventario["Hierro Negro"] == 50, "Cantidad incorrecta"
    
    storage_usado = sum(casa.inventario.values())
    print(f"  ✓ Storage: {storage_usado}/{capacidad}")


def test_8_nombre_personalizado(system, house_id):
    """Test 8: Establecer nombre personalizado."""
    print("\n[TEST 8] Nombre personalizado...")
    
    casa = system.casas[house_id]
    success, msg = casa.establecer_nombre_personalizado("Casa del Dragón")
    assert success, f"Error: {msg}"
    
    casa_info = system.obtener_casa(house_id)
    assert casa_info["nombre"] == "Casa del Dragón", "Nombre no actualizado"
    
    print(f"  ✓ Casa renombrada a: {casa_info['nombre']}")


def test_9_casas_por_jugador(system):
    """Test 9: Obtener casas por jugador."""
    print("\n[TEST 9] Obtener casas por jugador...")
    
    casas_p1 = system.obtener_casas_jugador("player_1")
    casas_p2 = system.obtener_casas_jugador("player_2")
    
    assert len(casas_p1) > 0, "Player 1 no tiene casas"
    assert len(casas_p2) > 0, "Player 2 no tiene casas"
    
    print(f"  ✓ Player 1: {len(casas_p1)} casa(s)")
    for casa in casas_p1:
        print(f"    • {casa['nombre']} ({casa['tipo']}) - {casa['estado']}")
    
    print(f"  ✓ Player 2: {len(casas_p2)} casa(s)")
    for casa in casas_p2:
        print(f"    • {casa['nombre']} ({casa['tipo']}) - {casa['estado']}")


def test_10_tipos_casas_disponibles():
    """Test 10: Listar tipos de casas."""
    print("\n[TEST 10] Tipos de casas disponibles...")
    
    tipos = listar_tipos_casas()
    assert len(tipos) == 5, "Debería haber 5 tipos de casas"
    
    for tipo_name, tipo_data in tipos.items():
        print(f"\n  • {tipo_data['nombre'].upper()}")
        print(f"    Descripción: {tipo_data['descripcion']}")
        print(f"    Costo: {tipo_data['costo_compra']} oro")
        print(f"    Materiales: {len(tipo_data['materiales'])} tipos")
        print(f"    Efectos: {len(tipo_data['efectos'])} tipos")


def test_11_guardar_cargar_casas(system):
    """Test 11: Guardar y cargar casas."""
    print("\n[TEST 11] Guardar y cargar casas...")
    
    filepath = "systems/casas_test.json"
    
    # Guardar
    system.guardar_casas(filepath)
    assert os.path.exists(filepath), "Archivo no se guardó"
    print(f"  ✓ Casas guardadas en {filepath}")
    
    # Cargar en nuevo sistema
    system2 = HousingSystem()
    system2.cargar_casas(filepath)
    
    casas_orig = len(system.casas)
    casas_cargadas = len(system2.casas)
    assert casas_cargadas == casas_orig, "Casas no se cargaron correctamente"
    
    print(f"  ✓ {casas_cargadas} casas cargadas")
    
    # Limpiar
    os.remove(filepath)


def test_12_multiples_casas_jugador(system):
    """Test 12: Un jugador puede tener múltiples casas."""
    print("\n[TEST 12] Múltiples casas por jugador...")
    
    casas_antes = len(system.obtener_casas_jugador("player_3"))
    
    # Construir primera casa
    success1, r1 = system.construir_casa("player_3", HousingType.PEQUEÑA, [50, 50])
    assert success1, "No se pudo construir primera casa"
    
    # Construir segunda casa
    success2, r2 = system.construir_casa("player_3", HousingType.MEDIANA, [150, 150])
    assert success2, "No se pudo construir segunda casa"
    
    # Construir tercera casa
    success3, r3 = system.construir_casa("player_3", HousingType.GRANDE, [300, 300])
    assert success3, "No se pudo construir tercera casa"
    
    # Intentar construir cuarta (debe fallar)
    success4, msg4 = system.construir_casa("player_3", HousingType.LUJOSA, [450, 450])
    assert not success4, "Debería fallar al construir 4ta casa"
    
    casas_despues = len(system.obtener_casas_jugador("player_3"))
    assert casas_despues == 3, "Debería tener exactamente 3 casas"
    
    print(f"  ✓ Máximo 3 casas por jugador funcionando")
    print(f"  ✓ Player 3 tiene {casas_despues} casas")
    for i, casa in enumerate(system.obtener_casas_jugador("player_3"), 1):
        print(f"    {i}. {casa['nombre']} ({casa['tipo']})")


def main():
    """Ejecutar todos los tests."""
    print("=" * 80)
    print("TEST COMPLETO - SISTEMA DE HOUSING")
    print("=" * 80)
    
    try:
        # Test 1-4: Construcción básica
        system = test_1_sistema_inicializa()
        house_id_1 = test_2_construir_casa(system)
        test_3_agregar_materiales(system, house_id_1)
        test_4_completar_construccion(system, house_id_1)
        
        # Test 5: Compra
        house_id_2 = test_5_comprar_casa_ciudad(system)
        
        # Test 6-9: Funcionalidades
        test_6_efectos_casa(system, house_id_2)
        test_7_storage_casa(system, house_id_2)
        test_8_nombre_personalizado(system, house_id_1)
        test_9_casas_por_jugador(system)
        
        # Test 10-12: Más funcionalidades
        test_10_tipos_casas_disponibles()
        test_11_guardar_cargar_casas(system)
        test_12_multiples_casas_jugador(system)
        
        # Resumen
        print("\n" + "=" * 80)
        print("RESULTADO: 12/12 TESTS PASARON")
        print("=" * 80)
        print("\nEl sistema de housing está funcionando correctamente:")
        print("  ✓ Construcción de casas")
        print("  ✓ Compra de casas en ciudades")
        print("  ✓ Sistema de materiales")
        print("  ✓ Storage de items")
        print("  ✓ Efectos de casas")
        print("  ✓ Persistencia de datos")
        print("  ✓ Múltiples casas por jugador")
        print("=" * 80)
        
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
