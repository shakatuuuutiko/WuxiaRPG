# Sistema de Crafting Mejorado - WuxiaRPG

## Descripción

Se ha implementado un sistema completo de crafting (forja y alquimia) que utiliza materiales dinámicos generados proceduralmente en `systems/Materiales.json`.

### Características

#### 1. **Forja Dinámica**
- Genera nombres automáticamente basados en los materiales utilizados
- Formato: `[Molde] [Descriptor_Madera] de [Mineral] ([Calidad])`
- Ejemplo: `Sable Eterno de Oro Galáctico (Legendario)`

**Moldes disponibles:**
- Daga, Espada, Lanza, Sable, Arco, Hacha, Pico

**Cálculo de daño:**
```
base_atk = base_del_molde + (dureza_mineral * 0.7 + dureza_madera * 0.3) * densidad_molde
factor_peso = ajuste por peso promedio
factor_calidad = 0.95 - 1.25 (variabilidad)
ataque_final = (base_atk) * factor_peso * factor_calidad
```

**Rareza de salida:**
- Se hereda de la rareza más alta entre madera y mineral
- Sufijos: Común, Raro, Épico, Legendario

#### 2. **Alquimia (Herbología)**
- Mezcla plantas con tags específicos (Fuego, Vida, Hielo, Agua, Sangre, etc.)
- Genera píldoras según los tags combinados
- Incorpora penalización por "pureza" de ingredientes

**Recetas disponibles:**
- Píldora Yang: Fuego > 30 + Estabilidad > 10
- Píldora Curativa Mayor: Vida > 20
- Píldora Congelante: Hielo > 25 + Agua > 15
- Píldora de Sangre Vital: Sangre > 20

#### 3. **Generación de Materiales**
- **Maderas:** 15 entradas (Común, Raro, Épico, Legendario)
- **Minerales:** 14 entradas (Común, Raro, Épico, Legendario)
- **Plantas:** 10 entradas (Común, Raro, Épico, Legendario)

Cada material tiene:
```json
{
  "name": "Sable Eterno",
  "rarity": "Legendario",
  "type": "Maderas",
  "stats_forja": {
    "dureza": 78,
    "conductividad": 125,
    "peso": 15.29
  }
}
```

## Uso

### Forjar un arma

```python
from systems.crafting import ForgeSystem, Materials

forge = ForgeSystem()

# Forja automática (materiales aleatorios)
weapon = forge.forge_weapon("Sable")
print(f"Arma: {weapon['name']}")
print(f"Ataque: {weapon['atk']}")

# Forja con materiales específicos
wood = Materials['Maderas'][0]  # Primer material de madera
mineral = Materials['Minerales'][0]
weapon = forge.forge_weapon("Espada", wood_entry=wood, mineral_entry=mineral)

# Lote de forja
batch = forge.forge_batch("Arco", count=5)
for weapon in batch:
    print(f"- {weapon['name']} (ATK: {weapon['atk']})")
```

### Crear pociones

```python
from systems.crafting import AlchemySystem

alchemy = AlchemySystem()

# Crear una poción
potion = alchemy.craft_potion(count=3)  # Usa 3 plantas
print(f"Poción: {potion['name']}")
print(f"Éxito: {potion['success']}")
print(f"Potencia: {potion['potency']}")
```

### Acceder a materiales

```python
from systems.crafting import Materials
import json

# Ver todas las maderas
print(f"Total de maderas: {len(Materials['Maderas'])}")

# Buscar por rareza
raras = [m for m in Materials['Maderas'] if m['rarity'] == 'Raro']
print(f"Maderas raras: {len(raras)}")

# Obtener estadísticas
madera = Materials['Maderas'][0]
stats = madera.get('stats_forja', {})
print(f"Dureza: {stats['dureza']}, Peso: {stats['peso']}")
```

## Archivos

- `systems/resource_gen_v2.py` - Generador de materiales procedurales
- `systems/crafting.py` - Sistema de forja y alquimia
- `systems/Materiales.json` - Base de datos de materiales (generado)
- `test_crafting.py` - Script de demostración

## Regenerar Materiales

Si deseas regenerar los materiales con valores diferentes:

```bash
python systems/resource_gen_v2.py
```

Esto creará un nuevo `systems/Materiales.json` con valores aleatorios.

## Estadísticas de Ejemplo

### Maderas
- **Roble (Común):** Dureza: 18, Conductividad: 13, Peso: 2.13
- **Madera de Fénix (Épico):** Dureza: 70, Conductividad: 73, Peso: 4.3
- **Roble Eterno (Legendario):** Dureza: 71, Conductividad: 93, Peso: 19.99

### Minerales
- **Roca (Común):** Dureza: 39, Conductividad: 24, Peso: 7.06
- **Mithril (Épico):** Dureza: 60, Conductividad: 50, Peso: 25.0
- **Adamantita Estelar (Legendario):** Dureza: 110, Conductividad: 130, Peso: 65.0

### Plantas
- **Hierba Medicinal (Común):** Tags: {Vida: 6, Hielo: 11}
- **Ginseng de 100 años (Raro):** Tags: {Fuego: 20, Estabilidad: 15}
- **Hierba de la Eternidad (Legendario):** Tags: {Vida: 50, Pureza: 60}

## Ejemplo de Salida Completa

```
=== SISTEMA DE CRAFTING ===

--- FORJA DE ARMAS ---
Nombre: Sable Eterno de Oro Galáctico (Eterno)
Ataque: 102
Componentes: {'madera': 'Raíz del Eterno Mundo', 'mineral': 'Oro Galáctico'}

--- LOTE DE ARCOS ---
1. Arco Eterno de Adamantita Estelar (Legendario) (ATK: 90)
2. Arco Roble de Hierro (Común) (ATK: 47)
3. Arco Eterno de Cristal (Legendario) (ATK: 70)

--- ALQUIMIA ---
Poción: Píldora Curativa Mayor
Éxito: True
Potencia: 202
```

## Extensiones Futuras

1. Mejora de rarezas según calidad de forja
2. Runas y encantamientos post-forja
3. Sistema de transmutación avanzada
4. Equipamiento de personajes
5. Almacenamiento y gestión de inventario
