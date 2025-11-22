# --- SCRIPT MAESTRO: WUXIA RPG ---
# Versión: 3.7 (FIX: Sincronización de Clases Finales)

import tkinter as tk
from tkinter import messagebox
import sys
import random

# =====================================================
# 1. VERIFICACIÓN DE INTEGRIDAD Y CARGA
# =====================================================
try:
    # Sistemas (Ahora deben apuntar a la lógica de Pygame/Tkinter unificada)
    from systems.cultivation import SpiritRoot
    from systems.bloodline import Bloodline
    from systems.time_system import TimeSystem, AgeManager
    from systems.origin_generator import OriginGenerator
    
    # FIX: Importamos el motor de juego con el nombre que usamos para el Pygame/Tkinter Engine
    from ui.main_gui import MainGUI as GameEngine # Usamos MainGUI como alias para el motor
    
except ImportError as e:
    print("FATAL ERROR: No se pudo importar un módulo necesario.")
    print(f"Asegúrate de que las carpetas 'systems', 'data' y 'ui' tengan todos los archivos. Error: {e}")
    sys.exit()

# =====================================================
# 2. CLASE JUGADOR (NÚCLEO DEL DAO)
# =====================================================
class Player:
    def __init__(self):
        self.origin_gen = OriginGenerator()
        self.origin_data = self.origin_gen.generate()
        self.name = self._generate_wuxia_name()
        self.title = self.origin_data["title"]
        
        # Stats Base (G0)
        self.stats = {
            "hp": 150, "max_hp": 150,
            "qi": 0, "max_qi": 100,
            "stamina": 100, "max_stamina": 100,
            "atk": 20, "def": 10,
            "comprension": 10, "suerte": 0,
            "dao_espacial": 0, "dao_devorar": 0
        }
        
        # Aplicar Modificadores
        mods = self.origin_data.get("stats_mod", {})
        for stat, value in mods.items():
            if stat in self.stats:
                self.stats[stat] += value
                if stat in ["hp", "stamina"]:
                    self.stats[f"max_{stat}"] += value
            elif stat == "qi":
                self.stats["qi"] = value

        if self.stats["max_hp"] < 50: self.stats["max_hp"] = 50
        self.stats["hp"] = self.stats["max_hp"]

        self.realm_idx = 0
        self.realm_name = "Mortal"
        
        self.spirit_root = SpiritRoot()
        self.bloodline = Bloodline()
        self.age_sys = AgeManager(self)
        
        # Inventario Inicial
        self.inventory = {"Oro": self.origin_data.get("gold", 0)}
        origin_inv = self.origin_data.get("inventory", {})
        for item, qty in origin_inv.items():
            self.inventory[item] = self.inventory.get(item, 0) + qty
            
        self.inventory["Píldora Curativa"] = self.inventory.get("Píldora Curativa", 0) + 3
        self.inventory["Píldora de Fundación"] = self.inventory.get("Píldora de Fundación", 0) + 1
            
        self.slaves = []
        self.skills = {}
        start_range = 1000
        start_x = random.randint(-start_range, start_range)
        start_y = random.randint(-start_range, start_range)
        self.location = [start_x, start_y] 

    def _generate_wuxia_name(self):
        surnames = ["Li", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou", "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Lin", "Luo", "Jiang", "Fan", "Su", "Han", "Tang", "Feng", "Jin", "Wei", "Ye", "Bai", "Long", "Xie", "Mo"]
        given_names = ["Wei", "Jie", "Hao", "Yi", "Fan", "Lei", "Xin", "Ying", "Xiu", "Mei", "Lan", "Feng", "Long", "Hu", "Gui", "Chen", "Yun", "Tian", "Ming", "Hua", "Shan", "Ren", "Kai", "Jian", "Ping", "An", "Bo", "Cheng", "Dong", "Gang", "Zian", "Yan"]
        return f"{random.choice(surnames)} {random.choice(given_names)}"

    @property
    def age(self): return self.age_sys.current_age
    @property
    def max_lifespan(self): return self.age_sys.max_lifespan

# =====================================================
# 3. MÉTODOS DE PARCHE (Fixes de Lógica)
# =====================================================

def patch_action_meditate(self):
    """ FIX: Evita desbordamiento de Qi y controla la ruptura. """
    if self.current_enemy: return
    current_realm_idx = self.player.realm_idx
    realm_info = self.cultivation.get_realm_info(current_realm_idx)
    real_max_qi = realm_info["max_qi"]
    self.player.stats["max_qi"] = real_max_qi

    if self.player.stats["qi"] >= real_max_qi:
        self.player.stats["qi"] = real_max_qi
        self.log(f"Qi Lleno ({int(real_max_qi)}).", "alert")
        
        req_item = "Píldora de Fundación"
        if current_realm_idx >= 1:
            if self.player.inventory.get(req_item, 0) > 0:
                if messagebox.askyesno("Cuello de Botella", f"¿Usar '{req_item}' para romper el reino?"):
                    self.player.inventory[req_item] -= 1
                    self._do_breakthrough()
            else:
                self.log(f"Necesitas {req_item} para avanzar.", "info")
        else:
            if messagebox.askyesno("Ruptura", "Tu cuerpo está listo para formar el primer Mar de Qi.\n¿Avanzar?"):
                self._do_breakthrough()
        self.update_all()
        return

    gain = int(20 * self.player.spirit_root.cultivation_mult)
    space_left = real_max_qi - self.player.stats["qi"]
    actual_gain = min(gain, space_left)
    
    self.player.stats["qi"] += actual_gain
    self.log(f"Meditas. +{actual_gain} Qi.", "gain")
    self.update_all()

def patch_do_breakthrough(self):
    """ FIX: Actualiza el límite de max_qi después de romper de reino. """
    self.player.realm_idx += 1
    new_info = self.cultivation.get_realm_info(self.player.realm_idx)
    self.player.stats["max_qi"] = new_info["max_qi"]
    self.player.stats["qi"] = 0
    self.player.realm_name = new_info["name"]
    self.player.stats["max_hp"] += 100
    self.player.stats["hp"] = self.player.stats["max_hp"]
    self.player.stats["atk"] += 15
    self.player.stats["def"] += 5
    self.log(f"¡RUPTURA EXITOSA! Has alcanzado: {new_info['name']}", "gain")
    self.update_all()

def patch_move(self, dx, dy):
    """ FIX: Permite caminar sobre terreno y soluciona WASD/Botones."""
    if self.current_enemy: return
    new_x = self.player.location[0] + dx
    new_y = self.player.location[1] + dy
    
    try:
        map_mgr = MapManager() 
        tile = map_mgr.get_tile_info(new_x, new_y)
        if tile in ["ABISMO ESPACIAL", "Volcán", "Océano"]:
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

# =====================================================
# 4. MENÚ DE INICIO (LAUNCHER)
# =====================================================
class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WUXIA RPG - LAUNCHER")
        self.geometry("600x450")
        self.configure(bg="#050505")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="LEYENDAS DE WUXIA", font=("Times New Roman", 28, "bold"), fg="#d4aa00", bg="#050505").pack(pady=60)
        btn_style = {"font": ("Arial", 12), "width": 25, "pady": 8, "bg": "#222", "fg": "white", "bd": 1, "relief": "raised", "cursor": "hand2"}
        tk.Button(self, text="✨ NUEVA REENCARNACIÓN", command=self.start_new_game, **btn_style).pack(pady=10)
        tk.Button(self, text="📂 CONTINUAR CAMINO", command=self.load_game, **btn_style).pack(pady=10)
        tk.Button(self, text="❌ CERRAR", command=self.quit, **btn_style).pack(pady=10)
        tk.Label(self, text="Sistema v3.7 - Final Stable", fg="#444", bg="#050505").pack(side="bottom", pady=10)

    def start_new_game(self):
        try:
            new_player = Player()
            game_time = TimeSystem()
            self.destroy()
            
            # FIX: Importamos MainGUI y aplicamos los parches de lógica
            from ui.main_gui import MainGUI
            MainGUI.action_meditate = patch_action_meditate
            MainGUI._do_breakthrough = patch_do_breakthrough
            MainGUI.move = patch_move
            
            app = MainGUI(new_player, game_time)
            app.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Error al iniciar el juego:\n{e}")
            print(f"ERROR: {e}")

    def load_game(self):
        messagebox.showinfo("Sistema", "Guardado persistente no disponible.\nIniciando nueva partida.")
        self.start_new_game()

# =====================================================
# 5. PUNTO DE ENTRADA
# =====================================================
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()