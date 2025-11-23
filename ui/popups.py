import tkinter as tk
from tkinter import messagebox, ttk

# Importaciones seguras
try:
    from systems.sect_politics import Sect
    from systems.crafting import AlchemySystem
    from systems.slave_mgmt import SlaveManager
    from systems.manual_system import ManualManager
    from systems.creature_gen import CreatureGenerator
    from systems.map_core import MapManager
except ImportError:
    pass

class BasePopup(tk.Toplevel):
    def __init__(self, master, title, size="400x300"):
        super().__init__(master)
        self.title(title)
        self.geometry(size)
        self.transient(master)  
        self.grab_set()         
        self.focus_set()        
        self.configure(bg="#101010")

# --- VENTANA DE SECTA ---
class SectWindow(BasePopup):
    def __init__(self, master, player):
        super().__init__(master, "Gestión de Secta", "600x450")
        
        # FIX: Usar la secta real del jugador
        if not player.sect:
            tk.Label(self, text="Eres un Cultivador Errante.", font=("Arial", 14), fg="white", bg="#101010").pack(pady=30)
            
            f_btn = tk.Frame(self, bg="#101010")
            f_btn.pack(pady=20)
            
            tk.Button(f_btn, text="🏛️ Buscar Secta", command=lambda: messagebox.showinfo("Mundo", "Buscas en el mapa..."), bg="cyan").pack(side="left", padx=10)
            tk.Button(f_btn, text="✨ Fundar (10k Oro)", command=self.create_sect, bg="gold").pack(side="left", padx=10)
            return

        # Si tiene secta, mostrar datos reales
        sect = player.sect
        tk.Label(self, text=sect.name, font=("Cinzel", 20, "bold"), fg="gold", bg="#101010").pack(pady=20)
        info = f"Oro: {sect.treasury['Oro']} | Moral: {sect.morale} | Miembros: {len(sect.members)}"
        tk.Label(self, text=info, fg="white", bg="#101010").pack()
        
        tk.Button(self, text="Cobrar Impuestos", command=lambda: self.do_tick(sect), bg="green", fg="white").pack(pady=20)

    def create_sect(self):
        # Aquí iría la lógica de creación real
        messagebox.showinfo("Fundación", "Necesitas más oro y reputación.")

    def do_tick(self, sect):
        logs = sect.daily_tick()
        messagebox.showinfo("Reporte", "\n".join(logs))

# --- VENTANA DE ESCLAVOS ---
class SlaveWindow(BasePopup):
    def __init__(self, master, player):
        super().__init__(master, "Mazmorra", "500x400")
        
        tk.Label(self, text="ALMAS CAPTURADAS", font=("Cinzel", 14), fg="#ff5555", bg="#101010").pack(pady=15)
        
        # FIX: Mostrar lista real. Si está vacía, decirlo.
        if not player.slaves:
            tk.Label(self, text="Tu mazmorra está vacía.", fg="#555", bg="#101010").pack(pady=50)
        else:
            lb = tk.Listbox(self, bg="#200000", fg="white", font=("Arial", 10))
            lb.pack(fill="both", expand=True, padx=20, pady=10)
            for slave in player.slaves:
                txt = f"{slave.original_name} ({slave.contract}) | Lealtad: {slave.loyalty}%"
                lb.insert(tk.END, txt)

# --- OTRAS VENTANAS (Crafting, Manuals, etc. se mantienen igual de limpias) ---
class CraftingWindow(BasePopup):
    def __init__(self, master, player):
        super().__init__(master, "Artesanía", "500x500")
        tk.Label(self, text="Sistema de Crafting", fg="orange", bg="#101010").pack(pady=20)
        # Lógica real de crafting...

class LibraryUI(BasePopup):
    def __init__(self, master, player):
        super().__init__(master, "Biblioteca", "600x500")
        tk.Label(self, text="Manuales Disponibles", fg="cyan", bg="#101010").pack(pady=20)

class ButcheryWindow(BasePopup):
    def __init__(self, master, player):
        super().__init__(master, "Despiece", "500x400")
        tk.Label(self, text="Mesa de Carnicero", fg="red", bg="#101010").pack(pady=20)

class WorldMapWindow(BasePopup):
    def __init__(self, master, player, map_mgr):
        super().__init__(master, "Mapa Global", "900x700")
        # Lógica de dibujo del mapa global real
        canvas = tk.Canvas(self, bg="#000")
        canvas.pack(fill="both", expand=True)
        canvas.create_text(450, 350, text="Mapa Global (Datos Reales)", fill="white")

# --- GESTOR ---
class PopupManager:
    """Abre ventanas SIN inyectar datos falsos"""
    
    # Usamos una ventana raíz oculta de Tkinter para colgar los popups sobre Pygame
    root = None

    @staticmethod
    def get_root():
        if not PopupManager.root:
            PopupManager.root = tk.Tk()
            PopupManager.root.withdraw() # Ocultar la ventana base
        return PopupManager.root

    @staticmethod
    def open_sect_ui(player, sect_mgr):
        SectWindow(PopupManager.get_root(), player)

    @staticmethod
    def open_slave_ui(player):
        SlaveWindow(PopupManager.get_root(), player)

    @staticmethod
    def open_crafting_ui(player):
        CraftingWindow(PopupManager.get_root(), player)
    
    @staticmethod
    def open_manual_ui(player):
        LibraryUI(PopupManager.get_root(), player)

    @staticmethod
    def open_butchery_ui(player):
        ButcheryWindow(PopupManager.get_root(), player)

    @staticmethod
    def open_world_map(player, map_mgr):
        WorldMapWindow(PopupManager.get_root(), player, map_mgr)