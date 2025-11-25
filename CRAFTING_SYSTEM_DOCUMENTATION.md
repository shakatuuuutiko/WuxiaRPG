# 🔨 SISTEMA DE CRAFTING AVANZADO - WuxiaRPG

## Descripción General

El nuevo sistema de crafting es un completo rediseño del módulo `systems/crafting.py` que permite crear:

- **Armas** (22 tipos) - Con prefijos y efectos especiales
- **Herramientas** (7 tipos) - Con sufijos de efectividad
- **Armaduras** (8 partes) - Con prefijos y defensa escalonada
- **Pócimas/Alquimia** (11 recetas) - Sistema procedural basado en tags

---

## 1️⃣ ARMAS - SISTEMA DE PREFIJOS

### 21 Tipos de Armas Disponibles

#### Armas Originales (7)
| Arma | ATK Base | SPD | Densidad |
|------|----------|-----|----------|
| Daga | 25 | 1.8 | 1.5 |
| Espada | 35 | 1.0 | 1.1 |
| Lanza | 32 | 1.2 | 0.9 |
| Sable | 30 | 1.3 | 1.0 |
| Arco | 28 | 1.5 | 0.7 |
| Hacha | 40 | 0.9 | 1.6 |
| Pico | 38 | 0.8 | 1.8 |

#### Armas Nuevas (15)
| Arma | ATK Base | SPD | Densidad | Tipo |
|------|----------|-----|----------|------|
| Catana | 36 | 1.4 | 1.05 | Cortante rápida |
| Falcata | 38 | 1.1 | 1.2 | Cortante equilibrada |
| Claymore | 45 | 0.85 | 1.3 | Gran espada |
| Tridente | 35 | 1.25 | 1.15 | Lanza con garfios |
| Martillo | 42 | 0.7 | 1.7 | Contundente |
| Maza | 39 | 0.75 | 1.55 | Arma contundente |
| Mangual | 41 | 0.95 | 1.4 | Cadena de impacto |
| Guadaña | 37 | 1.3 | 0.95 | Hoz de batalla |
| Espada Ancha | 43 | 0.95 | 1.25 | Espada pesada |
| Bastón | 26 | 1.6 | 0.8 | Arma mágica |
| Garras | 28 | 1.7 | 1.2 | Ataque rápido |
| Horca | 31 | 1.15 | 1.0 | Herramienta de batalla |
| Espada Corta | 27 | 1.35 | 1.1 | Arma rápida |
| Alabarda | 40 | 1.1 | 1.05 | Lanza con hacha |

### 10 Prefijos para Armas

Cada prefijo modifica los stats base y proporciona un efecto especial:

```python
WEAPON_PREFIXES = {
    "Fantasmal":    {"atk_mult": 0.95, "speed_mult": 1.15, "special": "Ignore Armor"},
    "Brutal":       {"atk_mult": 1.25, "speed_mult": 0.85, "special": "Bleed"},
    "Ágil":         {"atk_mult": 0.90, "speed_mult": 1.25, "special": "Extra Hit"},
    "Fiero":        {"atk_mult": 1.30, "speed_mult": 0.80, "special": "Crush"},
    "Maldito":      {"atk_mult": 1.10, "speed_mult": 0.95, "special": "Drain HP"},
    "Bendito":      {"atk_mult": 1.05, "speed_mult": 1.05, "special": "Heal on Hit"},
    "Glacial":      {"atk_mult": 1.00, "speed_mult": 1.10, "special": "Slow Enemy"},
    "Ígneo":        {"atk_mult": 1.15, "speed_mult": 0.95, "special": "Burn Damage"},
    "Venenoso":     {"atk_mult": 0.95, "speed_mult": 1.05, "special": "Poison"},
    "Eléctrico":    {"atk_mult": 1.05, "speed_mult": 1.20, "special": "Stun"}
}
```

### Ejemplos de Uso

#### Forjar Arma Aleatorio
```python
from systems.crafting import ForgeSystem

forge = ForgeSystem()

# Arma aleatoria con prefijo aleatorio
weapon = forge.forge_weapon("Claymore")
print(f"Arma: {weapon['name']}")
print(f"ATK: {weapon['atk']} | SPD: {weapon['speed']}")
print(f"Prefijo: {weapon['prefix']}")
print(f"Efecto: {weapon['special_effect']}")

# Salida ejemplo:
# Arma: Brutal Claymore Espiritual de Mithril del Vacío (Divina)
# ATK: 153 | SPD: 0.72
# Prefijo: Brutal
# Efecto: Bleed
```

#### Forjar Arma con Prefijo Específico
```python
# Arma con prefijo específico
weapon = forge.forge_weapon("Espada", prefix="Eléctrico")
print(f"Arma: {weapon['name']}")
print(f"Efecto Especial: {weapon['special_effect']}")
```

#### Lote de Armas
```python
# Forjar 5 arcos diferentes
bows = forge.forge_batch("Arco", count=5)
for bow in bows:
    print(f"{bow['name']} - ATK: {bow['atk']}, SPD: {bow['speed']}")
```

---

## 2️⃣ HERRAMIENTAS - SISTEMA DE SUFIJOS

### 7 Tipos de Herramientas

```python
TOOL_MOLDS = {
    "Pico":        {"mining_power": 40},
    "Hacha":       {"chopping_power": 38},
    "Pala":        {"digging_power": 35},
    "Azada":       {"tilling_power": 32},
    "Hoz":         {"harvesting_power": 28},
    "Cuchillo":    {"cutting_power": 22},
    "Sierra":      {"sawing_power": 36}
}
```

### 8 Sufijos para Herramientas

Los sufijos afectan potencia y durabilidad:

```python
TOOL_SUFFIXES = {
    "Refinada":     {"power_mult": 1.10, "durability_mult": 0.95},
    "Robusta":      {"power_mult": 0.95, "durability_mult": 1.15},
    "Maestra":      {"power_mult": 1.20, "durability_mult": 1.05},
    "Perdurable":   {"power_mult": 0.90, "durability_mult": 1.25},
    "Experta":      {"power_mult": 1.15, "durability_mult": 1.00},
    "Imbuida":      {"power_mult": 1.25, "durability_mult": 0.90},
    "Afilada":      {"power_mult": 1.18, "durability_mult": 0.92},
    "Templada":     {"power_mult": 1.05, "durability_mult": 1.10}
}
```

### Ejemplos de Uso

#### Crear Herramienta
```python
from systems.crafting import ToolSystem

tools = ToolSystem()

# Crear un pico aleatorio
pico = tools.craft_tool("Pico")
print(f"Nombre: {pico['name']}")
print(f"Potencia: {pico['power']}")
print(f"Durabilidad: {pico['durability']}")
print(f"Sufijo: {pico['suffix']}")

# Salida ejemplo:
# Nombre: Pico Tronco Maestra (Común)
# Potencia: 76
# Durabilidad: 105
# Sufijo: Maestra
```

#### Crear Herramienta con Sufijo Específico
```python
# Crear hacha Perdurable
hacha = tools.craft_tool("Hacha", suffix="Perdurable")
print(f"Durabilidad máxima: {hacha['durability']}")
```

#### Lote de Herramientas
```python
# Crear 10 picos diferentes
picos = tools.craft_batch("Pico", count=10)
for i, pico in enumerate(picos, 1):
    print(f"{i}. {pico['name']} - Potencia: {pico['power']}")
```

---

## 3️⃣ ARMADURAS - SISTEMA DE PREFIJOS

### 8 Partes de Armadura

```python
ARMOR_PARTS = {
    "Casco":            {"def_base": 15, "weight": 8, "slots": 1},
    "Pechera":          {"def_base": 25, "weight": 15, "slots": 2},
    "Guantes":          {"def_base": 10, "weight": 4, "slots": 1},
    "Cintura":          {"def_base": 12, "weight": 5, "slots": 1},
    "Grebas":           {"def_base": 18, "weight": 10, "slots": 1},
    "Botas":            {"def_base": 8, "weight": 3, "slots": 1},
    "Escudo":           {"def_base": 20, "weight": 12, "slots": 1},
    "Cota de Malla":    {"def_base": 22, "weight": 18, "slots": 2}
}
```

### Características de Armadura

- **Prefijo**: Mismo sistema que las armas (Brutal, Bendito, Maldito, etc.)
- **Defensa**: Calculada según mineral y prefijo
- **Peso**: Afecta agilidad del portador
- **Slots**: Espacios para encantamientos (futuro)

### Ejemplos de Uso

#### Forjar Pieza Individual
```python
from systems.crafting import ArmorSystem

armor = ArmorSystem()

# Crear pechera aleatoria
pechera = armor.forge_armor("Pechera")
print(f"Nombre: {pechera['name']}")
print(f"Defensa: {pechera['defense']}")
print(f"Peso: {pechera['weight']}")
print(f"Efecto: {pechera['special_effect']}")

# Salida ejemplo:
# Nombre: Brutal Pechera de Adamantita (Excelente)
# Defensa: 92
# Peso: 15
# Efecto: Bleed
```

#### Forjar Conjunto Completo
```python
# Crear conjunto con prefijo específico (Benedito)
full_set = armor.forge_full_set(prefix="Bendito")

total_def = 0
for piece in full_set:
    print(f"{piece['name']} - DEF: {piece['defense']}")
    total_def += piece['defense']

print(f"DEFENSA TOTAL: {total_def}")
```

#### Lote de Piezas
```python
# Crear 5 cascos diferentes
cascos = armor.forge_batch("Casco", count=5)
for casco in cascos:
    print(f"{casco['name']} - DEF: {casco['defense']}")
```

---

## 4️⃣ ALQUIMIA - SISTEMA PROCEDURAL

### 11 Recetas Disponibles

El sistema de alquimia analiza los tags de plantas y genera pócimas dinámicamente:

```python
RECIPE_TEMPLATES = {
    'Fuego':        {'efecto': 'Daño por Fuego'},
    'Hielo':        {'efecto': 'Daño por Hielo'},
    'Veneno':       {'efecto': 'Daño por Veneno'},
    'Electricidad': {'efecto': 'Daño por Electricidad'},
    'Vida':         {'efecto': 'Restauración de Salud'},
    'Defensa':      {'efecto': 'Aumento de Defensa'},
    'Velocidad':    {'efecto': 'Aumento de Velocidad'},
    'Sabiduría':    {'efecto': 'Aumento de Mana/Energía'},
    'Yang':         {'efecto': 'Poder Ofensivo Aumentado'},
    'Yin':          {'efecto': 'Defensa y Regeneración'},
    'Sangre':       {'efecto': 'Daño Crítico Aumentado'}
}
```

### Ejemplos de Uso

#### Mezclar Poción
```python
from systems.crafting import AlchemySystem

alchemy = AlchemySystem()

# Crear poción con 3 ingredientes
potion = alchemy.craft_potion(count=3)
print(f"Poción: {potion['name']}")
print(f"Éxito: {potion['success']}")
print(f"Efecto: {potion['effect']}")
print(f"Potencia: {potion['potency']}")
```

#### Lote de Pócimas
```python
# Crear 10 pócimas
potions = alchemy.craft_batch(count=10)
successful = sum(1 for p in potions if p['success'])
print(f"Éxito: {successful}/10")
```

#### Descubrir Receta
```python
# Buscar receta con tag específico
recipe = alchemy.discover_recipe("Fuego", min_value=25)
if recipe:
    print(f"Receta: {recipe['recipe_name']}")
    print(f"Necesita: {recipe['tags_needed']}")
```

---

## 5️⃣ CARACTERÍSTICAS PRINCIPALES

### ✅ Sistema de Nombre Dinámico

Cada item generado tiene un nombre único y descriptivo:

```
"Brutal Claymore Espiritual de Mithril del Vacío (Divina)"
  ↓      ↓        ↓            ↓       ↓     ↓        ↓
Prefijo Molde    Descriptor   Mineral  Extra Rareza Quality
```

### ✅ Multiplicadores de Stats

- **Armas**: Prefijo modifica ATK × SPD
- **Herramientas**: Sufijo modifica Potencia × Durabilidad  
- **Armaduras**: Prefijo modifica Defensa

### ✅ Sistema de Rarezas

```python
RARITY_ORDER = {"Común": 0, "Raro": 1, "Épico": 2, "Legendario": 3}

MATERIAL_SUFFIXES = {
    "Común": ["Común", "Ordinaria", "Básica"],
    "Raro": ["Rara", "Refinada", "Bien Hecha"],
    "Épico": ["Épica", "Magistral", "Excelente"],
    "Legendario": ["Legendaria", "Divina", "Celestial"]
}
```

### ✅ Efectos Especiales

Cada arma/armadura puede tener un efecto especial:
- Bleed (Sangrado)
- Stun (Aturdimiento)
- Burn Damage (Daño por Fuego)
- Drain HP (Drenaje de Vida)
- Ignore Armor (Ignora Armadura)
- Heal on Hit (Cura al Golpear)
- Poison (Veneno)
- Slow Enemy (Ralentizar)
- Extra Hit (Golpe Extra)
- Crush (Aplastante)

---

## 6️⃣ INTEGRACIÓN EN game_engine.py

### Ejemplo de Integración

```python
from systems.crafting import ForgeSystem, ToolSystem, ArmorSystem, AlchemySystem

# En el método __init__ del GameEngine
self.forge = ForgeSystem()
self.tools = ToolSystem()
self.armor = ArmorSystem()
self.alchemy = AlchemySystem()

# En los comandos de jugador
def cmd_forjar_arma(self, tipo_arma, prefijo=None):
    """Forja un arma específica"""
    arma = self.forge.forge_weapon(tipo_arma, prefix=prefijo)
    self.player.inventory.agregar_item(arma)
    return f"✓ Se forjó: {arma['name']}"

def cmd_craftar_herramienta(self, tipo_herramienta):
    """Crea una herramienta"""
    tool = self.tools.craft_tool(tipo_herramienta)
    self.player.inventory.agregar_item(tool)
    return f"✓ Se crafteó: {tool['name']}"

def cmd_crear_armadura(self, parte_armadura, prefijo=None):
    """Forja una pieza de armadura"""
    piece = self.armor.forge_armor(parte_armadura, prefix=prefijo)
    self.player.inventory.agregar_item(piece)
    return f"✓ Se forjó: {piece['name']}"

def cmd_mezclar_pocion(self, cantidad_ingredientes=3):
    """Mezcla una poción con plantas"""
    potion = self.alchemy.craft_potion(count=cantidad_ingredientes)
    if potion['success']:
        self.player.inventory.agregar_item(potion)
        return f"✓ Poción exitosa: {potion['name']}"
    else:
        return f"✗ Poción fallida: {potion['name']}"
```

---

## 7️⃣ ESTADÍSTICAS FINALES

| Categoría | Cantidad |
|-----------|----------|
| **Armas** | 21 |
| **Herramientas** | 7 |
| **Partes de Armadura** | 8 |
| **Prefijos** | 10 |
| **Sufijos** | 8 |
| **Recetas Alquímicas** | 11 |
| **Efectos Especiales** | 10 |
| **Rarezas** | 4 |
| **TOTAL de Combinaciones** | 1000+ únicas |

---

## 🎯 CASOS DE USO

### Caso 1: Jugador Recolector
```python
# Recolecta minerales y madera
# Los transforma en herramientas especializadas
tools = ToolSystem()
pico = tools.craft_tool("Pico", suffix="Maestra")  # Mayor potencia de minería
hacha = tools.craft_tool("Hacha", suffix="Robusta")  # Mayor durabilidad
```

### Caso 2: Forjador Especializado
```python
# Forja armas con prefijos específicos
forge = ForgeSystem()
espada_brutal = forge.forge_weapon("Espada", prefix="Brutal")  # Daño alto
arco_agil = forge.forge_weapon("Arco", prefix="Ágil")  # Velocidad alta
```

### Caso 3: Alquimista
```python
# Experimenta con recetas
alchemy = AlchemySystem()
for i in range(20):
    potion = alchemy.craft_potion(count=random.randint(2, 5))
    if potion['success']:
        print(f"✓ {potion['name']}")
```

### Caso 4: Guerrero Equipado
```python
# Forma conjunto completo de armadura
armor = ArmorSystem()
full_set = armor.forge_full_set(prefix="Brutal")
total_def = sum(p['defense'] for p in full_set)
print(f"Armadura Brutal: {total_def} defensa total")
```

---

## 📝 NOTAS TÉCNICAS

- Todos los valores se calculan dinámicamente según materiales disponibles
- El factor de calidad (0.95 - 1.25) añade variabilidad incluso con los mismos materiales
- Los prefijos y sufijos son independientes: se pueden combinar cualquier prefijo con cualquier molde
- El sistema es modular y permite agregar nuevos prefijos/sufijos sin modificar código existente

---

## 🚀 FUTURAS MEJORAS

1. **Encantamientos**: Sistema de slots para encantar items
2. **Degradación**: Durabilidad decreciente con uso
3. **Mejoras**: Sistema de upgrade para items existentes
4. **Desencanto**: Extraer materials de items viejos
5. **Especializaciones**: Crafteros que producen items mejores
6. **Recetas Dinámicas**: Descubrimiento de nuevas recetas en juego

---

## 📌 REFERENCIAS RÁPIDAS

### Imports
```python
from systems.crafting import ForgeSystem, ToolSystem, ArmorSystem, AlchemySystem
from systems.crafting import WEAPON_MOLDS, TOOL_MOLDS, ARMOR_PARTS
from systems.crafting import WEAPON_PREFIXES, TOOL_SUFFIXES, MATERIAL_SUFFIXES
```

### Objetos Retornados

**Arma**:
```python
{
    'name': str,
    'type': 'Arma',
    'mold': str,
    'prefix': str,
    'atk': int,
    'speed': float,
    'special_effect': str,
    'components': dict,
    'rarities': dict
}
```

**Herramienta**:
```python
{
    'name': str,
    'type': 'Herramienta',
    'tool_type': str,
    'suffix': str,
    'power': int,
    'durability': int,
    'components': dict,
    'rarity': str
}
```

**Armadura**:
```python
{
    'name': str,
    'type': 'Armadura',
    'part': str,
    'prefix': str,
    'defense': int,
    'weight': int,
    'slots': int,
    'special_effect': str,
    'component': str,
    'rarity': str
}
```

**Poción**:
```python
{
    'name': str,
    'success': bool,
    'effect': str,
    'potency': int,
    'ingredients': list,
    'ingredient_count': int
}
```
