import os
import sys

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gui.main_app import RSProjectReadinessApp
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = RSProjectReadinessApp()
    app.mainloop()
