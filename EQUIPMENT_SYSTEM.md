# Sistema de Equipamiento Integrado - WuxiaRPG

## Resumen

Se ha implementado un sistema completo de **equipamiento para personajes y NPCs** que integra:
- Sistema de crafting mejorado
- Gestión de armas con durabilidad
- Compañeros (NPCs) equipables
- Combate considerando equipamiento
- Persistencia de datos

## Características

### 1. **Equipamiento Individual** (`equipment.py`)

#### Clase `Equipment`
Representa un arma forjada que puede ser equipada.

```python
# Crear una arma
weapon = Equipment(forge.forge_weapon("Sable"))

# Acceder a propiedades
print(weapon.name)           # "Sable Espiritual de Hierro (Legendario)"
print(weapon.atk)            # 95
print(weapon.durability)     # 100/120
print(weapon.speed)          # 1.3

# Degradación en combate
weapon.take_damage(10)       # -10 durabilidad
damage_efectivo = weapon.get_effective_damage()  # ATK * (durabilidad/max)

# Reparación
weapon.repair()              # Restaura completamente
```

#### Clase `CharacterEquipment`
Gestiona el inventario de armas de un personaje.

```python
eq = CharacterEquipment()

# Equipar arma
eq.equip_weapon(weapon1)

# Inventario
eq.add_to_inventory(weapon2)
eq.add_to_inventory(weapon3)

# Cambiar equipo
eq.equip_weapon(eq.remove_from_inventory(0))

# Información
print(eq.list_inventory())   # Lista formateada
print(eq.get_equipped_damage())  # Daño total
print(eq.get_equipped_speed())   # Velocidad
```

### 2. **Player con Equipamiento** (actualizado en `main.py`)

El jugador ahora tiene:
- Sistema de equipamiento integrado
- Método `get_total_atk()` que suma stats base + arma
- Método `get_attack_speed()` para velocidad de ataque

```python
player = Player()

# Equipamiento automático
print(player.equipment.equipped_weapon.name)  # Espada inicial

# Daño total (stats + equipo)
total_damage = player.get_total_atk()

# Equipar nuevas armas
new_weapon = Equipment(forge.forge_weapon("Sable"))
player.equipment.equip_weapon(new_weapon)
```

### 3. **Compañeros Equipables** (`companion.py`)

#### Clase `Companion`
Representa un NPC/esclavo/aliado con equipamiento.

```python
# Crear compañero
comp = Companion("Xiao Ming", rank=2)

# Propiedades
print(comp.archetype)           # "Guerrero", "Arquero", "Mago", etc.
print(comp.get_total_atk())     # ATK stats + arma equipada
print(comp.equipment)           # Sistema de equipamiento

# Experiencia y niveles
comp.gain_experience(50)
comp.level_up()  # Stats aumentan automáticamente

# Salud
comp.take_damage(30)
comp.heal(15)
comp.is_alive()  # bool
```

#### Clase `CompanionParty`
Gestiona múltiples compañeros.

```python
party = CompanionParty(max_size=5)

# Añadir miembros
party.add_companion(comp1)
party.add_companion(comp2)

# Información del grupo
print(party.get_total_power())      # Poder combinado ATK
print(party.get_alive_count())      # Vivos / totales

# Curación
party.heal_all(20)

# Serialización
data = party.to_dict()
party_loaded = CompanionParty.from_dict(data)
```

#### Clase `CompanionGenerator`
Genera compañeros procedurales.

```python
# Generar compañero aleatorio
comp = CompanionGenerator.generate(rank=3)

# Características:
# - Arqueotipo aleatorio (Guerrero, Mago, etc.)
# - Stats modificados según arqueotipo
# - Equipo forjado automáticamente
```

### 4. **Combate Mejorado** (actualizado en `combat.py`)

El sistema de combate ahora:
- Acepta Player/NPC u objetos con `get_total_atk()`
- Calcula automáticamente daño con equipamiento
- Mantiene compatibilidad con sistema anterior

```python
engine = CombatEngine()

# Combate con Player (con equipamiento)
damage, is_crit, advantage = engine.calculate_damage(
    player,              # Automáticamente usa total_atk
    enemy.stats,
    skill_data=None
)

# Combate con stats simples (compatibilidad)
damage, is_crit, advantage = engine.calculate_damage(
    {"atk": 50, "element": "Fuego"},
    enemy.stats
)
```

## Flujo Integrado

### Ejemplo Completo: Forjar y Equipar

```python
from systems.crafting import ForgeSystem
from systems.equipment import Equipment
from systems.companion import Companion, CompanionGenerator
from main import Player

# 1. FORJAR ARMAS
forge = ForgeSystem()
sable = Equipment(forge.forge_weapon("Sable"))
arco = Equipment(forge.forge_weapon("Arco"))

# 2. EQUIPAR JUGADOR
player = Player()
player.equipment.equip_weapon(sable)
print(f"Jugador ATK: {player.get_total_atk()}")

# 3. CREAR COMPAÑEROS Y EQUIPARLOS
comp = CompanionGenerator.generate(rank=2)
comp.equip_weapon(arco)
print(f"Compañero ATK: {comp.get_total_atk()}")

# 4. COMBATE
engine = CombatEngine()
damage = engine.calculate_damage(player, comp.stats)[0]
print(f"Daño: {damage}")

# 5. DEGRADACIÓN
player.equipment.equipped_weapon.take_damage(15)
print(f"Nueva durabilidad: {player.equipment.equipped_weapon.durability}")

# 6. REPARACIÓN
player.equipment.equipped_weapon.repair()
```

## Archivos Modificados

1. **`systems/equipment.py`** (NUEVO)
   - `Equipment`: Representa armas con durabilidad
   - `CharacterEquipment`: Gestión de inventario
   - Funciones helper para serialización

2. **`systems/companion.py`** (NUEVO)
   - `Companion`: NPC/esclavo equipable
   - `CompanionParty`: Gestión de grupos
   - `CompanionGenerator`: Generación procedural

3. **`main.py`** (MODIFICADO)
   - `Player` ahora tiene `equipment: CharacterEquipment`
   - Métodos `get_total_atk()` y `get_attack_speed()`
   - Importa equipment y crafting

4. **`systems/combat.py`** (MEJORADO)
   - `calculate_damage()` ahora acepta objetos con equipamiento
   - Detecta si el atacante es Player/NPC u objeto stats
   - Automáticamente suma daño del equipo

5. **`systems/crafting.py`** (SIN CAMBIOS)
   - Continúa funcionando igual
   - Compatible con sistema de equipamiento

## Tests

### `test_crafting.py`
- Forja de armas individuales
- Lotes de forja
- Alquimia de pociones

### `test_equipment_integration.py`
- Equipamiento de jugador
- Compañeros con equipo
- Combate con equipamiento
- Gestión de inventario
- Integración end-to-end

**Ejecución:**
```bash
python test_equipment_integration.py
```

**Output de Ejemplo:**
```
TEST 1: EQUIPAMIENTO DEL JUGADOR
Jugador: Hu Bo
ATK Total (con equipo): 120
Arma equipada: Espada Raíz de Cristal (Magistral)
  Daño base: 100
  Durabilidad: 120/120

TEST 2: COMPAÑEROS CON EQUIPAMIENTO
1. Compañero 4860 (Mago) - Rango G2
   ATK Total: 83
   Arma: Lanza Rama de Hierro (Común)

TEST 3: COMBATE CON EQUIPAMIENTO
Ataque del Jugador: 114 daño
Enemigo ahora tiene 0/100 HP

✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE
```

## Mecanánica de Durabilidad

**Degradación:**
- Cada ataque/combate reduce durabilidad
- Daño efectivo = ATK_base * (durabilidad / max_durabilidad)

**Rangos de durabilidad:**
- Verde (80-100%): Sin penalización
- Amarillo (50-80%): -10% daño
- Naranja (25-50%): -30% daño
- Rojo (0-25%): -50% daño

**Reparación:**
- `weapon.repair()`: Restaura completamente
- `weapon.repair(amount)`: Repara cantidad parcial
- `equipment.repair_all()`: Repara todo el inventario

## Persistencia

Todas las clases incluyen métodos `to_dict()` y `from_dict()`:

```python
# Guardar
player_data = {
    'name': player.name,
    'equipment': player.equipment.to_dict(),
    # ... otros datos
}

# Cargar
player.equipment = CharacterEquipment.from_dict(data['equipment'])
```

## Límites Actuales

1. Solo armas (no armadura, accesorios)
2. Un arma equipada por personaje
3. Sin encantamientos post-forja
4. Sin mejora de durabilidad

## Extensiones Futuras

1. Sistema de armadura (yelmo, pecho, guantes, botas)
2. Accesorios (anillos, brazaletes)
3. Encantamientos y runas
4. Mejora de durabilidad
5. Armas únicas legendarias
6. Transmutación de equipamiento
7. Herencia de equipment entre jugadores
8. Comercio de equipamiento

## Ejemplo: Sistema Completo en Acción

```python
# ESCENARIO: Jugador negocia con comerciante de armas

# 1. Comerciante forja 10 espadas
merchant_forge = ForgeSystem()
merchant_inventory = []
for i in range(10):
    sword = Equipment(merchant_forge.forge_weapon("Espada"))
    merchant_inventory.append(sword)

# 2. Jugador elige la mejor
player = Player()
best_sword = max(merchant_inventory, key=lambda w: w.atk)
cost = best_sword.atk * 10  # 10 oro por daño

if player.inventory.get("Oro", 0) >= cost:
    player.inventory["Oro"] -= cost
    player.equipment.equip_weapon(best_sword)
    print(f"¡Comprada! Nueva espada: {best_sword.name}")
    print(f"Nuevo ATK: {player.get_total_atk()}")

# 3. Jugador forma grupo para mazmorras
party = CompanionParty(max_size=3)
for i, sword in enumerate(merchant_inventory[:3]):
    comp = CompanionGenerator.generate(rank=1)
    comp.equip_weapon(sword)
    party.add_companion(comp)

print(f"Poder del grupo: {party.get_total_power()}")

# 4. Simulación de mazmorra (5 combates)
enemies_defeated = 0
for round_num in range(5):
    enemy = CompanionGenerator.generate(rank=1)
    
    # Combate
    engine = CombatEngine()
    while player.stats["hp"] > 0 and enemy.stats["hp"] > 0:
        # Ataque del jugador
        dmg = engine.calculate_damage(player, enemy.stats)[0]
        enemy.take_damage(dmg)
        player.equipment.equipped_weapon.take_damage(5)
        
        if enemy.stats["hp"] <= 0:
            enemies_defeated += 1
            break
        
        # Ataque del enemigo
        dmg = engine.calculate_damage(enemy, player.stats)[0]
        player.stats["hp"] -= dmg
    
    if player.stats["hp"] <= 0:
        break

print(f"Enemigos derrotados: {enemies_defeated}")
print(f"Durabilidad del arma: {player.equipment.equipped_weapon.durability}")

# 5. Reparación después de mazmorra
player.equipment.repair_equipped()
print("¡Arma reparada en el templo!")
```

## Soporte

Para problemas o sugerencias, revisar logs en:
- `test_equipment_integration.py` - Tests funcionales
- `systems/equipment.py` - Implementación detallada
- `systems/companion.py` - Lógica de compañeros
