# CyberUsuario

Cliente del sistema **Cyber Control**.  
Este módulo se ejecuta en cada computadora del cyber y permite que los usuarios inicien sesión, consuman su tiempo en vivo y se comuniquen con el administrador.

---

## 🚀 Requisitos

- Python 3.11 o superior
- PostgreSQL (base de datos compartida con el administrador)
- Librerías necesarias (instalar con `pip install -r requirements.txt`)

---

## ⚙️ Configuración inicial

1. Clonar el repositorio o copiar los archivos en la PC cliente.

2. Crear un archivo `.env` en la carpeta raíz con al menos las variables:

   ```env
   DB_PORT="tu puerto"
   DB_NAME=cyber_control
   DB_USER="usuario"
   DB_PASSWORD="contraseña"
   EXIT_USER="usuario_fijo"
   EXIT_PASS="clave fija"
   ```

   > **Nota:** `DB_HOST` lo configura automáticamente cada cliente desde la ventana de configuración.

3. Ejecutar el programa (`main_user.py`).  
   - Si es la **primera vez**, se abrirá una ventana de **Configuración**.  
   - Ahí debes ingresar:
     - **Número de PC** (ejemplo: 1, 2, 3...)  
     - **IP del Servidor** (ejemplo: `192.168.1.14`, donde está PostgreSQL).  
   - El sistema guarda estos datos junto con el `hostname` real en un archivo `config.json`.

---

## 👤 Uso

- Al iniciar, aparece la **pantalla de Login** mostrando el número de PC.  
- El usuario ingresa su usuario y contraseña registrados en el sistema.  
- Una vez dentro, se muestra la **barra de sesión** con su tiempo en vivo.  
- El tiempo se descuenta automáticamente y se sincroniza con el servidor.  

---

## 🔒 Salida de emergencia

- En la esquina superior izquierda de la pantalla de Login hay un botón **"X"**.  
- Al hacer clic, se abre un cuadro de validación.  
- Solo con las credenciales de administrador definidas en `.env`:

  ```
  EXIT_USER=administrador
  EXIT_PASS=Pifos4117@
  ```

  se permite cerrar el programa y liberar la máquina.

---

## 🖥️ Compilación a .exe (opcional)

Para distribuir el cliente en cada PC sin instalar Python:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main_user.py
```

El ejecutable quedará en la carpeta `dist/`.

---

## 📂 Archivos importantes

- `main_user.py` → punto de entrada del cliente.  
- `dialogs/config_dialog.py` → configuración inicial de PC.  
- `dialogs/login.py` → pantalla de login de usuarios.  
- `session.py` → barra de sesión con tiempo en vivo.  
- `utils/config_manager.py` → lectura/escritura de `config.json`.  
- `utils/db.py` → conexión a PostgreSQL.  
- `.env` → credenciales de BD y claves de salida.  
- `config.json` → archivo generado automáticamente en cada PC cliente con número de PC, IP del servidor y hostname.

---

## 📌 Notas finales

- Cada cliente debe configurarse la primera vez para registrar su **número de PC** e **IP del servidor**.  
- El administrador verá en su panel la lista de PCs con usuario, tiempo y estado en tiempo real.  
- Si el administrador fuerza un **Cerrar Sesión**, la ventana del cliente se cerrará automáticamente.
