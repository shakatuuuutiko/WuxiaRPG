#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Expansión de Casas - WuxiaRPG
Permite expandir casas con salas modulares en múltiples niveles
Niveles: Sótano (B-), Planta Baja (0), Pisos Superiores (1, 2, 3...)
"""

import json
import os
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Tuple, Optional


# ============================================================================
# ENUMS Y CONSTANTES
# ============================================================================

class RoomType(Enum):
    """Tipos de salas disponibles."""
    DORMITORIO = "dormitorio"
    SALA_ESTAR = "sala_estar"
    COCINA = "cocina"
    BIBLIOTECA = "biblioteca"
    DOJO = "dojo"              # Sala de entrenamiento
    LABORATORIO = "laboratorio"  # Para alquimia/crafting
    MEDITACION = "meditacion"  # Sala de meditación
    DEPOSITO = "deposito"      # Storage adicional
    TESORO = "tesoro"          # Bóveda de seguridad
    ARMERIA = "armeria"        # Almacenamiento de armas
    SANTUARIO = "santuario"    # Bonificación espiritual
    JARDIN = "jardin"          # Solo planta baja, bonificación agricultura


class RoomSize(Enum):
    """Tamaños de salas."""
    PEQUEÑA = "pequeña"        # 2x2
    MEDIANA = "mediana"        # 3x3
    GRANDE = "grande"          # 4x4


class FloorLevel(Enum):
    """Niveles de la casa."""
    SOTANO_1 = -1
    SOTANO_2 = -2
    SOTANO_3 = -3
    PLANTA_BAJA = 0
    PISO_1 = 1
    PISO_2 = 2
    PISO_3 = 3
    PISO_4 = 4


# Especificaciones de salas
ROOM_SPECIFICATIONS = {
    RoomType.DORMITORIO: {
        "nombre": "Dormitorio",
        "descripcion": "Espacio para descansar",
        "efectos": {"descanso": 1.15},
        "costo_base": {"madera": 20, "mineral": 10},
        "permite_piso": True,
        "permite_sotano": False,
        "permite_planta_baja": True,
        "capacidad": {"items": 50, "mascotas": 1},
    },
    
    RoomType.SALA_ESTAR: {
        "nombre": "Sala de Estar",
        "descripcion": "Lugar para relajarse",
        "efectos": {"relajacion": 1.2},
        "costo_base": {"madera": 15, "mineral": 5},
        "permite_piso": True,
        "permite_sotano": False,
        "permite_planta_baja": True,
        "capacidad": {"items": 30, "mascotas": 2},
    },
    
    RoomType.COCINA: {
        "nombre": "Cocina",
        "descripcion": "Para preparar comidas",
        "efectos": {"regeneracion": 1.1},
        "costo_base": {"madera": 25, "mineral": 15},
        "permite_piso": False,
        "permite_sotano": False,
        "permite_planta_baja": True,
        "capacidad": {"items": 200, "mascotas": 0},
        "requiere": ["planta_baja"],  # Debe estar en planta baja
    },
    
    RoomType.BIBLIOTECA: {
        "nombre": "Biblioteca",
        "descripcion": "Colección de libros y pergaminos",
        "efectos": {"sabiduria": 1.15, "iluminacion": 1.1},
        "costo_base": {"madera": 30, "mineral": 20},
        "permite_piso": True,
        "permite_sotano": True,
        "permite_planta_baja": True,
        "capacidad": {"items": 500, "mascotas": 0},
    },
    
    RoomType.DOJO: {
        "nombre": "Dojo",
        "descripcion": "Sala de entrenamiento",
        "efectos": {"cultivo": 1.25, "ataque": 1.1},
        "costo_base": {"madera": 40, "mineral": 30},
        "permite_piso": False,
        "permite_sotano": False,
        "permite_planta_baja": True,
        "capacidad": {"items": 100, "mascotas": 1},
        "requiere": ["planta_baja"],
    },
    
    RoomType.LABORATORIO: {
        "nombre": "Laboratorio",
        "descripcion": "Para alquimia y crafting",
        "efectos": {"crafting": 1.2},
        "costo_base": {"madera": 35, "mineral": 40},
        "permite_piso": True,
        "permite_sotano": True,
        "permite_planta_baja": False,
        "capacidad": {"items": 300, "mascotas": 0},
    },
    
    RoomType.MEDITACION: {
        "nombre": "Sala de Meditación",
        "descripcion": "Para meditación profunda",
        "efectos": {"meditacion": 1.3, "iluminacion": 1.15},
        "costo_base": {"madera": 45, "mineral": 35},
        "permite_piso": True,
        "permite_sotano": True,
        "permite_planta_baja": False,
        "capacidad": {"items": 20, "mascotas": 0},
        "max_por_casa": 1,  # Solo una por casa
    },
    
    RoomType.DEPOSITO: {
        "nombre": "Depósito",
        "descripcion": "Almacenamiento adicional",
        "efectos": {},
        "costo_base": {"madera": 20, "mineral": 15},
        "permite_piso": True,
        "permite_sotano": True,
        "permite_planta_baja": True,
        "capacidad": {"items": 1000, "mascotas": 0},
    },
    
    RoomType.TESORO: {
        "nombre": "Bóveda de Tesoro",
        "descripcion": "Almacenamiento seguro para valuables",
        "efectos": {},
        "costo_base": {"madera": 60, "mineral": 80},
        "permite_piso": False,
        "permite_sotano": True,
        "permite_planta_baja": False,
        "capacidad": {"items": 500, "mascotas": 0},
        "max_por_casa": 1,
        "requiere": ["sotano"],
    },
    
    RoomType.ARMERIA: {
        "nombre": "Armería",
        "descripcion": "Almacenamiento de armas y armaduras",
        "efectos": {"defensa": 1.1},
        "costo_base": {"madera": 40, "mineral": 50},
        "permite_piso": True,
        "permite_sotano": True,
        "permite_planta_baja": False,
        "capacidad": {"items": 400, "mascotas": 0},
    },
    
    RoomType.SANTUARIO: {
        "nombre": "Santuario",
        "descripcion": "Lugar sagrado de poder espiritual",
        "efectos": {"afinidad": 1.25, "iluminacion": 1.2, "meditacion": 1.15},
        "costo_base": {"madera": 80, "mineral": 100},
        "permite_piso": False,
        "permite_sotano": False,
        "permite_planta_baja": False,
        "capacidad": {"items": 50, "mascotas": 0},
        "max_por_casa": 1,
        "requiere": ["piso_alto"],  # Debe estar en piso alto
    },
    
    RoomType.JARDIN: {
        "nombre": "Jardín",
        "descripcion": "Cultivo de plantas y hierbas",
        "efectos": {"agricultura": 1.3, "cosecha": 1.2},
        "costo_base": {"madera": 30, "mineral": 10},
        "permite_piso": False,
        "permite_sotano": False,
        "permite_planta_baja": True,
        "capacidad": {"items": 200, "mascotas": 0},
        "max_por_casa": 1,
        "requiere": ["planta_baja"],
    },
}

# Costos de expansión por nivel
EXPANSION_COSTS = {
    FloorLevel.SOTANO_1: {"madera": 100, "mineral": 150},
    FloorLevel.SOTANO_2: {"madera": 150, "mineral": 200},
    FloorLevel.SOTANO_3: {"madera": 200, "mineral": 250},
    FloorLevel.PISO_1: {"madera": 120, "mineral": 100},
    FloorLevel.PISO_2: {"madera": 180, "mineral": 150},
    FloorLevel.PISO_3: {"madera": 250, "mineral": 200},
    FloorLevel.PISO_4: {"madera": 350, "mineral": 300},
}

# Máximo de salas por tipo de casa base
MAX_ROOMS_BY_HOUSE_TYPE = {
    "pequeña": {"planta_baja": 2, "pisos": 0, "sotanos": 0, "salas_total": 2},
    "mediana": {"planta_baja": 4, "pisos": 1, "sotanos": 1, "salas_total": 6},
    "grande": {"planta_baja": 6, "pisos": 2, "sotanos": 2, "salas_total": 12},
    "lujosa": {"planta_baja": 8, "pisos": 3, "sotanos": 3, "salas_total": 20},
    "templo": {"planta_baja": 10, "pisos": 4, "sotanos": 3, "salas_total": 30},
}


# ============================================================================
# CLASES PRINCIPALES
# ============================================================================

class Room:
    """Representa una sala dentro de una casa."""
    
    def __init__(self, room_id, room_type, size, floor_level, nombre=None):
        self.id = room_id
        self.type = room_type
        self.size = size
        self.floor_level = floor_level
        self.nombre_personalizado = nombre
        
        # Estado
        self.fecha_construccion = datetime.now().isoformat()
        self.estado = "completa"  # Podrían tener construcción también
        self.nivel_mejora = 0     # 0-5 para mejoras
        
        # Contenido
        self.inventario = {}
        self.mascotas = []
        
        # Decoraciones
        self.decoraciones = []
    
    def obtener_info(self):
        """Obtiene información de la sala."""
        specs = ROOM_SPECIFICATIONS[self.type]
        return {
            "id": self.id,
            "tipo": self.type.value,
            "nombre": self.nombre_personalizado or specs["nombre"],
            "tamaño": self.size.value,
            "piso": self.floor_level.value,
            "descripcion": specs["descripcion"],
            "efectos": specs["efectos"],
            "items": sum(self.inventario.values()),
            "capacidad": specs["capacidad"]["items"],
            "mascotas": len(self.mascotas),
            "nivel_mejora": self.nivel_mejora,
        }
    
    def agregar_item(self, item_name, cantidad):
        """Agrega item a la sala."""
        specs = ROOM_SPECIFICATIONS[self.type]
        capacidad = specs["capacidad"]["items"]
        usado = sum(self.inventario.values())
        
        if usado >= capacidad:
            return False, "Sala llena"
        
        espacio = capacidad - usado
        cantidad_a_agregar = min(cantidad, espacio)
        self.inventario[item_name] = self.inventario.get(item_name, 0) + cantidad_a_agregar
        
        return True, f"Guardado {cantidad_a_agregar}x {item_name}"
    
    def mejorar_sala(self, materiales_requeridos):
        """Mejora la sala a nivel siguiente."""
        if self.nivel_mejora >= 5:
            return False, "Sala ya está al máximo nivel"
        
        self.nivel_mejora += 1
        
        # Aumenta efectos por mejora (+5% por nivel)
        specs = ROOM_SPECIFICATIONS[self.type]
        for efecto, valor in specs["efectos"].items():
            multiplicador_mejora = 1.0 + (0.05 * self.nivel_mejora)
            specs["efectos"][efecto] = valor * (1.0 + 0.05)
        
        return True, f"Sala mejorada a nivel {self.nivel_mejora}"


class HouseFloor:
    """Representa un piso/nivel de una casa."""
    
    def __init__(self, floor_level):
        self.floor_level = floor_level
        self.salas = {}  # {room_id: Room}
        self.estado = "disponible"  # "disponible", "en_construccion", "cerrado"
        self.fecha_expansion = datetime.now().isoformat()
    
    def agregar_sala(self, room):
        """Agrega una sala al piso."""
        self.salas[room.id] = room
        return True, f"Sala {room.id} agregada al piso {self.floor_level.value}"
    
    def remover_sala(self, room_id):
        """Remueve una sala del piso."""
        if room_id in self.salas:
            del self.salas[room_id]
            return True, f"Sala {room_id} removida"
        return False, f"Sala {room_id} no encontrada"
    
    def obtener_info(self):
        """Obtiene información del piso."""
        return {
            "piso": self.floor_level.value,
            "estado": self.estado,
            "salas": len(self.salas),
            "salas_lista": {rid: r.obtener_info() for rid, r in self.salas.items()},
            "fecha_expansion": self.fecha_expansion,
        }


class ExpandedHouse:
    """Extensión del sistema de casas con salas modulares."""
    
    def __init__(self, base_house):
        self.base_house = base_house
        self.pisos = {}  # {FloorLevel: HouseFloor}
        
        # Inicializar planta baja automáticamente
        self.pisos[FloorLevel.PLANTA_BAJA] = HouseFloor(FloorLevel.PLANTA_BAJA)
        
        # Contador de salas
        self.contador_salas = 0
        self.salas_por_tipo = {}  # {RoomType: cantidad}
        
        # Expansiones realizadas
        self.expansiones = {
            "sotanos": [],
            "pisos": [],
        }
        
        # Límites
        casa_type = base_house.type.value
        self.limites = MAX_ROOMS_BY_HOUSE_TYPE[casa_type]
    
    def expandir_piso(self, floor_level, materiales_disponibles):
        """Expande la casa agregando un nuevo piso/sótano."""
        
        # Validar que no exista ya
        if floor_level in self.pisos:
            return False, f"Piso {floor_level.value} ya existe"
        
        # Obtener costo
        if floor_level not in EXPANSION_COSTS:
            return False, f"No se puede expandir a piso {floor_level.value}"
        
        costo = EXPANSION_COSTS[floor_level]
        
        # Validar materiales
        for material, cantidad in costo.items():
            if materiales_disponibles.get(material, 0) < cantidad:
                return False, f"No tienes suficiente {material}"
        
        # Crear piso
        self.pisos[floor_level] = HouseFloor(floor_level)
        
        # Registrar expansión
        if floor_level.value < 0:
            self.expansiones["sotanos"].append(floor_level)
        else:
            self.expansiones["pisos"].append(floor_level)
        
        return True, f"Piso {floor_level.value} expandido exitosamente"
    
    def agregar_sala(self, room_type, size, floor_level, nombre=None, materiales_disponibles=None):
        """Agrega una sala a un piso específico."""
        
        # Validar piso existe
        if floor_level not in self.pisos:
            return False, f"Piso {floor_level.value} no existe. Expande primero."
        
        # Obtener especificaciones
        specs = ROOM_SPECIFICATIONS[room_type]
        
        # Validar restricciones de piso
        if floor_level == FloorLevel.PLANTA_BAJA and not specs["permite_planta_baja"]:
            return False, f"{specs['nombre']} no puede estar en planta baja"
        
        if floor_level.value < 0 and not specs["permite_sotano"]:
            return False, f"{specs['nombre']} no puede estar en sótano"
        
        if floor_level.value > 0 and not specs["permite_piso"]:
            return False, f"{specs['nombre']} no puede estar en piso superior"
        
        # Validar límite máximo por tipo
        if "max_por_casa" in specs:
            cantidad_existente = sum(1 for r in self._obtener_todas_salas() 
                                    if r.type == room_type)
            if cantidad_existente >= specs["max_por_casa"]:
                return False, f"Ya tienes el máximo de {specs['nombre']} permitidas"
        
        # Validar límite total de salas
        if len(self._obtener_todas_salas()) >= self.limites["salas_total"]:
            return False, f"Máximo de salas alcanzado ({self.limites['salas_total']})"
        
        # Calcular costo
        costo = self._calcular_costo_sala(room_type, size)
        
        if materiales_disponibles:
            for material, cantidad in costo.items():
                if materiales_disponibles.get(material, 0) < cantidad:
                    return False, f"No tienes suficiente {material}"
        
        # Crear sala
        self.contador_salas += 1
        room_id = f"room_{self.contador_salas}"
        sala = Room(room_id, room_type, size, floor_level, nombre)
        
        # Agregar al piso
        self.pisos[floor_level].agregar_sala(sala)
        
        # Registrar
        self.salas_por_tipo[room_type] = self.salas_por_tipo.get(room_type, 0) + 1
        
        return True, f"Sala {specs['nombre']} agregada en piso {floor_level.value}"
    
    def remover_sala(self, room_id):
        """Remueve una sala de la casa."""
        for floor in self.pisos.values():
            if room_id in floor.salas:
                sala = floor.salas[room_id]
                floor.remover_sala(room_id)
                
                # Decrementar contador
                self.salas_por_tipo[sala.type] -= 1
                if self.salas_por_tipo[sala.type] == 0:
                    del self.salas_por_tipo[sala.type]
                
                return True, f"Sala {room_id} removida"
        
        return False, f"Sala {room_id} no encontrada"
    
    def _obtener_todas_salas(self):
        """Obtiene lista de todas las salas."""
        salas = []
        for floor in self.pisos.values():
            salas.extend(floor.salas.values())
        return salas
    
    def _calcular_costo_sala(self, room_type, size):
        """Calcula costo de una sala según tipo y tamaño."""
        specs = ROOM_SPECIFICATIONS[room_type]
        costo = specs["costo_base"].copy()
        
        # Multiplicador por tamaño
        multiplicadores = {
            RoomSize.PEQUEÑA: 1.0,
            RoomSize.MEDIANA: 1.5,
            RoomSize.GRANDE: 2.0,
        }
        
        multiplicador = multiplicadores.get(size, 1.0)
        costo = {k: int(v * multiplicador) for k, v in costo.items()}
        
        return costo
    
    def obtener_efectos_totales(self):
        """Calcula todos los efectos de la casa."""
        efectos = {}
        
        for sala in self._obtener_todas_salas():
            specs = ROOM_SPECIFICATIONS[sala.type]
            for efecto, valor in specs["efectos"].items():
                if efecto not in efectos:
                    efectos[efecto] = 1.0
                # Multiplicar efectos
                efectos[efecto] *= valor
        
        return efectos
    
    def obtener_info_completa(self):
        """Obtiene información completa de la casa expandida."""
        return {
            "casa_base": self.base_house.obtener_info(),
            "pisos": {
                str(piso_nivel.value): floor.obtener_info() 
                for piso_nivel, floor in self.pisos.items()
            },
            "total_salas": len(self._obtener_todas_salas()),
            "salas_por_tipo": {t.value: c for t, c in self.salas_por_tipo.items()},
            "limites": self.limites,
            "efectos_totales": self.obtener_efectos_totales(),
            "expansiones": {
                "sotanos": [s.value for s in self.expansiones["sotanos"]],
                "pisos": [p.value for p in self.expansiones["pisos"]],
            },
        }
    
    def guardar(self):
        """Convierte la casa expandida a formato serializable."""
        return {
            "base_house_id": self.base_house.id,
            "pisos": {
                str(piso.value): {
                    "estado": floor.estado,
                    "fecha_expansion": floor.fecha_expansion,
                    "salas": {
                        rid: {
                            "tipo": r.type.value,
                            "tamaño": r.size.value,
                            "piso": r.floor_level.value,
                            "nombre": r.nombre_personalizado,
                            "nivel_mejora": r.nivel_mejora,
                            "inventario": r.inventario,
                        }
                        for rid, r in floor.salas.items()
                    }
                }
                for piso, floor in self.pisos.items()
            },
            "contador_salas": self.contador_salas,
            "salas_por_tipo": {t.value: c for t, c in self.salas_por_tipo.items()},
            "expansiones": {
                "sotanos": [s.value for s in self.expansiones["sotanos"]],
                "pisos": [p.value for p in self.expansiones["pisos"]],
            },
        }


class HousingExpansionSystem:
    """Sistema completo de expansión de casas."""
    
    def __init__(self):
        self.casas_expandidas = {}  # {house_id: ExpandedHouse}
    
    def inicializar_expansion(self, base_house):
        """Inicializa el sistema de expansión para una casa."""
        if base_house.id not in self.casas_expandidas:
            self.casas_expandidas[base_house.id] = ExpandedHouse(base_house)
            return True, "Sistema de expansión inicializado"
        return False, "Casa ya tiene sistema de expansión"
    
    def obtener_casa_expandida(self, house_id):
        """Obtiene una casa con expansión."""
        return self.casas_expandidas.get(house_id)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def generar_materiales_para_sala(room_type, size):
    """Genera los materiales necesarios para construir una sala."""
    specs = ROOM_SPECIFICATIONS[room_type]
    costo = specs["costo_base"].copy()
    
    multiplicadores = {
        RoomSize.PEQUEÑA: 1.0,
        RoomSize.MEDIANA: 1.5,
        RoomSize.GRANDE: 2.0,
    }
    
    multiplicador = multiplicadores.get(size, 1.0)
    return {k: int(v * multiplicador) for k, v in costo.items()}


def obtener_tipos_salas_disponibles(floor_level):
    """Obtiene tipos de salas disponibles para un piso específico."""
    disponibles = []
    
    for room_type, specs in ROOM_SPECIFICATIONS.items():
        if floor_level == FloorLevel.PLANTA_BAJA:
            if specs["permite_planta_baja"]:
                disponibles.append(room_type)
        elif floor_level.value < 0:
            if specs["permite_sotano"]:
                disponibles.append(room_type)
        else:
            if specs["permite_piso"]:
                disponibles.append(room_type)
    
    return disponibles


def listar_todos_tipos_salas():
    """Lista todos los tipos de salas disponibles."""
    return [
        {
            "tipo": t.value,
            "nombre": specs["nombre"],
            "descripcion": specs["descripcion"],
            "efectos": specs["efectos"],
            "costo_base": specs["costo_base"],
        }
        for t, specs in ROOM_SPECIFICATIONS.items()
    ]


def listar_todos_pisos():
    """Lista todos los pisos disponibles."""
    return [
        {
            "piso": f.value,
            "nombre": f.name,
            "tipo": "sotano" if f.value < 0 else "piso",
        }
        for f in FloorLevel
    ]


if __name__ == "__main__":
    # Pruebas rápidas
    print("=" * 80)
    print("SISTEMA DE EXPANSION DE CASAS")
    print("=" * 80)
    
    print("\nTipos de salas disponibles:")
    for sala in listar_todos_tipos_salas()[:3]:
        print(f"  • {sala['nombre']}: {sala['descripcion']}")
        print(f"    Efectos: {sala['efectos']}")
        print(f"    Costo base: {sala['costo_base']}\n")
    
    print("\nPisos disponibles:")
    for piso in listar_todos_pisos():
        print(f"  • {piso['nombre']} ({piso['piso']})")
