#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el Sistema de Expansión de Casas - WuxiaRPG
Valida creación de pisos, salas, efectos y limitaciones
"""

import json
from datetime import datetime
from systems.housing_system import House, HousingType, HousingStatus
from systems.housing_expansion_system import (
    ExpandedHouse, Room, HouseFloor, HousingExpansionSystem,
    RoomType, RoomSize, FloorLevel, ROOM_SPECIFICATIONS,
    EXPANSION_COSTS, listar_todos_tipos_salas, listar_todos_pisos
)


# ============================================================================
# UTILIDADES DE TEST
# ============================================================================

def crear_casa_base():
    """Crea una casa base para testing."""
    casa = House("house_test_001", HousingType.GRANDE, "jugador_1", [100, 200])
    casa.status = HousingStatus.COMPLETA
    return casa


def crear_casa_expandida():
    """Crea una casa expandida."""
    return ExpandedHouse(crear_casa_base())


def test_resultado(num, nombre, condicion, mensaje=""):
    """Imprime resultado de test."""
    estado = "[PASS]" if condicion else "[FAIL]"
    print(f"{estado} Test {num}: {nombre}")
    if mensaje:
        print(f"      {mensaje}")
    return condicion


# ============================================================================
# TESTS
# ============================================================================

def test_001_inicializacion():
    """Test: Inicialización de casa expandida."""
    casa_expandida = crear_casa_expandida()
    
    test1 = test_resultado(
        1, "Inicializar casa expandida",
        FloorLevel.PLANTA_BAJA in casa_expandida.pisos,
        f"Planta baja presente"
    )
    
    test2 = test_resultado(
        1, "Contador de salas en 0",
        casa_expandida.contador_salas == 0,
        f"Contador: {casa_expandida.contador_salas}"
    )
    
    return test1 and test2


def test_002_crear_sala_planta_baja():
    """Test: Crear sala en planta baja."""
    casa_expandida = crear_casa_expandida()
    
    exito, msg = casa_expandida.agregar_sala(
        RoomType.DORMITORIO,
        RoomSize.MEDIANA,
        FloorLevel.PLANTA_BAJA,
        nombre="Mi Dormitorio"
    )
    
    test1 = test_resultado(2, "Crear sala planta baja", exito, msg)
    
    test2 = test_resultado(
        2, "Sala en lista",
        len(casa_expandida._obtener_todas_salas()) == 1,
        f"Total salas: {len(casa_expandida._obtener_todas_salas())}"
    )
    
    return test1 and test2


def test_003_multiplas_salas():
    """Test: Crear múltiples salas."""
    casa_expandida = crear_casa_expandida()
    
    tipos_salas = [
        (RoomType.DORMITORIO, "Dormitorio Principal"),
        (RoomType.SALA_ESTAR, "Sala de Estar"),
        (RoomType.BIBLIOTECA, "Biblioteca"),
        (RoomType.DOJO, "Dojo Entrenamiento"),
    ]
    
    todas_exito = True
    for room_type, nombre in tipos_salas:
        exito, msg = casa_expandida.agregar_sala(
            room_type,
            RoomSize.MEDIANA,
            FloorLevel.PLANTA_BAJA,
            nombre=nombre
        )
        if not exito:
            print(f"  ❌ Fallo crear {nombre}: {msg}")
            todas_exito = False
    
    test1 = test_resultado(
        3, "Crear 4 salas",
        todas_exito and len(casa_expandida._obtener_todas_salas()) == 4,
        f"Total salas creadas: {len(casa_expandida._obtener_todas_salas())}"
    )
    
    return test1


def test_004_expandir_piso():
    """Test: Expandir a primer piso."""
    casa_expandida = crear_casa_expandida()
    
    materiales = {"madera": 500, "mineral": 500}
    
    exito, msg = casa_expandida.expandir_piso(FloorLevel.PISO_1, materiales)
    
    test1 = test_resultado(4, "Expandir piso 1", exito, msg)
    
    test2 = test_resultado(
        4, "Piso en lista",
        FloorLevel.PISO_1 in casa_expandida.pisos,
        f"Pisos disponibles: {len(casa_expandida.pisos)}"
    )
    
    return test1 and test2


def test_005_expandir_sotano():
    """Test: Expandir sótano."""
    casa_expandida = crear_casa_expandida()
    
    materiales = {"madera": 500, "mineral": 500}
    
    exito, msg = casa_expandida.expandir_piso(FloorLevel.SOTANO_1, materiales)
    
    test1 = test_resultado(5, "Expandir sótano 1", exito, msg)
    
    test2 = test_resultado(
        5, "Sótano registrado",
        FloorLevel.SOTANO_1 in casa_expandida.expansiones["sotanos"],
        f"Sotanos expandidos: {len(casa_expandida.expansiones['sotanos'])}"
    )
    
    return test1 and test2


def test_006_sala_en_piso():
    """Test: Crear sala en piso expandido."""
    casa_expandida = crear_casa_expandida()
    
    casa_expandida.expandir_piso(FloorLevel.PISO_1, {"madera": 500, "mineral": 500})
    
    exito, msg = casa_expandida.agregar_sala(
        RoomType.BIBLIOTECA,
        RoomSize.GRANDE,
        FloorLevel.PISO_1,
        nombre="Biblioteca Superior"
    )
    
    test1 = test_resultado(6, "Crear sala en piso", exito, msg)
    
    test2 = test_resultado(
        6, "Sala en piso correcto",
        len(casa_expandida.pisos[FloorLevel.PISO_1].salas) == 1,
        f"Salas en piso 1: {len(casa_expandida.pisos[FloorLevel.PISO_1].salas)}"
    )
    
    return test1 and test2


def test_007_restriccion_piso_invalido():
    """Test: No permite crear sala en piso no expandido."""
    casa_expandida = crear_casa_expandida()
    
    exito, msg = casa_expandida.agregar_sala(
        RoomType.BIBLIOTECA,
        RoomSize.MEDIANA,
        FloorLevel.PISO_1
    )
    
    test1 = test_resultado(
        7, "Restricción piso no expandido",
        not exito and "no existe" in msg.lower(),
        f"Error capturado"
    )
    
    return test1


def test_008_restriccion_sala_por_piso():
    """Test: Restricción de salas específicas por piso."""
    casa_expandida = crear_casa_expandida()
    
    casa_expandida.expandir_piso(FloorLevel.PISO_1, {"madera": 500, "mineral": 500})
    
    exito, msg = casa_expandida.agregar_sala(
        RoomType.DOJO,
        RoomSize.MEDIANA,
        FloorLevel.PISO_1
    )
    
    test1 = test_resultado(
        8, "Dojo no en pisos superiores",
        not exito and "no puede estar en piso" in msg.lower(),
        f"Error capturado"
    )
    
    return test1


def test_009_max_sala_especial():
    """Test: Restricción de máximo de salas especiales."""
    casa_expandida = crear_casa_expandida()
    
    # Expandir piso (Meditación no puede estar en planta baja)
    casa_expandida.expandir_piso(FloorLevel.PISO_1, {"madera": 500, "mineral": 500})
    
    exito1, _ = casa_expandida.agregar_sala(
        RoomType.MEDITACION,
        RoomSize.MEDIANA,
        FloorLevel.PISO_1
    )
    
    exito2, msg = casa_expandida.agregar_sala(
        RoomType.MEDITACION,
        RoomSize.MEDIANA,
        FloorLevel.PISO_1
    )
    
    test1 = test_resultado(9, "Primera meditación OK", exito1)
    test2 = test_resultado(
        9, "Segunda meditación rechazada",
        not exito2 and "máximo" in msg.lower(),
        f"Restricción aplicada"
    )
    
    return test1 and test2


def test_010_materiales_insuficientes():
    """Test: No permite crear sala sin materiales suficientes."""
    casa_expandida = crear_casa_expandida()
    
    materiales = {"madera": 1, "mineral": 1}
    
    exito, msg = casa_expandida.agregar_sala(
        RoomType.DORMITORIO,
        RoomSize.GRANDE,
        FloorLevel.PLANTA_BAJA,
        materiales_disponibles=materiales
    )
    
    test1 = test_resultado(
        10, "Materiales insuficientes",
        not exito and "suficiente" in msg.lower(),
        f"Validación correcta"
    )
    
    return test1


def test_011_efectos_individuales():
    """Test: Verificar efectos de sala individual."""
    casa_expandida = crear_casa_expandida()
    
    casa_expandida.agregar_sala(
        RoomType.DORMITORIO,
        RoomSize.MEDIANA,
        FloorLevel.PLANTA_BAJA
    )
    
    efectos = casa_expandida.obtener_efectos_totales()
    
    test1 = test_resultado(
        11, "Efectos presentes",
        "descanso" in efectos,
        f"Efectos: {list(efectos.keys())}"
    )
    
    test2 = test_resultado(
        11, "Efectos son multiplicadores",
        efectos.get("descanso", 0) > 1.0,
        f"Descanso: {efectos.get('descanso')}"
    )
    
    return test1 and test2


def test_012_efectos_multiples():
    """Test: Efectos de múltiples salas."""
    casa_expandida = crear_casa_expandida()
    
    casa_expandida.agregar_sala(
        RoomType.DORMITORIO,
        RoomSize.MEDIANA,
        FloorLevel.PLANTA_BAJA
    )
    
    casa_expandida.agregar_sala(
        RoomType.BIBLIOTECA,
        RoomSize.MEDIANA,
        FloorLevel.PLANTA_BAJA
    )
    
    efectos = casa_expandida.obtener_efectos_totales()
    
    test1 = test_resultado(
        12, "Múltiples efectos",
        "descanso" in efectos and "sabiduria" in efectos and "iluminacion" in efectos,
        f"Efectos totales: {len(efectos)}"
    )
    
    return test1


def test_013_guardar_casa():
    """Test: Guardar estado de casa expandida."""
    casa_expandida = crear_casa_expandida()
    
    casa_expandida.agregar_sala(
        RoomType.DORMITORIO,
        RoomSize.MEDIANA,
        FloorLevel.PLANTA_BAJA,
        nombre="Dormitorio Principal"
    )
    
    casa_expandida.expandir_piso(
        FloorLevel.PISO_1,
        {"madera": 500, "mineral": 500}
    )
    
    datos = casa_expandida.guardar()
    
    test1 = test_resultado(
        13, "Guardar datos",
        "base_house_id" in datos and "pisos" in datos,
        f"Campos guardados"
    )
    
    test2 = test_resultado(
        13, "Datos consistentes",
        datos["contador_salas"] == 1 and len(datos["pisos"]) >= 2,
        f"Salas: {datos['contador_salas']}, Pisos: {len(datos['pisos'])}"
    )
    
    return test1 and test2


def test_014_info_completa():
    """Test: Obtener información completa."""
    casa_expandida = crear_casa_expandida()
    
    try:
        casa_expandida.agregar_sala(RoomType.DORMITORIO, RoomSize.MEDIANA, FloorLevel.PLANTA_BAJA)
        casa_expandida.agregar_sala(RoomType.DOJO, RoomSize.GRANDE, FloorLevel.PLANTA_BAJA)
        casa_expandida.expandir_piso(FloorLevel.PISO_1, {"madera": 500, "mineral": 500})
        casa_expandida.agregar_sala(RoomType.BIBLIOTECA, RoomSize.MEDIANA, FloorLevel.PISO_1)
        
        info = casa_expandida.obtener_info_completa()
        
        test1 = test_resultado(
            14, "Información completa",
            "casa_base" in info and "pisos" in info and "efectos_totales" in info,
            f"Estructura correcta"
        )
        
        test2 = test_resultado(
            14, "Salas contadas",
            info["total_salas"] == 3,
            f"Total salas: {info['total_salas']}"
        )
        
        return test1 and test2
    except Exception as e:
        print(f"    ERROR en test 14: {str(e)[:80]}")
        return False


def test_015_limite_salas():
    """Test: Límite de salas por casa."""
    casa_expandida = crear_casa_expandida()
    
    limite = casa_expandida.limites["salas_total"]
    
    creadas = 0
    for i in range(limite + 2):
        exito, msg = casa_expandida.agregar_sala(
            RoomType.DEPOSITO,
            RoomSize.PEQUEÑA,
            FloorLevel.PLANTA_BAJA
        )
        
        if exito:
            creadas += 1
    
    test1 = test_resultado(
        15, "Límite respetado",
        creadas == limite,
        f"Límite: {limite}, Creadas: {creadas}"
    )
    
    return test1


def test_016_tipos_salas():
    """Test: Listar tipos de salas."""
    tipos = listar_todos_tipos_salas()
    
    test1 = test_resultado(
        16, "Listar tipos",
        len(tipos) > 0,
        f"Total tipos: {len(tipos)}"
    )
    
    test2 = test_resultado(
        16, "Tipos incluyen dormitorio",
        any(t["tipo"] == "dormitorio" for t in tipos),
        f"Primeros tipos: {[t['tipo'] for t in tipos[:3]]}"
    )
    
    return test1 and test2


def test_017_pisos():
    """Test: Listar pisos."""
    pisos = listar_todos_pisos()
    
    test1 = test_resultado(
        17, "Listar pisos",
        len(pisos) > 0,
        f"Total pisos: {len(pisos)}"
    )
    
    test2 = test_resultado(
        17, "Pisos incluyen sótano y superior",
        any(p["piso"] < 0 for p in pisos) and any(p["piso"] > 0 for p in pisos),
        f"Estructura correcta"
    )
    
    return test1 and test2


def test_018_sistema_expansion():
    """Test: Sistema de expansión."""
    sistema = HousingExpansionSystem()
    casa = House("house_sys_001", HousingType.MEDIANA, "jugador_2", [50, 60])
    
    exito, msg = sistema.inicializar_expansion(casa)
    
    test1 = test_resultado(18, "Inicializar sistema", exito, msg)
    
    casa_exp = sistema.obtener_casa_expandida(casa.id)
    test2 = test_resultado(
        18, "Recuperar casa",
        casa_exp is not None,
        f"Casa recuperada"
    )
    
    return test1 and test2


# ============================================================================
# EJECUCION
# ============================================================================

def ejecutar_tests():
    """Ejecuta todos los tests."""
    print("\n" + "=" * 80)
    print("TESTS DEL SISTEMA DE EXPANSION DE CASAS - WuxiaRPG")
    print("=" * 80 + "\n")
    
    tests = [
        test_001_inicializacion,
        test_002_crear_sala_planta_baja,
        test_003_multiplas_salas,
        test_004_expandir_piso,
        test_005_expandir_sotano,
        test_006_sala_en_piso,
        test_007_restriccion_piso_invalido,
        test_008_restriccion_sala_por_piso,
        test_009_max_sala_especial,
        test_010_materiales_insuficientes,
        test_011_efectos_individuales,
        test_012_efectos_multiples,
        test_013_guardar_casa,
        test_014_info_completa,
        test_015_limite_salas,
        test_016_tipos_salas,
        test_017_pisos,
        test_018_sistema_expansion,
    ]
    
    pasaron = 0
    fallaron = 0
    
    for test in tests:
        try:
            print(f"\n{test.__doc__}")
            resultado = test()
            if resultado:
                pasaron += 1
            else:
                fallaron += 1
        except Exception as e:
            print(f"[ERROR] EXCEPCION: {str(e)[:100]}")
            fallaron += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTADOS: {pasaron} PASS, {fallaron} FAIL")
    print(f"TASA DE EXITO: {(pasaron / (pasaron + fallaron) * 100):.1f}%")
    print("=" * 80 + "\n")
    
    return pasaron, fallaron


if __name__ == "__main__":
    ejecutar_tests()
