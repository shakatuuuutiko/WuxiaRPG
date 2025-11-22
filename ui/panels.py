import tkinter as tk
from tkinter import ttk

class StatusPanel(tk.Frame):
    def __init__(self, parent, player, time_sys):
        super().__init__(parent, bg="#101010")
        self.player = player
        self.time = time_sys
        
        # Estilos
        self.lbl_style = {"bg": "#101010", "fg": "#cccccc", "font": ("Arial", 10)}
        self.val_style = {"bg": "#101010", "fg": "#ffffff", "font": ("Arial", 9, "bold")} # Estilo brillante para números
        self.header_style = {"bg": "#101010", "fg": "#d4aa00", "font": ("Cinzel", 12, "bold")}
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="-- ESTADO --", **self.header_style).pack(pady=5)
        self.lbl_info = tk.Label(self, text="", justify="left", **self.lbl_style)
        self.lbl_info.pack(padx=5, anchor="w")
        
        self.create_bar("HP", "red")
        self.create_bar("Qi", "#4fa4ff")

    def create_bar(self, label, color):
        f = tk.Frame(self, bg="#101010")
        f.pack(fill="x", padx=5, pady=2)
        
        # Etiqueta Nombre (HP)
        tk.Label(f, text=label, **self.lbl_style, width=4).pack(side="left")
        
        # Barra
        pb = ttk.Progressbar(f, length=100) # Un poco más corta para dejar espacio al texto
        pb.pack(side="left", fill="x", expand=True, padx=5)
        
        # Etiqueta Valor (100/100) - Guardamos referencia para actualizarla
        lbl_val = tk.Label(f, text="0/0", **self.val_style)
        lbl_val.pack(side="right")
        
        setattr(self, f"pb_{label.lower()}", pb)
        setattr(self, f"val_{label.lower()}", lbl_val)

    def update(self):
        p = self.player
        
        # Texto Principal
        txt = f"{p.name}\n[{p.title}]\nEdad: {p.age}/{p.max_lifespan}\nReino: {p.realm_name} (G{p.realm_idx})"
        self.lbl_info.config(text=txt)
        
        # Actualizar Barras y Números
        self._update_single_bar("hp", p.stats["hp"], p.stats["max_hp"])
        self._update_single_bar("qi", p.stats["qi"], p.stats["max_qi"])

    def _update_single_bar(self, name, current, maximum):
        pb = getattr(self, f"pb_{name}")
        lbl = getattr(self, f"val_{name}")
        
        pb["maximum"] = maximum
        pb["value"] = current
        # Aquí forzamos que muestre el número
        lbl.config(text=f"{int(current)}/{int(maximum)}")

class InventoryPanel(tk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent, bg="#101010")
        self.player = player
        
        tk.Label(self, text="-- BOLSA --", bg="#101010", fg="#d4aa00", font=("Cinzel", 12, "bold")).pack(pady=5)
        
        self.tree = ttk.Treeview(self, columns=("Item", "Cant"), show="headings", height=15)
        self.tree.heading("Item", text="Objeto")
        self.tree.heading("Cant", text="#")
        self.tree.column("Item", width=180)
        self.tree.column("Cant", width=40)
        self.tree.pack(fill="both", expand=True, padx=5)

    def update(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item, qty in self.player.inventory.items():
            self.tree.insert("", "end", values=(item, qty))