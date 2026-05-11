from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from utils.paths import get_resource_path
from database.servicio_dao import ServicioDAO
from database.cliente_dao import ClienteDAO
from utils.pdf_generator import PDFGenerator
from database.config_dao import ConfigDAO
import datetime
import threading
import sys
import os
from tkcalendar import DateEntry

class Servicios_realizados(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.servicio_dao = ServicioDAO()
        self.cliente_dao = ClienteDAO()
        self.config_dao = ConfigDAO()
        self.widgets()
        self.cargar_servicios()
        self.timer_servicios = None

        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder): #si no existe en el directorio la carpeta este lo crea
            os.makedirs(self.image_folder)

        lblframe_buscar = tk.LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#85c1e9")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
#Crea primero el combobox
        self.combobox_buscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.combobox_buscar.place(x=5, y=5, width=260, height=40)
        self.combobox_buscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
#Llama al combobox
        self.servicios_combobox()

    def widgets(self):
#Primer Label Frame
        canvas_servicios = tk.LabelFrame(self, text="Servicios Realizados", font="arial 16 bold", bg="#85c1e9")
        canvas_servicios.place(x=300, y=10, width=780, height=580)

        self.canvas = tk.Canvas(canvas_servicios, bg="#85c1e9")
        self.scrollbar = tk.Scrollbar(canvas_servicios, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#85c1e9")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        lblframe_seleccion = LabelFrame(self, text="Selección", font="arial 14 bold", bg="#85c1e9")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Cliente:", font="arial 12", bg="#85c1e9", wraplength=300)
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Nombre del equipo:", font="arial 12", bg="#85c1e9", wraplength=300)
        self.label2.place(x=5, y=30)

        self.label3 = tk.Label(lblframe_seleccion, text="Servicio:", font="arial 12", bg="#85c1e9")
        self.label3.place(x=5, y=55)

        self.label4 = tk.Label(lblframe_seleccion, text="Precio:", font="arial 12", bg="#85c1e9")
        self.label4.place(x=5, y=80)

        self.label5 = tk.Label(lblframe_seleccion, text="Fecha de entrega:", font="arial 12", bg="#85c1e9")
        self.label5.place(x=5, y=105)

        self.label6 = tk.Label(lblframe_seleccion, text="Estado:", font="arial 12", bg="#85c1e9")
        self.label6.place(x=5, y=130)

        lblframe_botones = LabelFrame(self, bg="#85c1e9", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)


        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/agregar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_servicios)
        btn1.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn1.image= imagen_tk
        btn1.place(x=20, y=20, width=180, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/editar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_servicios)
        btn2.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn2.image= imagen_tk
        btn2.place(x=20, y=80, width=180, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/eliminar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        btn3 = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_servicio)
        btn3.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn3.image= imagen_tk
        btn3.place(x=20, y=140, width=180, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/hoja_servicio.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        #Crear Botones y configurarlos
        btn4 = tk.Button(lblframe_botones, text="Hoja de Servicio", font="arial 14 bold", command=self.hoja_servicio)
        btn4.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn4.image= imagen_tk
        btn4.place(x=20, y=200, width=210, height=40)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path)
            
            self.image_tk = ImageTk.PhotoImage(image)
            self.servicio_image = self.image_tk
            self.image_path = image_save_path
            
            img_label = tk.Label(self.frameimg, image=self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)

    def servicios_combobox(self):
        try:
            self.servicios = self.servicio_dao.get_all_nombres_servicios()
            self.combobox_buscar["values"] = self.servicios
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar servicios: {e}")

    def agregar_servicios(self):
        top = tk.Toplevel(self)
        top.title("Agregar Servicio")
        top.geometry("700x400+200+50")
        top.config(bg="#85c1e9")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        tk.Label(top, text="Servicio:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=20, width=150, height=25)
        entry_servicio = ttk.Entry(top, font="arial 12 bold")
        entry_servicio.place(x=180, y=20, width=250, height=30)

        tk.Label(top, text="Cliente:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=60, width=150, height=25)
        entry_cliente = ttk.Entry(top, font="arial 12 bold")
        entry_cliente.place(x=180, y=60, width=250, height=30)

        tk.Label(top, text="Nombre del equipo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=100, width=150, height=25)
        entry_equipo = ttk.Entry(top, font="arial 12 bold")
        entry_equipo.place(x=180, y=100, width=250, height=30)

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=140, width=150, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=180, y=140, width=250, height=30)

        tk.Label(top, text="Fecha de recibo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=180, width=150, height=25)
        entry_fecha_recibo = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        entry_fecha_recibo.place(x=180, y=180, width=250, height=30)

        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=220, width=150, height=25)
        entry_estado = ttk.Combobox(top, font="arial 12 bold", state="readonly")
        entry_estado["values"] = ("Recibido", "En Proceso", "Entregado")
        entry_estado.place(x=180, y=220, width=250, height=30)

        # Variables locales de imagen para este diálogo
        dialog_state = {"image_path": r"fotos/default.png"}

        frameimg_add = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg_add.place(x=440, y=30, width=200, height=200)

        def load_image_add():
            file_path = filedialog.askopenfilename()
            if file_path:
                img = Image.open(file_path)
                img = img.resize((200, 200), Image.LANCZOS)
                image_name = os.path.basename(file_path)
                image_save_path = os.path.join(self.image_folder, image_name)
                img.save(image_save_path)
                dialog_state["image_tk"] = ImageTk.PhotoImage(img)
                dialog_state["image_path"] = image_save_path
                img_lbl = tk.Label(frameimg_add, image=dialog_state["image_tk"])
                img_lbl.place(x=0, y=0, width=200, height=200)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/subir_imagen.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_image = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=load_image_add)
        btn_image.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_image.image= imagen_tk
        btn_image.place(x=470, y=260, width=150, height=40)

        def guardar():
            cliente = entry_cliente.get()
            equipo = entry_equipo.get()
            servicio = entry_servicio.get()
            precio = entry_precio.get()
            fecha = entry_fecha_recibo.get()
            estado = entry_estado.get()

            if not cliente or not equipo or not servicio or not precio or not fecha or not estado:
                messagebox.showerror("Error", "Todos los campos deben de ser completados")
                return

            try:
                precio = float(precio)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return

            cliente_id = self.cliente_dao.obtener_id_por_nombre(cliente)
            if not cliente_id:
                messagebox.showerror("Error", "Cliente no encontrado en la base de datos.")
                return

            image_path = dialog_state["image_path"]

            try:
                self.servicio_dao.agregar_servicio(cliente_id, equipo, servicio, precio, fecha, estado, image_path)
                messagebox.showinfo("Éxito", "Servicio Agregado Correctamente")
                top.destroy()
                self.cargar_servicios()
                self.servicios_combobox()
            except Exception as e:
                print("Error al cargar el Servicio", e)
                messagebox.showerror("Error", "Error al agregar el servicio")

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/guardar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_guardar= tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btn_guardar.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn_guardar.image= imagen_tk
        btn_guardar.place(x=50, y=260, width=150, height=40)

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
        # Eliminar widgets existentes en el frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # Ejecutar la consulta a través del DAO
            servicios = self.servicio_dao.get_servicios_basico(filtro)

            # Mostrar los servicios en la interfaz gráfica
            self.row = 0
            self.column = 0

            for servicio, precio, image_path in servicios:
                self.mostrar_servicio(servicio, precio, image_path)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los servicios: {e}")

    def mostrar_servicio(self, servicio, precio, image_path):
        servicio_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", cursor="hand2")
        servicio_frame.grid(row=self.row, column=self.column, padx=10, pady=10)

        def seleccionar(nombre=servicio):
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
        
        name_label = tk.Label(servicio_frame, text=servicio, bg="white", anchor="w", wraplength=150, font="arial 10 bold", cursor="hand2")
        name_label.pack(side="top", fill="x")
        name_label.bind("<Button-1>", lambda e: seleccionar())

        precio_label = tk.Label(servicio_frame, text=f"Precio: ${precio:.2f}", bg="white", anchor="w", wraplength=150, font="arial 8 bold", cursor="hand2")
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
        servicio_seleccionado = self.combobox_buscar.get()

        try: 
            resultado = self.servicio_dao.get_servicio_por_nombre(servicio_seleccionado)

            if resultado is not None:
                cliente, equipo, servicio, precio, fecha, estado = resultado

                self.label1.config(text=f"Cliente: {cliente}")
                self.label2.config(text=f"Equipo: {equipo}")
                self.label3.config(text=f"Servicio: {servicio}")
                self.label4.config(text=f"Precio: ${precio:.2f}")
                self.label5.config(text=f"Fecha recibida: {fecha}")
                self.label6.config(text=f"Estado: {estado}")

                estado = estado.lower()  # Convertir a minúsculas una sola vez
                if estado == "recibido":
                    self.label6.config(fg="green")
                elif estado == "en proceso":
                    self.label6.config(fg="blue")
                elif estado == "entregado":
                    self.label6.config(fg="red")
            else:
                self.label1.config(text="Cliente: No encontrado")
                self.label2.config(text="Equipo: N/A")
                self.label3.config(text="Servicio: N/A")
                self.label4.config(text="Precio: N/A")
                self.label5.config(text="Fecha recibida: N/A")
                self.label6.config(text="Estado: N/A", fg="black")

        except sqlite3.Error as e:
            print("Error al obtener los datos del artículo:", e)
            messagebox.showerror("Error", "Error al obtener los datos del artículo")

    def filtrar_servicios(self, event):
        """Filtra los servicios en tiempo real sin usar un temporizador"""
        typed = self.combobox_buscar.get()

        if typed == "":
            data = self.servicios
        else:
            data = [item for item in self.servicios if typed.lower() in item.lower()]

        if data:
            self.combobox_buscar['values'] = data
            self.combobox_buscar.event_generate('<Down>')
        else:
            self.combobox_buscar['values'] = ['No se encontraron resultados']
            self.combobox_buscar.event_generate('<Down>')

        # Actualizar la interfaz gráfica con el filtro aplicado
        self.cargar_servicios(filtro=typed)
        self.servicios_combobox()

    def editar_servicios(self):
        selected_item = self.combobox_buscar.get()

        if not selected_item:
            messagebox.showerror("Error", "Selecciona un servicio para editar")
            return

        try:
            resultado = self.servicio_dao.get_servicio_por_nombre(selected_item, include_image=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar el servicio: {e}")
            return

        if not resultado:
            messagebox.showerror("Error", "Servicio no encontrado en la base de datos")
            return

        top = tk.Toplevel(self)
        top.title("Editar Servicio")
        top.geometry("700x500+200+50")
        top.config(bg="#85c1e9")
        top.resizable(False, False)
        top.grab_set()
        top.focus_set()
        top.lift()

        (cliente, equipo, servicio, precio, fecha, estado, image_path) = resultado

        # --- Campos izquierda ---
        tk.Label(top, text="Cliente:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=20, width=110, height=25)
        entry_cliente = ttk.Entry(top, font="arial 12 bold")
        entry_cliente.place(x=140, y=20, width=260, height=30)
        entry_cliente.insert(0, cliente if cliente else "")

        tk.Label(top, text="Equipo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=65, width=110, height=25)
        entry_equipo = ttk.Entry(top, font="arial 12 bold")
        entry_equipo.place(x=140, y=65, width=260, height=30)
        entry_equipo.insert(0, equipo if equipo else "")

        tk.Label(top, text="Servicio:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=110, width=110, height=25)
        entry_servicio = ttk.Entry(top, font="arial 12 bold")
        entry_servicio.place(x=140, y=110, width=260, height=30)
        entry_servicio.insert(0, servicio if servicio else "")

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=155, width=110, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=140, y=155, width=260, height=30)
        entry_precio.insert(0, str(precio) if precio is not None else "")

        tk.Label(top, text="Fecha de recibo:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=200, width=110, height=25)
        entry_fecha = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        entry_fecha.place(x=140, y=200, width=260, height=30)
        try:
            from datetime import datetime as _dt
            dt = _dt.strptime(fecha, '%Y-%m-%d')
            entry_fecha.set_date(dt.date())
        except Exception:
            pass

        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#85c1e9").place(x=20, y=245, width=110, height=25)
        entry_estado = ttk.Combobox(top, font="arial 12 bold", state="readonly")
        entry_estado["values"] = ("Recibido", "En Proceso", "Entregado")
        entry_estado.place(x=140, y=245, width=260, height=30)
        # Usar .set() — .insert() no funciona en Combobox readonly
        if estado in ("Recibido", "En Proceso", "Entregado"):
            entry_estado.set(estado)
        else:
            entry_estado.current(0)

        # --- Imagen derecha ---
        edit_state = {"image_path": image_path if image_path else r"fotos/default.png"}

        frameimg_edit = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg_edit.place(x=440, y=30, width=200, height=200)

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.LANCZOS)
                edit_state["image_tk"] = ImageTk.PhotoImage(img)
                image_label = tk.Label(frameimg_edit, image=edit_state["image_tk"])
                image_label.pack(expand=True, fill="both")
            except Exception:
                pass

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

        ruta = get_resource_path(r"Iconos/subir_imagen.png")
        imagen_pil = Image.open(ruta)
        imagen_tk = ImageTk.PhotoImage(imagen_pil.resize((30, 30)))
        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=load_image_edit)
        btnimagen.config(image=imagen_tk, compound=LEFT, padx=5)
        btnimagen.image = imagen_tk
        btnimagen.place(x=450, y=380, width=180, height=40)

        # --- Guardar ---
        def guardar():
            nuevo_cliente = entry_cliente.get().strip()
            nuevo_equipo = entry_equipo.get().strip()
            nuevo_servicio = entry_servicio.get().strip()
            nuevo_precio_str = entry_precio.get().strip()
            nuevo_estado = entry_estado.get().strip()

            # Obtener fecha correctamente desde DateEntry
            try:
                nuevo_fecha = entry_fecha.get_date().strftime('%Y-%m-%d')
            except Exception:
                nuevo_fecha = entry_fecha.get()

            if not nuevo_cliente or not nuevo_equipo or not nuevo_servicio or not nuevo_precio_str or not nuevo_fecha or not nuevo_estado:
                messagebox.showerror("Error", "Todos los campos deben de ser completados")
                return

            try:
                nuevo_precio = float(nuevo_precio_str)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return

            cliente_id = self.cliente_dao.obtener_id_por_nombre(nuevo_cliente)
            if not cliente_id:
                messagebox.showerror("Error", f"Cliente '{nuevo_cliente}' no encontrado en la base de datos.")
                return

            img_path = edit_state["image_path"]

            try:
                self.servicio_dao.actualizar_servicio(
                    cliente_id, nuevo_equipo, nuevo_servicio,
                    nuevo_precio, nuevo_fecha, nuevo_estado,
                    img_path, selected_item
                )
                top.destroy()
                self.servicios_combobox()
                self.cargar_servicios()
                messagebox.showinfo("Éxito", "Servicio editado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al editar el servicio: {e}")

        ruta = get_resource_path(r"Iconos/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_tk2 = ImageTk.PhotoImage(imagen_pil.resize((30, 30)))
        btn_guardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btn_guardar.config(image=imagen_tk2, compound=LEFT, padx=5)
        btn_guardar.image = imagen_tk2
        btn_guardar.place(x=140, y=420, width=150, height=40)

        ruta = get_resource_path(r"Iconos/cancelar.png")
        imagen_pil = Image.open(ruta)
        imagen_tk3 = ImageTk.PhotoImage(imagen_pil.resize((30, 30)))
        btn_cancelar = tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btn_cancelar.config(image=imagen_tk3, compound=LEFT, padx=5)
        btn_cancelar.image = imagen_tk3
        btn_cancelar.place(x=310, y=420, width=150, height=40)

    def eliminar_servicio(self):
        """Elimina un servicio seleccionado de la base de datos y actualiza la interfaz"""
        servicio_seleccionado = self.combobox_buscar.get()

        if not servicio_seleccionado:
            messagebox.showerror("Error", "Selecciona un servicio para eliminar")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el servicio '{servicio_seleccionado}'?")
        if not respuesta:
            return

        try:
            # Eliminar el servicio a través del DAO
            self.servicio_dao.eliminar_servicio(servicio_seleccionado)

            # Actualizar la interfaz gráfica
            self.cargar_servicios()
            self.servicios_combobox()
            self.actualizar_label()

            messagebox.showinfo("Éxito", f"El servicio '{servicio_seleccionado}' ha sido eliminado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el servicio: {e}")

    def hoja_servicio(self):
        selected_item = self.combobox_buscar.get()

        if not selected_item:
            messagebox.showerror("Error", "Selecciona un servicio para generar la hoja de servicio")
            return

        # Obtener los datos del servicio seleccionado
        try:
            resultado = self.servicio_dao.get_servicio_por_nombre(selected_item)

            if not resultado:
                messagebox.showerror("Error", "No se encontraron datos para el servicio seleccionado")
                return

            cliente, equipo, servicio, precio, fecha_recibo, estado = resultado

            # Generar número de orden automáticamente
            try:
                nuevo_numero = self.servicio_dao.obtener_nuevo_numero_orden()

            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el número de orden: {e}")
                return

            # Crear ventana de hoja de servicio
            ventana_hoja = tk.Toplevel()
            ventana_hoja.title("Hoja de Servicio")
            ventana_hoja.geometry("800x900")
            ventana_hoja.configure(bg="#f0f0f0")
            
            # Frame con scroll
            main_frame = tk.Frame(ventana_hoja, bg="#f0f0f0")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            canvas = tk.Canvas(main_frame, bg="#f0f0f0")
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Título
            tk.Label(scrollable_frame, text="HOJA DE SERVICIO", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

            # Frame para información básica
            info_frame = tk.LabelFrame(scrollable_frame, text="Información Básica", font=("Arial", 12, "bold"), bg="#f0f0f0")
            info_frame.pack(fill="x", padx=10, pady=5)

            # Número de orden (readonly)
            tk.Label(info_frame, text="Número de Orden:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            entry_numero_orden = tk.Entry(info_frame, font=("Arial", 10), state="readonly")
            entry_numero_orden.grid(row=0, column=1, padx=5, pady=5)
            entry_numero_orden.configure(state="normal")
            entry_numero_orden.delete(0, tk.END)
            entry_numero_orden.insert(0, nuevo_numero)
            entry_numero_orden.configure(state="readonly")

            # Frame para información del cliente
            cliente_frame = tk.LabelFrame(scrollable_frame, text="Información del Cliente", font=("Arial", 12, "bold"), bg="#f0f0f0")
            cliente_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(cliente_frame, text="Cliente:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(cliente_frame, text=cliente, font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5)

            # Frame para información del equipo
            equipo_frame = tk.LabelFrame(scrollable_frame, text="Información del Equipo", font=("Arial", 12, "bold"), bg="#f0f0f0")
            equipo_frame.pack(fill="x", padx=10, pady=5)

            # Primera columna
            tk.Label(equipo_frame, text="Equipo:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(equipo_frame, text=equipo, font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5)

            tk.Label(equipo_frame, text="IMEI:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
            entry_imei = tk.Entry(equipo_frame, font=("Arial", 10))
            entry_imei.grid(row=1, column=1, padx=5, pady=5)

            tk.Label(equipo_frame, text="Contraseña:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
            entry_contrasena = tk.Entry(equipo_frame, font=("Arial", 10))
            entry_contrasena.grid(row=2, column=1, padx=5, pady=5)

            # Segunda columna - Checkboxes
            estados_equipo = {}
            checkboxes = [
                "Autorizado", "Tarjeta SIM", "Memoria", "Apagado", 
                "Encendido", "Mojado", "Bandeja SIM"
            ]
            
            for i, texto in enumerate(checkboxes):
                var = tk.BooleanVar()
                estados_equipo[texto] = var
                tk.Checkbutton(equipo_frame, text=texto, variable=var, bg="#f0f0f0").grid(
                    row=i, column=2, padx=5, pady=5, sticky="w"
                )

            # Frame para detalles del servicio
            servicio_frame = tk.LabelFrame(scrollable_frame, text="Detalles del Servicio", font=("Arial", 12, "bold"), bg="#f0f0f0")
            servicio_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(servicio_frame, text="Cantidad:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            entry_cantidad = tk.Entry(servicio_frame, font=("Arial", 10))
            entry_cantidad.grid(row=0, column=1, padx=5, pady=5)
            entry_cantidad.insert(0, "1")

            tk.Label(servicio_frame, text="Servicio:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
            tk.Label(servicio_frame, text=servicio, font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=1, padx=5, pady=5)

            tk.Label(servicio_frame, text="Precio:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
            entry_precio = tk.Entry(servicio_frame, font=("Arial", 10))
            entry_precio.grid(row=2, column=1, padx=5, pady=5)
            entry_precio.insert(0, str(precio))

            tk.Label(servicio_frame, text="Anticipo:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
            entry_anticipo = tk.Entry(servicio_frame, font=("Arial", 10))
            entry_anticipo.grid(row=3, column=1, padx=5, pady=5)
            entry_anticipo.insert(0, "0")

            # Frame para fechas
            fechas_frame = tk.LabelFrame(scrollable_frame, text="Fechas", font=("Arial", 12, "bold"), bg="#f0f0f0")
            fechas_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(fechas_frame, text="Fecha de Entrega:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            entry_fecha_entrega = DateEntry(fechas_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            entry_fecha_entrega.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(fechas_frame, text="Fecha de Instalación:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
            entry_fecha_instalacion = DateEntry(fechas_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            entry_fecha_instalacion.grid(row=1, column=1, padx=5, pady=5)

            # Frame para detalles técnicos
            tecnicos_frame = tk.LabelFrame(scrollable_frame, text="Detalles Técnicos", font=("Arial", 12, "bold"), bg="#f0f0f0")
            tecnicos_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(tecnicos_frame, text="Falla reportada:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            entry_falla = tk.Text(tecnicos_frame, font=("Arial", 10), height=3, width=40)
            entry_falla.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(tecnicos_frame, text="Diagnóstico:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
            entry_diagnostico = tk.Text(tecnicos_frame, font=("Arial", 10), height=3, width=40)
            entry_diagnostico.grid(row=1, column=1, padx=5, pady=5)

            tk.Label(tecnicos_frame, text="Observaciones:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
            entry_observaciones = tk.Text(tecnicos_frame, font=("Arial", 10), height=3, width=40)
            entry_observaciones.grid(row=2, column=1, padx=5, pady=5)

            # Frame para pruebas de funcionamiento
            pruebas_frame = tk.LabelFrame(scrollable_frame, text="Pruebas de Funcionamiento", font=("Arial", 12, "bold"), bg="#f0f0f0")
            pruebas_frame.pack(fill="x", padx=10, pady=5)

            pruebas = [
                "Señal", "Pantalla", "Batería", "Sistema", "Auricular", 
                "Altavoz", "Micrófono", "Subir Volumen", "Bajar Volumen",
                "Botón de Encendido", "Touch", "Estética de Chasis", "Flash",
                "Cámara Principal", "Cámara Selfie", "Huella", "Face ID",
                "Bloqueo de Sonido", "Carga", "Vibrador"
            ]

            estado_pruebas = {"ingreso": {}, "egreso": {}}

            # Crear encabezados
            tk.Label(pruebas_frame, text="Prueba", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(pruebas_frame, text="Ingreso", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=1, columnspan=2, padx=5, pady=5)
            tk.Label(pruebas_frame, text="Egreso", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=3, columnspan=2, padx=5, pady=5)

            for idx, prueba in enumerate(pruebas, 1):
                tk.Label(pruebas_frame, text=prueba, font=("Arial", 10), bg="#f0f0f0").grid(row=idx, column=0, padx=5, pady=2, sticky="w")
                
                # Variables para ingreso
                var_ingreso = tk.StringVar(value="No")
                estado_pruebas["ingreso"][prueba] = var_ingreso
                tk.Radiobutton(pruebas_frame, text="Si", variable=var_ingreso, value="Si", bg="#f0f0f0").grid(row=idx, column=1, padx=2, pady=2)
                tk.Radiobutton(pruebas_frame, text="No", variable=var_ingreso, value="No", bg="#f0f0f0").grid(row=idx, column=2, padx=2, pady=2)
                
                # Variables para egreso
                var_egreso = tk.StringVar(value="No")
                estado_pruebas["egreso"][prueba] = var_egreso
                tk.Radiobutton(pruebas_frame, text="Si", variable=var_egreso, value="Si", bg="#f0f0f0").grid(row=idx, column=3, padx=2, pady=2)
                tk.Radiobutton(pruebas_frame, text="No", variable=var_egreso, value="No", bg="#f0f0f0").grid(row=idx, column=4, padx=2, pady=2)

            # Frame para botones
            botones_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
            botones_frame.pack(fill="x", padx=10, pady=15)

            # Botón guardar
            btn_guardar = tk.Button(
                botones_frame,
                text="Guardar",
                command=lambda: self.guardar_hoja(
                    entry_numero_orden, entry_fecha_entrega, entry_fecha_instalacion,
                    entry_falla, entry_diagnostico, entry_observaciones,
                    entry_cantidad, entry_precio, cliente, equipo, servicio,
                    estado_pruebas, entry_imei, entry_contrasena, estados_equipo,
                    entry_anticipo
                ),
                bg="#28a745",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=20
            )
            btn_guardar.pack(side=tk.LEFT, padx=5)

            # Botón cancelar
            btn_cancelar = tk.Button(
                botones_frame,
                text="Cancelar",
                command=ventana_hoja.destroy,
                bg="#dc3545",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=20
            )
            btn_cancelar.pack(side=tk.LEFT, padx=5)

            # Configurar el scroll
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la hoja de servicio: {str(e)}")

    def calcular_total(self, entry_cantidad, entry_precio, entry_total):
        try:
            cantidad = int(entry_cantidad.get())
            precio = float(entry_precio.get())
            total = cantidad * precio
            entry_total.config(state="normal")
            entry_total.delete(0, tk.END)
            entry_total.insert(0, f"{total:.2f}")
            entry_total.config(state="readonly")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos para cantidad y precio.")

    def guardar_hoja(self, entry_numero_orden, entry_fecha_entrega, entry_fecha_instalacion, entry_falla, entry_diagnostico, entry_observaciones, entry_cantidad, entry_precio, cliente, equipo, servicio, estado_pruebas, entry_imei, entry_contrasena, estados_equipo, entry_anticipo):
        try:
            # Obtener y validar los datos ingresados
            numero_orden = entry_numero_orden.get().strip()
            fecha_entrega = entry_fecha_entrega.get().strip()
            fecha_instalacion = entry_fecha_instalacion.get().strip()
            falla = entry_falla.get("1.0", "end").strip()
            diagnostico = entry_diagnostico.get("1.0", "end").strip()
            observaciones = entry_observaciones.get("1.0", "end").strip()
            cantidad = int(entry_cantidad.get().strip())
            precio = float(entry_precio.get().strip())
            imei = entry_imei.get().strip()
            contrasena = entry_contrasena.get().strip()
            anticipo = float(entry_anticipo.get().strip())

            # Validar campos obligatorios
            campos_obligatorios = {
                'Número de orden': numero_orden,
                'Fecha de entrega': fecha_entrega,
                'Fecha de instalación': fecha_instalacion,
                'Falla reportada': falla,
                'Diagnóstico': diagnostico,
                'IMEI': imei
            }
            
            campos_vacios = [campo for campo, valor in campos_obligatorios.items() if not valor]
            if campos_vacios:
                messagebox.showerror("Error", f"Los siguientes campos son obligatorios:\n{', '.join(campos_vacios)}")
                return False

            # Obtener datos de empresa usando ConfigDAO
            datos_empresa = self.config_dao.obtener_info_completa()

            # Extraer los estados a una lista pura
            estados_lista = [nombre for nombre, var in estados_equipo.items() if var.get()]

            # Extraer las pruebas a una lista de diccionarios puros
            pruebas_data = []
            for prueba in list(estado_pruebas["ingreso"].keys()):
                pruebas_data.append({
                    "nombre": prueba,
                    "ingreso": estado_pruebas["ingreso"][prueba].get(),
                    "egreso": estado_pruebas["egreso"][prueba].get()
                })

            # Llamar a PDFGenerator
            nombre_archivo = PDFGenerator.generar_hoja_servicio(
                datos_empresa=datos_empresa,
                cliente=cliente,
                equipo=equipo,
                servicio=servicio,
                precio=precio,
                falla=falla,
                diagnostico=diagnostico,
                numero_orden=numero_orden,
                estado="N/A", 
                fecha_entrega=fecha_entrega,
                fecha_instalacion=fecha_instalacion,
                observaciones=observaciones,
                cantidad=cantidad,
                imei=imei,
                contrasena=contrasena,
                estados_equipo_lista=estados_lista,
                pruebas_data=pruebas_data,
                anticipo=anticipo
            )

            # Guardar el nuevo número de orden en la base de datos
            try:
                import sqlite3
                conn = self.servicio_dao.db.get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Hojas_de_Servicio (numero_orden, fecha_creacion) VALUES (?, datetime('now'))",
                    (numero_orden,)
                )
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar el número de orden en la base de datos: {e}")
                
            messagebox.showinfo("Éxito", f"Hoja de servicio guardada como: {nombre_archivo}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la hoja de servicio: {str(e)}")
            return False
