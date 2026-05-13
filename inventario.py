from tkinter import *
from servicios_realizados import Servicios_realizados
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from utils.paths import get_resource_path
from database.inventario_dao import InventarioDAO
from PIL import Image, ImageTk
import os
import sys

class Inventario(Servicios_realizados):
    
    def __init__(self, padre):
        self.inventario_dao = InventarioDAO()
        super().__init__(padre)
        self.widgets()
        self.combobox_buscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.servicios_combobox()  # Llama a servicios_combobox para llenar el combobox

    def widgets(self):
        super().widgets()  # Llama al método de la clase padre para crear widgets comunes

        # Crear el LabelFrame específico para Inventario
        canvas_servicios = tk.LabelFrame(self, text="Inventario", font="arial 16 bold", bg="#85c1e9")
        canvas_servicios.place(x=300, y=10, width=780, height=580)

        self.canvas = tk.Canvas(canvas_servicios, bg="#85c1e9")
        self.scrollbar = tk.Scrollbar(canvas_servicios, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#85c1e9")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Combobox para buscar productos
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#85c1e9")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.combobox_buscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.combobox_buscar.place(x=5, y=5, width=260, height=40)
        self.combobox_buscar.bind("<KeyRelease>", self.filtrar_servicios)

        # Labels para mostrar selección
        lblframe_seleccion = LabelFrame(self, text="Selección", font="arial 14 bold", bg="#85c1e9")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Producto:", font="arial 12", bg="#85c1e9", wraplength=300)
        self.label1.place(x=5, y=5)

        self.label7 = tk.Label(lblframe_seleccion, text="No. Serie:", font="arial 12", bg="#85c1e9", wraplength=300)
        self.label7.place(x=5, y=30)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio costo:", font="arial 12", bg="#85c1e9", wraplength=300)
        self.label2.place(x=5, y=55)

        self.label3 = tk.Label(lblframe_seleccion, text="Precio venta:", font="arial 12", bg="#85c1e9")
        self.label3.place(x=5, y=80)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock:", font="arial 12", bg="#85c1e9")
        self.label4.place(x=5, y=105)

        self.label5 = tk.Label(lblframe_seleccion, text="Estado:", font="arial 12", bg="#85c1e9")
        self.label5.place(x=5, y=130)

        # Botones
        lblframe_botones = LabelFrame(self, bg="#85c1e9", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/agregar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        # Crear Botones y configurarlos
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_servicios)
        btn1.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn1.image= imagen_tk
        btn1.place(x=20, y=20, width=180, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/editar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        # Crear Botones y configurarlos
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_servicios)
        btn2.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn2.image= imagen_tk
        btn2.place(x=20, y=80, width=180, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/eliminar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear botones y configurarlos
        btn3 = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_producto)
        btn3.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn3.image= imagen_tk
        btn3.place(x=20, y=140, width=180, height=40)


    def servicios_combobox(self):
        try:
            self.inventario = self.inventario_dao.get_all_nombres_productos()
            self.combobox_buscar["values"] = self.inventario
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inventario: {e}")

    def agregar_servicios(self):
        top = tk.Toplevel(self)
        top.title("Agregar Producto")
        top.geometry("700x400+200+50")
        top.config(bg="#85c1e9")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=20, width=150, height=25)
        entry_producto = ttk.Entry(top, font="arial 12 bold")
        entry_producto.place(x=180, y=20, width=250, height=30)

        tk.Label(top, text="No. Serie:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=60, width=150, height=25)
        entry_serie = ttk.Entry(top, font="arial 12 bold")
        entry_serie.place(x=180, y=60, width=250, height=30)

        tk.Label(top, text="Precio costo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=100, width=150, height=25)
        entry_precosto = ttk.Entry(top, font="arial 12 bold")
        entry_precosto.place(x=180, y=100, width=250, height=30)

        tk.Label(top, text="Precio venta:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=140, width=150, height=25)
        entry_preventa = ttk.Entry(top, font="arial 12 bold")
        entry_preventa.place(x=180, y=140, width=250, height=30)

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=180, width=150, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=180, y=180, width=250, height=30)

        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=220, width=150, height=25)
        # Cambiar ttk.Entry por ttk.Combobox
        entry_estado = ttk.Combobox(top, font="arial 12 bold", state="readonly")
        entry_estado["values"] = ["Activo", "Inactivo"]  # Opciones disponibles
        entry_estado.place(x=180, y=220, width=250, height=30)

        # Variables locales para la imagen de este diálogo (no compartidas con otras ventanas)
        dialog_state = {"image_path": r"fotos/default.png"}

        frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg.place(x=440, y=30, width=200, height=200)

        def load_image_local():
            file_path = filedialog.askopenfilename()
            if file_path:
                image = Image.open(file_path)
                image = image.resize((200, 200), Image.LANCZOS)
                image_name = os.path.basename(file_path)
                image_save_path = os.path.join(self.image_folder, image_name)
                image.save(image_save_path)
                dialog_state["image_tk"] = ImageTk.PhotoImage(image)
                dialog_state["image_path"] = image_save_path
                img_label = tk.Label(frameimg, image=dialog_state["image_tk"])
                img_label.place(x=0, y=0, width=200, height=200)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/subir_imagen.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_image = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=load_image_local)
        btn_image.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_image.image= imagen_tk
        btn_image.place(x=470, y=260, width=200, height=40)

        def guardar():
            producto = entry_producto.get()
            precosto = entry_precosto.get()
            preventa = entry_preventa.get()
            stock = entry_stock.get()
            estado = entry_estado.get()
            serie= entry_serie.get()

            if not producto or not precosto or not preventa or not stock or not estado or not serie:
                messagebox.showerror("Error", "Todos los campos deben de ser completados")
                return
            
            try:
                precosto = float(precosto)
                preventa = float(preventa)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Los precios y el stock deben ser números válidos")
                return
            
            image_path = dialog_state["image_path"]

            try:
                self.inventario_dao.agregar_producto(producto, preventa, precosto, stock, estado, image_path, serie)
                messagebox.showinfo("Éxito", "Producto Agregado Correctamente")
                top.destroy()
                self.cargar_servicios()
                self.servicios_combobox()
            except Exception as e:
                print("Error al cargar el producto", e)
                messagebox.showerror("Error", "Error al agregar el producto")

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/guardar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_guardar2= tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btn_guardar2.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_guardar2.image= imagen_tk
        btn_guardar2.place(x=50, y=260, width=150, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/cancelar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_cancelar= tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btn_cancelar.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_cancelar.image= imagen_tk
        btn_cancelar.place(x=260, y=260, width=150, height=40)

    def cargar_servicios(self, filtro=None, categoria=None):
        self.after(0, self._cargar_servicios, filtro, categoria)

    def _cargar_servicios(self, filtro=None, categoria=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            productos = self.inventario_dao.get_productos_basico(filtro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
            productos = []

        self.row = 0
        self.column = 0

        for producto, precosto, image_path in productos:
            self.mostrar_servicio(producto, precosto, image_path)

    def mostrar_servicio(self, producto, precosto, image_path):
        servicio_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", cursor="hand2")
        servicio_frame.grid(row=self.row, column=self.column, padx=10, pady=10)

        def seleccionar(nombre=producto):
            self.combobox_buscar.set(nombre)
            self.actualizar_label()
            # Resaltar la tarjeta seleccionada
            for widget in self.scrollable_frame.winfo_children():
                widget.config(bg="white")
                for child in widget.winfo_children():
                    try:
                        child.config(bg="white")
                    except Exception:
                        pass
            servicio_frame.config(bg="#aed6f1")
            for child in servicio_frame.winfo_children():
                try:
                    child.config(bg="#aed6f1")
                except Exception:
                    pass

        ruta_imagen = get_resource_path(image_path)
        if image_path and os.path.exists(ruta_imagen):
            image = Image.open(ruta_imagen)
            image = image.resize((200, 200), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(servicio_frame, image=imagen, cursor="hand2")
            image_label.image = imagen
            image_label.pack(expand=True, fill="both")
            image_label.bind("<Button-1>", lambda e: seleccionar())
        
        name_label = tk.Label(servicio_frame, text=producto, bg="white", anchor="w", wraplength=150, font="arial 10 bold", cursor="hand2")
        name_label.pack(side="top", fill="x")
        name_label.bind("<Button-1>", lambda e: seleccionar())

        precio_label = tk.Label(servicio_frame, text=f"Precio: ${precosto:.2f}", bg="white", anchor="w", wraplength=150, font="arial 8 bold", cursor="hand2")
        precio_label.pack(side="bottom", fill="x")
        precio_label.bind("<Button-1>", lambda e: seleccionar())

        servicio_frame.bind("<Button-1>", lambda e: seleccionar())

        self.column += 1
        if self.column >= 3:
            self.column = 0
            self.row += 1

    def on_combobox_select(self, event):
        self.actualizar_label()

    def actualizar_label(self, event=None):
        producto_seleccionado = self.combobox_buscar.get().strip()


        try: 
            resultado = self.inventario_dao.get_producto_por_nombre(producto_seleccionado)

            if resultado is not None:
                producto, preciocos, precioven, stock, estado, serie = resultado

                self.label1.config(text=f"Producto: {producto}")
                self.label2.config(text=f"Precio costo: {preciocos}")
                self.label3.config(text=f"Precio venta: {precioven}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")
                self.label7.config(text=f"No. Serie: {serie}")

                if estado is None:
                    estado = "N/A"

                if estado is None:
                    estado = "N/A"

                estado = estado.lower()  # Convertir a minúsculas una sola vez
                if estado == "activo":
                    self.label5.config(fg="green")
                elif estado == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.label1.config(text="Producto: No encontrado")
                self.label2.config(text="Precio costo: N/A")
                self.label3.config(text="Precio venta: N/A")
                self.label4.config(text="Stock: N/A")
                self.label5.config(text="Estado: N/A")
                self.label7.config(text="No. Serie: N/A")

        except sqlite3.Error as e:
            print("Error al obtener los datos del producto:", e)
            messagebox.showerror("Error", "Error al obtener los datos del producto")

    def filtrar_servicios(self, event):
        typed = self.combobox_buscar.get()  
        if typed == "":
            data = self.inventario
        else:
            data = [item for item in self.inventario if typed.lower() in item.lower()]

        if data:
            self.combobox_buscar['values'] = data
            self.combobox_buscar.event_generate('<Down>')
        else: 
            self.combobox_buscar['values'] = ['No se encontraron resultados']
            self.combobox_buscar.event_generate('<Down>')

        self.cargar_servicios(filtro=typed)
        self.servicios_combobox()

    def editar_servicios(self):
        selected_item = self.combobox_buscar.get()

        if not selected_item:
            messagebox.showerror("Error", "Selecciona un producto para editar")
            return
        try:
            resultado = self.inventario_dao.get_producto_por_nombre(selected_item, include_image=True)
        except Exception:
            resultado = None

        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        top = tk.Toplevel(self)
        top.title("Editar Producto")
        top.geometry("700x400+200+50")
        top.config(bg="#85c1e9")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        (producto, precosto, preventa, stock, estado, image_path, serie) = resultado
        
        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=20, width=80, height=25)
        entry_producto = ttk.Entry(top, font="arial 12 bold")
        entry_producto.place(x=120, y=20, width=250, height=30)
        entry_producto.insert(0, producto)

        tk.Label(top, text="No. Serie:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=60, width=80, height=25)
        entry_serie = ttk.Entry(top, font="arial 12 bold")
        entry_serie.place(x=120, y=60, width=250, height=30)
        # Validar que el valor de 'serie' sea válido antes de insertarlo
        if serie is None:
            serie = ""  # Asignar un valor predeterminado si es None
        entry_serie.insert(0, serie)

        tk.Label(top, text="P. Venta:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=100, width=80, height=25)
        entry_preventa = ttk.Entry(top, font="arial 12 bold")
        entry_preventa.place(x=120, y=100, width=250, height=30)
        entry_preventa.insert(0, preventa)

        tk.Label(top, text="P. Costo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=135, width=80, height=25)
        entry_precosto = ttk.Entry(top, font="arial 12 bold")
        entry_precosto.place(x=120, y=140, width=250, height=30)
        entry_precosto.insert(0, precosto)

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=180, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=180, width=250, height=30)
        entry_stock.insert(0, stock)

        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=220, width=80, height=25)
        entry_estado2 = ttk.Combobox(top, font="arial 12 bold", state="readonly")
        entry_estado2["values"] = ["Activo", "Inactivo"]  # Opciones disponibles
        entry_estado2.place(x=120, y=220, width=250, height=30)
        entry_estado2.insert(0, estado)

        # Variables locales para la imagen de este diálogo (no compartidas con otras ventanas)
        edit_state = {"image_path": image_path if image_path else r"fotos/default.png"}

        frameimg_edit = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg_edit.place(x=440, y=30, width=200, height=200)

        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((200, 200), Image.LANCZOS)
            edit_state["image_tk"] = ImageTk.PhotoImage(img)
            image_label = tk.Label(frameimg_edit, image=edit_state["image_tk"])
            image_label.pack(expand=True, fill="both")

        def load_image_edit():
            file_path = filedialog.askopenfilename()
            if file_path:
                img = Image.open(file_path)
                img = img.resize((200, 200), Image.LANCZOS)
                image_name = os.path.basename(file_path)
                image_save_path = os.path.join(self.image_folder, image_name)
                img.save(image_save_path)
                edit_state["image_tk"] = ImageTk.PhotoImage(img)
                edit_state["image_path"] = image_save_path
                img_lbl = tk.Label(frameimg_edit, image=edit_state["image_tk"])
                img_lbl.place(x=0, y=0, width=200, height=200)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/subir_imagen.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=load_image_edit)
        btnimagen.config(image= imagen_tk, compound= LEFT, padx= 5)
        btnimagen.image= imagen_tk
        btnimagen.place(x=470, y=260, width=150, height=40)

        def guardar():
            nuevo_producto = entry_producto.get()
            nuevo_pre_ven = entry_preventa.get()
            nuevo_pre_cos = entry_precosto.get()
            nuevo_stock = entry_stock.get()
            nuevo_estado = entry_estado2.get()
            nuevo_serie = entry_serie.get()

            if not nuevo_producto or not nuevo_pre_ven or not nuevo_pre_cos or not nuevo_stock or not nuevo_estado or not nuevo_serie:
                messagebox.showerror("Error", "Todos los campos deben de ser completados")
                return
            
            try:
                nuevo_pre_cos = float(nuevo_pre_cos)
                nuevo_pre_ven = float(nuevo_pre_ven)
                nuevo_stock = int(nuevo_stock)
            except ValueError:
                messagebox.showerror("Error", "Los precios y el stock deben ser números válidos")

            image_path = edit_state["image_path"]

            try:
                self.inventario_dao.actualizar_producto(nuevo_producto, nuevo_pre_ven, nuevo_pre_cos, nuevo_stock, nuevo_estado, image_path, nuevo_serie, selected_item)
            except Exception as e:
                messagebox.showerror("Error", f"Error al editar producto: {e}")
                return
            self.servicios_combobox()
            self.actualizar_label()
            
            self.after(0, lambda: self.cargar_servicios(filtro=nuevo_producto))

            top.destroy()
            messagebox.showinfo("Éxito", "Producto editado exitosamente")

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/guardar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_guardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btn_guardar.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_guardar.image= imagen_tk
        btn_guardar.place(x=260, y=260, width=150, height=40)

    def eliminar_producto(self):
        """Elimina un producto seleccionado de la base de datos y actualiza la interfaz"""
        producto_seleccionado = self.combobox_buscar.get()

        if not producto_seleccionado:
            messagebox.showerror("Error", "Selecciona un producto para eliminar")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el producto '{producto_seleccionado}'?")
        if not respuesta:
            return

        try:
            # Eliminar el producto a través del DAO
            self.inventario_dao.eliminar_producto(producto_seleccionado)

            # Actualizar la interfaz gráfica
            self.cargar_servicios()
            self.servicios_combobox()

            messagebox.showinfo("Éxito", f"El producto '{producto_seleccionado}' ha sido eliminado correctamente.")
        except (sqlite3.Error, ValueError) as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")