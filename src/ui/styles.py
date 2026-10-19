"""
Módulo de estilos CSS personalizados e inyección tipográfica para Streamlit.
Aplica los colores, contrastes y jerarquías visuales definidos en docs/brand_book.md
e implementa el layout ejecutivo inspirado en paneles de alta densidad visual (Catchr/Pinterest).
"""

import streamlit as st


def apply_custom_styles() -> None:
    """
    Inyecta hojas de estilo CSS estáticas para armonizar la interfaz con la identidad EECA-UCV.
    No interpola datos de entrada de usuarios para garantizar cero vulnerabilidades XSS.
    """
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Montserrat:wght@600;700;800&display=swap');

    /* Variables CSS del Brand Book */
    :root {
        --color-primary: #0A2540;
        --color-accent: #1D4ED8;
        --color-secondary: #059669;
        --color-bg-card: #FFFFFF;
        --color-bg-subtle: #F8FAFC;
        --color-border: #E2E8F0;
        --color-text-dark: #1E293B;
        --color-text-muted: #64748B;
        --color-alert: #DC2626;
    }

    /* Tipografía Global */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--color-text-dark);
    }

    h1, h2, h3, h4 {
        font-family: 'Montserrat', 'Inter', sans-serif !important;
        color: var(--color-primary) !important;
        font-weight: 700 !important;
    }

    /* Tarjeta Ejecutiva (Estilo Catchr/Pinterest) */
    .exec-card {
        background-color: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        height: 100%;
        margin-bottom: 12px;
    }

    .exec-card-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #FFFFFF;
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
        padding: 6px 14px;
        border-radius: 8px 8px 4px 4px;
        margin: -16px -20px 14px -20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        letter-spacing: 0.3px;
    }

    .exec-card-header.accent-red {
        background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);
    }

    .exec-card-header.accent-blue {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    }

    /* Fila de Métricas Verticales (Account KPIs Style) */
    .kpi-row-item {
        border-bottom: 1px solid #F1F5F9;
        padding: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kpi-row-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    .kpi-label {
        font-size: 12px;
        color: var(--color-text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: var(--color-primary);
    }
    .kpi-val.alert {
        color: var(--color-alert);
    }
    .kpi-val.success {
        color: var(--color-secondary);
    }

    /* Cuadrícula de Operaciones (Global Performances Style) */
    .ops-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    .ops-tile {
        background-color: var(--color-bg-subtle);
        border: 1px solid var(--color-border);
        border-radius: 10px;
        padding: 10px 12px;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .ops-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
        border-color: var(--color-accent);
    }
    .ops-icon {
        font-size: 20px;
        margin-bottom: 2px;
    }
    .ops-name {
        font-size: 11px;
        font-weight: 600;
        color: var(--color-text-muted);
        text-transform: uppercase;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ops-pct {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 700;
        color: var(--color-primary);
    }

    /* Banner Superior del Dashboard */
    .dash-top-bar {
        background: #FFFFFF;
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Banner Narrativo del Formulario */
    .form-story-banner {
        background: linear-gradient(135deg, #0A2540 0%, #1D4ED8 100%);
        padding: 28px 32px;
        border-radius: 14px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px -2px rgba(10, 37, 64, 0.25);
    }
    .form-story-banner h1 {
        color: #FFFFFF !important;
        font-size: 24px !important;
        margin: 0 0 10px 0 !important;
    }
    .form-story-banner p {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        line-height: 1.6;
        margin: 0 !important;
    }

    /* Caja de Compromiso Ético y Confidencialidad */
    .privacy-pledge {
        background-color: #F0FDF4;
        border-left: 4px solid var(--color-secondary);
        padding: 12px 18px;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 13px;
        color: #14532D;
    }

    /* Botones de Envío y Acción */
    .stButton > button[kind="primary"] {
        background-color: var(--color-accent) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        transition: background-color 0.2s ease;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1E40AF !important;
    }

    /* Badges Informativos */
    .badge-s11 {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-s12 {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
