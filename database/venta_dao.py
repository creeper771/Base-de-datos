from database.db_manager import DBManager

class VentaDAO:
    def __init__(self):
        self.db = DBManager()

    def obtener_ultimo_numero_factura(self):
        query = "SELECT MAX(factura) as max_factura FROM Ventas"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            last = row['max_factura'] if row and row['max_factura'] is not None else 0
            return last + 1
        except Exception as e:
            print(f"Error obteniendo numero de factura: {e}")
            return 1

    def registrar_venta(self, factura, cliente_id, producto_id, precio, cantidad, total, costo, fecha, hora, usuario_id=None):
        query = "INSERT INTO Ventas(factura, cliente_id, producto_id, precio, cantidad, total, costo, fecha, hora, usuario_id) VALUES (?,?,?,?,?,?,?,?,?,?)"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (factura, cliente_id, producto_id, precio, cantidad, total, costo, fecha, hora, usuario_id))
            # OJO: El commit no se hace aquí si se quiere mantener una transacción atómica para múltiples artículos. 
            # Pero para seguir con la lógica del proyecto original:
            conn.commit()
            return True
        except Exception as e:
            print(f"Error registrando venta: {e}")
            raise e

    def obtener_todas_ventas(self):
        query = """
            SELECT v.factura, c.nombre as cliente, i.producto as articulo, v.precio, v.cantidad, v.total, v.fecha, v.hora, v.costo
            FROM Ventas v
            LEFT JOIN Clientes c ON v.cliente_id = c.id
            LEFT JOIN Inventario i ON v.producto_id = i.id
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return [tuple(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error cargando ventas: {e}")
            raise e

    def obtener_ventas_agrupadas(self, agrupacion):
        """Retorna datos agrupados para gráficas (Día, Mes, Año)."""
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            if agrupacion == "Día":
                cursor.execute("SELECT fecha as etiqueta, SUM(total) as suma FROM Ventas GROUP BY fecha")
            elif agrupacion == "Mes":
                cursor.execute("SELECT substr(fecha,1,7) as etiqueta, SUM(total) as suma FROM Ventas GROUP BY etiqueta")
            else:  # Año
                cursor.execute("SELECT substr(fecha,1,4) as etiqueta, SUM(total) as suma FROM Ventas GROUP BY etiqueta")
            
            return [(row['etiqueta'], row['suma']) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error cargando agrupación de ventas: {e}")
            raise e
