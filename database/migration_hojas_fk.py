import sqlite3

from database.hojas_schema import HOJAS_CREATE_SQL, HOJAS_DATA_COLUMNS


def _drop_stray_hojas_tables(cur):
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name GLOB 'Hojas_de_Servicio*'"
    )
    for (name,) in cur.fetchall():
        if name != "Hojas_de_Servicio":
            cur.execute(f'DROP TABLE IF EXISTS "{name}"')


def _schema_ok(cur):
    cur.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='Hojas_de_Servicio'"
    )
    row = cur.fetchone()
    if not row or not row[0]:
        return False
    sql = row[0]
    if "REFERENCES Servicios_realizados" not in sql:
        return False
    cur.execute("PRAGMA table_info(Hojas_de_Servicio)")
    have = {r[1] for r in cur.fetchall()}
    need = set(HOJAS_DATA_COLUMNS) | {"id"}
    return need.issubset(have)


def migrate_hojas_de_servicio_fk(db_path):
    """
    Deja una sola tabla Hojas_de_Servicio con todas las columnas de negocio y FK.
    Elimina tablas residuales (p. ej. Hojas_de_Servicio__new) y migra datos antiguos.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA foreign_keys=OFF")
        _drop_stray_hojas_tables(cur)

        if _schema_ok(cur):
            conn.commit()
            return

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Hojas_de_Servicio'"
        )
        had_main = cur.fetchone() is not None
        old_cols = set()
        if had_main:
            cur.execute("PRAGMA table_info(Hojas_de_Servicio)")
            old_cols = {r[1] for r in cur.fetchall()}

        cur.execute("DROP TABLE IF EXISTS Hojas_de_Servicio__mig")
        ddl = HOJAS_CREATE_SQL.replace(
            "CREATE TABLE Hojas_de_Servicio", "CREATE TABLE Hojas_de_Servicio__mig", 1
        )
        cur.execute(ddl)

        if had_main:
            parts = []
            for c in HOJAS_DATA_COLUMNS:
                if c in old_cols:
                    parts.append(c)
                elif c == "numero_orden":
                    parts.append("COALESCE(numero_orden, '')")
                else:
                    parts.append("NULL")
            select_sql = ", ".join(parts)
            cols_sql = ", ".join(HOJAS_DATA_COLUMNS)
            cur.execute(
                f"INSERT INTO Hojas_de_Servicio__mig ({cols_sql}) SELECT {select_sql} FROM Hojas_de_Servicio"
            )
            cur.execute("DROP TABLE Hojas_de_Servicio")
        cur.execute("ALTER TABLE Hojas_de_Servicio__mig RENAME TO Hojas_de_Servicio")
        conn.commit()
    finally:
        try:
            cur.execute("PRAGMA foreign_keys=ON")
        except Exception:
            pass
        conn.close()


if __name__ == "__main__":
    import os

    p = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db"
    )
    migrate_hojas_de_servicio_fk(p)
    print("Migración Hojas_de_Servicio completada.")
