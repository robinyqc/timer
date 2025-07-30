import os
import toml

CONFIG_PATH = os.path.expanduser("~/.timer_config.toml")

DEFAULT_CONFIG = {
    "sound_path": "",
    "shortcuts": {
        "start/stop": "<F5>"
    },
    "default_language": "English"
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return toml.load(f)
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_PATH, "w") as f:
            toml.dump(config, f)
    except Exception as e:
        print(f"Failed to save config: {e}")
