from tkinter import *
from utils.paths import get_resource_path
from database.venta_dao import VentaDAO
from database.cliente_dao import ClienteDAO
from database.inventario_dao import InventarioDAO
from database.config_dao import ConfigDAO
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import datetime
import threading
from utils.pdf_generator import PDFGenerator
import sys
import os
from PIL import Image, ImageTk
import openpyxl
import pandas as pd
from tkcalendar import DateEntry




class Ventas_productos(tk.Frame):

    db_name= "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.venta_dao = VentaDAO()
        self.cliente_dao = ClienteDAO()
        self.inventario_dao = InventarioDAO()
        self.config_dao = ConfigDAO()
        self.numero_factura= self.obtener_numero_factura_act()
        self.productos_seleccionados= []
        self.empresa_nombre = ""  # Inicializar con valores vacíos
        self.direccion = ""
        self.telefono = ""
        self.email = ""
        self.atiende = ""
        self.widgets()
        self.cargar_productos()
        self.cargar_clientes()
        self.timer_producto = None
        self.timer_cliente = None

    def obtener_numero_factura_act(self):
        return self.venta_dao.obtener_ultimo_numero_factura()
        
    def cargar_clientes(self):
        try:
            self.clientes = self.cliente_dao.obtener_nombres_clientes()
            self.entry_cliente["values"] = self.clientes
        except Exception as e:
            print("Error cargando clientes: ", e)

    def filtrar_clientes(self, event):
        if self.timer_cliente:
            self.timer_cliente.cancel()
        self.timer_cliente = threading.Timer(0.5, self._filter_clients)
        self.timer_cliente.start()

    def _filter_clients(self):
        typed = self.entry_cliente.get()

        if typed == '':
            data = self.clientes
        else:
            data = [item for item in self.clientes if typed.lower() in item.lower()]

        if data:
            self.entry_cliente['values'] = data
            self.entry_cliente.event_generate('<Down>')
        else:
            self.entry_cliente['values'] = ['No se encontraron resultados']
            self.entry_cliente.event_generate('<Down>')
            self.entry_cliente.delete(0, tk.END)
    
    def cargar_productos(self):
        try:
            self.products = self.inventario_dao.get_all_nombres_productos()
            self.entry_producto["values"] = self.products
        except Exception as e:
            print("Error cargando productos: ", e)

    def filtrar_productos(self, event):
        if hasattr(self, 'timer_producto') and self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()

    def _filter_products(self):
        typed = self.entry_producto.get().strip()  # Eliminamos espacios innecesarios

        if not typed:  # Si está vacío, mostramos todos los productos
            data = self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]

        if data:
            self.entry_producto['values'] = data
            self.entry_producto.event_generate('<Down>')  # Simula la apertura de la lista
        else:
            self.entry_producto['values'] = ['No se encontraron resultados']
            self.entry_producto.event_generate('<Down>')
            self.entry_producto.delete(0, tk.END)  # Borra el texto solo si no hay resultados

    def agregar_productos(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()

        if not cliente:
            cliente = "Público General"
            self.entry_cliente.set(cliente)

        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")
            return  # Detener ejecución en caso de error

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return  # Detener ejecución en caso de error

        cantidad = int(cantidad)

        try:
            resultado = self.inventario_dao.get_producto_por_nombre(producto)

            if resultado is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return  # Evitar seguir si el producto no existe

            precio = resultado[2]
            costo = resultado[1]
            stock = resultado[3]

            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                return  # Evitar seguir si hay stock insuficiente

            total = precio * cantidad
            total_cop = "{:,.0f}".format(total)

            self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, "{:,.0f}".format(precio), cantidad, total_cop))
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total_cop, costo))

            self.entry_producto.set("")
            self.entry_cantidad.delete(0, 'end')

        except Exception as e:
            print("Error al agregar el producto:", e)

        self.calcular_precio_total()

    def calcular_precio_total(self):
        total_pagar= sum(float(str(self.tre.item(item)["values"][-1]).replace(" ", "").replace(",", "")) for item in self.tre.get_children())
        total_pagar_cop= "{:,.0f}".format(total_pagar) 
        self.label_precio_total.config(text=f"Precio a Pagar: $ {total_pagar_cop}")

    def actualizar_stock(self, event=None):
        producto_seleccionado = self.entry_producto.get()

        try:
            resultado = self.inventario_dao.get_producto_por_nombre(producto_seleccionado)
            stock = resultado[3] if resultado else 0
            self.label_stock.config(text=f"Stock: {stock}")

        except Exception as e:
            print("Error al obtener el stock del producto: ", e)

    def realizar_pago(self):
        if not self.tre.get_children():
            messagebox.showerror("Error","No hay productos seleccionados para realizar el pago.")

        total_venta = sum(float(item[5].replace(" ","").replace(",","")) for item in self.productos_seleccionados)
        total_formateado = "{:,.0f}".format(total_venta)

        ventana_pago= tk.Toplevel(self) 
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg= "#85c1e9")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()

        label_titulo= tk.Label(ventana_pago, text="Realizar pago", font= "sans 30 bold", bg= "#85c1e9")
        label_titulo.place(x=70, y=10)

        label_total= tk.Label(ventana_pago, text=f"Total a pagar ${total_formateado}", font= "sans 14 bold", bg= "#85c1e9")
        label_total.place(x=80, y=100)

        label_monto= tk.Label(ventana_pago, text="Ingrese el monto pagado", font= "sans 14 bold", bg= "#85c1e9")
        label_monto.place(x=80, y=160)

        entry_monto =ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        button_confirmar_pago= tk.Button(ventana_pago, text="Confirmar pago", font="sans 14 bold", command= lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta))
        button_confirmar_pago.place(x=80, y=270, width=240, height=40)

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
            cantidad_pagada= float(cantidad_pagada)
            cliente= self.entry_cliente.get()

            if cantidad_pagada < total_venta:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
                return
            
            cambio = cantidad_pagada - total_venta
            total_formateado= "{:,.0f}".format(total_venta)

            mensaje= f"Total: {total_formateado} \nCantidad pagada: {cantidad_pagada:,.0f} \nCambio: {cambio:,.0f}"
            messagebox.showinfo("Pago realizado", mensaje)

            try:
                fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
                hora_actual= datetime.datetime.now().strftime("%H:%M:%S")

                for item in self.productos_seleccionados:
                    factura, cliente, producto, precio, cantidad, total, costo = item

                    cliente_id = self.cliente_dao.obtener_id_por_nombre(cliente)
                    producto_id = self.inventario_dao.obtener_id_por_nombre(producto)
                    
                    try:
                        usuario_id = self.master.controlador.usuario_activo_id
                    except AttributeError:
                        usuario_id = None

                    self.venta_dao.registrar_venta(
                        factura, cliente_id, producto_id, precio, cantidad, 
                        total.replace(" ", "").replace(",", ""), 
                        costo * cantidad, fecha_actual, hora_actual, usuario_id
                    )
                    self.inventario_dao.restar_stock(producto, cantidad)

                self.generar_factura_pdf(total_venta, cliente)

            except Exception as e:
                 messagebox.showerror("Error", f"Error al registrar la venta: {e}")

            self.numero_factura += 1
            self.label_numero_factura.config(text= str(self.numero_factura))

            self.productos_seleccionados = []
            self.limpiar_campos()

            ventana_pago.destroy()
    
    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a pagar: $ 0")

        self.entry_producto.set('')
        self.entry_cantidad.delete(0, 'end')

    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        self.calcular_precio_total()

    def eliminar_producto(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "Por favor seleccione un producto para eliminar.")
            return
        
        item_id= item_seleccionado[0]
        valores_item=self.tre.item(item_id)["values"]
        factura, cliente, producto, precio, cantidad, total= valores_item

        self.tre.delete(item_id)

        self.productos_seleccionados=[producto for producto in self.productos_seleccionados if producto[2] != producto]

        self.calcular_precio_total()

    def editar_producto(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un producto para editar.")
            return
        
        item_values = self.tre.item(selected_item[0],'values')
        if not item_values:
            messagebox.showerror("Error", "No se encontraron valores para editar.")
            return
        
        current_product = item_values[2]
        current_cantidad = item_values[4]

        new_cantidad = simpledialog.askinteger("Editar cantidad", f"Ingrese la nueva cantidad para {current_product}:", initialvalue=current_cantidad)

        if new_cantidad is not None:
            try:
                resultado = self.inventario_dao.get_producto_por_nombre(current_product)

                if resultado is None:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return
                    
                precio = resultado[2]
                costo = resultado[1]
                stock = resultado[3]

                if new_cantidad > stock:
                    messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                    return
                
                total= precio * new_cantidad
                total_cop= "{:,.0f}".format(total)

                self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cliente.get(), current_product, "{:,.0f}".format(precio), new_cantidad, total_cop))

                for idx, producto in enumerate(self.productos_seleccionados):
                    if producto[2] == current_product:
                        self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), current_product, precio, new_cantidad, total_cop, costo)
                        break

                self.calcular_precio_total()
            except Exception as e:
                messagebox.showerror("Error al editar el producto: ", e)
        
    def ver_ventas_realizadas(self):
        try:
            ventas = self.venta_dao.obtener_todas_ventas()

            ventana_ventas= tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x700+120+20")
            ventana_ventas.config(bg="#85c1e9")
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()

            def filtrar_ventas():
                factura_a_buscar= entry_factura.get().strip()
                cliente_a_buscar= entry_cliente_filtro.get().strip()
                producto_a_buscar = entry_producto_filtro.get().strip()
                fecha_a_buscar = entry_fecha_filtro.get().strip()
                
                for item in tree.get_children():
                    tree.delete(item)

                ventas_filtradas= []
                for venta in ventas:
                    match_factura = str(venta[0]) == factura_a_buscar if factura_a_buscar else True
                    match_cliente = cliente_a_buscar.lower() in str(venta[1]).lower() if cliente_a_buscar else True
                    match_producto = producto_a_buscar.lower() in str(venta[2]).lower() if producto_a_buscar else True
                    
                    try:
                        fecha_str = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d/%m/%Y")
                    except Exception:
                        fecha_str = str(venta[6])
                        
                    match_fecha = fecha_a_buscar in str(venta[6]) or fecha_a_buscar in fecha_str if fecha_a_buscar else True
                    
                    if match_factura and match_cliente and match_producto and match_fecha:
                        ventas_filtradas.append(venta)

                for venta in ventas_filtradas:
                    venta= list(venta)
                    venta[3]= "{:,.0f}".format(venta[3])
                    venta[5]= "{:,.0f}".format(venta[5])
                    venta[6]= datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d/%m/%Y")
                    tree.insert("", "end", values=venta)

            label_ventas_realizadas= tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 28 bold", bg="#85c1e9")
            label_ventas_realizadas.place(x=350, y=20)

            filro_frame = tk.LabelFrame(ventana_ventas, bg="#85c1e9")
            filro_frame.place(x=20, y=60, width=1060, height=120)

            label_factura= tk.Label(filro_frame, text="Numero de factura", font="sans 14 bold", bg="#85c1e9")
            label_factura.place(x=10, y=15)
            entry_factura= ttk.Entry(filro_frame, font="sans 14 bold")
            entry_factura.place(x=200, y=10, width=200, height=40)

            label_cliente= tk.Label(filro_frame, text="Cliente", font="sans 14 bold", bg="#85c1e9")
            label_cliente.place(x=420, y=15)
            entry_cliente_filtro= ttk.Entry(filro_frame, font="sans 14 bold")
            entry_cliente_filtro.place(x=620, y=10, width=200, height=40)

            label_producto = tk.Label(filro_frame, text="Producto", font="sans 14 bold", bg="#85c1e9")
            label_producto.place(x=10, y=65)
            entry_producto_filtro = ttk.Entry(filro_frame, font="sans 14 bold")
            entry_producto_filtro.place(x=200, y=60, width=200, height=40)

            label_fecha = tk.Label(filro_frame, text="Fecha", font="sans 14 bold", bg="#85c1e9")
            label_fecha.place(x=420, y=65)
            entry_fecha_filtro = DateEntry(filro_frame, font="sans 14 bold", background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            entry_fecha_filtro.place(x=620, y=60, width=200, height=40)
            entry_fecha_filtro.delete(0, 'end') # Dejarlo vacío para no filtrar por defecto

            #Agregar icono a los botones FILTRAR
            ruta= get_resource_path(r"Iconos/filtrar.png")
            imagen_pil_filtrar = Image.open(ruta)
            imagen_resize_filtrar = imagen_pil_filtrar.resize((30, 30))
            imagen_tk_filtrar = ImageTk.PhotoImage(imagen_resize_filtrar)
            btn_filtar = tk.Button(filro_frame, text="Filtrar", font="sans 14 bold", command=filtrar_ventas)
            btn_filtar.config(image=imagen_tk_filtrar, compound=LEFT, padx=5)
            btn_filtar.image = imagen_tk_filtrar  # Mantener referencia
            btn_filtar.place(x=840, y=35, width=200, height=50)

            #Agregar icono a los botones EXPORTAR
            ruta= get_resource_path(r"Iconos/excel.png")
            imagen_pil_exportar = Image.open(ruta)
            imagen_resize_exportar = imagen_pil_exportar.resize((30, 30))
            imagen_tk_exportar = ImageTk.PhotoImage(imagen_resize_exportar)
            btn_exportar = tk.Button(ventana_ventas, text="Exportar a Excel", font="sans 14 bold", command=self.exportar_treeview_excel)
            btn_exportar.config(image=imagen_tk_exportar, compound=LEFT, padx=5)
            btn_exportar.image = imagen_tk_exportar  # Mantener referencia
            btn_exportar.place(x=20, y=640, width=200, height=40)

            tree_frame= tk.Frame(ventana_ventas, bg="white")
            tree_frame.place(x=20, y=190, width=1060, height=440)

            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)

            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            tree= ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"), show="headings")
            tree.pack(expand=True, fill=BOTH)

            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)

            tree.heading("Factura", text="Factura")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Producto", text="Producto")
            tree.heading("Precio", text="Precio")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            tree.column("Factura", width=60, anchor="center")
            tree.column("Cliente", width=120, anchor="center")
            tree.column("Producto", width=120, anchor="center")
            tree.column("Precio", width=80, anchor="center")
            tree.column("Cantidad", width=80, anchor="center")
            tree.column("Total", width=80, anchor="center")
            tree.column("Fecha", width=80, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            for venta in ventas:
                venta= list(venta)
                venta[3]= "{:,.0f}".format(venta[3])
                venta[5]= "{:,.0f}".format(venta[5])
                venta[6]= datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d/%m/%Y")
                tree.insert("", "end", values=venta)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las ventas: {e}")

    def generar_factura_pdf(self, total_venta, cliente):
        try:
            # Obtener los datos de la empresa desde la base de datos
            datos_empresa = self.config_dao.obtener_info_completa()

            if not datos_empresa:
                messagebox.showerror("Error", "No se encontraron datos de la empresa en la base de datos.")
                return

            factura_path = PDFGenerator.generar_factura_venta(
                datos_empresa=datos_empresa,
                cliente=cliente,
                total_venta=total_venta,
                productos_seleccionados=self.productos_seleccionados,
                numero_factura=self.numero_factura
            )
            
            messagebox.showinfo("Éxito", f"Factura generada correctamente en {factura_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la factura: {e}")

    def exportar_treeview_excel(self):

        # Crear la carpeta si no existe
        carpeta_destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Excel_Ventas")
        os.makedirs(carpeta_destino, exist_ok=True)

        # Nombre del archivo
        archivo = os.path.join(carpeta_destino, "Ventas.xlsx")

        try:
            conn = self.venta_dao.db.get_connection()
            df = pd.read_sql_query("SELECT * FROM Ventas", conn)
            df.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")
        
    def widgets(self):
        labelframe = tk.LabelFrame(self, font= "sans 12 bold", bg="#85c1e9")
        labelframe.place(x=25, y=30, width=1045, height=180)

        label_cliente= tk.Label(labelframe, text="Cliente", font="sans 14 bold", bg="#85c1e9")
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        self.entry_cliente.bind('<KeyRelease>', self.filtrar_clientes)

        label_producto= tk.Label(labelframe, text="Producto", font="sans 14 bold", bg="#85c1e9")
        label_producto.place(x=10, y=70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_producto.place(x=120, y=66, width=260, height=40)
        self.entry_producto.bind('<KeyRelease>', self.filtrar_productos)

        label_cantidad= tk.Label(labelframe, text="Cantidad", font="sans 14 bold", bg="#85c1e9")
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad= ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)

        self.label_stock= label_cantidad= tk.Label(labelframe, text="Stock", font="sans 14 bold", bg="#85c1e9")
        self.label_stock.place(x=500, y=70)
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)

        label_factura = tk.Label(labelframe, text="Numero de factura:", font="sans 14 bold", bg="#85c1e9" )
        label_factura.place(x=750, y=11)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#85c1e9")
        self.label_numero_factura.place(x=950, y=11)

        # Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/agregar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_agregar= tk.Button(labelframe, text="Agregar producto", font="sans 14 bold", command= self.agregar_productos)
        boton_agregar.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_agregar.image= imagen_tk
        boton_agregar.place(x=60, y=120, width=210, height=40)

        # Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/eliminar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_eliminar= tk.Button(labelframe, text="Eliminar producto", font="sans 14 bold", command= self.eliminar_producto)
        boton_eliminar.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_eliminar.image= imagen_tk
        boton_eliminar.place(x=290, y=120, width=220, height=40)

        # Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/editar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_editar= tk.Button(labelframe, text="Editar producto", font="sans 14 bold", command= self.editar_producto)
        boton_editar.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_editar.image= imagen_tk
        boton_editar.place(x=530, y=120, width=200, height=40)

        # Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/limpiar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_limpiar= tk.Button(labelframe, text="Limpiar Lista", font="sans 14 bold", command= self.limpiar_lista)
        boton_limpiar.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_limpiar.image= imagen_tk
        boton_limpiar.place(x=750, y=120, width=200, height=40)

        treframe =tk.Frame(self, bg="white")
        treframe.place(x=60, y=220, width=980, height=300)

        scroll_y= ttk.Scrollbar(treframe)
        scroll_y.pack(side= RIGHT, fill=Y)

        scroll_x= ttk.Scrollbar(treframe, orient=HORIZONTAL)
        scroll_x.pack(side= BOTTOM, fill=X)

        self.tre = ttk.Treeview(treframe, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=40, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad","Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scroll_y.config(command=self.tre.yview)
        scroll_y.config(command=self.tre.xview)

        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura",width=70, anchor="center")
        self.tre.column("Cliente",width=250, anchor="center")
        self.tre.column("Producto",width=250, anchor="center")
        self.tre.column("Precio",width=120, anchor="center")
        self.tre.column("Cantidad",width=120, anchor="center")
        self.tre.column("Total",width=150, anchor="center")

        self.label_precio_total= tk.Label(self, text="Precio a Pagar: $", font="sans 18 bold",bg="#85c1e9")
        self.label_precio_total.place(x=680, y=550)

        # Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/pagar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold", command= self.realizar_pago)
        boton_pagar.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_pagar.image= imagen_tk
        boton_pagar.place(x=70, y=550, width=180, height=40)

        #Agregar icono a los botones
        ruta= get_resource_path(r"Iconos/limpiar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        boton_ver_ventas = tk.Button(self, text="Ver Ventas Realizadas", font="sans 14 bold", command= self.ver_ventas_realizadas)
        boton_ver_ventas.config(image= imagen_tk, compound= LEFT, padx= 5)
        boton_ver_ventas.image= imagen_tk
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)

    

    