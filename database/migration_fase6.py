import sqlite3
import os

def run_migration():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        # Añadir usuario_id a Ventas si no existe
        cur.execute("PRAGMA table_info(Ventas)")
        columns = [col[1] for col in cur.fetchall()]
        if "usuario_id" not in columns:
            cur.execute("ALTER TABLE Ventas ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)")
            print("Columna usuario_id añadida a Ventas.")
        
        # Insertar cliente "Público General" si no existe
        cur.execute("SELECT id FROM Clientes WHERE nombre = 'Público General'")
        res = cur.fetchone()
        if not res:
            cur.execute("INSERT INTO Clientes (nombre, celular, direccion, correo) VALUES ('Público General', 'N/A', 'N/A', 'N/A')")
            print("Cliente 'Público General' insertado.")
        
        conn.commit()
        print("Migración Fase 6 completada exitosamente.")
    except Exception as e:
        print(f"Error en la migración: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
