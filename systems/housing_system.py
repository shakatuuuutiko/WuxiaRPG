#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Housing Completo - WuxiaRPG
Permite construir casas en zonas abiertas o comprar en ciudades
Requiere: Maderas y Minerales de Materiales.json
"""

import json
import os
import random
from datetime import datetime, timedelta
from enum import Enum


# ============================================================================
# ENUMS Y CONSTANTES
# ============================================================================

class HousingType(Enum):
    """Tipos de casas disponibles."""
    PEQUEÑA = "pequeña"        # Cabaña básica
    MEDIANA = "mediana"        # Casa confortable
    GRANDE = "grande"          # Mansión
    LUJOSA = "lujosa"         # Mansion de lujo
    TEMPLO = "templo"         # Hogar espiritual


class HousingStatus(Enum):
    """Estados de una casa."""
    PLANEADA = "planeada"          # En construcción
    EN_CONSTRUCCION = "en_construccion"
    COMPLETA = "completa"          # Completada
    DECORANDO = "decorando"        # Fase de decoración


# Requisitos de construcción por tipo
HOUSING_REQUIREMENTS = {
    HousingType.PEQUEÑA: {
        "nombre": "Cabaña",
        "descripcion": "Pequeño refugio para comenzar",
        "costo_compra": 500,
        "construccion": {
            "Roble": 20,
            "Pino": 30,
            "Hierro Negro": 10,
            "Cobre": 5,
        },
        "tiempo_construccion_horas": 24,
        "efectos": {
            "descanso": 1.1,        # +10% descanso
            "relajacion": 1.05,     # +5% relajación
        },
        "capacidad_storage": 100,
        "slots_decoracion": 5,
    },
    
    HousingType.MEDIANA: {
        "nombre": "Casa",
        "descripcion": "Casa confortable para vivir",
        "costo_compra": 2000,
        "construccion": {
            "Roble": 50,
            "Nogal": 30,
            "Hierro Negro": 30,
            "Cobre": 20,
            "Plata": 10,
        },
        "tiempo_construccion_horas": 72,
        "efectos": {
            "descanso": 1.2,        # +20% descanso
            "relajacion": 1.15,     # +15% relajación
            "cultivo": 1.05,        # +5% cultivo
        },
        "capacidad_storage": 300,
        "slots_decoracion": 15,
    },
    
    HousingType.GRANDE: {
        "nombre": "Mansión",
        "descripcion": "Vasta mansión con múltiples habitaciones",
        "costo_compra": 5000,
        "construccion": {
            "Nogal": 60,
            "Ébano": 40,
            "Hierro Negro": 50,
            "Plata": 40,
            "Oro": 20,
            "Mármol": 30,
        },
        "tiempo_construccion_horas": 168,  # 1 semana
        "efectos": {
            "descanso": 1.35,       # +35% descanso
            "relajacion": 1.25,     # +25% relajación
            "cultivo": 1.15,        # +15% cultivo
            "meditacion": 1.1,      # +10% meditación
        },
        "capacidad_storage": 800,
        "slots_decoracion": 30,
    },
    
    HousingType.LUJOSA: {
        "nombre": "Mansión de Lujo",
        "descripcion": "Palacio de absoluto lujo y poder",
        "costo_compra": 15000,
        "construccion": {
            "Ébano": 80,
            "Madera de Dragón": 50,
            "Platino": 60,
            "Oro": 50,
            "Mármol": 50,
            "Cristal Espiritual": 30,
        },
        "tiempo_construccion_horas": 336,  # 2 semanas
        "efectos": {
            "descanso": 1.5,        # +50% descanso
            "relajacion": 1.4,      # +40% relajación
            "cultivo": 1.25,        # +25% cultivo
            "meditacion": 1.2,      # +20% meditación
            "afinidad": 1.15,       # +15% afinidad elemental
        },
        "capacidad_storage": 1500,
        "slots_decoracion": 50,
    },
    
    HousingType.TEMPLO: {
        "nombre": "Templo Espiritual",
        "descripcion": "Templo sagrado para la iluminación",
        "costo_compra": 20000,
        "construccion": {
            "Ébano": 100,
            "Madera de Dragón": 80,
            "Mármol": 80,
            "Oro": 80,
            "Cristal Espiritual": 60,
            "Esencia Celestial": 40,
        },
        "tiempo_construccion_horas": 504,  # 3 semanas
        "efectos": {
            "descanso": 1.6,        # +60% descanso
            "relajacion": 1.5,      # +50% relajación
            "cultivo": 1.4,         # +40% cultivo
            "meditacion": 1.35,     # +35% meditación
            "afinidad": 1.3,        # +30% afinidad elemental
            "iluminacion": 1.2,     # +20% iluminación
        },
        "capacidad_storage": 2000,
        "slots_decoracion": 75,
    },
}

# Materiales disponibles por tipo
MATERIAL_TYPES = {
    "madera": [
        "Roble", "Pino", "Rama", "Nogal", "Ébano", "Madera de Dragón", "Madera Celestial"
    ],
    "mineral": [
        "Hierro Negro", "Cobre", "Estaño", "Plata", "Oro", "Platino", "Mármol",
        "Cristal Espiritual", "Esencia Celestial"
    ],
}


# ============================================================================
# CLASES PRINCIPALES
# ============================================================================

class House:
    """Representa una casa del jugador."""
    
    def __init__(self, house_id, house_type, owner_id, ubicacion, metodo_adquisicion="construida"):
        self.id = house_id
        self.type = house_type
        self.owner_id = owner_id
        self.ubicacion = ubicacion  # [x, y] o nombre de ciudad
        self.metodo_adquisicion = metodo_adquisicion  # "comprada" o "construida"
        
        # Estado
        self.status = HousingStatus.COMPLETA if metodo_adquisicion == "comprada" else HousingStatus.PLANEADA
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_completacion = None
        
        # Progreso de construcción
        self.progreso_construccion = 0.0  # 0-100%
        self.tiempo_inicio_construccion = None
        
        # Materiales
        self.materiales_requeridos = HOUSING_REQUIREMENTS[house_type]["construccion"].copy()
        self.materiales_usados = {}
        
        # Storage
        self.inventario = {}  # {item_name: cantidad}
        self.capacidad_storage = HOUSING_REQUIREMENTS[house_type]["capacidad_storage"]
        
        # Decoración
        self.decoraciones = []  # Lista de objetos decorativos
        self.slots_decoracion_disponibles = HOUSING_REQUIREMENTS[house_type]["slots_decoracion"]
        
        # Efectos activos
        self.efectos = HOUSING_REQUIREMENTS[house_type]["efectos"].copy()
        
        # Nombre personalizado
        self.nombre_personalizado = None
        
        # Mascotas/NPCs
        self.residentes = []  # NPCs que viven aquí
        
    def obtener_info(self):
        """Obtiene información completa de la casa."""
        return {
            "id": self.id,
            "tipo": self.type.value,
            "dueno": self.owner_id,
            "ubicacion": self.ubicacion,
            "estado": self.status.value,
            "nombre": self.nombre_personalizado or HOUSING_REQUIREMENTS[self.type]["nombre"],
            "descripcion": HOUSING_REQUIREMENTS[self.type]["descripcion"],
            "fecha_creacion": self.fecha_creacion,
            "progreso_construccion": self.progreso_construccion,
            "materiales_requeridos": self.materiales_requeridos,
            "materiales_usados": self.materiales_usados,
            "storage_usado": sum(self.inventario.values()),
            "storage_total": self.capacidad_storage,
            "decoraciones": len(self.decoraciones),
            "slots_decoracion": self.slots_decoracion_disponibles,
            "efectos": self.efectos,
            "residentes": len(self.residentes),
        }
    
    def agregar_material(self, material_name, cantidad):
        """Agrega material a la construcción."""
        if self.status != HousingStatus.PLANEADA and self.status != HousingStatus.EN_CONSTRUCCION:
            return False, "La casa ya está completada"
        
        if material_name not in self.materiales_requeridos:
            return False, f"{material_name} no es necesario para esta casa"
        
        material_necesario = self.materiales_requeridos[material_name]
        material_usado_actual = self.materiales_usados.get(material_name, 0)
        
        if material_usado_actual >= material_necesario:
            return False, f"Ya tienes suficiente {material_name}"
        
        material_restante = material_necesario - material_usado_actual
        cantidad_a_agregar = min(cantidad, material_restante)
        
        self.materiales_usados[material_name] = material_usado_actual + cantidad_a_agregar
        self._actualizar_progreso()
        
        return True, f"Agregado {cantidad_a_agregar}x {material_name}"
    
    def _actualizar_progreso(self):
        """Actualiza el progreso de construcción."""
        if not self.materiales_requeridos:
            self.progreso_construccion = 100.0
            return
        
        total_requerido = sum(self.materiales_requeridos.values())
        total_usado = sum(self.materiales_usados.values())
        
        self.progreso_construccion = min(100.0, (total_usado / total_requerido) * 100)
        
        if self.progreso_construccion >= 100.0:
            self.status = HousingStatus.COMPLETA
            self.fecha_completacion = datetime.now().isoformat()
    
    def completar_construccion(self):
        """Completa la construcción si está lista."""
        if self.progreso_construccion < 100.0:
            return False, f"Construcción incompleta ({self.progreso_construccion:.1f}%)"
        
        self.status = HousingStatus.COMPLETA
        self.fecha_completacion = datetime.now().isoformat()
        return True, "¡Casa completada exitosamente!"
    
    def agregar_item_storage(self, item_name, cantidad):
        """Agrega item al storage."""
        usado_actual = sum(self.inventario.values())
        
        if usado_actual >= self.capacidad_storage:
            return False, "Storage lleno"
        
        espacio_disponible = self.capacidad_storage - usado_actual
        cantidad_a_agregar = min(cantidad, espacio_disponible)
        
        self.inventario[item_name] = self.inventario.get(item_name, 0) + cantidad_a_agregar
        
        return True, f"Guardado {cantidad_a_agregar}x {item_name}"
    
    def extraer_item_storage(self, item_name, cantidad):
        """Extrae item del storage."""
        if item_name not in self.inventario:
            return False, f"No hay {item_name} en el storage"
        
        cantidad_disponible = self.inventario[item_name]
        cantidad_a_extraer = min(cantidad, cantidad_disponible)
        
        self.inventario[item_name] -= cantidad_a_extraer
        if self.inventario[item_name] == 0:
            del self.inventario[item_name]
        
        return True, f"Extraído {cantidad_a_extraer}x {item_name}"
    
    def agregar_decoracion(self, decoracion_data):
        """Agrega una decoración a la casa."""
        if self.slots_decoracion_disponibles <= 0:
            return False, "No hay slots de decoración disponibles"
        
        self.decoraciones.append(decoracion_data)
        self.slots_decoracion_disponibles -= 1
        
        # Actualizar efectos según decoración (opcional)
        if "bonus" in decoracion_data:
            for efecto, valor in decoracion_data["bonus"].items():
                if efecto in self.efectos:
                    self.efectos[efecto] *= (1 + valor)
        
        return True, f"Decoración agregada: {decoracion_data.get('nombre', 'Decoración')}"
    
    def establecer_nombre_personalizado(self, nombre):
        """Establece nombre personalizado para la casa."""
        self.nombre_personalizado = nombre
        return True, f"Casa renombrada a: {nombre}"


class HousingSystem:
    """Sistema principal de housing."""
    
    def __init__(self, data_dir="systems"):
        self.data_dir = data_dir
        self.casas = {}  # {house_id: House}
        self.casas_por_propietario = {}  # {player_id: [house_ids]}
        self.house_counter = 1000
        
        # Cargar materiales disponibles
        self.materiales = self._cargar_materiales()
    
    def _cargar_materiales(self):
        """Carga los materiales desde Materiales.json."""
        try:
            materiales_path = os.path.join(self.data_dir, 'Materiales.json')
            with open(materiales_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            materiales = {}
            for categoria, items in data.items():
                for item in items:
                    materiales[item.get("name")] = {
                        "tipo": categoria,
                        "rareza": item.get("rarity"),
                        "stats": item.get("stats_forja", {}),
                    }
            
            return materiales
        except Exception as e:
            print(f"Error cargando materiales: {e}")
            return {}
    
    def construir_casa(self, player_id, house_type, ubicacion):
        """Inicia la construcción de una casa."""
        if not isinstance(house_type, HousingType):
            house_type = HousingType[house_type.upper()]
        
        # Verificar que el jugador no tenga demasiadas casas
        casas_actuales = len(self.casas_por_propietario.get(player_id, []))
        if casas_actuales >= 3:  # Máximo 3 casas por jugador
            return False, "Ya tienes el máximo de casas (3)"
        
        # Crear nueva casa
        house_id = f"house_{self.house_counter}"
        self.house_counter += 1
        
        nueva_casa = House(house_id, house_type, player_id, ubicacion, "construida")
        
        self.casas[house_id] = nueva_casa
        if player_id not in self.casas_por_propietario:
            self.casas_por_propietario[player_id] = []
        self.casas_por_propietario[player_id].append(house_id)
        
        return True, {
            "house_id": house_id,
            "tipo": house_type.value,
            "ubicacion": ubicacion,
            "materiales_requeridos": nueva_casa.materiales_requeridos,
        }
    
    def comprar_casa(self, player_id, ubicacion_ciudad, house_type):
        """Compra una casa en una ciudad."""
        if not isinstance(house_type, HousingType):
            house_type = HousingType[house_type.upper()]
        
        # Verificar que el jugador no tenga demasiadas casas
        casas_actuales = len(self.casas_por_propietario.get(player_id, []))
        if casas_actuales >= 3:
            return False, "Ya tienes el máximo de casas (3)"
        
        costo = HOUSING_REQUIREMENTS[house_type]["costo_compra"]
        
        # Aquí iría verificación de dinero del jugador
        # Por ahora asumimos que tiene dinero suficiente
        
        # Crear nueva casa comprada
        house_id = f"house_{self.house_counter}"
        self.house_counter += 1
        
        nueva_casa = House(house_id, house_type, player_id, ubicacion_ciudad, "comprada")
        nueva_casa.status = HousingStatus.COMPLETA
        nueva_casa.fecha_completacion = datetime.now().isoformat()
        
        self.casas[house_id] = nueva_casa
        if player_id not in self.casas_por_propietario:
            self.casas_por_propietario[player_id] = []
        self.casas_por_propietario[player_id].append(house_id)
        
        return True, {
            "house_id": house_id,
            "tipo": house_type.value,
            "ubicacion": ubicacion_ciudad,
            "costo": costo,
            "mensaje": f"¡Felicidades! Compraste una {HOUSING_REQUIREMENTS[house_type]['nombre']} en {ubicacion_ciudad}",
        }
    
    def agregar_material_construccion(self, house_id, material_name, cantidad):
        """Agrega material a una casa en construcción."""
        if house_id not in self.casas:
            return False, "Casa no encontrada"
        
        casa = self.casas[house_id]
        return casa.agregar_material(material_name, cantidad)
    
    def obtener_casas_jugador(self, player_id):
        """Obtiene todas las casas de un jugador."""
        house_ids = self.casas_por_propietario.get(player_id, [])
        return [self.casas[hid].obtener_info() for hid in house_ids]
    
    def obtener_casa(self, house_id):
        """Obtiene información de una casa específica."""
        if house_id not in self.casas:
            return None
        
        return self.casas[house_id].obtener_info()
    
    def guardar_casas(self, filepath):
        """Guarda todas las casas a un archivo JSON."""
        datos = {}
        
        for house_id, casa in self.casas.items():
            datos[house_id] = {
                "id": casa.id,
                "tipo": casa.type.value,
                "propietario": casa.owner_id,
                "ubicacion": casa.ubicacion,
                "estado": casa.status.value,
                "fecha_creacion": casa.fecha_creacion,
                "fecha_completacion": casa.fecha_completacion,
                "progreso_construccion": casa.progreso_construccion,
                "materiales_requeridos": casa.materiales_requeridos,
                "materiales_usados": casa.materiales_usados,
                "inventario": casa.inventario,
                "decoraciones": casa.decoraciones,
                "nombre_personalizado": casa.nombre_personalizado,
                "residentes": casa.residentes,
                "efectos": casa.efectos,
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def cargar_casas(self, filepath):
        """Carga casas desde un archivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            for house_id, data in datos.items():
                house_type = HousingType[data["tipo"].upper()]
                casa = House(house_id, house_type, data["propietario"], data["ubicacion"])
                
                # Restaurar datos
                casa.status = HousingStatus[data["estado"].upper()]
                casa.fecha_creacion = data["fecha_creacion"]
                casa.fecha_completacion = data.get("fecha_completacion")
                casa.progreso_construccion = data["progreso_construccion"]
                casa.materiales_requeridos = data["materiales_requeridos"]
                casa.materiales_usados = data["materiales_usados"]
                casa.inventario = data.get("inventario", {})
                casa.decoraciones = data.get("decoraciones", [])
                casa.nombre_personalizado = data.get("nombre_personalizado")
                casa.residentes = data.get("residentes", [])
                casa.efectos = data.get("efectos", casa.efectos)
                
                self.casas[house_id] = casa
                
                # Restaurar índice por propietario
                propietario = data["propietario"]
                if propietario not in self.casas_por_propietario:
                    self.casas_por_propietario[propietario] = []
                self.casas_por_propietario[propietario].append(house_id)
                
                # Actualizar contador
                self.house_counter = max(self.house_counter, int(house_id.split("_")[1]) + 1)
        
        except Exception as e:
            print(f"Error cargando casas: {e}")


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def obtener_materiales_disponibles():
    """Retorna lista de materiales disponibles para construcción."""
    return MATERIAL_TYPES


def obtener_requisitos_casa(house_type):
    """Obtiene requisitos para un tipo de casa."""
    if isinstance(house_type, str):
        house_type = HousingType[house_type.upper()]
    
    return HOUSING_REQUIREMENTS.get(house_type)


def listar_tipos_casas():
    """Lista todos los tipos de casas disponibles."""
    return {
        tipo.value: {
            "nombre": HOUSING_REQUIREMENTS[tipo]["nombre"],
            "descripcion": HOUSING_REQUIREMENTS[tipo]["descripcion"],
            "costo_compra": HOUSING_REQUIREMENTS[tipo]["costo_compra"],
            "materiales": HOUSING_REQUIREMENTS[tipo]["construccion"],
            "efectos": HOUSING_REQUIREMENTS[tipo]["efectos"],
        }
        for tipo in HousingType
    }


if __name__ == "__main__":
    # Test del sistema
    print("=" * 80)
    print("SISTEMA DE HOUSING - TEST")
    print("=" * 80)
    
    system = HousingSystem()
    
    # Test 1: Construir casa pequeña
    print("\n[TEST 1] Construir casa pequeña...")
    success, result = system.construir_casa("player_1", HousingType.PEQUEÑA, [100, 200])
    if success:
        house_id = result["house_id"]
        print(f"✓ Casa creada: {house_id}")
        print(f"  Materiales requeridos: {result['materiales_requeridos']}")
    
    # Test 2: Agregar materiales
    print("\n[TEST 2] Agregando materiales...")
    success, msg = system.agregar_material_construccion(house_id, "Roble", 20)
    print(f"{'✓' if success else '✗'} {msg}")
    
    success, msg = system.agregar_material_construccion(house_id, "Pino", 30)
    print(f"{'✓' if success else '✗'} {msg}")
    
    success, msg = system.agregar_material_construccion(house_id, "Hierro Negro", 10)
    print(f"{'✓' if success else '✗'} {msg}")
    
    success, msg = system.agregar_material_construccion(house_id, "Cobre", 5)
    print(f"{'✓' if success else '✗'} {msg}")
    
    # Test 3: Ver progreso
    print("\n[TEST 3] Progreso de construcción...")
    info = system.obtener_casa(house_id)
    print(f"Progreso: {info['progreso_construccion']:.1f}%")
    print(f"Estado: {info['estado']}")
    
    # Test 4: Comprar casa
    print("\n[TEST 4] Comprar casa en ciudad...")
    success, result = system.comprar_casa("player_2", "Metrópolis Maldita en el Bosque", HousingType.MEDIANA)
    if success:
        print(f"✓ {result['mensaje']}")
        print(f"  Costo: {result['costo']} oro")
    
    # Test 5: Obtener casas del jugador
    print("\n[TEST 5] Casas del jugador 1...")
    casas = system.obtener_casas_jugador("player_1")
    for casa in casas:
        print(f"  • {casa['nombre']} ({casa['tipo']}) - {casa['estado']}")
    
    print("\n" + "=" * 80)
