"""
Módulo de interfaz de usuario (UI) para Streamlit y visualización estadística con Matplotlib.
Cumple estrictamente con la guía visual (brand_book.md) y la reorganización ejecutiva.
"""

from src.ui.dashboard_view import render_dashboard_page
from src.ui.form_view import render_form_page
from src.ui.styles import apply_custom_styles

__all__ = [
    "apply_custom_styles",
    "render_form_page",
    "render_dashboard_page",
]
