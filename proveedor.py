from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from gestionar import GestorProductos, GestorServicios
import matplotlib.pyplot as plt
import datetime
from tkinter import filedialog
import io
from utils.paths import get_resource_path
from database.config_dao import ConfigDAO
from database.venta_dao import VentaDAO

class Proveedor(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.pack(fill="both", expand=True)
        self.config_dao = ConfigDAO()
        self.venta_dao = VentaDAO()
        self.widgets()

    def widgets(self):
        # Botón para abrir la ventana de datos de la empresa
        #Poner iconos al boton
        ruta= get_resource_path(r"Iconos/informacion.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((50, 50))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_datos_empresa = tk.Button(self, text="Datos de la Empresa", font="arial 12 bold", command=self.abrir_ventana_datos_empresa)
        btn_datos_empresa.config(image=imagen_tk, compound="top", padx=10)
        btn_datos_empresa.image = imagen_tk  # Mantener una referencia a la imagen
        btn_datos_empresa.place(x=20, y=20, width=250, height=250)

        # Botón para gestionar productos
        ruta= get_resource_path(r"Iconos/producto.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((50, 50))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_productos = tk.Button(self, text="Gestionar Inventario", font="arial 12 bold", command=self.gestionar_productos)
        btn_productos.config(image=imagen_tk, compound="top", padx=10)
        btn_productos.image = imagen_tk  # Mantener una referencia a la imagen
        btn_productos.place(x=290, y=20, width=250, height=250)

        # Botón para gestionar servicios
        ruta= get_resource_path(r"Iconos/servicio.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((50, 50))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_servicios = tk.Button(self, text="Gestionar Servicios", font="arial 12 bold", command=self.gestionar_servicios)
        btn_servicios.config(image=imagen_tk, compound="top", padx=10)
        btn_servicios.image = imagen_tk  # Mantener una referencia a la imagen
        btn_servicios.place(x=560, y=20, width=250, height=250)

        #Boton para grafica
        ruta= get_resource_path(r"Iconos/grafica.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((50, 50))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn_grafica = tk.Button(self, text="Grafica de Ventas", font="arial 12 bold", command=self.mostrar_grafica_ventas)
        btn_grafica.config(image=imagen_tk, compound="top", padx=10)
        btn_grafica.image = imagen_tk  # Mantener una referencia a la imagen
        btn_grafica.place(x=830, y=20, width=250, height=250)


    def abrir_ventana_datos_empresa(self):
        """Abre una ventana emergente para mostrar y modificar los datos de la empresa."""
        # Crear la ventana emergente
        ventana_empresa = tk.Toplevel(self)
        ventana_empresa.title("Datos de la Empresa")
        ventana_empresa.geometry("900x500+450+150")
        ventana_empresa.config(bg="#85c1e9")
        ventana_empresa.resizable(False, False)
        ventana_empresa.transient(self.master)
        ventana_empresa.grab_set()
        ventana_empresa.focus_set()
        ventana_empresa.lift()

        # Campos para los datos de la empresa
        label_empresa = tk.Label(ventana_empresa, text="Nombre de la Empresa:", font="sans 14 bold", bg="#85c1e9")
        label_empresa.place(x=20, y=20)
        entry_empresa = ttk.Entry(ventana_empresa, font="sans 14 bold")
        entry_empresa.place(x=20, y=60, width=350, height=30)

        label_direccion = tk.Label(ventana_empresa, text="Dirección:", font="sans 14 bold", bg="#85c1e9")
        label_direccion.place(x=20, y=100)
        entry_direccion = ttk.Entry(ventana_empresa, font="sans 14 bold")
        entry_direccion.place(x=20, y=140, width=350, height=30)

        label_telefono = tk.Label(ventana_empresa, text="Teléfono:", font="sans 14 bold", bg="#85c1e9")
        label_telefono.place(x=20, y=180)
        entry_telefono = ttk.Entry(ventana_empresa, font="sans 14 bold")
        entry_telefono.place(x=20, y=220, width=350, height=30)

        label_email = tk.Label(ventana_empresa, text="Email:", font="sans 14 bold", bg="#85c1e9")
        label_email.place(x=20, y=260)
        entry_email = ttk.Entry(ventana_empresa, font="sans 14 bold")
        entry_email.place(x=20, y=300, width=350, height=30)

        label_atiende = tk.Label(ventana_empresa, text="Atiende:", font="sans 14 bold", bg="#85c1e9")
        label_atiende.place(x=20, y=340)
        entry_atiende = ttk.Entry(ventana_empresa, font="sans 14 bold")
        entry_atiende.place(x=20, y=380, width=350, height=30)

        # Etiqueta para mostrar el logo
        label_logo = tk.Label(ventana_empresa, bg="#85c1e9")
        label_logo.place(x=400, y=20, width=400, height=400)
        self.mostrar_logo(label_logo)

        # Consultar los datos existentes en la base de datos
        try:
            datos = self.config_dao.obtener_informacion()
            if datos:
                # Rellenar los campos con los datos existentes
                entry_empresa.insert(0, datos[0])
                entry_direccion.insert(0, datos[1])
                entry_telefono.insert(0, datos[2])
                entry_email.insert(0, datos[3])
                entry_atiende.insert(0, datos[4])
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar los datos: {e}")

        # Botón para guardar o actualizar los datos
        def guardar_datos_empresa():
            empresa_nombre = entry_empresa.get().strip()
            direccion = entry_direccion.get().strip()
            telefono = entry_telefono.get().strip()
            email = entry_email.get().strip()
            atiende = entry_atiende.get().strip()

            # Validar que todos los campos estén completos
            if not all([empresa_nombre, direccion, telefono, email, atiende]):
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            # Guardar o actualizar los datos en la base de datos
            try:
                if self.config_dao.obtener_informacion():
                    # Confirmación antes de actualizar
                    if not messagebox.askyesno("Confirmación", "¿Desea actualizar los datos existentes?"):
                        return
                
                self.config_dao.guardar_informacion(empresa_nombre, direccion, telefono, email, atiende)
                messagebox.showinfo("Éxito", "Datos de la empresa guardados correctamente.")
                ventana_empresa.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar los datos: {e}")

        #Poner icono al boton
        ruta= get_resource_path(r"Iconos/guardar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_guardar = tk.Button(ventana_empresa, text="Guardar", font="sans 14 bold", command=guardar_datos_empresa)
        boton_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_guardar.image = imagen_tk  # Mantener una referencia a la imagen
        boton_guardar.place(x=140, y=420, width=150, height=40)

        # Poner icono al boton
        ruta= get_resource_path(r"Iconos/agregar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_ingresar_logo = tk.Button(ventana_empresa, text="Agregar Logo", font="sans 14 bold", command=lambda: [self.agregar_logo(), self.mostrar_logo(label_logo)])
        boton_ingresar_logo.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_ingresar_logo.image = imagen_tk  # Mantener una referencia a la imagen
        boton_ingresar_logo.place(x=450, y=420, width=250, height=40)



    def gestionar_productos(self):
        """Abre la ventana para gestionar productos"""
        gestor_productos = GestorProductos()
        gestor_productos.mainloop()

    def gestionar_servicios(self):
        """Abre la ventana para gestionar servicios"""
        gestor_servicios = GestorServicios()
        gestor_servicios.mainloop()

    def mostrar_grafica_ventas(self):
        # Ventana para seleccionar agrupación
        ventana = tk.Toplevel(self)
        ventana.title("Selecciona agrupación")
        ventana.geometry("300x120")
        tk.Label(ventana, text="Ver ventas por:").pack(pady=10)
        opciones = ["Día", "Mes", "Año"]
        seleccion = tk.StringVar(value="Día")
        combo = ttk.Combobox(ventana, values=opciones, textvariable=seleccion, state="readonly")
        combo.pack(pady=5)

        def graficar():
            agrupacion = seleccion.get()
            try:
                datos = self.venta_dao.obtener_ventas_agrupadas(agrupacion)
                if agrupacion == "Día":
                    etiquetas = [datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%d/%m/%Y") for row in datos]
                elif agrupacion == "Mes":
                    etiquetas = [datetime.datetime.strptime(row[0], "%Y-%m").strftime("%m/%Y") for row in datos]
                else:  # Año
                    etiquetas = [row[0] for row in datos]
                totales = [row[1] for row in datos]
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar la gráfica: {e}")
                return

            if not datos:
                messagebox.showinfo("Sin datos", "No hay ventas registradas para graficar.")
                return

            plt.figure(figsize=(10,5))
            plt.bar(etiquetas, totales, color="#4a90e2")
            plt.xlabel(agrupacion)
            plt.ylabel("Total vendido")
            plt.title(f"Ventas por {agrupacion.lower()}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            ventana.destroy()

        tk.Button(ventana, text="Mostrar gráfica", command=graficar).pack(pady=10)

    def agregar_logo(self):
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if ruta_imagen:
            try:
                with open(ruta_imagen, "rb") as f:
                    imagen_blob = f.read()
                self.config_dao.actualizar_logo(imagen_blob)
                messagebox.showinfo("Éxito", "Logo guardado en la base de datos correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el logo: {e}")

    def mostrar_logo(self, label):
        try:
            logo = self.config_dao.obtener_logo()
            if logo:
                imagen = Image.open(io.BytesIO(logo))
                imagen = imagen.resize((300, 300))  # Ajusta el tamaño si lo deseas
                imagen_tk = ImageTk.PhotoImage(imagen)
                label.config(image=imagen_tk)
                label.image = imagen_tk  # Mantener referencia
            else:
                label.config(image='', text="Sin logo", font="sans 12 bold")
        except Exception as e:
            label.config(text="Error al cargar logo")