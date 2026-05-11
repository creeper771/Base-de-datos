import os
import io
import datetime
from tkinter import messagebox
from PIL import Image

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Image as RLImage
except ImportError:
    print("reportlab no está instalado. Instálalo con: pip install reportlab")

class PDFGenerator:
    """Clase encargada de la generación de documentos PDF (Facturas y Hojas de Servicio)."""
    
    @staticmethod
    def generar_factura_venta(datos_empresa, cliente, total_venta, productos_seleccionados, numero_factura):
        """Genera el PDF de la factura de venta."""
        if not datos_empresa:
            raise ValueError("No se encontraron datos de la empresa.")

        empresa_nombre, direccion, telefono, email, atiende, logo_blob = datos_empresa

        carpeta_facturas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Facturas")
        if not os.path.exists(carpeta_facturas):
            os.makedirs(carpeta_facturas)

        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        factura_path = os.path.join(carpeta_facturas, f"Factura_{numero_factura}_{fecha_actual}.pdf")
        
        c = canvas.Canvas(factura_path, pagesize=letter)

        # Prepara el logo
        if logo_blob:
            try:
                logo_image = Image.open(io.BytesIO(logo_blob))
                logo_image = logo_image.resize((100, 100))
                logo_buffer = io.BytesIO()
                logo_image.save(logo_buffer, format='PNG')
                logo_buffer.seek(0)
                logo_reader = ImageReader(logo_buffer)
                c.drawImage(logo_reader, 450, 700, width=100, height=100, mask='auto')
            except Exception as e:
                print("No se pudo cargar el logo en la factura:", e)

        # Datos de la empresa
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.darkblue)
        c.drawCentredString(300, 750, "Factura de Venta")

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 710, f"Empresa: {empresa_nombre}")

        c.setFont("Helvetica", 12)
        c.drawString(50, 690, f"Dirección: {direccion}")
        c.drawString(50, 670, f"Teléfono: {telefono}")
        c.drawString(50, 650, f"Email: {email}")
        c.drawString(50, 630, f"Atiende: {atiende}")

        c.setLineWidth(0.5)
        c.setStrokeColor(colors.gray)
        c.line(50, 620, 550, 620)

        c.setFont("Helvetica", 12)
        c.drawString(50, 600, f"Factura N°: {numero_factura}")
        c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.line(50, 560, 550, 560)
        c.drawString(50, 540, f"Cliente: {cliente}")
        c.drawString(50, 520, "Descripción de productos:")

        y_offset = 500
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y_offset, "Producto")
        c.drawString(270, y_offset, "Cantidad")
        c.drawString(370, y_offset, "Precio")
        c.drawString(470, y_offset, "Total")

        c.line(50, y_offset - 10, 550, y_offset - 10)
        y_offset -= 30
        c.setFont("Helvetica", 12)
        
        for item in productos_seleccionados:
            factura_id, cliente_nom, producto, precio, cantidad, total_cop, costo = item
            c.drawString(70, y_offset, str(producto))
            c.drawString(270, y_offset, str(cantidad))
            c.drawString(370, y_offset, "${:,.0f}".format(precio))
            c.drawString(470, y_offset, str(total_cop))
            y_offset -= 20

        c.line(50, y_offset, 550, y_offset)
        y_offset -= 20

        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(50, y_offset, f"Total a Pagar: ${total_venta:,.0f}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)

        y_offset -= 20
        c.line(50, y_offset, 550, y_offset)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(150, y_offset - 60, "Gracias por su compra!, Vuelva pronto!")

        y_offset -= 100
        c.setFont("Helvetica", 10)
        c.drawString(50, y_offset, "Este documento es una representación de la factura. Para cualquier consulta, contáctenos.")
        c.drawString(50, y_offset - 20, f"Teléfono: {telefono} | Email: {email}")
        c.drawString(50, y_offset - 40, f"Dirección: {direccion}")
        c.drawString(50, y_offset - 60, "Términos y condiciones:")
        c.drawString(50, y_offset - 80, "Los productos no tienen devolución.")
        c.drawString(50, y_offset - 100, "Conserve su factura para cualquier reclamo.")
        
        c.save()
        return factura_path

    @staticmethod
    def generar_hoja_servicio(datos_empresa, cliente, equipo, servicio, precio, falla, diagnostico, numero_orden, estado, fecha_entrega, fecha_instalacion, observaciones, cantidad, imei, contrasena, estados_equipo_lista, pruebas_data, anticipo):
        """Genera el PDF de la hoja de servicio técnico usando Platypus."""
        if not datos_empresa:
            empresa_nombre = "NOMBRE DE LA EMPRESA"
            direccion = "DIRECCIÓN"
            telefono = "TELÉFONO"
            email = "EMAIL"
            atiende = "TÉCNICO"
            logo_blob = None
        else:
            empresa_nombre, direccion, telefono, email, atiende, logo_blob = datos_empresa

        total = cantidad * precio
        resto = total - anticipo

        carpeta_hojas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hojas_de_servicio")
        if not os.path.exists(carpeta_hojas):
            os.makedirs(carpeta_hojas)

        nombre_archivo = os.path.join(carpeta_hojas, f"Hoja_Servicio_{numero_orden}.pdf")
        
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elementos = []
        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle('CustomTitle', parent=estilos['Title'], fontSize=16, spaceAfter=30, alignment=1)
        estilo_normal = estilos['Normal']

        # Prepara el logo
        logo_flowable = None
        if logo_blob:
            try:
                logo_image = Image.open(io.BytesIO(logo_blob))
                logo_image = logo_image.resize((80, 80))
                logo_buffer = io.BytesIO()
                logo_image.save(logo_buffer, format='PNG')
                logo_buffer.seek(0)
                logo_flowable = RLImage(logo_buffer, width=80, height=80)
            except Exception as e:
                print("No se pudo cargar el logo en la hoja de servicio:", e)

        datos_empresa_formato = [
            Paragraph(f"<b>{empresa_nombre}</b>", estilo_normal),
            Paragraph(f"Dirección: {direccion}", estilo_normal),
            Paragraph(f"Teléfono: {telefono}", estilo_normal),
            Paragraph(f"Email: {email}", estilo_normal)
        ]

        if logo_flowable:
            tabla_encabezado = Table([[logo_flowable, datos_empresa_formato]], colWidths=[100, 400])
        else:
            tabla_encabezado = Table([["", datos_empresa_formato]], colWidths=[100, 400])
        
        tabla_encabezado.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(tabla_encabezado)
        elementos.append(Spacer(1, 20))

        elementos.append(Paragraph(f"<b>HOJA DE SERVICIO - ORDEN {numero_orden}</b>", estilo_titulo))

        datos_cliente = [
            ['Cliente:', cliente, 'Equipo:', equipo],
            ['Servicio:', servicio, 'Estado Pruebas:', estado],
            ['IMEI:', imei, 'Contraseña:', contrasena]
        ]
        
        tabla_cliente = Table(datos_cliente, colWidths=[100, 170, 100, 170])
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 20))

        datos_fechas = [
            ['Fecha Recepción:', datetime.datetime.now().strftime("%Y-%m-%d"), 'Fecha Entrega:', fecha_entrega],
            ['Fecha Instalación:', fecha_instalacion, '', '']
        ]
        
        tabla_fechas = Table(datos_fechas, colWidths=[100, 170, 100, 170])
        tabla_fechas.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(tabla_fechas)
        elementos.append(Spacer(1, 20))

        if estados_equipo_lista:
            elementos.append(Paragraph("<b>Condiciones de Recepción del Equipo:</b>", estilo_normal))
            elementos.append(Spacer(1, 10))
            
            items_por_fila = 3
            datos_estados = []
            fila_actual = []
            
            for estado_eq in estados_equipo_lista:
                estado_texto = f"[X] {estado_eq}"
                fila_actual.append(estado_texto)
                
                if len(fila_actual) == items_por_fila:
                    datos_estados.append(fila_actual)
                    fila_actual = []
            
            if fila_actual:
                while len(fila_actual) < items_por_fila:
                    fila_actual.append("")
                datos_estados.append(fila_actual)
            
            if datos_estados:
                tabla_estados = Table(datos_estados, colWidths=[180, 180, 180])
                tabla_estados.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elementos.append(tabla_estados)
                elementos.append(Spacer(1, 20))

        elementos.append(Paragraph("<b>Detalles del Servicio:</b>", estilo_normal))
        elementos.append(Spacer(1, 10))
        
        datos_detalles = [
            ['Falla Reportada:', Paragraph(falla, estilo_normal)],
            ['Diagnóstico:', Paragraph(diagnostico, estilo_normal)],
            ['Observaciones:', Paragraph(observaciones, estilo_normal)]
        ]
        
        tabla_detalles = Table(datos_detalles, colWidths=[100, 440])
        tabla_detalles.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(tabla_detalles)
        elementos.append(Spacer(1, 20))

        if pruebas_data:
            datos_pruebas = [
                ['PRUEBAS DE FUNCIONAMIENTO', '', '', '', '', ''],
                ['Prueba', 'Ingreso', 'Egreso', 'Prueba', 'Ingreso', 'Egreso'],
            ]
            
            n = len(pruebas_data)
            i = 0
            while i < n:
                fila = []
                # Primera prueba del par
                prueba1 = pruebas_data[i]
                fila.extend([prueba1['nombre'], prueba1['ingreso'], prueba1['egreso']])
                # Segunda prueba del par (si existe)
                if i + 1 < n:
                    prueba2 = pruebas_data[i + 1]
                    fila.extend([prueba2['nombre'], prueba2['ingreso'], prueba2['egreso']])
                else:
                    fila.extend(['', '', ''])
                datos_pruebas.append(fila)
                i += 2

            tabla_pruebas = Table(datos_pruebas, colWidths=[120, 45, 45, 120, 45, 45])
            tabla_pruebas.setStyle(TableStyle([
                ('SPAN', (0, 0), (5, 0)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 2), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('BACKGROUND', (0, 0), (5, 0), colors.lightgrey),
                ('BACKGROUND', (0, 1), (5, 1), colors.lightgrey),
                ('FONTNAME', (0, 0), (5, 1), 'Helvetica-Bold'),
            ]))
            elementos.append(tabla_pruebas)
            elementos.append(Spacer(1, 20))

        datos_costos = [
            ['Cantidad:', str(cantidad), 'Precio Unitario:', f"${precio:,.0f}"],
            ['Anticipo:', f"${anticipo:,.0f}", 'Total a Pagar:', f"${total:,.0f}"],
            ['Restante:', f"${resto:,.0f}", '', '']
        ]
        
        tabla_costos = Table(datos_costos, colWidths=[100, 170, 100, 170])
        tabla_costos.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(tabla_costos)
        elementos.append(Spacer(1, 40))

        datos_firmas = [
            ['_______________________', '_______________________'],
            ['Firma del Cliente', 'Firma del Técnico']
        ]
        
        tabla_firmas = Table(datos_firmas, colWidths=[270, 270])
        tabla_firmas.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ]))
        elementos.append(tabla_firmas)
        elementos.append(Spacer(1, 20))
        
        terminos = [
            "Términos y Condiciones:",
            "1. Todo equipo reparado cuenta con 30 días de garantía sobre la reparación efectuada.",
            "2. La garantía no cubre daños por humedad, golpes, sobrecargas eléctricas o mal uso.",
            "3. Pasados 30 días de la notificación de reparación, el equipo causará recargos por almacenaje.",
            "4. Después de 60 días, la empresa no se hace responsable por el equipo."
        ]
        
        for termino in terminos:
            elementos.append(Paragraph(f"<font size=8>{termino}</font>", estilo_normal))
        
        doc.build(elementos)
        return nombre_archivo
