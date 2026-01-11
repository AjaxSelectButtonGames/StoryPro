"""
StoryPro - Run the application
"""

import sys
import os

# Add the project root to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main import main
import flet as ft

if __name__ == "__main__":
    ft.app(target=main)
