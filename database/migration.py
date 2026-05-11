import sqlite3
import os

def migrate_database(db_path):
    print("Iniciando migración de base de datos...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Deshabilitar soporte para llaves foráneas en SQLite durante la migración
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Limpiar posibles tablas residuales de intentos fallidos
        cursor.execute("DROP TABLE IF EXISTS Servicios_realizados_new")
        cursor.execute("DROP TABLE IF EXISTS Ventas_new")

        # --- MIGRACIÓN DE Servicios_realizados ---
        print("Migrando Servicios_realizados...")
        cursor.execute("""
            CREATE TABLE Servicios_realizados_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                Nombre_equipo TEXT,
                Servicio TEXT,
                Precio REAL,
                Fecha_de_recibo TEXT,
                Estado TEXT,
                Image_path TEXT,
                FOREIGN KEY(cliente_id) REFERENCES Clientes(id)
            )
        """)

        # Copiar datos mapeando el nombre del cliente a su id
        cursor.execute("""
            INSERT INTO Servicios_realizados_new (id, cliente_id, Nombre_equipo, Servicio, Precio, Fecha_de_recibo, Estado, Image_path)
            SELECT sr.Id,
                   (SELECT c.id FROM Clientes c WHERE c.nombre = sr.Cliente),
                   sr.Nombre_equipo,
                   sr.Servicio,
                   sr.Precio,
                   sr.Fecha_de_recibo,
                   sr.Estado,
                   sr.Image_path
            FROM Servicios_realizados sr
        """)

        # Reemplazar tabla antigua por la nueva
        cursor.execute("DROP TABLE Servicios_realizados")
        cursor.execute("ALTER TABLE Servicios_realizados_new RENAME TO Servicios_realizados")

        # --- MIGRACIÓN DE Ventas ---
        print("Migrando Ventas...")
        cursor.execute("""
            CREATE TABLE Ventas_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura INTEGER,
                cliente_id INTEGER,
                producto_id INTEGER,
                precio REAL,
                cantidad INTEGER,
                total REAL,
                fecha TEXT,
                hora TEXT,
                costo REAL,
                FOREIGN KEY(cliente_id) REFERENCES Clientes(id),
                FOREIGN KEY(producto_id) REFERENCES Inventario(id)
            )
        """)

        # Copiar datos mapeando cliente y articulo a sus respectivos IDs
        cursor.execute("""
            INSERT INTO Ventas_new (factura, cliente_id, producto_id, precio, cantidad, total, fecha, hora, costo)
            SELECT v.factura,
                   (SELECT c.id FROM Clientes c WHERE c.nombre = v.cliente),
                   (SELECT i.id FROM Inventario i WHERE i.producto = v.articulo),
                   v.precio, v.cantidad, v.total, v.fecha, v.hora, v.costo
            FROM Ventas v
        """)

        cursor.execute("DROP TABLE Ventas")
        cursor.execute("ALTER TABLE Ventas_new RENAME TO Ventas")

        # Confirmar los cambios
        conn.commit()
        print("Migración completada con éxito.")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error durante la migración: {e}")
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    # Ejecutar la migración
    db_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    migrate_database(db_file)
