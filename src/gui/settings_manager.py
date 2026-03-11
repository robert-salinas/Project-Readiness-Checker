import os
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".rs_prc_config.json"

DEFAULT_CONFIG = {
    "export_path": str(Path.home() / "Documents" / "RS_Audit_Reports"),
    "audit_profile": "Estándar",
    "calc_hidden": False,
    "forbidden_files": ["__pycache__", ".DS_Store", ".venv", "*.log", "node_modules"]
}

AUDIT_PROFILES = {
    "Estándar": ["__pycache__", ".DS_Store", ".venv", "*.log", "node_modules"],
    "Python": ["__pycache__", ".venv", "*.pyc", "*.pyo", ".pytest_cache", ".mypy_cache"],
    "Web": ["node_modules", ".next", ".cache", "dist", "build", ".env.local"],
    "Limpieza Profunda": ["__pycache__", ".venv", "node_modules", ".DS_Store", "*.log", "temp", "tmp", "dist", "build"]
}

def load_settings():
    if not CONFIG_FILE.exists():
        save_settings(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_settings(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
