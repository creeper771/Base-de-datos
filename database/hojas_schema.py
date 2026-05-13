"""Esquema único de la tabla Hojas_de_Servicio (una sola definición para app y migraciones)."""

# Columnas de negocio (sin id); orden fijo para INSERT/migración
HOJAS_DATA_COLUMNS = [
    "numero_orden",
    "fecha_creacion",
    "servicio_id",
    "fecha_entrega",
    "fecha_instalacion",
    "falla",
    "diagnostico",
    "observaciones",
    "cantidad",
    "precio",
    "anticipo",
    "imei",
    "contrasena",
    "estados_equipo",
    "pruebas_json",
    "cliente_nombre",
    "equipo_nombre",
    "servicio_nombre",
    "ruta_pdf",
]

HOJAS_CREATE_IF_NOT_EXISTS = """
CREATE TABLE IF NOT EXISTS Hojas_de_Servicio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_orden TEXT NOT NULL,
    fecha_creacion TEXT,
    servicio_id INTEGER,
    fecha_entrega TEXT,
    fecha_instalacion TEXT,
    falla TEXT,
    diagnostico TEXT,
    observaciones TEXT,
    cantidad INTEGER,
    precio REAL,
    anticipo REAL,
    imei TEXT,
    contrasena TEXT,
    estados_equipo TEXT,
    pruebas_json TEXT,
    cliente_nombre TEXT,
    equipo_nombre TEXT,
    servicio_nombre TEXT,
    ruta_pdf TEXT,
    FOREIGN KEY(servicio_id) REFERENCES Servicios_realizados(id) ON DELETE SET NULL
)
"""

HOJAS_CREATE_SQL = HOJAS_CREATE_IF_NOT_EXISTS.replace(
    "CREATE TABLE IF NOT EXISTS", "CREATE TABLE", 1
)
