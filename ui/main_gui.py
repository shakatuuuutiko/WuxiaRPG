import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

# Importar Paneles y Popups
from ui.panels import StatusPanel, InventoryPanel
from ui.popups import PopupManager
from ui.map_render import MapWidget

# Importar Sistemas
from systems.map_core import MapManager, SpatialDao
from systems.creature_gen import CreatureGenerator
from systems.cultivation import CultivationManager
from systems.combat import CombatEngine
from systems.resource_gen_v2 import ProceduralResourceGen
from systems.slave_mgmt import SlaveManager

class MainGUI(tk.Tk):
    def __init__(self, player, time_sys):
        super().__init__()
        self.title("WUXIA: ETERNIDAD INFINITA")
        self.geometry("1000x700") 
        self.configure(bg="#050505")
        
        self.player = player
        self.time = time_sys
        
        # Inicializar Sistemas Locales
        self.map_mgr = MapManager()
        self.spatial = SpatialDao(self.map_mgr)
        self.beast_gen = CreatureGenerator()
        self.cultivation = CultivationManager(self.player.stats)
        self.combat = CombatEngine()
        self.res_gen = ProceduralResourceGen()
        self.slave_mgr = SlaveManager(self.player) 
        
        self.current_enemy = None
        
        # FIX WASD: Bindeo robusto a mayúsculas y minúsculas
        self.bind('w', lambda event: self.move(0, -1)); self.bind('W', lambda event: self.move(0, -1))
        self.bind('s', lambda event: self.move(0, 1)); self.bind('S', lambda event: self.move(0, 1))
        self.bind('a', lambda event: self.move(-1, 0)); self.bind('A', lambda event: self.move(-1, 0))
        self.bind('d', lambda event: self.move(1, 0)); self.bind('D', lambda event: self.move(1, 0))
        
        self.focus_force() 

        self.setup_ui()
        self.refresh_contextual_buttons()
        self.update_map_display()
        self.update_all()
        
        self.log("--- INICIO DEL CAMINO ---", "info")
        self.log(f"Bienvenido, {player.name}.", "gain")

    def setup_ui(self):
        # --- LAYOUT PRINCIPAL ---
        col_left = tk.Frame(self, bg="#101010", width=250); col_left.pack(side="left", fill="y", padx=2) 
        col_mid = tk.Frame(self, bg="#000000"); col_mid.pack(side="left", fill="both", expand=True, padx=2)
        col_right = tk.Frame(self, bg="#101010", width=200); col_right.pack(side="right", fill="y", padx=2) 

        # IZQUIERDA
        self.panel_status = StatusPanel(col_left, self.player, self.time)
        self.panel_status.pack(fill="x", pady=10, padx=5)
        self.panel_inv = InventoryPanel(col_left, self.player)
        self.panel_inv.pack(fill="both", expand=True, pady=10, padx=5)

        # CENTRO
        self.txt_log = scrolledtext.ScrolledText(col_mid, height=10, bg="#111", fg="#0f0", font=("Consolas", 10))
        self.txt_log.pack(fill="x", padx=5, pady=5)

        self.f_actions = tk.Frame(col_mid, bg="#222", height=50)
        self.f_actions.pack(fill="x", pady=5, side="bottom")

        self.f_visual = tk.LabelFrame(col_mid, text="Entorno", bg="#000", fg="white")
        self.f_visual.pack(fill="both", expand=True, padx=5, pady=5) 
        self.map_widget = MapWidget(self.f_visual, width=480, height=480, cell_size=15)
        self.map_widget.pack(pady=5)
        self.lbl_coords = tk.Label(self.f_visual, text="Coords: 0, 0", bg="black", fg="#aaa")
        self.lbl_coords.pack()
        
        # DERECHA
        tk.Label(col_right, text="SISTEMAS", font=("Cinzel", 14), fg="#4fa4ff", bg="#101010").pack(pady=10)
        sys_btn_style = {"bg": "#222", "fg": "white", "pady": 5}
        
        tk.Button(col_right, text="🗺️ Mapa Global", command=self.open_world_map, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        tk.Button(col_right, text="🏛️ Secta", command=self.open_sect, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        tk.Button(col_right, text="⚒️ Crafting", command=self.open_craft, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        tk.Button(col_right, text="⛓️ Esclavos", command=self.open_slaves, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        tk.Button(col_right, text="📖 Manuales", command=self.open_manuals, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        tk.Button(col_right, text="🔪 Desmantelar", command=self.open_butchery, **sys_btn_style).pack(fill="x", padx=10, pady=5)
        
        self.f_enemy = tk.LabelFrame(col_right, text="OBJETIVO", bg="#101010", fg="red")
        self.f_enemy.pack(fill="x", padx=5, pady=20)
        self.lbl_enemy_status = tk.Label(self.f_enemy, text="Ninguno", fg="#777", bg="#101010")
        self.lbl_enemy_status.pack(pady=5)

    def refresh_contextual_buttons(self):
        for widget in self.f_actions.winfo_children(): widget.destroy()
        
        if self.current_enemy:
            # MODO COMBATE
            self.f_actions.config(bg="#400000")
            tk.Button(self.f_actions, text="⚔️ ATACAR", command=self.combat_attack, bg="#800000", fg="white", width=15).pack(side="left", padx=5, pady=10)
            tk.Button(self.f_actions, text="🏃 HUIR", command=self.action_flee, bg="#444", fg="white", width=10).pack(side="right", padx=5, pady=10)
            tk.Button(self.f_actions, text="⛓️ SOMETER", command=self.combat_enslave, bg="#440044", fg="white", width=15).pack(side="left", padx=5)
        else:
            # MODO EXPLORACIÓN
            self.f_actions.config(bg="#222")
            f_move = tk.Frame(self.f_actions, bg="#222")
            f_move.pack(side="left", padx=10)
            
            tk.Button(f_move, text="⬆", command=lambda: self.move(0, -1), width=3).grid(row=0, column=1)
            tk.Button(f_move, text="⬅", command=lambda: self.move(-1, 0), width=3).grid(row=1, column=0)
            tk.Button(f_move, text="⬇", command=lambda: self.move(0, 1), width=3).grid(row=1, column=1)
            tk.Button(f_move, text="➡", command=lambda: self.move(1, 0), width=3).grid(row=1, column=2)
            
            tk.Button(self.f_actions, text="👁️ Investigar Aquí", command=self.action_explore_spot, bg="#333", fg="white").pack(side="left", padx=10)
            tk.Button(self.f_actions, text="🧘 Meditar", command=self.action_meditate, bg="#333", fg="white").pack(side="left", padx=5)
            tk.Button(self.f_actions, text="⏳ Pasar Tiempo", command=self.action_wait, bg="#333", fg="white").pack(side="left", padx=5)

    def update_map_display(self):
        gx, gy = self.player.location
        cx, cy = gx // 32, gy // 32
        lx, ly = gx % 32, gy % 32
        
        chunk_data = self.map_mgr._load_chunk(cx, cy)
        biome = chunk_data.get("biome", "Desconocido")
        
        self.map_widget.draw_chunk(chunk_data, lx, ly)
        self.lbl_coords.config(text=f"Coords: {gx}, {gy} | Bioma: {biome}")

    def move(self, dx, dy):
        # FIX: Colisión revisada
        if self.current_enemy: return
            
        new_x = self.player.location[0] + dx
        new_y = self.player.location[1] + dy
        
        try:
            tile = self.map_mgr.get_tile_info(new_x, new_y)
            if tile in ["Volcán", "Océano", "ABISMO ESPACIAL"]:
                self.log(f"El camino está bloqueado por {tile}.", "alert")
                return
        except:
            pass

        self.player.location[0] = new_x
        self.player.location[1] = new_y
        self.log(f"Te moviste a ({new_x}, {new_y})", "info")
        
        self.update_map_display()
        
        if random.random() < 0.10: self.trigger_encounter()
        self.update_all()

    def action_explore_spot(self):
        self.time.pass_time(1)
        if random.random() < 0.4:
            self.trigger_encounter()
        else:
            # FIX: Acceso al nombre del diccionario del recurso
            target_rank = max(1, self.player.realm_idx + 1)
            resource_data = self.res_gen.generate(target_rank=target_rank)
            
            name = resource_data["name"]
            
            self.player.inventory[name] = self.player.inventory.get(name, 0) + 1
            self.log(f"Encuentras: {name} (Tier {resource_data['rank']})", "gain")
        self.update_all()
        
    def trigger_encounter(self):
        rank = self.player.realm_idx + 1
        beast = self.beast_gen.generate(target_rank=rank)
        self.current_enemy = beast
        self.log(f"¡{beast['name']} te bloquea el paso!", "combat")
        
        e_txt = f"{beast['name']}\n[{beast['rank']}]\n"
        e_txt += f"HP: {beast['stats']['hp']}/{beast['stats']['max_hp']}\n"
        e_txt += f"ATK: {beast['stats']['atk']} DEF: {beast['stats']['def']}"
        self.lbl_enemy_status.config(text=e_txt, fg="red")
        
        self.refresh_contextual_buttons()

    # --- ACCIONES DE COMBATE ---
    def combat_attack(self):
        self._execute_turn("Ataque Básico")

    def combat_enslave(self):
        """Intento de esclavitud que usa la instancia de SlaveManager"""
        from systems.slave_mgmt import SlaveManager
        mgr = SlaveManager(self.player)
        success, msg = mgr.attempt_capture(self.current_enemy, "Siervo")
        
        if success:
            self.log(f"🎉 CAPTURA EXITOSA: {msg}", "gain")
            self.current_enemy = None
            self.refresh_contextual_buttons()
        else:
            self.log(f"FALLO DE CAPTURA: {msg}", "alert")
            self._enemy_turn()
        self.update_all()

    def _execute_turn(self, atk_name, skill_mult=1.0):
        from systems.combat import CombatEngine
        
        # 1. Calcular contribución de esclavos (FIX DE INTEGRACIÓN)
        slave_contribution = 0
        slaves_guarding = [s for s in self.player.slaves if s.current_task == "Guardaespaldas"]
        
        if slaves_guarding:
            for slave in slaves_guarding:
                slave_contribution += max(1, int(slave.stats.get("atk", 0) / 3))
            self.log(f"Tus {len(slaves_guarding)} guardaespaldas añaden +{slave_contribution} daño.", "info")

        # 2. Tu Ataque
        skill_data = {"stats": {"dmg_mult": skill_mult}, "element": "Neutro"}
        player_stats_modified = self.player.stats.copy()
        player_stats_modified["atk"] += slave_contribution

        dmg, crit, eff = self.combat.calculate_damage(player_stats_modified, self.current_enemy["stats"], skill_data)
        
        self.current_enemy["stats"]["hp"] -= dmg
        msg = f"Usas {atk_name}: {dmg} daño."
        if crit: msg += " ¡CRÍTICO!"
        self.log(msg, "combat")

        # 3. Verificar Victoria (y Botín)
        if self.current_enemy["stats"]["hp"] <= 0:
            self.log(f"Derrotaste a {self.current_enemy['name']}.", "gain")
            corpse = self.current_enemy["loot"][0]
            self.player.inventory[corpse] = self.player.inventory.get(corpse, 0) + 1
            self.log(f"Obtienes: {corpse}", "loot")
            
            self.current_enemy = None
            self.lbl_enemy_status.config(text="Ninguno")
            self.refresh_contextual_buttons()
        else:
            self._enemy_turn()
        self.update_all()

    def _enemy_turn(self):
        if not self.current_enemy: return
        dmg = max(1, self.current_enemy["stats"]["atk"] - self.player.stats["def"])
        self.player.stats["hp"] -= dmg
        self.log(f"Recibes {dmg} daño.", "combat")
        
        # Check Rebelión del Esclavo
        if self.player.stats["hp"] <= 0:
            self.player.stats["hp"] = 0
            messagebox.showerror("MUERTE", "Tu cultivo se ha disipado.")
            self.destroy()

        e = self.current_enemy
        e_txt = f"{e['name']}\n[{e['rank']}]\nHP: {e['stats']['hp']}/{e['stats']['max_hp']}"
        self.lbl_enemy_status.config(text=e_txt)
        self.update_all()

    def action_flee(self):
        if not self.current_enemy: return
        if random.random() < 0.5:
            self.log("¡Escapaste!", "info")
            self.current_enemy = None
            self.refresh_contextual_buttons()
        else:
            self.log("Fallo al huir. El enemigo te golpea.", "alert")
            self._enemy_turn()
        self.update_all()

    def action_meditate(self):
        self.log("Sistema de Cultivo Activo.", "info")

    def action_wait(self):
        self.time.pass_time(1)
        self.log("Pasa un mes...", "info")
        self.update_all()

    def update_all(self):
        self.panel_status.update()
        self.panel_inv.update()

    def log(self, msg, tag="info"):
        self.txt_log.insert(tk.END, f"> {msg}\n", tag)
        self.txt_log.see(tk.END)

    # --- VENTANAS ---
    def open_world_map(self): PopupManager.open_world_map(self, self.player, self.map_mgr)
    def open_sect(self): PopupManager.open_sect_ui(self, self.player, None)
    def open_craft(self): PopupManager.open_crafting_ui(self, self.player)
    def open_slaves(self): PopupManager.open_slave_ui(self, self.player)
    def open_manuals(self): PopupManager.open_manual_ui(self, self.player)
    def open_butchery(self): PopupManager.open_butchery_ui(self, self.player)
    def open_soul(self): messagebox.showinfo("Alma", f"Raíz: {self.player.spirit_root.tier}")
    def combat_skills_menu(self): self.log("Sistema de skills en UI pendiente.")
    def combat_items_menu(self): self.log("Sistema de items en UI pendiente.")