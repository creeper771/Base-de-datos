from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils.paths import get_resource_path
from database.cliente_dao import ClienteDAO

class Clientes(tk.Frame):
    db_name = "database.db"

    def __init__(self,padre):
        super().__init__(padre)
        self.cliente_dao = ClienteDAO()
        self.widgets()
        self.cargar_registros()

    def widgets(self):
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="sans 20 bold", bg="#85c1e9")
        self.labelframe.place(x=20, y=20, width=250, height=560)

        lblnombre = tk.Label(self.labelframe, text="Nombre: ", font="sans 14 bold", bg="#85c1e9")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14")
        self.nombre.place(x=10, y=50, width=220, height=40)

        lbltelefono = tk.Label(self.labelframe, text="No. Celular: ", font="sans 14 bold", bg="#85c1e9")
        lbltelefono.place(x=10, y=100)
        self.telefono = ttk.Entry(self.labelframe, font="sans 14")
        self.telefono.place(x=10, y=130, width=220, height=40)

        lblcorreo = tk.Label(self.labelframe, text="Correo: ", font="sans 14 bold", bg="#85c1e9")
        lblcorreo.place(x=10, y=180)
        self.correo = ttk.Entry(self.labelframe, font="sans 14")
        self.correo.place(x=10, y=210, width=220, height=40)

        lbldireccion = tk.Label(self.labelframe, text="Direccion: ", font="sans 14 bold", bg="#85c1e9")
        lbldireccion.place(x=10, y=260)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14")
        self.direccion.place(x=10, y=290, width=220, height=40)


        #agregar icono a los botones
        ruta= get_resource_path(r"Iconos/agregar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_1 = tk.Button(self.labelframe, text="Agregar", font="sans 16 bold", command= self.registrar)
        btn_1.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_1.image= imagen_tk
        btn_1.place(x=10, y=380, width=220, height=40)

        #agregar icono a los botones
        ruta= get_resource_path(r"Iconos/modificar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_2 = tk.Button(self.labelframe, text="Modificar", font="sans 16 bold", command= self.modificar)
        btn_2.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_2.image= imagen_tk
        btn_2.place(x=10, y=428, width=220, height=40)

        #agregar icono a los botones
        ruta= get_resource_path(r"Iconos/eliminar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_3 = tk.Button(self.labelframe, text="Eliminar", font="sans 16 bold", command= self.eliminar)
        btn_3.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_3.image= imagen_tk
        btn_3.place(x=10, y=476, width=220, height=40)
        
        treFrame = Frame(self, bg="white")
        treFrame.place(x=280, y=20, width=800, height=560)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                 columns=("ID", "Nombre", "Telefono", "Direccion", "Correo"), show="headings")
        self.tree.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Telefono", text="Telefono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Direccion", text="Direccion")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150, anchor="center")
        self.tree.column("Telefono", width=120, anchor="center")
        self.tree.column("Correo", width=200, anchor="center")
        self.tree.column("Direccion", width=200, anchor="center")

    def validar_campos(self):
        if not self.nombre.get() or not self.telefono.get() or not self.direccion.get() or not self.correo.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False
        return True
    def registrar(self):
        if not self.validar_campos():
            return
        
        nombre = self.nombre.get()
        telefono = self.telefono.get()
        correo = self.correo.get()
        direccion = self.direccion.get()

        try:
            self.cliente_dao.agregar_cliente(nombre, telefono, correo, direccion)
            messagebox.showinfo("Exito", "Cliente registrado exitosamente.")
            self.limpiar_treeview()
            self.limpiar_campos()
            self.cargar_registros()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el cliente: {e}")

    def cargar_registros(self):
        try:
            rows = self.cliente_dao.obtener_clientes()
            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los registros: {e}")

    def limpiar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)
        

    def eliminar(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Seleccione un cliente para eliminar.")
            return

        item = self.tree.selection()[0]
        id_cliente = self.tree.item(item, "values")[0]
        nombre_cliente = self.tree.item(item, "values")[1]

        respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar al cliente '{nombre_cliente}'?")
        if not respuesta:
            return

        try:
            self.cliente_dao.eliminar_cliente(id_cliente)
            messagebox.showinfo("Exito", f"Cliente '{nombre_cliente}' eliminado correctamente.")
            self.limpiar_treeview()
            self.limpiar_campos()
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el cliente: {e}")

    def modificar(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Seleccione un cliente para modificar.")
            return
        
        item = self.tree.selection()[0]
        id_cliente = self.tree.item(item, "values")[0]

        nombre_actual = self.tree.item(item, "values")[1]
        telefono_actual = self.tree.item(item, "values")[2]
        direccion_actual = self.tree.item(item, "values")[3]
        correo_actual = self.tree.item(item, "values")[4]
        

        top_modificar = Toplevel(self)
        top_modificar.title("Modificar Cliente")
        top_modificar.geometry("400x400")
        top_modificar.config(bg="#85c1e9")
        top_modificar.resizable(False, False)
        top_modificar.grab_set()
        top_modificar.focus_set()
        top_modificar.lift()

        tk.Label(top_modificar, text="Nombre: ", font="sans 14 bold", bg="#85c1e9").grid(row=0, column=0, padx=10, pady=5)
        nombre_nuevo = tk.Entry(top_modificar, font="sans 14")
        nombre_nuevo.insert(0, nombre_actual)
        nombre_nuevo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Telefono: ", font="sans 14 bold", bg="#85c1e9").grid(row=1, column=0, padx=10, pady=5)
        telefono_nuevo = tk.Entry(top_modificar, font="sans 14")
        telefono_nuevo.insert(0, telefono_actual)
        telefono_nuevo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Direccion: ", font="sans 14 bold", bg="#85c1e9").grid(row=3, column=0, padx=10, pady=5)
        direccion_nueva = tk.Entry(top_modificar, font="sans 14")
        direccion_nueva.insert(0, direccion_actual)
        direccion_nueva.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Correo: ", font="sans 14 bold", bg="#85c1e9").grid(row=2, column=0, padx=10, pady=5)
        correo_nuevo = tk.Entry(top_modificar, font="sans 14")
        correo_nuevo.insert(0, correo_actual)
        correo_nuevo.grid(row=2, column=1, padx=10, pady=5)

        def guardar_modificaciones():
            nuevo_nombre = nombre_nuevo.get()
            nuevo_telefono = telefono_nuevo.get()
            nueva_direccion = direccion_nueva.get()
            nuevo_correo = correo_nuevo.get()

            try:
                self.cliente_dao.actualizar_cliente(id_cliente, nuevo_nombre, nuevo_telefono, nuevo_correo, nueva_direccion)
                messagebox.showinfo("Exito", "Cliente modificado exitosamente.")
                self.limpiar_treeview()
                self.cargar_registros()
                top_modificar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar el cliente: {e}")
        #agregar icono a los botones
        ruta= get_resource_path(r"Iconos/guardar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_guardar = tk.Button(top_modificar, text="Guardar", font="sans 16 bold", command=guardar_modificaciones)
        btn_guardar.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_guardar.image= imagen_tk
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)





