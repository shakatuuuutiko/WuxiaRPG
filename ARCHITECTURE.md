# 🏗️ ARQUITECTURA DEL SISTEMA INTEGRADO

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                   WUXIA RPG - SISTEMA INTEGRADO                 │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│   GENERACIÓN (Backend)   │
├──────────────────────────┤
│                          │
│  resource_gen_v2.py      │  ◄─ Genera 39 materiales
│  ├─ Maderas (15)         │     con atributos
│  ├─ Minerales (14)       │     dureza, conductividad, peso
│  └─ Plantas (10)         │     o tags para alquimia
│                          │
│  ↓ Guardado en           │
│  Materiales.json         │
│                          │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│   CRAFTING (Sistema)     │
├──────────────────────────┤
│                          │
│  crafting.py             │  ◄─ Forja dinámica
│  ├─ ForgeSystem          │     Nombres generados
│  │  ├─ forge_weapon()    │     automáticamente
│  │  └─ forge_batch()     │
│  │                       │
│  └─ AlchemySystem        │  ◄─ Alquimia procedural
│     ├─ craft_potion()    │     Recetas por tags
│     └─ mix_ingredients() │
│                          │
│  ↓ Output                │
│  Equipment objects       │
│                          │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  EQUIPAMIENTO (Nueva)    │
├──────────────────────────┤
│                          │
│  equipment.py            │  ◄─ Gestión de armas
│  ├─ Equipment            │     Durabilidad
│  │  ├─ stats base        │     Degradación
│  │  └─ durability        │     Serialización
│  │                       │
│  └─ CharacterEquipment   │  ◄─ Inventario
│     ├─ equipped_weapon   │     Cambio de equipo
│     ├─ inventory[]       │     Reparación
│     └─ métodos útiles    │
│                          │
└──────────┬───────────────┘
           │
           ├─────────────────────┬─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │ PLAYER        │    │ COMPANION     │    │ NPC/Boss      │
    ├───────────────┤    ├───────────────┤    ├───────────────┤
    │ main.py       │    │ companion.py  │    │ (Godot/Future)│
    │               │    │               │    │               │
    │ ├─ equipment  │    │ ├─ equipment  │    │ ├─ equipment  │
    │ ├─ stats      │    │ ├─ stats      │    │ ├─ stats      │
    │ ├─ inventory  │    │ ├─ inventory  │    │ ├─ inventory  │
    │ │             │    │ │             │    │ │             │
    │ ├─ get_total  │    │ ├─ get_total  │    │ ├─ get_total  │
    │ │ _atk()      │    │ │ _atk()      │    │ │ _atk()      │
    │ └─ methods    │    │ └─ methods    │    │ └─ methods    │
    │               │    │               │    │               │
    └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
            │                    │                    │
            └────────┬───────────┴────────┬───────────┘
                     │                    │
                     ▼                    ▼
            ┌────────────────────────────────┐
            │     COMBAT ENGINE              │
            ├────────────────────────────────┤
            │ combat.py                      │
            │                                │
            │ calculate_damage():            │  ◄─ Detecta automáticamente
            │ ├─ if hasattr(obj, 'equip')    │     si tiene equipamiento
            │ │  ├─ usa get_total_atk()      │     Suma daño de arma
            │ │  └─ calcula con equipo       │
            │ └─ else                        │
            │    └─ usa stats simples        │
            │                                │
            │ Retorna: (daño, crítico,      │
            │          ventaja elemental)    │
            │                                │
            └────────────────────────────────┘
```

## Flujo de Datos

```
GENERACIÓN
┌─────────────────────────────────────────┐
│ Materiales.json se carga en crafting.py │
│ al importar el módulo                   │
└──────────────────────────────┬──────────┘
                               │
FORJA
┌──────────────────────────────▼──────────┐
│ ForgeSystem.forge_weapon(molde,         │
│   wood_entry, mineral_entry)            │
│                                         │
│ Selecciona materiales (aleatorios)      │
│ Calcula daño base + bonificadores       │
│ Genera nombre dinámico                  │
│ Retorna weapon_dict                     │
└──────────────────────────────┬──────────┘
                               │
EQUIPAMIENTO
┌──────────────────────────────▼──────────┐
│ weapon = Equipment(weapon_dict)         │
│ player.equipment.equip_weapon(weapon)   │
│                                         │
│ Almacena: nombre, ATK, durabilidad      │
│           componentes, rareza           │
└──────────────────────────────┬──────────┘
                               │
COMBATE
┌──────────────────────────────▼──────────┐
│ engine.calculate_damage(player,         │
│   enemy.stats, skill=None)              │
│                                         │
│ Detecta: hasattr(player, 'equipment')   │
│ Llama: player.get_total_atk()           │
│ Calcula: 20 + 100 = 120 ATK            │
│ Retorna: daño final considerando        │
│          elementos, defensa, crítico    │
└──────────────────────────────┬──────────┘
                               │
RESULTADO
┌──────────────────────────────▼──────────┐
│ Daño aplicado a enemigo                 │
│ Durabilidad del arma se degrada         │
│ Combate continúa...                     │
└─────────────────────────────────────────┘
```

## Interconexiones

### Player ↔ Equipment
```
Player
├─ stats: dict
├─ equipment: CharacterEquipment
│  ├─ equipped_weapon: Equipment
│  │  ├─ name: str
│  │  ├─ atk: int
│  │  ├─ durability: int
│  │  └─ ...
│  └─ inventory: [Equipment, ...]
│
├─ get_total_atk()
│  └─ return stats['atk'] + equipment.get_equipped_damage()
│
└─ get_attack_speed()
   └─ return equipment.get_equipped_speed()
```

### Companion ↔ Equipment
```
Companion (similar a Player)
├─ stats: dict
├─ archetype: str
├─ level: int
├─ equipment: CharacterEquipment (mismo sistema)
│
├─ get_total_atk()
├─ get_attack_speed()
├─ gain_experience()
├─ level_up()
└─ take_damage() / heal()
```

### CompanionParty ↔ Companion
```
CompanionParty
├─ companions: [Companion, ...]
├─ max_size: int
│
├─ add_companion(companion)
├─ remove_companion(index)
├─ get_total_power()  ← sum(c.get_total_atk())
├─ get_alive_count()
└─ heal_all(amount)
```

## Clases Principales

### 1. `equipment.py`
```
Equipment
├─ name: str
├─ type: str ('Arma')
├─ mold: str
├─ atk: int
├─ speed: float
├─ durability: int
├─ max_durability: int
├─ components: dict
├─ rarities: dict
│
├─ take_damage(amount)
├─ repair(amount=None)
├─ get_effective_damage()
├─ is_broken()
└─ to_dict() / from_dict()

CharacterEquipment
├─ equipped_weapon: Equipment
├─ inventory: [Equipment]
│
├─ equip_weapon(equipment)
├─ unequip_weapon()
├─ add_to_inventory(equipment)
├─ remove_from_inventory(index)
├─ get_equipped_damage()
├─ get_equipped_speed()
├─ repair_equipped()
├─ repair_all()
├─ list_inventory()
└─ to_dict() / from_dict()
```

### 2. `companion.py`
```
Companion
├─ name: str
├─ rank: int
├─ stats: dict
├─ equipment: CharacterEquipment
├─ loyalty: int (0-100)
├─ archetype: str
│
├─ get_total_atk()
├─ gain_experience(amount)
├─ level_up()
├─ take_damage(damage)
├─ heal(amount)
├─ is_alive()
└─ to_dict() / from_dict()

CompanionParty
├─ companions: [Companion]
├─ max_size: int
│
├─ add_companion(companion)
├─ remove_companion(index)
├─ heal_all(amount)
├─ get_total_power()
├─ get_alive_count()
└─ to_dict() / from_dict()

CompanionGenerator
└─ generate(rank) → Companion proceduralmente generado
```

## Patrón de Diseño: Template Method

El sistema usa el patrón **Template Method** en combate:

```
CombatEngine.calculate_damage()
├─ if hasattr(attacker, 'equipment'):
│  └─ usa get_total_atk() del attacker
├─ else:
│  └─ usa stats simples del dict
└─ Resto del cálculo igual para ambos casos
```

Esto permite:
- ✅ Compatibilidad con código antiguo
- ✅ Soporte automático para nuevos objetos
- ✅ Extensibilidad futura

## Inversión de Dependencias

```
Alto Nivel
    │
    ├─ Player, Companion, NPC
    │      │
    │      ▼
    │  CharacterEquipment (interfaz de equipamiento)
    │      │
    │      ▼
    │  Equipment (arma forjada)
    │      │
    │      ▼
Bajo Nivel
    └─ crafting.Materials (datos)
```

**Beneficios:**
- Bajo acoplamiento
- Fácil testing
- Escalable a más tipos de personajes

## Extensibilidad

Para añadir un nuevo tipo de personaje equipable:

```python
class MysteryMaster:
    def __init__(self):
        self.equipment = CharacterEquipment()  # Hereda toda la funcionalidad
        self.stats = {...}
    
    def get_total_atk(self):
        return self.stats['atk'] + self.equipment.get_equipped_damage()
    
    # ¡Ya funciona con el sistema de combate sin cambios!
```

## Persistencia

Todo el sistema soporta serialización JSON:

```
Player
├─ to_dict()
│  ├─ equipment: equipment.to_dict()
│  │  ├─ equipped: weapon.to_dict()
│  │  └─ inventory: [weapon.to_dict(), ...]
│  └─ otros datos...
│
└─ from_dict(data)
   └─ equipment = CharacterEquipment.from_dict(data['equipment'])
```

---

## Conclusión

La arquitectura es:
- ✅ **Modular**: Cada componente es independiente
- ✅ **Extensible**: Fácil añadir nuevos tipos de personajes
- ✅ **Escalable**: Soporta grupos grandes
- ✅ **Persistente**: Todo se puede guardar/cargar
- ✅ **Compatible**: No rompe código existente
- ✅ **Testeable**: Cada componente puede testearse aisladamente
