import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
from abc import ABC, abstractmethod
from exportar import exportar_datos
from PIL import Image, ImageTk
import os
import sys

class GestorBase(ABC):
    """Clase abstracta base para gestores de datos"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def crear_interfaz(self):
        pass

    @abstractmethod
    def cargar_datos(self):
        """Método para cargar datos"""
        pass

    def exportar_datos(self):
        """Método para exportar datos"""
        pass
    def rutas(self, ruta):
        """Método para obtener la ruta de los iconos"""
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

class GestorProductos(tk.Toplevel, GestorBase):
    """Clase que gestiona la tabla de productos"""

    def __init__(self):
        super().__init__()
        self.title("Gestión de Productos")
        self.geometry("900x550")
        self.config(bg="#85c1e9")
        self.db_name = "database.db"
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        # Frame para mostrar productos
        frame_lista = tk.LabelFrame(self, text="Lista de Productos", font="sans 14 bold", bg="#85c1e9")
        frame_lista.place(x=20, y=20, width=860, height=450)

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "No. Serie", "Producto", "Precio Costo", "Precio Venta", "Stock", "Estado"), show="headings")
        self.tree.pack(expand=True, fill="both")

        self.tree.heading("ID", text="ID")
        self.tree.heading("No. Serie", text="No. Serie")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Precio Costo", text="Precio Costo")
        self.tree.heading("Precio Venta", text="Precio Venta")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=90, anchor="center")
        self.tree.column("No. Serie", width=80, anchor="center")
        self.tree.column("Producto", width=190, anchor="center")
        self.tree.column("Precio Costo", width=90, anchor="center")
        self.tree.column("Precio Venta", width=90, anchor="center")
        self.tree.column("Stock", width=90, anchor="center")
        self.tree.column("Estado", width=90, anchor="center")

        # Botón para exportar datos
        #Icono de exportar
        ruta = self.rutas(r"Iconos/excel.png")
        self.icono_exportar = Image.open(ruta)
        self.icono_exportar = self.icono_exportar.resize((30, 30))
        self.icono_exportar = ImageTk.PhotoImage(self.icono_exportar)
        btn_exportar = tk.Button(self, text="Exportar a Excel", command=self.exportar_datos, font="sans 12 bold")
        btn_exportar.config(image=self.icono_exportar, compound=tk.LEFT, padx=5)
        btn_exportar.image = self.icono_exportar
        btn_exportar.place(x=20, y=480, width=200, height=40)

    def cargar_datos(self):
        """Carga los datos de la tabla Inventario"""
        try:
            self.tree.delete(*self.tree.get_children())
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT id, serie, producto, precio_cos, precio_ven, stock, estado FROM Inventario")
            productos = cursor.fetchall()
            for producto in productos:
                self.tree.insert("", "end", values=producto)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def exportar_datos(self):
        """Exporta los datos de productos a un archivo Excel"""
        exportar_datos(self.db_name, "Inventario")

class GestorServicios(tk.Toplevel, GestorBase):
    """Clase que gestiona la tabla de servicios realizados"""

    def __init__(self):
        super().__init__()
        self.title("Gestión de Servicios Realizados")
        self.geometry("900x550")
        self.config(bg="#85c1e9")
        self.db_name = "database.db"
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        # Frame para mostrar servicios realizados
        frame_lista = tk.LabelFrame(self, text="Lista de Servicios Realizados", font="sans 14 bold", bg="#85c1e9")
        frame_lista.place(x=20, y=20, width=860, height=450)

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Cliente", "Nombre Equipo", "Servicio", "Precio", "Fecha Entrega", "Estado"), show="headings")
        self.tree.pack(expand=True, fill="both")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Nombre Equipo", text="Nombre Equipo")
        self.tree.heading("Servicio", text="Servicio")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Fecha Entrega", text="Fecha Entrega")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Cliente", width=150, anchor="center")
        self.tree.column("Nombre Equipo", width=150, anchor="center")
        self.tree.column("Servicio", width=150, anchor="center")
        self.tree.column("Precio", width=100, anchor="center")
        self.tree.column("Fecha Entrega", width=150, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        # Botón para exportar datos
        #Icono de exportar
        ruta = self.rutas(r"Iconos/excel.png")
        self.icono_exportar = Image.open(ruta)
        self.icono_exportar = self.icono_exportar.resize((30, 30))
        self.icono_exportar = ImageTk.PhotoImage(self.icono_exportar)
        btn_exportar = tk.Button(self, text="Exportar a Excel", command=self.exportar_datos, font="sans 12 bold")
        btn_exportar.config(image=self.icono_exportar, compound=tk.LEFT, padx=5)
        btn_exportar.image = self.icono_exportar
        btn_exportar.place(x=20, y=480, width=200, height=40)

    def cargar_datos(self):
        """Carga los datos de la tabla Servicios_realizados"""
        try:
            self.tree.delete(*self.tree.get_children())
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT s.id, c.nombre, s.Nombre_equipo, s.Servicio, s.Precio, s.Fecha_de_recibo, s.Estado FROM Servicios_realizados s LEFT JOIN Clientes c ON s.cliente_id = c.id")
            servicios = cursor.fetchall()
            for servicio in servicios:
                self.tree.insert("", "end", values=servicio)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def exportar_datos(self):
        """Exporta los datos de servicios a un archivo Excel"""
        exportar_datos(self.db_name, "Servicios_realizados")