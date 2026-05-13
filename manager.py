from tkinter import *
from tkinter import ttk
from login import Login
from login import Registro
from container import Container
import sys
import os
from ttkthemes import ThemedStyle
from utils.paths import get_resource_path
from database.startup_migrations import run_startup_migrations


class Manager(Tk):
    def __init__(self, *args, **kwagrs):
        run_startup_migrations()
        super().__init__(*args, **kwagrs)
        self.title("Sistema de Gestión de Inventarios, Ventas y Servicios")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)
        
        self.usuario_activo_id = None
        self.usuario_activo_nombre = None
        
        ruta= get_resource_path(r"icono.ico")
        try:
            self.iconbitmap(ruta)
        except Exception:
            pass # Evita el crasheo en Linux al no soportar .ico directamente

        container= Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="#C6D9E3")

        self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i]=frame

        self.show_frame(Login)

        self.style= ThemedStyle(self)
        try:
            self.style.theme_use("winnative")
        except Exception:
            self.style.theme_use("clam")


    def show_frame(self, container):
        frame= self.frames[container]
        frame.tkraise()

def main():
    app = Manager()
    app.mainloop()

if __name__== "__main__":
    main()