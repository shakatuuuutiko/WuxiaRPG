#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUIA RAPIDA DE INTEGRACION - Sistema de Expansion de Casas
Para integrar en game_engine.py
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================

from systems.housing_expansion_system import (
    ExpandedHouse, HousingExpansionSystem,
    RoomType, RoomSize, FloorLevel,
    listar_todos_tipos_salas, listar_todos_pisos
)


# ============================================================================
# FUNCIONES DE INTEGRACION (COPIAR A game_engine.py)
# ============================================================================

# Instancia global del sistema
housing_system = HousingExpansionSystem()


def cmd_expandir_casa(player_id, house_id, piso_destino):
    """
    Expande una casa a un nuevo piso/sótano.
    
    Uso: expandir_casa <id_casa> <piso>
    Ejemplo: expandir_casa house_001 piso_1
    """
    try:
        # Obtener casa
        expanded = housing_system.obtener_casa_expandida(house_id)
        if not expanded:
            return False, "Casa no encontrada"
        
        # Mapear string a FloorLevel
        piso_map = {
            "sotano_3": FloorLevel.SOTANO_3,
            "sotano_2": FloorLevel.SOTANO_2,
            "sotano_1": FloorLevel.SOTANO_1,
            "piso_1": FloorLevel.PISO_1,
            "piso_2": FloorLevel.PISO_2,
            "piso_3": FloorLevel.PISO_3,
            "piso_4": FloorLevel.PISO_4,
        }
        
        if piso_destino not in piso_map:
            return False, f"Piso inválido: {piso_destino}"
        
        # Obtener materiales del jugador (integrar con inventario)
        materiales = obtener_materiales_jugador(player_id)
        
        # Expandir
        exito, msg = expanded.expandir_piso(piso_map[piso_destino], materiales)
        
        if exito:
            # Deducir materiales
            deducir_materiales_jugador(player_id, expanded.expandir_piso.__doc__)
        
        return exito, msg
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def cmd_agregar_sala(player_id, house_id, tipo_sala, tamaño, piso, nombre=""):
    """
    Agrega una sala a una casa.
    
    Uso: agregar_sala <id_casa> <tipo> <tamaño> <piso> [nombre]
    Ejemplo: agregar_sala house_001 dormitorio mediana piso_1 "Mi Habitación"
    """
    try:
        # Obtener casa
        expanded = housing_system.obtener_casa_expandida(house_id)
        if not expanded:
            return False, "Casa no encontrada"
        
        # Mapear strings a enums
        tipo_map = {t.value: t for t in RoomType}
        tamaño_map = {s.value: s for s in RoomSize}
        piso_map = {
            "sotano_3": FloorLevel.SOTANO_3,
            "sotano_2": FloorLevel.SOTANO_2,
            "sotano_1": FloorLevel.SOTANO_1,
            "planta_baja": FloorLevel.PLANTA_BAJA,
            "piso_1": FloorLevel.PISO_1,
            "piso_2": FloorLevel.PISO_2,
            "piso_3": FloorLevel.PISO_3,
            "piso_4": FloorLevel.PISO_4,
        }
        
        # Validar inputs
        if tipo_sala not in tipo_map:
            return False, f"Tipo de sala inválido: {tipo_sala}"
        if tamaño not in tamaño_map:
            return False, f"Tamaño inválido: {tamaño}"
        if piso not in piso_map:
            return False, f"Piso inválido: {piso}"
        
        # Obtener materiales
        materiales = obtener_materiales_jugador(player_id)
        
        # Agregar sala
        exito, msg = expanded.agregar_sala(
            room_type=tipo_map[tipo_sala],
            size=tamaño_map[tamaño],
            floor_level=piso_map[piso],
            nombre=nombre or None,
            materiales_disponibles=materiales
        )
        
        if exito:
            # Deducir materiales
            deducir_materiales_jugador(player_id, msg)
        
        return exito, msg
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def cmd_ver_casa_expandida(house_id):
    """
    Muestra información completa de una casa expandida.
    
    Uso: ver_casa_expandida <id_casa>
    """
    try:
        expanded = housing_system.obtener_casa_expandida(house_id)
        if not expanded:
            return False, "Casa no encontrada"
        
        info = expanded.obtener_info_completa()
        
        # Formatear salida
        output = f"=== INFORMACION DE CASA ===\n"
        output += f"Total Salas: {info['total_salas']}\n"
        output += f"Límite: {info['limites']['salas_total']}\n"
        output += f"\nPisos disponibles:\n"
        for piso, datos in info['pisos'].items():
            output += f"  Piso {piso}: {datos['salas']} salas\n"
        output += f"\nEfectos Totales:\n"
        for efecto, valor in info['efectos_totales'].items():
            bonus = (valor - 1.0) * 100
            output += f"  {efecto}: +{bonus:.1f}%\n"
        
        return True, output
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def cmd_listar_salas_disponibles(piso):
    """
    Lista todos los tipos de salas disponibles para un piso.
    
    Uso: listar_salas <piso>
    """
    try:
        piso_map = {
            "sotano": FloorLevel.SOTANO_1,
            "planta_baja": FloorLevel.PLANTA_BAJA,
            "piso": FloorLevel.PISO_1,
        }
        
        if piso not in piso_map:
            return False, f"Piso inválido: {piso}"
        
        disponibles = obtener_tipos_salas_disponibles(piso_map[piso])
        
        output = f"=== SALAS DISPONIBLES EN {piso.upper()} ===\n"
        for room_type in disponibles:
            specs = ROOM_SPECIFICATIONS[room_type]
            output += f"• {specs['nombre']}\n"
            output += f"  Efectos: {specs['efectos']}\n"
            output += f"  Costo: {specs['costo_base']}\n"
        
        return True, output
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def cmd_guardar_expansion(house_id):
    """
    Guarda el estado de expansión de una casa.
    """
    try:
        import json
        expanded = housing_system.obtener_casa_expandida(house_id)
        if not expanded:
            return False, "Casa no encontrada"
        
        datos = expanded.guardar()
        
        with open(f"saves/expansion_{house_id}.json", "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2)
        
        return True, f"Expansión guardada: expansion_{house_id}.json"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


# ============================================================================
# FUNCIONES AUXILIARES (IMPLEMENTAR)
# ============================================================================

def obtener_materiales_jugador(player_id):
    """Obtener materiales disponibles del jugador."""
    # TODO: Integrar con inventario del jugador
    # Retornar: {"madera": cantidad, "mineral": cantidad}
    pass


def deducir_materiales_jugador(player_id, cantidad):
    """Deducir materiales del inventario del jugador."""
    # TODO: Integrar con inventario del jugador
    pass


def obtener_tipos_salas_disponibles(floor_level):
    """Obtener tipos de salas permitidas en un piso."""
    from systems.housing_expansion_system import obtener_tipos_salas_disponibles
    return obtener_tipos_salas_disponibles(floor_level)


# ============================================================================
# EJEMPLO DE USO EN game_engine.py
# ============================================================================

"""
# En la función principal de comandos:

def procesar_comando(comando, args, player_id):
    
    # Comandos de expansión de casas
    if comando == "expandir_casa":
        exito, msg = cmd_expandir_casa(player_id, args[0], args[1])
        print(msg)
    
    elif comando == "agregar_sala":
        exito, msg = cmd_agregar_sala(
            player_id, args[0], args[1], args[2], args[3],
            args[4] if len(args) > 4 else ""
        )
        print(msg)
    
    elif comando == "ver_casa_expandida":
        exito, msg = cmd_ver_casa_expandida(args[0])
        print(msg)
    
    elif comando == "listar_salas_disponibles":
        exito, msg = cmd_listar_salas_disponibles(args[0])
        print(msg)
    
    elif comando == "guardar_expansion":
        exito, msg = cmd_guardar_expansion(args[0])
        print(msg)
"""


# ============================================================================
# COMANDOS DISPONIBLES
# ============================================================================

"""
expandir_casa <id_casa> <piso>
  • Expande una casa a un nuevo piso/sótano
  • Requiere materiales
  • Ejemplo: expandir_casa house_001 piso_1

agregar_sala <id_casa> <tipo> <tamaño> <piso> [nombre]
  • Agrega una sala a un piso
  • Tipos: dormitorio, dojo, biblioteca, etc.
  • Tamaños: pequeña, mediana, grande
  • Pisos: sotano_3 a piso_4
  • Ejemplo: agregar_sala house_001 dormitorio mediana piso_1 "Mi Habitación"

ver_casa_expandida <id_casa>
  • Muestra información completa de la casa
  • Total de salas, efectos, pisos
  • Ejemplo: ver_casa_expandida house_001

listar_salas_disponibles <piso>
  • Lista tipos de salas disponibles en un piso
  • Pisos: sotano, planta_baja, piso
  • Ejemplo: listar_salas_disponibles piso

guardar_expansion <id_casa>
  • Guarda el estado de expansión
  • Crea archivo JSON
  • Ejemplo: guardar_expansion house_001
"""


# ============================================================================
# INTEGRACIÓN CON PERSISTENCIA
# ============================================================================

"""
En el sistema de guardado del juego, agregar:

def guardar_juego(save_path):
    # Guardar housing normal
    guardar_housing(save_path)
    
    # Guardar expansiones de casas
    for house_id, expanded in housing_system.casas_expandidas.items():
        datos = expanded.guardar()
        guardar_json(f"{save_path}/expansion_{house_id}.json", datos)

def cargar_juego(save_path):
    # Cargar housing normal
    cargar_housing(save_path)
    
    # Cargar expansiones
    for expansion_file in listar_expansion_files(save_path):
        house_id = extraer_house_id(expansion_file)
        datos = cargar_json(expansion_file)
        # Reconstruir expanded house desde datos
"""


# ============================================================================
# NOTAS DE INTEGRACION
# ============================================================================

"""
1. INVENTARIO DE MATERIALES
   - Necesita integración con sistema de inventario
   - Obtener: obtener_materiales_jugador(player_id)
   - Deducir: deducir_materiales_jugador(player_id, cantidad)

2. PERSISTENCIA
   - Guardar expansion automáticamente con el juego
   - Cargar expansion al iniciar sesión

3. INTERFAZ VISUAL
   - Mostrar estructura de pisos en UI
   - Permitir drag-drop de salas
   - Mostrar efectos combinados

4. RESTRICCIONES DE JUEGO
   - Limitar expansión por nivel del jugador
   - Requiere recursos específicos
   - Puede tomar tiempo (construcción)

5. EVENTOS
   - Completar expansión de piso
   - Crear sala especial
   - Alcanzar límite de casa
   - Activar efecto especial
"""

print("Guía de integración de Sistema de Expansión de Casas")
