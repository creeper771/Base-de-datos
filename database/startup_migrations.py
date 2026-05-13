import os


def _default_db_path():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db"
    )


def run_startup_migrations():
    """Migraciones idempotentes antes de usar la app."""
    db_path = _default_db_path()
    if not os.path.isfile(db_path):
        return
    try:
        from database.migration_fase6 import run_migration

        run_migration()
    except Exception as e:
        print(f"Aviso: migración fase6 no aplicada: {e}")
    try:
        from database.migration_hojas_fk import migrate_hojas_de_servicio_fk

        migrate_hojas_de_servicio_fk(db_path)
    except Exception as e:
        print(f"Aviso: migración Hojas_de_Servicio FK no aplicada: {e}")
