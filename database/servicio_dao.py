import datetime
import sqlite3

from database.db_manager import DBManager
from database.hojas_schema import HOJAS_CREATE_IF_NOT_EXISTS, HOJAS_DATA_COLUMNS


class ServicioDAO:
    def __init__(self):
        self.db = DBManager()

    def get_all_nombres_servicios(self):
        """Retorna una lista con todos los nombres de los servicios (para el combobox)."""
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Servicio FROM Servicios_realizados")
            # Devolvemos una lista simple de strings
            return [row['Servicio'] if isinstance(row, dict) else row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener nombres de servicios: {e}")
            raise e

    def get_servicios_basico(self, filtro=None):
        """Retorna los campos básicos de los servicios, opcionalmente filtrados."""
        query = "SELECT Servicio, Precio, Image_path FROM Servicios_realizados"
        params = []
        if filtro:
            query += " WHERE Servicio LIKE ?"
            params.append(f"%{filtro}%")

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            # Retornamos como lista de tuplas para mantener compatibilidad con el código existente
            return [(row['Servicio'], row['Precio'], row['Image_path']) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al cargar los servicios: {e}")
            raise e

    def get_servicio_por_nombre(self, servicio, include_image=False):
        """Busca un servicio por su nombre exacto."""
        if include_image:
            query = "SELECT c.nombre as Cliente, s.Nombre_equipo, s.Servicio, s.Precio, s.Fecha_de_recibo, s.Estado, s.Image_path FROM Servicios_realizados s LEFT JOIN Clientes c ON s.cliente_id = c.id WHERE s.Servicio=?"
        else:
            query = "SELECT c.nombre as Cliente, s.Nombre_equipo, s.Servicio, s.Precio, s.Fecha_de_recibo, s.Estado FROM Servicios_realizados s LEFT JOIN Clientes c ON s.cliente_id = c.id WHERE s.Servicio=?"
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (servicio,))
            row = cursor.fetchone()
            if row is None:
                return None
            
            # Retornar como tupla según el modo
            if include_image:
                return (row['Cliente'], row['Nombre_equipo'], row['Servicio'], row['Precio'], row['Fecha_de_recibo'], row['Estado'], row['Image_path'])
            else:
                return (row['Cliente'], row['Nombre_equipo'], row['Servicio'], row['Precio'], row['Fecha_de_recibo'], row['Estado'])
        except Exception as e:
            print("Error al obtener los datos del artículo:", e)
            raise e

    def agregar_servicio(self, cliente_id, equipo, servicio, precio, fecha, estado, image_path):
        """Inserta un nuevo servicio en la base de datos."""
        query = "INSERT INTO Servicios_realizados(cliente_id, Nombre_equipo, Servicio, Precio, Fecha_de_recibo, Estado, Image_path) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (cliente_id, equipo, servicio, precio, fecha, estado, image_path))
            conn.commit()
            return True
        except Exception as e:
            print("Error al cargar el Servicio", e)
            raise e

    def actualizar_servicio(self, cliente_id, equipo, servicio, precio, fecha, estado, image_path, old_servicio_name):
        """Actualiza un servicio existente."""
        query = "UPDATE Servicios_realizados SET cliente_id=?, Nombre_equipo=?, Servicio=?, Precio=?, Fecha_de_recibo=?, Estado=?, Image_path=? WHERE Servicio=?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (cliente_id, equipo, servicio, precio, fecha, estado, image_path, old_servicio_name))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al editar el servicio: {e}")
            raise e

    def eliminar_servicio(self, servicio):
        """Elimina un servicio por su nombre."""
        query = "DELETE FROM Servicios_realizados WHERE Servicio = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (servicio,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar el servicio: {e}")
            raise e

    def init_hojas_servicio_table(self):
        """Asegura que la tabla de hojas de servicio exista (esquema completo; migración al inicio la alinea)."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute(HOJAS_CREATE_IF_NOT_EXISTS)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la tabla de Hojas_de_Servicio: {e}")

    def obtener_ultimo_numero_orden(self):
        """Obtiene el último número de orden generado."""
        self.init_hojas_servicio_table()
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            # Intentar con tabla que tiene id como PK
            try:
                cursor.execute("SELECT numero_orden FROM Hojas_de_Servicio ORDER BY numero_orden DESC LIMIT 1")
            except Exception:
                return "OS-0001"
            row = cursor.fetchone()
            if row and row[0]:
                val = str(row[0])
                if '-' in val:
                    ultimo_num = int(val.split('-')[1])
                else:
                    try:
                        ultimo_num = int(val)
                    except ValueError:
                        ultimo_num = 0
                return f"OS-{str(ultimo_num + 1).zfill(4)}"
            else:
                return "OS-0001"
        except Exception as e:
            print(f"Error al generar el número de orden: {e}")
            return "OS-0001"

    def obtener_nuevo_numero_orden(self):
        """Alias de obtener_ultimo_numero_orden para compatibilidad."""
        return self.obtener_ultimo_numero_orden()

    def obtener_id_servicio_realizado_por_servicio_y_cliente(self, nombre_servicio, nombre_cliente):
        """ID de la fila en Servicios_realizados; el más reciente si hubiera duplicados de nombre."""
        query = """
            SELECT s.id FROM Servicios_realizados s
            INNER JOIN Clientes c ON s.cliente_id = c.id
            WHERE s.Servicio = ? AND c.nombre = ?
            ORDER BY s.id DESC LIMIT 1
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_servicio, nombre_cliente))
            row = cursor.fetchone()
            return row["id"] if row else None
        except Exception as e:
            print(f"Error al resolver id de servicio: {e}")
            raise e

    def registrar_hoja_servicio(
        self,
        numero_orden,
        servicio_id=None,
        *,
        fecha_entrega=None,
        fecha_instalacion=None,
        falla=None,
        diagnostico=None,
        observaciones=None,
        cantidad=None,
        precio=None,
        anticipo=None,
        imei=None,
        contrasena=None,
        estados_equipo=None,
        pruebas_json=None,
        cliente_nombre=None,
        equipo_nombre=None,
        servicio_nombre=None,
        ruta_pdf=None,
    ):
        """Registra una hoja de servicio emitida con todos los campos persistidos."""
        self.init_hojas_servicio_table()
        fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "numero_orden": numero_orden,
            "fecha_creacion": fecha_creacion,
            "servicio_id": servicio_id,
            "fecha_entrega": fecha_entrega,
            "fecha_instalacion": fecha_instalacion,
            "falla": falla,
            "diagnostico": diagnostico,
            "observaciones": observaciones,
            "cantidad": cantidad,
            "precio": precio,
            "anticipo": anticipo,
            "imei": imei,
            "contrasena": contrasena,
            "estados_equipo": estados_equipo,
            "pruebas_json": pruebas_json,
            "cliente_nombre": cliente_nombre,
            "equipo_nombre": equipo_nombre,
            "servicio_nombre": servicio_nombre,
            "ruta_pdf": ruta_pdf,
        }
        cols = ", ".join(HOJAS_DATA_COLUMNS)
        ph = ", ".join(["?"] * len(HOJAS_DATA_COLUMNS))
        sql = f"INSERT INTO Hojas_de_Servicio ({cols}) VALUES ({ph})"
        values = tuple(payload[c] for c in HOJAS_DATA_COLUMNS)
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar hoja de servicio: {e}")
            raise e
