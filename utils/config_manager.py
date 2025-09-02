import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def save_config(pc_number, server_ip):
    config = {"pc_number": pc_number, "server_ip": server_ip}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
