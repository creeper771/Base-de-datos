from database.db_manager import DBManager

class UserDAO:
    def __init__(self):
        self.db = DBManager()

    def verify_user(self, username, password):
        """Verifica si las credenciales coinciden con un usuario existente y devuelve su información."""
        consulta = "SELECT id, username FROM usuarios WHERE username= ? AND password= ?"
        parametros = (username, password)
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            result = cursor.fetchone()
            if result:
                return {"id": result[0], "username": result[1]}
            return None
        except Exception as e:
            print(f"Error al verificar usuario: {e}")
            raise e

    def register_user(self, username, password):
        """Registra un nuevo usuario en la base de datos."""
        consulta = "INSERT INTO usuarios VALUES (?,?,?)"
        parametros = (None, username, password)
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            raise e
