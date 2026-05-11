import re

with open('servicios_realizados.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscamos 'def guardar_hoja(self...' hasta el final del archivo o el final del metodo
match = re.search(r'( {4}def guardar_hoja\(self,.*?)(?= {4}def |$)', content, re.DOTALL)

new_code = """    def guardar_hoja(self, entry_numero_orden, entry_fecha_entrega, entry_fecha_instalacion, entry_falla, entry_diagnostico, entry_observaciones, entry_cantidad, entry_precio, cliente, equipo, servicio, estado_pruebas, entry_imei, entry_contrasena, estados_equipo, entry_anticipo):
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
                messagebox.showerror("Error", f"Los siguientes campos son obligatorios:\\n{', '.join(campos_vacios)}")
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
                    "INSERT INTO Hojas_Servicio (numero_orden, fecha_creacion) VALUES (?, datetime('now'))",
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
"""

if match:
    new_content = content.replace(match.group(1), new_code)
    with open('servicios_realizados.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Reemplazo exitoso.")
else:
    print("No se encontro el metodo.")

