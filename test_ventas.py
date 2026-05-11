import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
query = """
    SELECT v.factura, c.nombre as cliente, i.producto as articulo, v.precio, v.cantidad, v.total, v.fecha, v.hora, v.costo
    FROM Ventas v
    LEFT JOIN Clientes c ON v.cliente_id = c.id
    LEFT JOIN Inventario i ON v.producto_id = i.id
"""
try:
    cursor.execute(query)
    ventas = [tuple(row) for row in cursor.fetchall()]
    print(f"Loaded {len(ventas)} ventas.")
    for venta in ventas:
        venta = list(venta)
        # Try to parse as done in ventas_pro.py
        import datetime
        venta[3]= "{:,.0f}".format(float(venta[3]))
        venta[5]= "{:,.0f}".format(float(venta[5]))
        venta[6]= datetime.datetime.strptime(str(venta[6]), "%Y-%m-%d").strftime("%d/%m/%Y")
except Exception as e:
    print(f"Exception type: {type(e)}")
    print(f"Exception message: {e}")
