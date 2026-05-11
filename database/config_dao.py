from database.db_manager import DBManager

class ConfigDAO:
    def __init__(self):
        self.db = DBManager()

    def obtener_informacion(self):
        query = "SELECT nombre, direccion, telefono, email, atiende FROM Informacion LIMIT 1"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return tuple(row) if row else None
        except Exception as e:
            print(f"Error al obtener configuración de empresa: {e}")
            raise e

    def guardar_informacion(self, nombre, direccion, telefono, email, atiende):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM Informacion")
            count = cursor.fetchone()['count']
            
            if count > 0:
                cursor.execute("""
                    UPDATE Informacion
                    SET nombre = ?, direccion = ?, telefono = ?, email = ?, atiende = ?
                """, (nombre, direccion, telefono, email, atiende))
            else:
                cursor.execute("""
                    INSERT INTO Informacion (nombre, direccion, telefono, email, atiende)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, direccion, telefono, email, atiende))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar configuración de empresa: {e}")
            raise e

    def actualizar_logo(self, imagen_blob):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Informacion SET logo = ? WHERE id = 1", (imagen_blob,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar logo: {e}")
            raise e
            
    def obtener_logo(self):
        query = "SELECT logo FROM Informacion LIMIT 1"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return row['logo'] if row else None
        except Exception as e:
            print(f"Error al obtener logo: {e}")
            raise e

    def obtener_info_completa(self):
        """Retorna todos los campos incluyendo el logo, útil para facturas."""
        query = "SELECT nombre, direccion, telefono, email, atiende, logo FROM Informacion LIMIT 1"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return tuple(row) if row else None
        except Exception as e:
            print(f"Error al obtener info completa: {e}")
            raise e
