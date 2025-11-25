#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUIA DE INTEGRACION - Sistema de Housing en game_engine.py
Cómo integrar el sistema de housing en el motor del juego
"""

from systems.housing_system import (
    HousingSystem, HousingType, HousingStatus,
    listar_tipos_casas, obtener_materiales_disponibles
)


# ============================================================================
# PASO 1: INICIALIZAR EL SISTEMA
# ============================================================================

def init_housing_system():
    """Inicializa el sistema de housing en game_engine."""
    housing_system = HousingSystem("systems")
    return housing_system

# Uso en game_engine.__init__():
# self.housing_system = init_housing_system()


# ============================================================================
# PASO 2: CONSTRUIR UNA CASA
# ============================================================================

def construir_casa_comando(game_engine, player_id, house_type, ubicacion_x, ubicacion_y):
    """
    Comando: /construir_casa <tipo> <x> <y>
    Inicia la construcción de una casa
    """
    try:
        success, result = game_engine.housing_system.construir_casa(
            player_id,
            HousingType[house_type.upper()],
            [ubicacion_x, ubicacion_y]
        )
        
        if success:
            house_id = result["house_id"]
            game_engine.mostrar_mensaje(
                f"Casa en construcción: {house_id}\n"
                f"Tipo: {result['tipo']}\n"
                f"Ubicación: {result['ubicacion']}\n"
                f"Materiales necesarios: {len(result['materiales_requeridos'])} tipos"
            )
            
            # Guardar progreso
            game_engine.guardar_estado()
            return True
        else:
            game_engine.mostrar_error(result)
            return False
    
    except Exception as e:
        game_engine.mostrar_error(f"Error: {e}")
        return False


# ============================================================================
# PASO 3: AGREGAR MATERIALES A LA CONSTRUCCION
# ============================================================================

def agregar_material_construccion(game_engine, player_id, house_id, material_name, cantidad):
    """
    Agrega materiales a una casa en construcción.
    Se llama después de recolectar/conseguir materiales.
    """
    # Verificar que el jugador tiene el material
    if not game_engine.inventario_jugador.tiene_item(player_id, material_name, cantidad):
        game_engine.mostrar_error(f"No tienes {cantidad}x {material_name}")
        return False
    
    # Remover del inventario
    game_engine.inventario_jugador.remover_item(player_id, material_name, cantidad)
    
    # Agregar a la construcción
    success, msg = game_engine.housing_system.agregar_material_construccion(
        house_id, material_name, cantidad
    )
    
    if success:
        game_engine.mostrar_mensaje(msg)
        
        # Verificar si se completó
        casa_info = game_engine.housing_system.obtener_casa(house_id)
        if casa_info["progreso_construccion"] >= 100:
            game_engine.mostrar_mensaje(
                f"¡Casa lista para completar! Progreso: {casa_info['progreso_construccion']:.1f}%"
            )
        
        game_engine.guardar_estado()
    else:
        game_engine.mostrar_error(msg)
    
    return success


# ============================================================================
# PASO 4: COMPLETAR CONSTRUCCION
# ============================================================================

def completar_construccion(game_engine, player_id, house_id):
    """Completa la construcción de una casa."""
    casa = game_engine.housing_system.casas.get(house_id)
    
    if not casa:
        game_engine.mostrar_error("Casa no encontrada")
        return False
    
    if casa.owner_id != player_id:
        game_engine.mostrar_error("No es tu casa")
        return False
    
    success, msg = casa.completar_construccion()
    
    if success:
        game_engine.mostrar_mensaje(
            f"¡{msg}\n"
            f"Casa: {casa_info.get('nombre', casa_info['tipo'])}\n"
            f"Efectos activos: {', '.join(casa_info['efectos'].keys())}"
        )
        game_engine.guardar_estado()
    else:
        game_engine.mostrar_error(msg)
    
    return success


# ============================================================================
# PASO 5: COMPRAR CASA EN CIUDAD
# ============================================================================

def comprar_casa_en_ciudad(game_engine, player_id, ciudad_nombre, house_type):
    """
    Compra una casa precompilada en una ciudad.
    Se llama desde una casa de reales en la ciudad.
    """
    # Obtener dinero del jugador
    oro_jugador = game_engine.obtener_oro(player_id)
    
    # Obtener costo
    from systems.housing_system import HOUSING_REQUIREMENTS
    costo = HOUSING_REQUIREMENTS[HousingType[house_type.upper()]]["costo_compra"]
    
    if oro_jugador < costo:
        game_engine.mostrar_error(f"No tienes oro suficiente. Necesitas {costo}, tienes {oro_jugador}")
        return False
    
    # Restar oro
    game_engine.restar_oro(player_id, costo)
    
    # Comprar casa
    success, result = game_engine.housing_system.comprar_casa(
        player_id, ciudad_nombre, HousingType[house_type.upper()]
    )
    
    if success:
        game_engine.mostrar_mensaje(result["mensaje"])
        game_engine.guardar_estado()
    else:
        # Reembolsar si falla
        game_engine.sumar_oro(player_id, costo)
        game_engine.mostrar_error(result)
    
    return success


# ============================================================================
# PASO 6: VISITAR CASA
# ============================================================================

def visitar_casa(game_engine, player_id, house_id):
    """Entra a la casa del jugador."""
    casa_info = game_engine.housing_system.obtener_casa(house_id)
    
    if not casa_info:
        game_engine.mostrar_error("Casa no encontrada")
        return False
    
    if casa_info["dueno"] != player_id:
        game_engine.mostrar_error("No es tu casa")
        return False
    
    if casa_info["estado"] != "completa":
        game_engine.mostrar_error("Casa no completada aún")
        return False
    
    # Mostrar interior
    game_engine.mostrar_casa_interior(casa_info)
    game_engine.entrada_actual = f"house_{house_id}"
    
    return True


# ============================================================================
# PASO 7: VER CASAS DE JUGADOR
# ============================================================================

def ver_mis_casas(game_engine, player_id):
    """Muestra todas las casas del jugador."""
    casas = game_engine.housing_system.obtener_casas_jugador(player_id)
    
    if not casas:
        game_engine.mostrar_mensaje("No tienes casas aún")
        return
    
    mensaje = "TUS CASAS:\n"
    mensaje += "=" * 50 + "\n"
    
    for i, casa in enumerate(casas, 1):
        mensaje += f"\n{i}. {casa['nombre']} ({casa['tipo']})\n"
        mensaje += f"   Estado: {casa['estado']}\n"
        mensaje += f"   Ubicación: {casa['ubicacion']}\n"
        
        if casa['estado'] != 'completa':
            mensaje += f"   Progreso: {casa['progreso_construccion']:.1f}%\n"
        else:
            mensaje += f"   Storage: {casa['storage_usado']}/{casa['storage_total']}\n"
            mensaje += f"   Decoraciones: {casa['decoraciones']}\n"
        
        if casa.get('efectos'):
            efectos_str = ', '.join(f"{e}: +{(v-1)*100:.0f}%" for e, v in casa['efectos'].items())
            mensaje += f"   Efectos: {efectos_str}\n"
    
    game_engine.mostrar_mensaje(mensaje)


# ============================================================================
# PASO 8: AGREGAR ITEM AL STORAGE
# ============================================================================

def guardar_en_storage(game_engine, player_id, house_id, item_name, cantidad):
    """
    Guarda un item en el storage de la casa.
    Se usa cuando el jugador está dentro de la casa.
    """
    casa = game_engine.housing_system.casas.get(house_id)
    
    if not casa or casa.owner_id != player_id:
        return False, "No es tu casa"
    
    # Verificar que tiene el item
    if not game_engine.inventario_jugador.tiene_item(player_id, item_name, cantidad):
        return False, f"No tienes {cantidad}x {item_name}"
    
    # Remover del inventario
    game_engine.inventario_jugador.remover_item(player_id, item_name, cantidad)
    
    # Agregar al storage
    success, msg = casa.agregar_item_storage(item_name, cantidad)
    
    if success:
        game_engine.guardar_estado()
    else:
        # Revertir si falla
        game_engine.inventario_jugador.agregar_item(player_id, item_name, cantidad)
    
    return success, msg


# ============================================================================
# PASO 9: EXTRAER ITEM DEL STORAGE
# ============================================================================

def extraer_storage(game_engine, player_id, house_id, item_name, cantidad):
    """Extrae item del storage de la casa."""
    casa = game_engine.housing_system.casas.get(house_id)
    
    if not casa or casa.owner_id != player_id:
        return False, "No es tu casa"
    
    # Extraer del storage
    success, msg = casa.extraer_item_storage(item_name, cantidad)
    
    if success:
        # Agregar al inventario
        game_engine.inventario_jugador.agregar_item(player_id, item_name, cantidad)
        game_engine.guardar_estado()
    
    return success, msg


# ============================================================================
# PASO 10: CAMBIAR NOMBRE DE CASA
# ============================================================================

def renombrar_casa(game_engine, player_id, house_id, nuevo_nombre):
    """Cambia el nombre personalizado de la casa."""
    casa = game_engine.housing_system.casas.get(house_id)
    
    if not casa or casa.owner_id != player_id:
        return False, "No es tu casa"
    
    if len(nuevo_nombre) > 50:
        return False, "Nombre demasiado largo"
    
    success, msg = casa.establecer_nombre_personalizado(nuevo_nombre)
    
    if success:
        game_engine.guardar_estado()
    
    return success, msg


# ============================================================================
# PASO 11: EFECTOS DE CASA EN STATS
# ============================================================================

def aplicar_efectos_casa(game_engine, player_id):
    """
    Aplica los efectos de la casa del jugador a sus stats.
    Se llama al entrar a la casa o al ejecutar acciones dentro.
    """
    # Obtener casa donde está el jugador
    casas = game_engine.housing_system.obtener_casas_jugador(player_id)
    
    if not casas:
        return {}
    
    # Asumir que está en la primera casa completa
    casa_actual = next((c for c in casas if c['estado'] == 'completa'), None)
    
    if not casa_actual:
        return {}
    
    # Retornar los efectos para aplicarlos a los stats
    return casa_actual['efectos']


# ============================================================================
# PASO 12: GUARDAR Y CARGAR
# ============================================================================

def guardar_housing(game_engine):
    """Guarda el estado del sistema de housing."""
    filepath = "saves/housing_state.json"
    game_engine.housing_system.guardar_casas(filepath)


def cargar_housing(game_engine):
    """Carga el estado del sistema de housing."""
    filepath = "saves/housing_state.json"
    try:
        game_engine.housing_system.cargar_casas(filepath)
    except:
        pass  # Si no existe, simplemente iniciar con 0 casas


# ============================================================================
# EJEMPLO: INTEGRACION EN GAME_ENGINE
# ============================================================================

"""
# En ui/game_engine.py:

class GameEngine:
    def __init__(self):
        # ... código existente ...
        
        # Inicializar housing system
        self.housing_system = HousingSystem("systems")
    
    def comando_construir(self, args):
        '''Comando: /construir <tipo> <x> <y>'''
        if len(args) < 3:
            self.mostrar_error("Uso: /construir <tipo> <x> <y>")
            return
        
        house_type = args[0]
        try:
            x = int(args[1])
            y = int(args[2])
        except ValueError:
            self.mostrar_error("Coordenadas deben ser números")
            return
        
        construir_casa_comando(self, self.player_id, house_type, x, y)
    
    def comando_comprar_casa(self, args):
        '''Comando: /comprar_casa <ciudad> <tipo>'''
        if len(args) < 2:
            self.mostrar_error("Uso: /comprar_casa <ciudad> <tipo>")
            return
        
        ciudad = " ".join(args[:-1])
        house_type = args[-1]
        
        comprar_casa_en_ciudad(self, self.player_id, ciudad, house_type)
    
    def comando_mis_casas(self):
        '''Comando: /mis_casas'''
        ver_mis_casas(self, self.player_id)
    
    def guardar_juego(self):
        # ... código existente ...
        guardar_housing(self)
    
    def cargar_juego(self):
        # ... código existente ...
        cargar_housing(self)
"""


if __name__ == "__main__":
    print("Guía de integración de Housing System")
    print("Ver comentarios en el código para ejemplos")
