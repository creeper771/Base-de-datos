from database.db_manager import DBManager

class InventarioDAO:
    def __init__(self):
        self.db = DBManager()

    def get_all_nombres_productos(self):
        """Retorna una lista con todos los nombres de los productos (para el combobox)."""
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT producto FROM Inventario")
            return [row['producto'] if isinstance(row, dict) else row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener nombres de productos: {e}")
            raise e

    def obtener_id_por_nombre(self, producto):
        """Retorna el ID de un producto dado su nombre."""
        query = "SELECT id FROM Inventario WHERE producto = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (producto,))
            row = cursor.fetchone()
            return row['id'] if row else None
        except Exception as e:
            print(f"Error al obtener ID del producto {producto}: {e}")
            raise e

    def get_productos_basico(self, filtro=None):
        """Retorna los campos básicos de los productos, opcionalmente filtrados."""
        query = "SELECT producto, Precio_cos, image_path_inv FROM Inventario"
        params = []
        if filtro:
            query += " WHERE producto LIKE ?"
            params.append(f"%{filtro}%")

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [(row['producto'], row['Precio_cos'], row['image_path_inv']) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al cargar los productos: {e}")
            raise e

    def get_producto_por_nombre(self, producto, include_image=False):
        """Busca un producto por su nombre exacto."""
        if include_image:
            query = "SELECT producto, Precio_cos, precio_ven, stock, estado, image_path_inv, serie FROM Inventario WHERE producto=?"
        else:
            query = "SELECT producto, Precio_cos, precio_ven, stock, estado, serie FROM Inventario WHERE producto=?"
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (producto,))
            row = cursor.fetchone()
            if row is None:
                return None
            
            if include_image:
                return (row['producto'], row['Precio_cos'], row['precio_ven'], row['stock'], row['estado'], row['image_path_inv'], row['serie'])
            else:
                return (row['producto'], row['Precio_cos'], row['precio_ven'], row['stock'], row['estado'], row['serie'])
        except Exception as e:
            print("Error al obtener los datos del producto:", e)
            raise e

    def agregar_producto(self, producto, precio_ven, precio_cos, stock, estado, image_path_inv, serie):
        """Inserta un nuevo producto en la base de datos."""
        query = "INSERT INTO Inventario(producto, precio_ven, Precio_cos, stock, estado, image_path_inv, serie) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (producto, precio_ven, precio_cos, stock, estado, image_path_inv, serie))
            conn.commit()
            return True
        except Exception as e:
            print("Error al cargar el producto", e)
            raise e

    def actualizar_producto(self, producto, precio_ven, precio_cos, stock, estado, image_path_inv, serie, old_producto_name):
        """Actualiza un producto existente."""
        query = "UPDATE Inventario SET producto=?, precio_ven=?, Precio_cos=?, stock=?, estado=?, Image_path_inv=?, serie=? WHERE producto=?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (producto, precio_ven, precio_cos, stock, estado, image_path_inv, serie, old_producto_name))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al editar el producto: {e}")
            raise e

    def eliminar_producto(self, producto):
        """Elimina un producto por su nombre."""
        query = "DELETE FROM Inventario WHERE producto = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (producto,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            raise e

    def restar_stock(self, producto, cantidad_a_restar):
        """Resta una cantidad específica del stock de un producto al realizar una venta."""
        query = "UPDATE Inventario SET stock = stock - ? WHERE producto = ?"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (cantidad_a_restar, producto))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar stock de {producto}: {e}")
            raise e
