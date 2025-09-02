import json
import os
import platform

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def save_config(pc_number, server_ip):
    hostname = platform.node()
    config = {
        "pc_number": pc_number,
        "server_ip": server_ip,
        "hostname": hostname
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
