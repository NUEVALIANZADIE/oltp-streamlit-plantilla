"""
Punto de Entrada Principal de la Aplicación Streamlit.
Sistema OLTP y Cuadro de Mando Ejecutivo: Nivel de Manejo de Excel (EECA - UCV).
Organizado en páginas independientes mediante st.navigation para garantizar máxima usabilidad y densidad visual.
"""

from __future__ import annotations

import os
import streamlit as st

from src.ui.dashboard_view import render_dashboard_page
from src.ui.form_view import render_form_page
from src.ui.styles import apply_custom_styles

# 1. Configuración de Página (Brand Book)
st.set_page_config(
    page_title="EECA-UCV | OLTP & Dashboard Excel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inyección de Estilos CSS Personalizados
apply_custom_styles()

# 3. Definición de Páginas Independientes con st.navigation
dashboard_page = st.Page(
    render_dashboard_page,
    title="Cuadro de Mando Ejecutivo",
    icon="📊",
    default=True,
)

formulario_page = st.Page(
    render_form_page,
    title="Formulario Diagnóstico Estudiantil",
    icon="📝",
)

# Router de navegación en la barra lateral
pg = st.navigation(
    {
        "Plataforma EECA-UCV": [dashboard_page, formulario_page],
    }
)

# 4. Barra Lateral (Sidebar) — Identidad Académica y Garantía Ética
with st.sidebar:
    logo_path = os.path.join("assets", "img", "logo_eeca.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_column_width=True)
    else:
        st.markdown(
            """
            <div style="background-color: #0A2540; color: #FFFFFF; padding: 14px; border-radius: 8px; text-align: center; margin-bottom: 12px;">
                <span style="font-size: 26px;">🏛️</span>
                <h3 style="color: #FFFFFF !important; margin: 4px 0 0 0; font-size: 15px;">EECA — UCV</h3>
                <p style="color: #CBD5E1; margin: 0; font-size: 11px;">Escuela de Estadística y Cs. Actuariales</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📌 Misión del Proyecto")
    st.markdown(
        """
        Demostrar formalmente la brecha operativa de hojas de cálculo en el Curso Propedéutico para sustentar ante las autoridades la **apertura de una materia electiva práctica de Excel**.
        """
    )

    st.markdown("---")
    st.markdown("### 👥 Cohortes del Estudio")
    st.markdown(
        """
        - <span class="badge-s11">Sección 11</span>: Cohorte Joven (~19 años), egresados de secundaria, alta heterogeneidad y déficit de equipos en casa.
        - <span class="badge-s12">Sección 12</span>: Cohorte Adulta (~29 años), experiencia laboral previa y mayor dominio técnico.
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🔒 Protección y Ética")
    st.caption(
        "• **Base de Datos:** PostgreSQL en 3FN en Supabase\n"
        "• **Privacidad:** Cero exposición de datos personales en el dashboard\n"
        "• **Caché:** `@st.cache_data(ttl=900)` para proteger la cuota del servicio\n"
        "• **Investigadores:** Schantal Troja, Vicente Díaz y Victoria Díaz"
    )

# 5. Ejecutar la Página Seleccionada
pg.run()
