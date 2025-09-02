import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = "config.json"

def get_server_ip():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("server_ip")
    return os.getenv("DB_HOST")

def get_connection(host=None):
    try:
        connection = psycopg2.connect(
            host=host or get_server_ip(),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
