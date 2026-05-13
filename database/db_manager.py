import sqlite3
import os


def configure_sqlite_connection(conn):
    """Activa integridad referencial en SQLite (debe ejecutarse por conexión)."""
    conn.execute("PRAGMA foreign_keys = ON")


class DBManager:
    _instance = None
    _connection = None

    def __new__(cls, db_path="database.db"):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.db_path = db_path
        return cls._instance

    def get_connection(self):
        """Devuelve la conexión a la base de datos (se crea si no existe o se reconecta si está cerrada)."""
        if self._connection is None:
            self._connect()
        return self._connection

    def _connect(self):
        try:
            self._connection = sqlite3.connect(self.db_path)
            # Para poder acceder a las columnas por nombre en lugar de índice
            self._connection.row_factory = sqlite3.Row
            configure_sqlite_connection(self._connection)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def close(self):
        """Cierra la conexión a la base de datos si está abierta."""
        if self._connection:
            self._connection.close()
            self._connection = None
