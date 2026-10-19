"""
Módulo del Cuadro de Mando Estadístico Ejecutivo (Pestaña / Página del Dashboard).
Reorganizado con estética tipo Catchr/Pinterest: alta densidad visual, KPIs consolidados,
operaciones básicas al inicio, distribuciones a la misma altura y resumen de cohortes desplegable.
Elimina cualquier exposición de datos personales de estudiantes para preservar confidencialidad absoluta.
"""

from __future__ import annotations

import logging
from typing import Any, Dict
import pandas as pd
import streamlit as st

from src.etl.pipeline import (
    invalidar_cache_dashboard,
    obtener_metricas_completas,
)
from src.ui.charts import (
    plot_brecha_tecnologica,
    plot_distribucion_autoevaluacion,
    plot_distribucion_operaciones,
    plot_distribucion_percepcion,
)

logger = logging.getLogger(__name__)


def render_dashboard_page() -> None:
    """
    Renderiza la página ejecutiva del Cuadro de Mando Estadístico.
    Organiza las métricas en un solo plano visual armónico:
    - Fila 1: KPIs generales, panel de operaciones básicas y brecha tecnológica en el hogar.
    - Fila 2: Distribuciones muestrales situadas a la misma altura sin sobreponerse.
    - Fila 3: Resumen descriptivo de subconjuntos (Sección 11 y 12) en componente desplegable.
    """
    # --------------------------------------------------------------------------
    # 1. Barra Superior Ejecutiva (Header Bar)
    # --------------------------------------------------------------------------
    col_head_left, col_head_right = st.columns([3.5, 1.5])
    with col_head_left:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 28px;">📊</span>
                <div>
                    <h2 style="margin: 0; font-size: 22px; color: #0A2540;">Cuadro de Mando Ejecutivo — Diagnóstico Excel</h2>
                    <p style="margin: 0; font-size: 13px; color: #64748B;">
                        Escuela de Estadística y Ciencias Actuariales (EECA - UCV) | Evaluación Comparativa de Cohortes
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_head_right:
        col_badge, col_ref = st.columns([1.2, 1])
        with col_badge:
            st.markdown(
                """
                <div style="text-align: right; margin-top: 6px;">
                    <span style="background-color: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                        🟢 Supabase 3FN
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_ref:
            if st.button("🔄 Actualizar", key="btn_refresh_dashboard", use_container_width=True, help="Refresca la memoria caché y consulta la base de datos."):
                invalidar_cache_dashboard()
                st.rerun()

    st.markdown("<hr style='margin: 8px 0 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 2. Carga de Métricas Consolidadas (Capa ETL con Caché)
    # --------------------------------------------------------------------------
    try:
        metricas: Dict[str, Any] = obtener_metricas_completas()
    except Exception as exc:
        st.error(f"Error al obtener métricas analíticas: {exc}")
        return

    kpis = metricas.get("kpis_globales", {})
    total_estudiantes = kpis.get("total_estudiantes", 0)

    if total_estudiantes == 0:
        st.info(
            "ℹ️ **Aún no se han registrado encuestas en el sistema OLTP.** "
            "Diríjase a la página **'Formulario Diagnóstico Estudiantil'** en la barra lateral para registrar el primer diagnóstico. "
            "El Cuadro de Mando se actualizará de inmediato."
        )
        return

    # --------------------------------------------------------------------------
    # 3. Fila 1: Tres Tarjetas Ejecutivas Alineadas (Estilo Catchr / Pinterest)
    # --------------------------------------------------------------------------
    # Columnas: [Tarjeta 1: KPIs Generales] | [Tarjeta 2: Operaciones Básicas] | [Tarjeta 3: Brecha Tecnológica]
    col_kpis, col_ops, col_brecha = st.columns([1.3, 2.1, 1.6])

    pct_uso = kpis.get("pct_uso_excel", 0.0)
    pct_interes = kpis.get("pct_interes_electiva", 0.0)
    pct_deficit = kpis.get("pct_deficit_tecnologico", 0.0)

    # --- Tarjeta 1: KPIs Generales (Account KPIs) ---
    with col_kpis:
        st.markdown(
            f"""
            <div class="exec-card">
                <div class="exec-card-header accent-red">
                    <span>MÉTRICAS CLAVE</span>
                    <span>GLOBAL</span>
                </div>
                <div class="kpi-row-item">
                    <span class="kpi-label">Muestra Total</span>
                    <span class="kpi-val">{total_estudiantes}</span>
                </div>
                <div class="kpi-row-item">
                    <span class="kpi-label">% Interés Electiva</span>
                    <span class="kpi-val success">{pct_interes:.1f}%</span>
                </div>
                <div class="kpi-row-item">
                    <span class="kpi-label">% Uso Previo</span>
                    <span class="kpi-val">{pct_uso:.1f}%</span>
                </div>
                <div class="kpi-row-item">
                    <span class="kpi-label">% Déficit Tecnológico</span>
                    <span class="kpi-val {'alert' if pct_deficit > 15 else ''}">{pct_deficit:.1f}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Tarjeta 2: Dominio de Operaciones Básicas (Global Performances) ---
    with col_ops:
        ops_pct = metricas.get("operaciones_especificas_pct", {})
        icons_map = {
            "Sumar": "➕",
            "Restar": "➖",
            "Multiplicar": "✖️",
            "Dividir": "➗",
            "Crear gráficos": "📈",
            "Crear tablas dinámicas": "📊",
        }

        # Generar tiles HTML para la cuadrícula 3x2
        tiles_html = ""
        for nombre_op, val_pct in ops_pct.items():
            icono = icons_map.get(nombre_op, "📌")
            tiles_html += f"""
            <div class="ops-tile">
                <div class="ops-icon">{icono}</div>
                <div class="ops-name">{nombre_op}</div>
                <div class="ops-pct">{val_pct:.1f}%</div>
            </div>
            """

        st.markdown(
            f"""
            <div class="exec-card">
                <div class="exec-card-header accent-blue">
                    <span>DOMINIO DE OPERACIONES BÁSICAS</span>
                    <span>PROPORCIÓN MUESTRAL</span>
                </div>
                <div class="ops-grid">
                    {tiles_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Tarjeta 3: Brecha Tecnológica en el Hogar (Interaction Rate by Type) ---
    with col_brecha:
        brecha = metricas.get("brecha_tecnologica_secciones", {})
        if brecha:
            fig_brecha = plot_brecha_tecnologica(brecha)
            st.pyplot(fig_brecha, use_container_width=True)

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 4. Fila 2: Distribuciones Situadas a la Misma Altura (Side by Side)
    # --------------------------------------------------------------------------
    st.markdown("#### 📈 Distribuciones Comparativas de Cohortes")
    col_dist1, col_dist2 = st.columns(2)

    with col_dist1:
        frec_ops = metricas.get("frecuencia_operaciones_por_seccion")
        if isinstance(frec_ops, pd.DataFrame):
            fig_ops = plot_distribucion_operaciones(frec_ops)
            st.pyplot(fig_ops, use_container_width=True)

    with col_dist2:
        dist_auto = metricas.get("distribucion_autoevaluacion", {})
        if dist_auto:
            fig_auto = plot_distribucion_autoevaluacion(dist_auto)
            st.pyplot(fig_auto, use_container_width=True)

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 5. Fila 3: Resumen Estadístico de Subconjuntos Desplegable (Sección 11 vs 12)
    # --------------------------------------------------------------------------
    with st.expander("📊 Ver Resumen Estadístico Descriptivo por Cohorte (Sección 11 vs. Sección 12)", expanded=False):
        st.markdown(
            """
            <p style="font-size: 13px; color: #475569; margin-bottom: 12px;">
                Medidas formales de la estadística descriptiva para la variable <strong>Cantidad de Operaciones Básicas Dominadas (0 a 6)</strong>,
                desglosadas entre la cohorte joven de ingreso reciente (Sección 11) y la cohorte con experiencia laboral (Sección 12).
            </p>
            """,
            unsafe_allow_html=True,
        )

        tabla_rigor = metricas.get("tabla_rigor_estadistico")
        if isinstance(tabla_rigor, pd.DataFrame) and not tabla_rigor.empty:
            st.dataframe(
                tabla_rigor.style.format({
                    "n": "{:d}",
                    "Media (x̄)": "{:.2f}",
                    "Moda (Mo)": "{:.1f}",
                    "Desv. Est. (S)": "{:.2f}",
                    "CV (%)": "{:.2f}%",
                    "Asimetría": "{:.2f}",
                    "Curtosis": "{:.2f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

        st.markdown(
            r"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 16px; border-radius: 8px; margin-top: 12px;">
                <p style="margin: 0; font-size: 13px; color: #1E293B; line-height: 1.5;">
                    💡 <strong>Criterio Estadístico para la Cátedra:</strong> 
                    Un <em>Coeficiente de Variación ($CV\%$)</em> elevado en la Sección 11 sustenta la necesidad imperativa de nivelar el curso propedéutico desde las operaciones más elementales. 
                    En contraste, la homogeneidad y media más alta de la Sección 12 evidencia que la experiencia laboral acelera el aprendizaje instrumental.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Gráfico complementario de percepción de utilidad dentro del resumen analítico
        dist_perc = metricas.get("distribucion_percepcion", {})
        if dist_perc:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### Percepción Tipificada de Beneficio Académico y Profesional")
            fig_perc = plot_distribucion_percepcion(dist_perc)
            st.pyplot(fig_perc, use_container_width=True)
