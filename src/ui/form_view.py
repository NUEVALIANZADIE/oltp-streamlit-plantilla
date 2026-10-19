"""
Módulo de la vista del formulario transaccional mobile-first (Página del Formulario).
Diseñado con una narrativa empática y motivadora que explica el por qué y para qué del estudio,
garantiza la confidencialidad y permite la redacción abierta de la percepción de beneficio.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import streamlit as st

from src.etl.pipeline import obtener_catalogos, registrar_encuesta

logger = logging.getLogger(__name__)


def render_form_page() -> None:
    """
    Renderiza la página independiente del Formulario Diagnóstico Estudiantil.
    Estructurado con narrativa pedagógica para incentivar la participación honesta
    y blindar la privacidad de los datos personales.
    """
    # --------------------------------------------------------------------------
    # 1. Banner Narrativo de Alto Impacto
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="form-story-banner">
            <span style="font-size: 32px;">🚀</span>
            <h1>¡Tu voz hace la diferencia en la EECA!</h1>
            <p>
                Como futuros estadísticos y actuarios de la <strong>Universidad Central de Venezuela (UCV)</strong>, sabemos que Microsoft Excel es la herramienta indispensable en el mercado financiero, asegurador y de análisis de datos. Sin embargo, muchos estudiantes inician el propedéutico sin una formación formal en hojas de cálculo.
                <br><br>
                <strong>¿Para qué respondemos este cuestionario?</strong> Tus respuestas constituyen la evidencia estadística formal que presentaremos ante la Dirección de Escuela y el Consejo de Facultad para sustentar y hacer realidad la apertura de una <strong>Materia Electiva Práctica de Excel</strong> desde los primeros semestres.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # 2. Compromiso de Confidencialidad y Ética Académica
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="privacy-pledge">
            🔒 <strong>Compromiso Ético de Confidencialidad:</strong> Tus datos personales (Cédula y Correo) se solicitan exclusivamente para certificar la validez de la muestra y garantizar que cada estudiante vote una sola vez. <u>Bajo ningún concepto tu información privada será expuesta en cuadros de mando públicos</u> ni compartida con terceros. Tu participación es estrictamente diagnóstica y académica.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cargar catálogos maestros desde la capa de caché ETL
    try:
        catalogos = obtener_catalogos()
    except Exception as exc:
        st.error(f"Error al cargar catálogos del sistema: {exc}")
        return

    cat_secciones = catalogos.get("secciones", [])
    cat_operaciones = catalogos.get("operaciones", [])
    cat_niveles = catalogos.get("niveles", [])

    # Contenedor centralizado para lectura y navegación móvil
    with st.container():
        # ----------------------------------------------------------------------
        # Paso 1: Identificación y Datos de Cohorte
        # ----------------------------------------------------------------------
        st.markdown("### 👤 Paso 1: Identificación y Datos de Cohorte")
        st.caption("Verifica tus datos para certificar tu participación en el propedéutico.")

        col_ced, col_nom = st.columns([1.2, 2])
        with col_ced:
            cedula_input = st.text_input(
                "Cédula de Identidad *",
                placeholder="Ej: V-28123456",
                help="Garantiza que tu respuesta sea contabilizada una sola vez en el estudio.",
            )
        with col_nom:
            nombre_input = st.text_input(
                "Nombre y Apellido *",
                placeholder="Ej: Victoria Díaz",
            )

        correo_input = st.text_input(
            "Correo Electrónico (Institucional o Personal) *",
            placeholder="estudiante@ciencias.ucv.ve",
            help="Utilizado para verificar la legitimidad del registro.",
        )

        col_sec, col_edad, col_gen = st.columns([1.6, 1, 1.4])
        with col_sec:
            seccion_opciones = {
                s["id_seccion"]: s["nombre_seccion"] for s in cat_secciones
            } if cat_secciones else {11: "Sección 11", 12: "Sección 12"}

            id_seccion_sel = st.selectbox(
                "Sección Asignada en el Propedéutico *",
                options=list(seccion_opciones.keys()),
                format_func=lambda s_id: f"{seccion_opciones[s_id]} ({'Cohorte Joven' if s_id == 11 else 'Cohorte Adulta / Laboral'})",
            )

        with col_edad:
            edad_input = st.number_input(
                "Edad (Años) *",
                min_value=15,
                max_value=75,
                value=19,
                step=1,
                help="Rango acotado entre 15 y 75 años.",
            )

        with col_gen:
            genero_sel = st.radio(
                "Género *",
                options=["Femenino", "Masculino"],
                horizontal=True,
            )

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Paso 2: Tu Experiencia Práctica con Microsoft Excel
        # ----------------------------------------------------------------------
        st.markdown("### 📊 Paso 2: Tu Experiencia Práctica con Excel")
        st.caption("Sé completamente sincero(a): no hay respuestas malas, todo diagnóstico suma para la apertura de la materia.")

        ha_usado_excel_str = st.radio(
            "¿Has utilizado o practicado anteriormente con Microsoft Excel? *",
            options=["Sí", "No"],
            horizontal=True,
            index=0,
            help="Si seleccionas 'No', el sistema registrará automáticamente cero operaciones dominadas.",
        )
        ha_usado_excel_bool = (ha_usado_excel_str == "Sí")

        # Diccionario de operaciones del catálogo
        ops_dict = {
            op["id_operacion"]: op["nombre_operacion"] for op in cat_operaciones
        } if cat_operaciones else {
            1: "Sumar",
            2: "Restar",
            3: "Multiplicar",
            4: "Dividir",
            5: "Crear gráficos",
            6: "Crear tablas dinámicas",
        }

        # Control Reactivo
        if not ha_usado_excel_bool:
            st.info("💡 ¡No te preocupes si no has usado Excel antes! Precisamente para nivelar a todos los estudiantes desde cero estamos impulsando la creación de la materia electiva.")
            operaciones_seleccionadas_ids: List[int] = []
        else:
            operaciones_seleccionadas_ids = st.multiselect(
                "Marca las operaciones básicas que sabes realizar por tu cuenta *",
                options=list(ops_dict.keys()),
                format_func=lambda op_id: ops_dict[op_id],
                default=[1, 2],
                help="Selecciona todas las que domines.",
            )
            st.caption(f"Operaciones seleccionadas: **{len(operaciones_seleccionadas_ids)} de 6**")

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Paso 3: Equipamiento, Demanda y Tu Visión Personal
        # ----------------------------------------------------------------------
        st.markdown("### 💡 Paso 3: Equipamiento, Demanda y Tu Visión")

        col_wifi, col_elect = st.columns(2)
        with col_wifi:
            tiene_herramientas_str = st.radio(
                "¿Cuentas con PC/Laptop e Internet en tu hogar para realizar prácticas? *",
                options=["Sí", "No"],
                horizontal=True,
                index=0,
                help="Esta métrica demuestra si la universidad debe habilitar laboratorios presenciales en la escuela.",
            )
            tiene_herramientas_bool = (tiene_herramientas_str == "Sí")

        with col_elect:
            interes_electiva_str = st.radio(
                "¿Te gustaría cursar una materia electiva práctica de Excel si la escuela la ofrece? *",
                options=["Sí", "No"],
                horizontal=True,
                index=0,
                help="Respaldo formal de demanda estudiantil para la EECA.",
            )
            interes_electiva_bool = (interes_electiva_str == "Sí")

        # PREGUNTA ABIERTA: Percepción de beneficio redactada con libertad
        st.markdown("<br>", unsafe_allow_html=True)
        texto_percepcion_input = st.text_area(
            "¿Qué beneficio principal consideras que te brindará el dominio de Excel en tu carrera y vida profesional? *",
            placeholder="Cuéntanos con tus propias palabras: ¿cómo crees que te ayudará en tus materias de estadística, en la carrera o al buscar empleo en el área actuarial/financiera?...",
            help="Tu redacción abierta nos servirá para citar testimonios estudiantiles en el informe de justificación curricular.",
            height=90,
        )

        # Autoevaluación Ordinal (1 al 5)
        niveles_dict = {
            n["id_nivel"]: n["etiqueta_ordinal"] for n in cat_niveles
        } if cat_niveles else {
            1: "Muy Malo",
            2: "Malo",
            3: "Regular",
            4: "Bueno",
            5: "Muy Bueno",
        }

        id_nivel_sel = st.select_slider(
            "En una escala del 1 al 5, ¿cómo autoevalúas tu nivel general de Excel hoy? *",
            options=list(niveles_dict.keys()),
            format_func=lambda n_id: f"{n_id}: {niveles_dict[n_id]}",
            value=3,
        )

        # ----------------------------------------------------------------------
        # Envío Transaccional
        # ----------------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        enviar_btn = st.button(
            "🗳️ ¡Sumar mi Respuesta por la Electiva de Excel!",
            type="primary",
            use_container_width=True,
        )

        if enviar_btn:
            # Validaciones en cliente
            if not cedula_input.strip() or not nombre_input.strip() or not correo_input.strip():
                st.error("⚠️ Por favor completa tus datos de identificación (Cédula, Nombre y Correo).")
                return

            if not texto_percepcion_input.strip():
                st.error("⚠️ Por favor redacta brevemente qué beneficio esperas que te brinde Excel.")
                return

            payload: Dict[str, Any] = {
                "cedula": cedula_input.strip(),
                "nombre_completo": nombre_input.strip(),
                "correo": correo_input.strip(),
                "id_seccion": int(id_seccion_sel),
                "edad": int(edad_input),
                "genero": genero_sel,
                "ha_usado_excel": ha_usado_excel_bool,
                "operaciones_seleccionadas": operaciones_seleccionadas_ids,
                "interes_electiva": interes_electiva_bool,
                "tiene_herramientas": tiene_herramientas_bool,
                "texto_percepcion": texto_percepcion_input.strip(),
                "id_nivel": int(id_nivel_sel),
            }

            with st.spinner("Registrando tu diagnóstico de forma segura en la base de datos..."):
                exito, mensaje, metadata = registrar_encuesta(payload)

            if exito:
                st.success(
                    f"🎉 **¡Muchísimas gracias por tu apoyo!** Tu respuesta fue registrada con éxito en el sistema "
                    f"(Cédula: {cedula_input.strip()}). Tus aportes fundamentarán formalmente la apertura de la materia electiva de Excel en la EECA-UCV."
                )
                st.balloons()
            else:
                st.error(f"❌ Error al procesar el registro: {mensaje}")
