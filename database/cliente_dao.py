import sqlite3

from database.db_manager import DBManager

class ClienteDAO:
    def __init__(self):
        self.db = DBManager()

    def agregar_cliente(self, nombre, celular, correo, direccion):
        """Inserta un nuevo cliente en la base de datos."""
        query = "INSERT INTO Clientes (nombre, celular, correo, direccion) VALUES (?, ?, ?, ?)"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (nombre, celular, correo, direccion))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar el cliente: {e}")
            raise e

    def obtener_clientes(self):
        """Retorna todos los registros de la tabla Clientes."""
        query = "SELECT * FROM Clientes"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            # Fetchall on sqlite3.Row usually returns rows, but tkinter's treeview expects a tuple/list for values
            return [tuple(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al cargar los clientes: {e}")
            raise e

    def obtener_nombres_clientes(self):
        """Retorna solo los nombres de los clientes para llenar el combobox."""
        query = "SELECT nombre FROM Clientes"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row['nombre'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al cargar nombres de clientes: {e}")
            raise e

    def obtener_id_por_nombre(self, nombre):
        """Retorna el ID de un cliente dado su nombre."""
        query = "SELECT id FROM Clientes WHERE nombre = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()
            return row['id'] if row else None
        except Exception as e:
            print(f"Error al obtener ID del cliente {nombre}: {e}")
            raise e

    def actualizar_cliente(self, id_cliente, nombre, celular, correo, direccion):
        """Actualiza la información de un cliente existente."""
        query = "UPDATE Clientes SET nombre=?, celular=?, correo=?, direccion=? WHERE id=?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (nombre, celular, correo, direccion, id_cliente))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al modificar el cliente: {e}")
            raise e

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de la base de datos por su ID."""
        query = "DELETE FROM Clientes WHERE id = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id_cliente,))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al eliminar el cliente: {e}")
            raise ValueError(
                "No se puede eliminar el cliente porque tiene ventas u órdenes de servicio asociadas."
            ) from None
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")
            raise e
