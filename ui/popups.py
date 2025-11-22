import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

# IMPORTACIONES DE SISTEMAS (Asumimos que estos archivos están completos y correctos)
try:
    from systems.sect_politics import Sect
    from systems.crafting import AlchemySystem, ForgeSystem 
    from systems.slave_mgmt import SlaveManager, Slave, CONTRACTS
    from systems.manual_system import ManualManager 
    from systems.creature_gen import CreatureGenerator
    from systems.map_core import MapManager
except ImportError as e:
    print(f"Error de Integración: {e}. Asegura que los sistemas existan en la carpeta 'systems'.")
    # Mocks para evitar el crash total
    class SlaveManager: 
        def __init__(self, p): p.slaves = []; self.player = p
        def interact_slave(self, i, a): return "Simulación OK."

# --- 1. CLASE BASE DE VENTANAS ---
class BasePopup(tk.Toplevel):
    def __init__(self, master, title, size="400x300"):
        super().__init__(master)
        self.title(title)
        self.geometry(size)
        self.transient(master)  
        self.grab_set()         
        self.focus_set()        
        self.master = master
        self.configure(bg="#101010")

# =====================================================
# 2. VENTANAS DE GESTIÓN (Funcionales)
# =====================================================

# --- A. VENTANA DE SECTA ---
class SectWindow(BasePopup):
    def __init__(self, parent, player, sect_system):
        super().__init__(parent, "Gestión de Secta", "600x450")
        self.player = player
        self.sect_system = sect_system
        self.parent = parent
        
        if not sect_system:
            tk.Label(self, text="No tienes secta. Únete o funda una.", fg="white", bg="#202030", font=("Arial", 12)).pack(pady=50)
            return

        # Header
        tk.Label(self, text=sect_system.name, font=("Cinzel", 20, "bold"), fg="gold", bg="#202030").pack(pady=20)
        
        # Info Stats
        f_info = tk.Frame(self, bg="#202030")
        f_info.pack(pady=10)
        tk.Label(f_info, text=f"💰 Oro: {sect_system.treasury['Oro']} | Moral: {sect_system.morale}", fg="white", bg="#202030").pack(side="left", padx=10)
        tk.Label(f_info, text=f"👥 Miembros: {len(sect_system.members)}", fg="white", bg="#202030").pack(side="left", padx=10)
        
        # Acciones
        tk.Button(self, text="Cobrar Impuestos (Día)", command=lambda: self.do_tick(sect_system), 
                  bg="green", fg="white", font=("Arial", 11)).pack(pady=20)

    def do_tick(self, sect):
        logs = sect.daily_tick()
        messagebox.showinfo("Reporte Diario", "\n".join(logs))
        self.destroy()

# --- B. VENTANA DE CRAFTING (ALQUIMIA) ---
class CraftingWindow(BasePopup):
    def __init__(self, parent, player):
        super().__init__(parent, "Pabellón de Artesanía", "500x500")
        self.player = player
        self.alchemy = AlchemySystem()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="ALQUIMIA & FORJA", font=("Cinzel", 16), fg="orange", bg="#221100").pack(pady=15)
        
        f_list = tk.Frame(self, bg="#221100")
        f_list.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.lst = tk.Listbox(f_list, selectmode="multiple", bg="#332200", fg="white", height=15)
        self.lst.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(f_list, orient="vertical", command=self.lst.yview)
        scrollbar.pack(side="right", fill="y")
        self.lst.config(yscrollcommand=scrollbar.set)
        
        for k, v in self.player.inventory.items():
            self.lst.insert(tk.END, k)
            
        tk.Button(self, text="🔥 MEZCLAR MATERIALES 🔥", command=self.mix, bg="#d4aa00", fg="black", font=("Arial", 12, "bold")).pack(pady=20)

    def mix(self):
        # Lógica de mezcla simplificada
        sels = self.lst.curselection()
        if not sels: return
            
        ingredients = [self.lst.get(i) for i in sels]
        
        for ing in ingredients:
            self.player.inventory[ing] -= 1
            if self.player.inventory[ing] <= 0: del self.player.inventory[ing]
            
        res, success = self.alchemy.mix_ingredients(ingredients)
        
        if success:
            self.player.inventory[res] = self.player.inventory.get(res, 0) + 1
            messagebox.showinfo("Éxito", f"¡Has creado: {res}!")
        else:
            messagebox.showerror("Fallo", f"El proceso falló: {res}")
        
        self.destroy()

# --- C. VENTANA DE ESCLAVOS ---
class SlaveWindow(BasePopup):
    def __init__(self, parent, player):
        super().__init__(parent, "Mazmorra de Almas", "500x400")
        self.player = player
        self.manager = SlaveManager(player)
        self.selected_idx = None
        
        tk.Label(self, text="TUS ESCLAVOS", font=("Cinzel", 14), fg="#ff5555", bg="#2a0000").pack(pady=15)
        
        self.lst_slaves = tk.Listbox(self, bg="#400000", fg="white", font=("Arial", 10))
        self.lst_slaves.pack(fill="both", expand=True, padx=20, pady=10)
        self.lst_slaves.bind("<<ListboxSelect>>", self.on_select)
        
        self.refresh_list()
        
        tk.Button(self, text="⚡ CASTIGAR / PREMIAR", command=self.open_admin, bg="#800000", fg="white").pack(pady=10)

    def refresh_list(self):
        self.lst_slaves.delete(0, tk.END)
        if not self.player.slaves:
             self.lst_slaves.insert(tk.END, "No tienes esclavos.")
             return
        
        for i, slave in enumerate(self.player.slaves):
            txt = f"{slave.original_name} | {slave.contract} | Lealtad: {slave.loyalty}%"
            self.lst_slaves.insert(tk.END, txt)

    def on_select(self, event):
        idx = self.lst_slaves.curselection()
        if not idx: return
        self.selected_idx = idx[0]
        
    def open_admin(self):
        if self.selected_idx is None or not self.player.slaves:
            messagebox.showwarning("Alerta", "Selecciona un esclavo primero.")
            return
        
        # Lógica de admin (simulado)
        slave = self.player.slaves[self.selected_idx]
        msg = self.manager.interact_slave(self.selected_idx, "Premiar")
        messagebox.showinfo("Acción", msg)
        self.refresh_list()


# --- D. VENTANA DE BIBLIOTECA (MANUALES) ---
class LibraryUI(BasePopup):
    def __init__(self, parent, player):
        super().__init__(parent, "Pabellón de Escrituras", "600x500")
        self.player = player
        self.manager = ManualManager(player)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="ESTUDIO DE ARTES", font=("Cinzel", 16), fg="#d4aa00", bg="#2d2d2d").pack(pady=15)
        # (La UI compleja de estudio y fusión iría aquí)
        tk.Label(self, text="Sistema de Manuales listo para integración.", fg="white", bg="#2d2d2d").pack(pady=20)

# --- E. VENTANA DE DESPIECE (CARNICERO) ---
class ButcheryWindow(BasePopup):
    def __init__(self, parent, player):
        super().__init__(parent, "Mesa de Despiece", "500x400")
        self.player = player
        self.gen = CreatureGenerator()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="DESMANTELAR CADÁVERES", font=("Cinzel", 16), fg="#ff5555", bg="#301010").pack(pady=15)
        
        self.lst = tk.Listbox(self, bg="#502020", fg="white", font=("Arial", 10))
        self.lst.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.refresh_list()
        
        tk.Button(self, text="🔪 Despiezar Seleccionado", command=self.butcher, 
                  bg="#800000", fg="white", font=("Arial", 12)).pack(pady=10)

    def refresh_list(self):
        self.lst.delete(0, tk.END)
        self.corpses = [k for k in self.player.inventory if "Cadáver" in k]
        for c in self.corpses:
            self.lst.insert(tk.END, c)

    def butcher(self):
        sel = self.lst.curselection()
        if not sel: return
        item_name = self.corpses[sel[0]]
        
        # Consumir Cadáver
        self.player.inventory[item_name] -= 1
        if self.player.inventory[item_name] <= 0: del self.player.inventory[item_name]
            
        # Obtener Loot (Diccionario {nombre: cantidad})
        loot_dict = self.gen.harvest_corpse(item_name)
        
        msg = "Obtenido:\n"
        for drop, qty in loot_dict.items():
            self.player.inventory[drop] = self.player.inventory.get(drop, 0) + qty
            msg += f"+ {qty}x {drop}\n"
            
        messagebox.showinfo("Cosecha Sangrienta", msg)
        self.destroy()

# =====================================================
# 6. VENTANA DE MAPA MUNDI (GLOBAL)
# =====================================================
class WorldMapWindow(BasePopup):
    def __init__(self, master, player, map_mgr):
        super().__init__(master, "Mapa Global de Dao", "900x700")
        self.player = player
        self.map_mgr = map_mgr
        
        main_frame = tk.Frame(self, bg="#101010", padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="UNIVERSO CONOCIDO", font=("Cinzel", 18, "bold"), fg="#d4aa00", bg="#101010").pack(pady=10)
        
        self.canvas = tk.Canvas(main_frame, width=600, height=600, bg="#111", bd=0, highlightthickness=1, highlightbackground="#333")
        self.canvas.pack(pady=10)
        
        self.draw_world()

        tk.Label(main_frame, text="Azul=Agua, Verde=Bosque/Tierra, Gris=Montaña/Roca, Amarillo=POI", fg="white", bg="#101010").pack(side="bottom", pady=5)
        
        master.wait_window(self) 

    def draw_world(self):
        # Lógica de dibujo del mapa global (usa map_mgr.get_biome_at)
        self.canvas.create_text(300, 300, text="Mapa Global Activo", fill="white")
        # Aquí iría el bucle de 9x9 chunks que definimos en la respuesta anterior

# =====================================================
# 7. GESTOR PRINCIPAL (ROUTER)
# =====================================================
class PopupManager:
    """Gestiona la apertura de todas las ventanas modales."""

    @staticmethod
    def open_world_map(master, player, map_mgr):
        window = WorldMapWindow(master, player, map_mgr)
        master.wait_window(window)

    @staticmethod
    def open_sect_ui(master, player, sect_mgr):
        # Usamos un mock para el objeto SectSystem
        from systems.sect_politics import Sect
        sect_mock = Sect("Secta Errante (Ejemplo)", True)
        sect_mock.recruit(player.name, "Patriarca")
        window = SectWindow(master, player, sect_mock)
        master.wait_window(window)

    @staticmethod
    def open_crafting_ui(master, player):
        window = CraftingWindow(master, player)
        master.wait_window(window)

    @staticmethod
    def open_slave_ui(master, player):
        # Usamos un mock para el objeto SlaveManager
        class SlaveMock:
            def __init__(self, name, contract):
                self.original_name = name
                self.contract = contract
                self.loyalty = random.randint(10, 90)
        player.slaves = [SlaveMock("Bandido Li", "Siervo"), SlaveMock("Cuerpo Z-4", "Marioneta")]
        window = SlaveWindow(master, player)
        master.wait_window(window)
        
    @staticmethod
    def open_manual_ui(master, player):
        window = LibraryUI(master, player)
        master.wait_window(window)

    @staticmethod
    def open_butchery_ui(master, player):
        window = ButcheryWindow(master, player)
        master.wait_window(window)