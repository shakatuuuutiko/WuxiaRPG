╔═══════════════════════════════════════════════════════════════════════════════╗
║              MAPA TÉCNICO DE VINCULACIONES - QUIEN USA A QUIÉN                ║
║                              WuxiaRPG Architecture                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
📋 ÍNDICE DE ARCHIVOS Y SUS DEPENDENCIAS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ CORE / CONFIGURACIÓN                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 config.py                                                                 │
│    Purpose: Configuración global del juego                                   │
│    Defines: WINDOW_WIDTH, HEIGHT, COLORS, TILE_SIZE, CHUNK_SIZE, FPS        │
│    Imports: None (library-only)                                              │
│    Used by:                                                                  │
│       ├─ main.py (config)                                                    │
│       ├─ systems/map_core.py (CHUNK_SIZE, VOID_TILE)                        │
│       ├─ ui/game_engine.py (FPS, WINDOW_WIDTH, COLORS)                      │
│       ├─ ui/main_menu.py (WINDOW_WIDTH, COLORS, APP_TITLE)                  │
│       ├─ ui/map_render.py (COLORS, TILE_SIZE, CHUNK_SIZE)                   │
│       ├─ ui/pygame_renderer.py (COLORS, WINDOW_WIDTH, TILE_SIZE, CHUNK_SIZE)│
│       └─ ui/pygame_utils.py (COLORS)                                        │
│    Total Importadores: 7                                                    │
│    Status: ✓ FUNDAMENTAL                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ENTRADA PRINCIPAL                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 main.py                                                                   │
│    Purpose: Script maestro, orquesta todo el juego                           │
│    Defines: class Player, main() function                                    │
│    Imports:                                                                  │
│       Library:                                                               │
│           ├─ pygame                                                          │
│           ├─ sys                                                             │
│           └─ random                                                          │
│       Local:                                                                 │
│           ├─ config (WINDOW_WIDTH, HEIGHT, APP_TITLE, FPS)                 │
│           ├─ systems.cultivation (SpiritRoot)                               │
│           ├─ systems.bloodline (Bloodline)                                  │
│           ├─ systems.time_system (TimeSystem, AgeManager)                   │
│           ├─ systems.origin_generator (OriginGenerator)                     │
│           ├─ systems.map_core (MapManager)                                  │
│           ├─ systems.equipment (CharacterEquipment, Equipment, create_starter_weapon)
│           ├─ systems.crafting (ForgeSystem)                                 │
│           ├─ ui.game_engine (GameEngine)                                    │
│           └─ ui.main_menu (MainMenu)                                        │
│    Used by:                                                                  │
│       ├─ verify_all.py (imports Player)                                     │
│       └─ verify_integration.py (imports Player)                             │
│    Total Importadores: 2 (test files)                                       │
│    Status: ✓ ORQUESTADOR CENTRAL                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ SISTEMAS ATÓMICOS (No dependen de otros sistemas)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 systems/time_system.py                                                    │
│    Purpose: Sistema de tiempo, edad y ciclos                                 │
│    Defines: TimeSystem, AgeManager, LIFESPAN_TABLE                          │
│    Imports: math (library)                                                   │
│    Used by: main.py, ui/game_engine.py                                       │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/origin_generator.py                                               │
│    Purpose: Generador procedural de orígenes de personajes                   │
│    Defines: OriginGenerator class                                            │
│    Imports: random (library)                                                 │
│    Used by: main.py                                                          │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/bloodline.py                                                      │
│    Purpose: Sistema de linajes de sangre                                     │
│    Defines: Bloodline class                                                  │
│    Imports: random (library)                                                 │
│    Used by: main.py                                                          │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/cultivation.py                                                    │
│    Purpose: Sistema de cultivo espiritual                                    │
│    Defines: SpiritRoot, CultivationManager                                   │
│    Imports: random (library)                                                 │
│    Used by: main.py, ui/game_engine.py                                       │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/combat.py                                                         │
│    Purpose: Motor de combate con sistema de elementos                        │
│    Defines: CombatEngine, ELEMENT_CHART                                      │
│    Imports: random (library)                                                 │
│    Used by: ui/game_engine.py, systems/tournament.py                         │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/manual_system.py                                                  │
│    Purpose: Sistema de manuales/técnicas                                     │
│    Defines: ManualManager class                                              │
│    Imports: random (library)                                                 │
│    Used by: ui/popups.py                                                     │
│    Status: ✓ INDEPENDIENTE                                                  │
│                                                                              │
│ 📄 systems/tournament.py                                                     │
│    Purpose: Sistema de torneos                                               │
│    Defines: Tournament classes                                               │
│    Imports: random, math (library)                                           │
│    Uses: systems.combat (CombatEngine)                                       │
│    Status: ✓ SIMPLE DEPENDENCIA                                             │
│                                                                              │
│ 📄 systems/artifact_spirit.py [NOT USED]                                     │
│    Purpose: Artefactos espirituales inteligentes                             │
│    Defines: Soul, ArtifactSpirit                                             │
│    Imports: random (library)                                                 │
│    Used by: NADIE (opcional para futuro)                                     │
│    Status: ⚠ HUÉRFANO                                                       │
│                                                                              │
│ 📄 systems/social_ai.py [NOT USED]                                           │
│    Purpose: Motor de IA social                                               │
│    Defines: SocialEngine, PERSONALITIES, DISGUISES                           │
│    Imports: random (library)                                                 │
│    Used by: NADIE (opcional para futuro)                                     │
│    Status: ⚠ HUÉRFANO                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DATOS (Carga desde archivos JSON/Python)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 data/beast_db_massive.py                                                  │
│    Purpose: Database de bestias                                              │
│    Defines: ROOT_CREATURES, FAMILY_PREFIXES, VARIANTS, ANATOMY              │
│    Imports: None (data only)                                                 │
│    Used by: systems/creature_gen.py                                          │
│    Status: ✓ DATA STORE                                                     │
│                                                                              │
│ 📄 data/items_db.py                                                          │
│    Purpose: Database de items                                                │
│    Defines: Item definitions                                                 │
│    Imports: None (data only)                                                 │
│    Used by: [potencial via game_engine]                                      │
│    Status: ✓ DATA STORE                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ GENERACIÓN PROCEDURAL                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 systems/resource_gen_v2.py                                                │
│    Purpose: Generador procedural de recursos/materiales                     │
│    Defines: ProceduralResourceGen, RESOURCES_DB, RARITY_WEIGHTS             │
│    Imports: json, random, os (library + file I/O)                           │
│    Generates: systems/Materiales.json                                        │
│    Used by: ui/game_engine.py                                                │
│    Status: ✓ GENERADOR DE RECURSOS                                          │
│    Note: Crea materiales dinámicamente para cada partida                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ SISTEMAS COMPUESTOS (Dependen de otros sistemas)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 systems/crafting.py                                                       │
│    Purpose: Sistemas de alquimia y forja                                     │
│    Defines: AlchemySystem (11 templates), ForgeSystem, Materials             │
│    Imports:                                                                  │
│       Library: random, json, os                                              │
│       Local: [carga dinámicamente] systems/Materiales.json                   │
│    Used by:                                                                  │
│       ├─ main.py (ForgeSystem)                                               │
│       ├─ systems/equipment.py (Materials, ForgeSystem)                       │
│       ├─ systems/companion.py (ForgeSystem)                                  │
│       ├─ ui/game_engine.py (AlchemySystem)                                   │
│       ├─ ui/popups.py (AlchemySystem)                                        │
│       ├─ verify_all.py (testing)                                             │
│       └─ verify_integration.py (testing)                                     │
│    Total Importadores: 7                                                    │
│    JSON Dependency: systems/Materiales.json (con fallback)                   │
│    Status: ✓ CRÍTICO - BIEN INTEGRADO                                       │
│    Note: Fallback a {"Maderas": [], ...} si falta JSON                       │
│                                                                              │
│ 📄 systems/equipment.py                                                      │
│    Purpose: Sistema de equipamiento de personajes                            │
│    Defines: Equipment, CharacterEquipment, create_starter_weapon()           │
│    Imports:                                                                  │
│       Library: None (solo estructura)                                        │
│       Local: systems.crafting (Materials, ForgeSystem)                       │
│    Used by:                                                                  │
│       ├─ main.py (CharacterEquipment, create_starter_weapon)                │
│       ├─ systems/companion.py (Equipment, CharacterEquipment)               │
│       ├─ verify_all.py (testing)                                             │
│       └─ verify_integration.py (testing)                                     │
│    Dependency Chain: equipment → crafting → Materiales.json                  │
│    Status: ✓ BIEN INTEGRADO                                                 │
│                                                                              │
│ 📄 systems/map_core.py                                                       │
│    Purpose: Sistema de mapa y gestión de ubicaciones                         │
│    Defines: MapManager                                                       │
│    Imports:                                                                  │
│       Library: json, os, random, math                                        │
│       Local: config (CHUNK_SIZE, VOID_TILE)                                  │
│              [carga dinámicamente] systems/Lugares.json                      │
│    Used by:                                                                  │
│       ├─ main.py (MapManager initialization)                                 │
│       └─ ui/popups.py (location interaction)                                 │
│    JSON Dependency: systems/Lugares.json (con fallback a 8 ubicaciones)     │
│    Status: ✓ CRÍTICO - BIEN INTEGRADO                                       │
│    Note: Fallback data implementado correctamente                            │
│                                                                              │
│ 📄 systems/creature_gen.py                                                   │
│    Purpose: Generador procedural de criaturas                                │
│    Defines: CreatureGenerator                                                │
│    Imports:                                                                  │
│       Library: random                                                        │
│       Local: data.beast_db_massive (databases)                               │
│    Used by:                                                                  │
│       ├─ systems/companion.py (CreatureGenerator)                            │
│       ├─ ui/game_engine.py (CreatureGenerator)                               │
│       └─ ui/popups.py (CreatureGenerator)                                    │
│    Status: ✓ BIEN INTEGRADO                                                 │
│                                                                              │
│ 📄 systems/companion.py                                                      │
│    Purpose: Sistema de compañeros/NPCs                                       │
│    Defines: Companion, CompanionParty, CompanionGenerator                    │
│    Imports:                                                                  │
│       Library: random                                                        │
│       Local: systems.equipment (CharacterEquipment, Equipment)               │
│              systems.creature_gen (CreatureGenerator)                        │
│              systems.crafting (ForgeSystem)                                  │
│    Used by:                                                                  │
│       ├─ verify_all.py (testing)                                             │
│       └─ verify_integration.py (testing)                                     │
│    Dependency Chain: companion → equipment,creature_gen,crafting             │
│    Status: ✓ BIEN INTEGRADO                                                 │
│                                                                              │
│ 📄 systems/slave_mgmt.py                                                     │
│    Purpose: Sistema de gestión de esclavos                                   │
│    Defines: SlaveManager, Slave                                              │
│    Imports: random (library)                                                 │
│    Used by: ui/game_engine.py, ui/popups.py                                  │
│    Status: ✓ INTEGRADO                                                      │
│                                                                              │
│ 📄 systems/sect_politics.py                                                  │
│    Purpose: Sistema de sectas y política interna                             │
│    Defines: Sect, SectPolitics                                               │
│    Imports: random (library)                                                 │
│    Used by: ui/game_engine.py, ui/popups.py                                  │
│    Status: ✓ INTEGRADO                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFAZ DE USUARIO (Renderizado y Control)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📄 ui/pygame_utils.py                                                        │
│    Purpose: Utilidades de pygame (botones, etc)                              │
│    Defines: Button, UI components                                            │
│    Imports:                                                                  │
│       Library: pygame                                                        │
│       Local: config (COLORS)                                                 │
│    Used by: ui/game_engine.py                                                │
│    Status: ✓ UTILIDAD UI                                                    │
│                                                                              │
│ 📄 ui/pygame_renderer.py                                                     │
│    Purpose: Renderizador de pygame                                           │
│    Defines: PygameRenderer                                                   │
│    Imports:                                                                  │
│       Library: pygame                                                        │
│       Local: config (COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, etc.)  │
│    Used by: ui/game_engine.py                                                │
│    Status: ✓ RENDERIZADOR CENTRAL                                           │
│                                                                              │
│ 📄 ui/map_render.py                                                          │
│    Purpose: Renderizador de mapa                                             │
│    Defines: MapRenderer                                                      │
│    Imports:                                                                  │
│       Library: pygame                                                        │
│       Local: config (COLORS, WINDOW_WIDTH, TILE_SIZE, CHUNK_SIZE)           │
│    Used by: [potencial via game_engine]                                      │
│    Status: ✓ RENDERIZADOR ESPECIALIZADO                                     │
│                                                                              │
│ 📄 ui/main_menu.py                                                           │
│    Purpose: Menú principal                                                   │
│    Defines: MainMenu class                                                   │
│    Imports:                                                                  │
│       Library: pygame, sys                                                   │
│       Local: config (WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, APP_TITLE)        │
│    Used by: main.py                                                          │
│    Status: ✓ INTERFAZ PRINCIPAL                                             │
│                                                                              │
│ 📄 ui/game_engine.py                                                         │
│    Purpose: Motor de juego principal (game loop)                             │
│    Defines: GameEngine class                                                 │
│    Imports:                                                                  │
│       Library: pygame, sys, random                                           │
│       Local: config (FPS, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS)              │
│              ui.pygame_utils (Button)                                        │
│              ui.pygame_renderer (PygameRenderer)                             │
│              systems.creature_gen (CreatureGenerator)                        │
│              systems.cultivation (CultivationManager)                        │
│              systems.combat (CombatEngine)                                   │
│              systems.resource_gen_v2 (ProceduralResourceGen)                │
│              systems.slave_mgmt (SlaveManager)                               │
│              systems.crafting (AlchemySystem)                                │
│              systems.sect_politics (Sect)                                    │
│    Used by: main.py                                                          │
│    Total Imports: 11 sistemas locales                                        │
│    Status: ✓ MOTOR CENTRAL - BIEN INTEGRADO                                 │
│                                                                              │
│ 📄 ui/popups.py                                                              │
│    Purpose: Ventanas emergentes y diálogos                                   │
│    Defines: BasePopup, SectWindow, etc.                                      │
│    Imports:                                                                  │
│       Library: tkinter, ttk                                                  │
│       Local: systems.sect_politics (Sect)                                    │
│              systems.crafting (AlchemySystem)                                │
│              systems.slave_mgmt (SlaveManager)                               │
│              systems.manual_system (ManualManager)                           │
│              systems.creature_gen (CreatureGenerator)                        │
│              systems.map_core (MapManager)                                   │
│    Note: Try-except para imports seguros                                     │
│    Status: ✓ UI SECUNDARIA - BIEN INTEGRADA                                 │
│    Note: No importado directamente por main.py (probable uso dinámico)       │
│                                                                              │
│ 📄 ui/panels.py [NOT USED IN MAIN]                                           │
│    Purpose: Paneles tkinter (legacy?)                                        │
│    Defines: StatusPanel, etc.                                                │
│    Imports:                                                                  │
│       Library: tkinter, ttk                                                  │
│       Local: NONE                                                            │
│    Note: Puede ser código legacy o en desarrollo                             │
│    Status: ⚠ HUÉRFANO (no integrado en flujo principal)                     │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
📊 MATRIZ DE DEPENDENCIAS CRUZADAS (Referencia Rápida)
═══════════════════════════════════════════════════════════════════════════════

                 config  crafting  equipment  combat  creature  game_eng
config            —         ✓         ✓        ✓        ✓        ✓
crafting          —         —         ✓        ✗        ✗        ✓
equipment         —         ↓         —        ✗        ✗        ✗
combat            —         ✗         ✗        —        ✗        ✓
creature_gen      —         ✗         ✗        ✗        —        ✓
game_engine       ↓         ↓         ↓        ↓        ↓        —

Leyenda:
  — = No aplica / Es el mismo archivo
  ↓ = Importa / Depende de
  ✓ = Lo importa otro
  ✗ = No tiene relación

═══════════════════════════════════════════════════════════════════════════════
🔍 ARCHIVOS JSON CRÍTICOS Y FALLBACKS
═══════════════════════════════════════════════════════════════════════════════

systems/Materiales.json
├─ Generado por: systems/resource_gen_v2.py
├─ Leído por: systems/crafting.py (línea 6-10)
├─ Fallback: ✓ SÍ - {"Maderas": [], "Minerales": [], "Plantas": []}
├─ Estructura: {"Maderas": [...], "Minerales": [...], "Plantas": [...]}
├─ Total items: ~39 (Común, Raro, Épico, Legendario)
└─ Status: ✓ CRÍTICO Y PROTEGIDO

systems/Lugares.json
├─ Cargado por: systems/map_core.py (línea 24-25)
├─ Fallback: ✓ SÍ - 8 ubicaciones por defecto
├─ Estructura: [{"Lugar": "...", "tipo": "...", "nivel": ..., ...}]
├─ Ubicaciones:
│   1. Pueblo Scarsha
│   2. Secta Nube Blanca
│   3. Secta Sangre del Maldito
│   4. Ruinas Antiguas
│   5. Montaña Celestial
│   6. Bosque Prohibido
│   7. Río del Olvido
│   8. Templo Abandonado
└─ Status: ✓ CRÍTICO Y PROTEGIDO

═══════════════════════════════════════════════════════════════════════════════
🎯 CONCLUSIÓN TÉCNICA
═══════════════════════════════════════════════════════════════════════════════

ESTRUCTURA: Jerárquica y clara
  Nivel 0: config.py (base de todo)
  Nivel 1: Sistemas atómicos (independientes)
  Nivel 2: Sistemas compuestos (dependen de nivel 1)
  Nivel 3: UI (orquesta todo)
  Nivel 4: main.py (entrada y Player class)

INTEGRIDAD: ✓ Verificada
  ✓ Sin circular dependencies
  ✓ Sin imports rotos
  ✓ Todos los JSONs tienen fallbacks
  ✓ Cambios recientes mantienen estructura

RECOMENDACIÓN: Sistema listo para operación. ✓

═══════════════════════════════════════════════════════════════════════════════
