# Base-de-datos

Programa para mundo fix (reparación de celulares): inventario, ventas, servicios, clientes y PDFs (facturas / hojas de servicio).

## Requisitos previos

- **Python 3.10+** (recomendado 3.11 o superior).
- **Tkinter** (interfaz gráfica):
  - **Linux (Debian/Ubuntu/Parrot, etc.):** suele venir en un paquete aparte. Si al ejecutar falta `tkinter`, instala por ejemplo:

    ```bash
    sudo apt update
    sudo apt install python3-tk python3-venv
    ```

  - **Windows:** el instalador oficial de Python desde [python.org](https://www.python.org/downloads/) suele incluir Tcl/Tk; marca la opción **tcl/tk** si el asistente la ofrece.

En muchas distribuciones Linux el Python del sistema **no permite** `pip install` global (PEP 668). Por eso el proyecto usa un **entorno virtual** (`.venv`).

---

## 1. Clonar o ubicarse en la carpeta del proyecto

Sustituye la ruta por la tuya si es distinta.

### Linux / macOS

```bash
cd /ruta/al/proyecto/Base-de-datos
```

### Windows (PowerShell o CMD)

```cmd
cd C:\ruta\al\proyecto\Base-de-datos
```

---

## 2. Crear el entorno virtual

### Linux / macOS

```bash
python3 -m venv .venv
```

Si `python3` no existe, prueba:

```bash
python -m venv .venv
```

### Windows (PowerShell o CMD)

```cmd
py -3 -m venv .venv
```

Si no tienes el launcher `py`, usa:

```cmd
python -m venv .venv
```

---

## 3. Activar el entorno virtual

Hazlo **siempre** en la misma terminal donde vayas a instalar dependencias o a ejecutar el programa.

### Linux / macOS (bash / zsh)

```bash
source .venv/bin/activate
```

Tras activarlo, el prompt suele mostrar `(.venv)`.

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea scripts: ejecuta una vez `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (como administrador de políticas de tu usuario) o usa **CMD** con `activate.bat`.

---

## 4. Instalar dependencias de Python

Con el entorno **activado** (debe verse `(.venv)` en el prompt):

### Linux / macOS / Windows (mismo comando)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Eso instala, entre otras: `reportlab`, `Pillow`, `tkcalendar`, `ttkthemes`, `matplotlib`, `openpyxl`, `pandas`.

---

## 5. Ejecutar la aplicación

Ejecuta desde la **raíz del proyecto** (donde está `index.py`), con el venv activado.

### Linux / macOS

```bash
python index.py
```

Sin activar el venv (ruta explícita al intérprete del proyecto):

```bash
./.venv/bin/python index.py
```

### Windows (con venv activado)

```cmd
python index.py
```

Sin activar el venv:

```cmd
.venv\Scripts\python.exe index.py
```

---

## Resumen rápido (copiar bloque completo)

### Linux / macOS

```bash
cd /ruta/al/proyecto/Base-de-datos
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python index.py
```

### Windows (CMD)

```cmd
cd C:\ruta\al\proyecto\Base-de-datos
py -3 -m venv .venv
.venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
python index.py
```

---

## Notas

- La base de datos SQLite del proyecto suele ser `database.db` en la raíz del repositorio (se crea o actualiza al usar la app).
- Si cambias de máquina o borras `.venv`, repite desde el **paso 2**.
- **No** hace falta `sudo pip install` dentro del venv; todo va en `.venv/` y no toca el Python del sistema.
