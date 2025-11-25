# Sistema de Expansión Modular de Casas - WuxiaRPG

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Conceptos Clave](#conceptos-clave)
3. [Tipos de Salas](#tipos-de-salas)
4. [Niveles y Pisos](#niveles-y-pisos)
5. [Materiales y Costos](#materiales-y-costos)
6. [API de Uso](#api-de-uso)
7. [Ejemplos Prácticos](#ejemplos-prácticos)
8. [Efectos y Bonificaciones](#efectos-y-bonificaciones)
9. [Restricciones y Límites](#restricciones-y-límites)
10. [Persistencia y Guardado](#persistencia-y-guardado)

---

## 🏠 Descripción General

El **Sistema de Expansión Modular de Casas** permite que los jugadores expandan y personalicen sus hogares agregando salas especializadas en múltiples niveles (sótanos, planta baja, pisos superiores).

### Características Principales

- ✅ **Múltiples Niveles**: Sótanos (hasta -3), Planta Baja (0), Pisos Superiores (1-4)
- ✅ **12 Tipos de Salas**: Dormitorios, Dojo, Biblioteca, Meditación, Tesoro, y más
- ✅ **Efectos Multiplicativos**: Cada sala otorga bonificaciones a diferentes stats
- ✅ **Límites Inteligentes**: Máximo de salas por tipo de casa base
- ✅ **Persistencia Total**: Todos los datos se guardan en JSON

---

## 🎯 Conceptos Clave

### Casa Base (ExpandedHouse)

La casa base es la estructura inicial que el jugador compra o construye. Sobre ella se pueden expandir múltiples pisos y sótanos.

```python
# Inicializar expansión de una casa
base_house = House("house_001", HousingType.GRANDE, "jugador_1", [100, 200])
expanded = ExpandedHouse(base_house)
```

### Pisos (HouseFloor)

Cada piso/nivel es un contenedor de salas. Inicialmente solo existe la planta baja.

```python
# Acceder al piso
planta_baja = expanded.pisos[FloorLevel.PLANTA_BAJA]
piso_1 = expanded.pisos[FloorLevel.PISO_1]
sotano_1 = expanded.pisos[FloorLevel.SOTANO_1]
```

### Salas (Room)

Las salas son los elementos modulares que se agregan a cada piso. Cada sala tiene efectos específicos.

```python
# Crear una sala
exito, msg = expanded.agregar_sala(
    RoomType.DORMITORIO,
    RoomSize.MEDIANA,
    FloorLevel.PLANTA_BAJA,
    nombre="Mi Dormitorio Personal"
)
```

---

## 🛏️ Tipos de Salas

### 1. **Dormitorio**
- **Descripción**: Espacio para descansar
- **Efectos**: +15% Descanso
- **Ubicaciones Permitidas**: Planta Baja, Pisos Superiores
- **Capacidad**: 50 items, 1 mascota
- **Costo Base**: 20 Madera, 10 Mineral

### 2. **Sala de Estar**
- **Descripción**: Lugar para relajarse
- **Efectos**: +20% Relajación
- **Ubicaciones Permitidas**: Planta Baja, Pisos Superiores
- **Capacidad**: 30 items, 2 mascotas
- **Costo Base**: 15 Madera, 5 Mineral

### 3. **Cocina**
- **Descripción**: Para preparar comidas
- **Efectos**: +10% Regeneración
- **Ubicaciones Permitidas**: Planta Baja SOLO
- **Capacidad**: 200 items
- **Costo Base**: 25 Madera, 15 Mineral
- **Máximo por Casa**: 1

### 4. **Biblioteca**
- **Descripción**: Colección de libros y pergaminos
- **Efectos**: +15% Sabiduría, +10% Iluminación
- **Ubicaciones Permitidas**: Cualquier nivel
- **Capacidad**: 500 items
- **Costo Base**: 30 Madera, 20 Mineral

### 5. **Dojo**
- **Descripción**: Sala de entrenamiento
- **Efectos**: +25% Cultivo, +10% Ataque
- **Ubicaciones Permitidas**: Planta Baja SOLO
- **Capacidad**: 100 items, 1 mascota
- **Costo Base**: 40 Madera, 30 Mineral

### 6. **Laboratorio**
- **Descripción**: Para alquimia y crafting
- **Efectos**: +20% Crafting
- **Ubicaciones Permitidas**: Pisos, Sótanos
- **Capacidad**: 300 items
- **Costo Base**: 35 Madera, 40 Mineral

### 7. **Sala de Meditación**
- **Descripción**: Para meditación profunda
- **Efectos**: +30% Meditación, +15% Iluminación
- **Ubicaciones Permitidas**: Pisos, Sótanos
- **Capacidad**: 20 items
- **Costo Base**: 45 Madera, 35 Mineral
- **Máximo por Casa**: 1

### 8. **Depósito**
- **Descripción**: Almacenamiento adicional
- **Efectos**: Ninguno
- **Ubicaciones Permitidas**: Cualquier nivel
- **Capacidad**: 1000 items
- **Costo Base**: 20 Madera, 15 Mineral

### 9. **Bóveda de Tesoro**
- **Descripción**: Almacenamiento seguro para valuables
- **Efectos**: Ninguno
- **Ubicaciones Permitidas**: Sótanos SOLO
- **Capacidad**: 500 items
- **Costo Base**: 60 Madera, 80 Mineral
- **Máximo por Casa**: 1

### 10. **Armería**
- **Descripción**: Almacenamiento de armas y armaduras
- **Efectos**: +10% Defensa
- **Ubicaciones Permitidas**: Pisos, Sótanos
- **Capacidad**: 400 items
- **Costo Base**: 40 Madera, 50 Mineral

### 11. **Santuario**
- **Descripción**: Lugar sagrado de poder espiritual
- **Efectos**: +25% Afinidad, +20% Iluminación, +15% Meditación
- **Ubicaciones Permitidas**: Pisos SOLO (no planta baja, no sótano)
- **Capacidad**: 50 items
- **Costo Base**: 80 Madera, 100 Mineral
- **Máximo por Casa**: 1

### 12. **Jardín**
- **Descripción**: Cultivo de plantas y hierbas
- **Efectos**: +30% Agricultura, +20% Cosecha
- **Ubicaciones Permitidas**: Planta Baja SOLO
- **Capacidad**: 200 items
- **Costo Base**: 30 Madera, 10 Mineral
- **Máximo por Casa**: 1

---

## 🏢 Niveles y Pisos

### Estructura de Pisos

```
┌─────────────────┐
│   PISO 4 (4)    │  Máximo nivel superior
├─────────────────┤
│   PISO 3 (3)    │
├─────────────────┤
│   PISO 2 (2)    │
├─────────────────┤
│   PISO 1 (1)    │
├─────────────────┤
│ PLANTA BAJA (0) │  Nivel inicial
├─────────────────┤
│  SÓTANO 1 (-1)  │
├─────────────────┤
│  SÓTANO 2 (-2)  │
├─────────────────┤
│  SÓTANO 3 (-3)  │  Máximo nivel inferior
└─────────────────┘
```

### Expansión de Pisos

Para agregar un nuevo piso/sótano, se debe expandir primero:

```python
# Expandir a primer piso
exito, msg = expanded.expandir_piso(
    FloorLevel.PISO_1,
    materiales_disponibles={"madera": 500, "mineral": 500}
)

# Expandir sótano
exito, msg = expanded.expandir_piso(
    FloorLevel.SOTANO_1,
    materiales_disponibles={"madera": 500, "mineral": 500}
)
```

### Costos de Expansión

| Nivel | Madera | Mineral |
|-------|--------|---------|
| Sótano 1 | 100 | 150 |
| Sótano 2 | 150 | 200 |
| Sótano 3 | 200 | 250 |
| Piso 1 | 120 | 100 |
| Piso 2 | 180 | 150 |
| Piso 3 | 250 | 200 |
| Piso 4 | 350 | 300 |

---

## 💎 Materiales y Costos

### Costos Base por Tamaño de Sala

Los costos base se multiplican según el tamaño de la sala:

```
Pequeña (2x2):   1.0x costo base
Mediana (3x3):   1.5x costo base
Grande (4x4):    2.0x costo base
```

### Ejemplo: Dormitorio Mediano
- Costo Base: 20 Madera, 10 Mineral
- Multiplicador Mediano: 1.5
- **Costo Final: 30 Madera, 15 Mineral**

---

## 🔧 API de Uso

### Inicializar Expansión

```python
from systems.housing_expansion_system import ExpandedHouse, HousingExpansionSystem

# Opción 1: Crear ExpandedHouse directamente
expanded = ExpandedHouse(base_house)

# Opción 2: Usar HousingExpansionSystem
system = HousingExpansionSystem()
system.inicializar_expansion(base_house)
expanded = system.obtener_casa_expandida(base_house.id)
```

### Agregar Salas

```python
# Agregar sala
exito, msg = expanded.agregar_sala(
    room_type=RoomType.DORMITORIO,
    size=RoomSize.MEDIANA,
    floor_level=FloorLevel.PLANTA_BAJA,
    nombre="Mi Dormitorio",
    materiales_disponibles={"madera": 500, "mineral": 500}
)

if exito:
    print(f"Sala creada: {msg}")
else:
    print(f"Error: {msg}")
```

### Expandir Pisos

```python
# Expandir piso
exito, msg = expanded.expandir_piso(
    floor_level=FloorLevel.PISO_1,
    materiales_disponibles={"madera": 500, "mineral": 500}
)

if exito:
    print(f"Piso expandido: {msg}")
```

### Obtener Información

```python
# Información completa
info = expanded.obtener_info_completa()
print(f"Total salas: {info['total_salas']}")
print(f"Efectos: {info['efectos_totales']}")

# Información de un piso
piso_info = expanded.pisos[FloorLevel.PLANTA_BAJA].obtener_info()
print(f"Salas en planta baja: {piso_info['salas']}")

# Información de una sala
sala = list(expanded.pisos[FloorLevel.PLANTA_BAJA].salas.values())[0]
sala_info = sala.obtener_info()
print(f"Sala: {sala_info['nombre']}")
```

### Guardar y Cargar

```python
# Guardar
datos = expanded.guardar()
with open("casa_data.json", "w") as f:
    json.dump(datos, f)

# Cargar
with open("casa_data.json", "r") as f:
    datos = json.load(f)
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Casa Simple

```python
# Crear casa base
casa = House("casa_001", HousingType.MEDIANA, "jugador_1", [100, 200])
expanded = ExpandedHouse(casa)

# Agregar dormitorio y sala de estar
expanded.agregar_sala(RoomType.DORMITORIO, RoomSize.MEDIANA, FloorLevel.PLANTA_BAJA)
expanded.agregar_sala(RoomType.SALA_ESTAR, RoomSize.MEDIANA, FloorLevel.PLANTA_BAJA)

# Obtener efectos
efectos = expanded.obtener_efectos_totales()
# Resultado: {'descanso': 1.15, 'relajacion': 1.2}
```

### Ejemplo 2: Casa Compleja

```python
# Casa tipo Lujosa
casa = House("casa_002", HousingType.LUJOSA, "jugador_2", [50, 75])
expanded = ExpandedHouse(casa)

# Planta baja: Áreas públicas
expanded.agregar_sala(RoomType.SALA_ESTAR, RoomSize.GRANDE, FloorLevel.PLANTA_BAJA)
expanded.agregar_sala(RoomType.DOJO, RoomSize.GRANDE, FloorLevel.PLANTA_BAJA)
expanded.agregar_sala(RoomType.COCINA, RoomSize.MEDIANA, FloorLevel.PLANTA_BAJA)

# Piso 1: Áreas privadas
expanded.expandir_piso(FloorLevel.PISO_1, {"madera": 500, "mineral": 500})
expanded.agregar_sala(RoomType.DORMITORIO, RoomSize.GRANDE, FloorLevel.PISO_1)
expanded.agregar_sala(RoomType.MEDITACION, RoomSize.MEDIANA, FloorLevel.PISO_1)

# Sótano: Almacenamiento
expanded.expandir_piso(FloorLevel.SOTANO_1, {"madera": 500, "mineral": 500})
expanded.agregar_sala(RoomType.TESORO, RoomSize.GRANDE, FloorLevel.SOTANO_1)
expanded.agregar_sala(RoomType.LABORATORIO, RoomSize.MEDIANA, FloorLevel.SOTANO_1)

# Ver información
info = expanded.obtener_info_completa()
print(f"Total salas: {info['total_salas']}")
print(f"Pisos: {list(info['pisos'].keys())}")
```

---

## ⭐ Efectos y Bonificaciones

### Cómo Funcionan los Efectos

Cada sala otorga bonificaciones multiplicativas a estadísticas del jugador. Los efectos se aplican cuando el jugador está dentro de la casa.

### Efectos Disponibles

| Efecto | Descripción | Salas |
|--------|-------------|-------|
| **Descanso** | Recuperación de HP | Dormitorio (+15%), Templo (+60%) |
| **Relajación** | Reducción de estrés | Sala de Estar (+20%), Templo (+50%) |
| **Cultivo** | Velocidad de entrenamiento | Dojo (+25%), Templo (+40%) |
| **Meditación** | Meditación profunda | Meditación (+30%), Templo (+35%) |
| **Iluminación** | Progreso espiritual | Biblioteca (+10%), Meditación (+15%), Santuario (+20%), Templo (+20%) |
| **Sabiduría** | Inteligencia | Biblioteca (+15%) |
| **Crafting** | Velocidad de creación | Laboratorio (+20%) |
| **Defensa** | Protección | Armería (+10%) |
| **Regeneración** | Regeneración automática | Cocina (+10%) |
| **Agricultura** | Cultivo de plantas | Jardín (+30%) |
| **Cosecha** | Recolección | Jardín (+20%) |
| **Afinidad** | Control elemental | Santuario (+25%), Templo (+30%) |
| **Ataque** | Daño | Dojo (+10%) |

### Cálculo de Efectos

Los efectos se **multiplican** cuando hay múltiples salas con el mismo efecto:

```
Dormitorio: descanso = 1.15
+ Templo: descanso = 1.60

Efecto total = 1.15 * 1.60 = 1.84x (84% de bonificación)
```

---

## 🔒 Restricciones y Límites

### Límites por Tipo de Casa

| Casa | Planta Baja | Pisos | Sótanos | Total Salas |
|------|-------------|-------|---------|------------|
| Pequeña | 2 | 0 | 0 | 2 |
| Mediana | 4 | 1 | 1 | 6 |
| Grande | 6 | 2 | 2 | 12 |
| Lujosa | 8 | 3 | 3 | 20 |
| Templo | 10 | 4 | 3 | 30 |

### Restricciones de Ubicación

- **Planta Baja SOLO**: Cocina, Dojo, Jardín
- **Pisos SOLO**: Santuario
- **Sótanos SOLO**: Bóveda de Tesoro
- **Cualquier Nivel**: Dormitorio, Biblioteca, Depósito, Laboratorio, Armería
- **Pisos o Sótanos**: Meditación

### Máximo por Casa

- Cocina: 1 máximo
- Meditación: 1 máximo
- Bóveda de Tesoro: 1 máximo
- Santuario: 1 máximo
- Jardín: 1 máximo

### Validaciones

✅ No se puede crear sala en piso no expandido
✅ No se puede crear más salas que el límite total
✅ No se puede crear sala especial si ya existe una
✅ No se puede crear sala sin materiales suficientes
✅ No se puede agregar material si la sala está completa

---

## 💾 Persistencia y Guardado

### Estructura de Datos Guardada

```json
{
  "base_house_id": "house_001",
  "contador_salas": 5,
  "pisos": {
    "0": {
      "estado": "disponible",
      "salas": {
        "room_1": {
          "tipo": "dormitorio",
          "tamaño": "mediana",
          "piso": 0,
          "nombre": "Mi Dormitorio",
          "nivel_mejora": 0,
          "inventario": {}
        }
      }
    }
  },
  "salas_por_tipo": {
    "dormitorio": 1,
    "dojo": 1
  },
  "expansiones": {
    "sotanos": [-1],
    "pisos": [1, 2]
  }
}
```

### Guardar Casa

```python
datos = expanded.guardar()

with open("saves/casas.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2)
```

### Cargar Casa

```python
with open("saves/casas.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Reconstruir
expanded = ExpandedHouse(base_house)
# ... lógica de reconstrucción basada en datos guardados
```

---

## 🧪 Testing

El sistema cuenta con **18 tests** que verifican:

- ✅ Inicialización de casas expandidas
- ✅ Creación de salas en diferentes niveles
- ✅ Expansión de pisos y sótanos
- ✅ Restricciones de ubicación
- ✅ Límites de salas especiales
- ✅ Validación de materiales
- ✅ Cálculo de efectos
- ✅ Persistencia de datos
- ✅ Información completa de casa

**Tasa de Éxito: 100% (18/18 PASS)**

---

## 📝 Notas Importantes

1. **Costos Modulares**: Los costos se calculan dinámicamente basados en tamaño y tipo
2. **Efectos Acumulativos**: Los efectos se multiplican, no suman
3. **Persistencia Automática**: Los datos deben guardarse manualmente
4. **Límites Balanceados**: Cada tipo de casa tiene límites apropiados a su poder
5. **Extensible**: Fácil agregar nuevos tipos de salas o niveles

---

## 🚀 Próximas Mejoras

- [ ] Decoraciones dentro de salas
- [ ] Residentes (NPCs) en casas
- [ ] Sistema de alquiler/venta de casas
- [ ] Eventos especiales en salas
- [ ] Mejoras de salas (nivel 1-5)
- [ ] Jardín con cultivo de plantas
- [ ] Mercado de viviendas

---

**Versión**: 1.0  
**Última Actualización**: 2024  
**Tests**: 18/18 PASS ✅  
**Status**: Production Ready 🚀
