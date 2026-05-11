from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from inventario import Inventario
from servicios_realizados import Servicios_realizados
from cliente import Clientes
from proveedor import Proveedor
from ventas_pro import Ventas_productos
from gestionar import GestorProductos
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames= {}
        self.buttons = []
        for i in (Inventario, Servicios_realizados, Clientes, Proveedor, Ventas_productos):
            frame= i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg= "#1f2f98", highlightbackground= "gray", highlightthickness=1)
            frame.place(x=0, y=40, widt= 1100, height= 610)
        self.show_frames(Inventario)
    
    def rutas(self, ruta):
        try:
            rutabase= sys._MEIPASS

        except Exception:
            rutabase= os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def show_frames(self, container):
        frame= self.frames[container]
        frame.tkraise()

    def inventario(self):
        self.show_frames(Inventario)

    def servicios_realizados(self):
        self.show_frames(Servicios_realizados)

    def cliente(self):
        self.show_frames(Clientes)
    
    def proveedor(self):
        self.show_frames(Proveedor)

    def informacion(self):
        self.show_frames(Ventas_productos)

    def gestionar(self):
        self.show_frames(GestorProductos)

    def widgets(self):
        frame2= tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)

        ruta=self.rutas(r"Iconos/inventario.png")
        #Poner iconos a los botones
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        self.btn_servicio= Button(frame2, fg="black", text="Inventario", font="sans 14 bold", command=self.inventario)
        self.btn_servicio.config(image= imagen_tk, compound= LEFT, padx= 5)
        self.btn_servicio.image= imagen_tk
        self.btn_servicio.place(x=0, y=0, width=150, height=40)

        ruta=self.rutas(r"Iconos/servicios.png")
        #Poner iconos a los botones
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        self.btn_servicios_realizados= Button(frame2, fg="black", text="Servicios Realizados", font="sans 14 bold", command=self.servicios_realizados)
        self.btn_servicios_realizados.config(image= imagen_tk, compound= LEFT, padx= 5)
        self.btn_servicios_realizados.image= imagen_tk
        self.btn_servicios_realizados.place(x=150, y=0, width=250, height=40)

        ruta=self.rutas(r"Iconos/cliente.png")
        #Poner iconos a los botones
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        self.btn_clientes= Button(frame2, fg="black", text="Clientes", font="sans 14 bold", command=self.cliente)
        self.btn_clientes.config(image= imagen_tk, compound= LEFT, padx= 5)
        self.btn_clientes.image= imagen_tk
        self.btn_clientes.place(x=400, y=0, width=200, height=40)

        ruta=self.rutas(r"Iconos/configuracion.png")
        #Poner iconos a los botones
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        self.btn_proveedor= Button(frame2, fg="black", text="Administrador", font="sans 14 bold", command=self.proveedor)
        self.btn_proveedor.config(image= imagen_tk, compound= LEFT, padx= 5)
        self.btn_proveedor.image= imagen_tk
        self.btn_proveedor.place(x=850, y=0, width=250, height=40)

        ruta=self.rutas(r"Iconos/ventas.png")
        #Poner iconos a los botones
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        self.btn_informacion= Button(frame2, fg="black", text="Ventas de productos", font="sans 14 bold", command=self.informacion)
        self.btn_informacion.config(image= imagen_tk, compound= LEFT, padx= 5)
        self.btn_informacion.image= imagen_tk
        self.btn_informacion.place(x=600, y=0, width=250, height=40)

        self.buttons= [self.btn_servicio, self.btn_servicios_realizados, self.btn_clientes, self.btn_proveedor,self.btn_informacion]