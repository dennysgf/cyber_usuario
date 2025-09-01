from utils.db import get_connection
import bcrypt

def validate_user(username, password):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, tiempo_restante FROM usuarios WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
            return None
        return {"id": user[0], "username": user[1], "tiempo": user[3]}
    except Exception as e:
        print(f"Error al validar usuario: {e}")
        return None

def get_time_remaining(user_id):
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT tiempo_restante FROM usuarios WHERE id = %s", (user_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return float(result[0]) if result else 0
    except Exception as e:
        print(f"Error al obtener tiempo: {e}")
        return 0

def logout_user(user_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET tiempo_restante = 0 WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al cerrar sesión: {e}")
        return False
