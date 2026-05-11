import sqlite3
import pandas as pd
from tkinter import messagebox
import os
import sys

# Definir las rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTARIO_DIR = os.path.join(BASE_DIR, "Inventario_Excel")
SERVICIOS_DIR = os.path.join(BASE_DIR, "Servicios_Excel")

# Asegurar que las carpetas existan
os.makedirs(INVENTARIO_DIR, exist_ok=True)
os.makedirs(SERVICIOS_DIR, exist_ok=True)

def exportar_datos(db_name, table_name):
    """
    Exporta los datos de una tabla a un archivo Excel.
    
    Args:
        db_name (str): Nombre de la base de datos
        table_name (str): Nombre de la tabla a exportar
    """
    try:
        # Determinar la carpeta de destino según la tabla
        if table_name == "Inventario":
            carpeta_destino = INVENTARIO_DIR
        elif table_name == "Servicios_realizados":
            carpeta_destino = SERVICIOS_DIR
        else:
            carpeta_destino = BASE_DIR
            
        # Construir la ruta completa del archivo
        archivo_salida = f"{table_name}.xlsx"
        ruta_completa = os.path.join(carpeta_destino, archivo_salida)
        
        # Conexión a la base de datos
        conn = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        
        # Crear DataFrame y exportar a Excel
        df = pd.read_sql_query(query, conn)
        df.to_excel(ruta_completa, index=False)
        conn.close()
        
        messagebox.showinfo("Éxito", f"Datos exportados exitosamente en:\n{ruta_completa}")
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar los datos:\n{str(e)}")
        return False

def exportar_inventario(db_name, archivo_salida="Inventario.xlsx"):
    """
    Exporta los datos de la tabla Inventario a un archivo Excel en la carpeta 'Inventario_Excel'.
    
    Args:
        db_name (str): Nombre de la base de datos
        archivo_salida (str): Nombre del archivo Excel de salida
    """
    try:
        # Construir la ruta completa del archivo
        ruta_completa = os.path.join(INVENTARIO_DIR, archivo_salida)
        
        # Conexión a la base de datos
        conn = sqlite3.connect(db_name)
        
        # Consulta SQL
        query = """
            SELECT id, serie, producto, precio_cos, precio_ven, stock, estado 
            FROM Inventario
        """
        
        # Crear DataFrame y exportar a Excel
        df = pd.read_sql_query(query, conn)
        df.to_excel(ruta_completa, index=False)
        conn.close()
        
        messagebox.showinfo("Éxito", f"Inventario exportado exitosamente en:\n{ruta_completa}")
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar el inventario:\n{str(e)}")
        return False

def exportar_servicios(db_name, archivo_salida="Servicios_realizados.xlsx"):
    """
    Exporta los datos de la tabla Servicios_realizados a un archivo Excel en la carpeta 'Servicios_Excel'.
    
    Args:
        db_name (str): Nombre de la base de datos
        archivo_salida (str): Nombre del archivo Excel de salida
    """
    try:
        # Construir la ruta completa del archivo
        ruta_completa = os.path.join(SERVICIOS_DIR, archivo_salida)
        
        # Conexión a la base de datos
        conn = sqlite3.connect(db_name)
        
        # Consulta SQL
        query = """
            SELECT id, cliente, nombre_equipo, servicio, precio, Fecha_de_recibo, estado 
            FROM Servicios_realizados
        """
        
        # Crear DataFrame y exportar a Excel
        df = pd.read_sql_query(query, conn)
        df.to_excel(ruta_completa, index=False)
        conn.close()
        
        messagebox.showinfo("Éxito", f"Servicios exportados exitosamente en:\n{ruta_completa}")
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar los servicios:\n{str(e)}")
        return False