"""
Módulo de pipeline y fachada del micro-ETL para Streamlit.
Encapsula la inserción transaccional, la invalidación de caché y las lecturas analíticas con @st.cache_data(ttl=900).
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import streamlit as st

from src.database.connection import get_supabase_client
from src.database.repository import (
    execute_atomic_survey_transaction,
    fetch_all_surveys_joined,
    fetch_catalogs,
)
from src.etl.analytics import aplanar_registros_encuestas, calcular_metricas_dashboard
from src.etl.transformers import transformar_payload_a_3fn

logger = logging.getLogger(__name__)


def invalidar_cache_dashboard() -> None:
    """
    Invalida de manera segura la memoria caché de Streamlit (@st.cache_data).
    Se invoca exclusivamente tras una inserción transaccional exitosa.
    """
    try:
        st.cache_data.clear()
        logger.info("Caché de Streamlit (@st.cache_data) invalidada exitosamente.")
    except Exception as exc:
        logger.warning("No se pudo invalidar caché de Streamlit (posible entorno CLI/test): %s", exc)


def registrar_encuesta(payload: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Punto de entrada para el procesamiento transaccional de una nueva encuesta.
    Valida el payload, lo descompone a 3FN, persiste de forma atómica en Supabase
    e invalida la caché de lectura para reflejar los datos en tiempo real.

    Args:
        payload: Diccionario crudo enviado por el formulario de la UI.

    Returns:
        Tuple[bool, str, Optional[Dict[str, Any]]]:
            - bool: True si la transacción fue exitosa, False en caso contrario.
            - str: Mensaje de resultado o detalle seguro del error.
            - Optional[Dict[str, Any]]: Metadatos de la transacción ('id_encuesta', 'duracion_ms').
    """
    start_time = time.perf_counter()
    cedula = payload.get("cedula", "DESCONOCIDA") if isinstance(payload, dict) else "DESCONOCIDA"
    logger.info("Pipeline ETL: Iniciando registro de encuesta para cédula %s", cedula)

    try:
        # 1. Transformación y validación estricta de negocio
        estudiante_data, encuesta_data, operaciones_ids = transformar_payload_a_3fn(payload)

        # 2. Conexión con Supabase y persistencia atómica
        client = get_supabase_client()
        tx_result = execute_atomic_survey_transaction(
            client=client,
            estudiante_data=estudiante_data,
            encuesta_data=encuesta_data,
            operaciones_ids=operaciones_ids,
        )

        # 3. Invalidación de caché dirigida (únicamente tras inserción exitosa)
        invalidar_cache_dashboard()

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "Pipeline ETL: Encuesta registrada con éxito para cédula %s en %.2f ms",
            cedula,
            elapsed_ms,
        )

        return (
            True,
            f"Encuesta registrada exitosamente (Cédula: {cedula}).",
            tx_result,
        )

    except ValueError as val_err:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.warning(
            "Pipeline ETL: Error de validación para cédula %s en %.2f ms: %s",
            cedula,
            elapsed_ms,
            val_err,
        )
        return False, str(val_err), None

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.error(
            "Pipeline ETL: Error crítico en transacción para cédula %s en %.2f ms: %s",
            cedula,
            elapsed_ms,
            exc,
        )
        return False, f"Error en la base de datos: {exc}", None


@st.cache_data(ttl=900)
def obtener_datos_dashboard() -> pd.DataFrame:
    """
    Consulta todas las encuestas y devuelve un DataFrame limpio y desanidado.
    Protegido con caché de 15 minutos (@st.cache_data(ttl=900)) para no saturar Supabase.

    Returns:
        pd.DataFrame: DataFrame consolidado con todas las variables del estudio.
    """
    logger.info("Caché MISS o refresco: Consultando datos analíticos en Supabase...")
    client = get_supabase_client()
    raw_surveys = fetch_all_surveys_joined(client)
    df = aplanar_registros_encuestas(raw_surveys)
    logger.info("Datos analíticos obtenidos exitosamente: %d registros.", len(df))
    return df


@st.cache_data(ttl=900)
def obtener_metricas_completas() -> Dict[str, Any]:
    """
    Calcula y cachea el compendio completo de indicadores estadísticos y descriptivos
    requeridos por el Cuadro de Mando de la EECA.

    Returns:
        Dict[str, Any]: Diccionario estructurado con KPIs, tablas de rigor y distribuciones.
    """
    df = obtener_datos_dashboard()
    return calcular_metricas_dashboard(df)


@st.cache_data(ttl=900)
def obtener_catalogos() -> Dict[str, List[Dict[str, Any]]]:
    """
    Obtiene y almacena en caché los catálogos maestros para poblar los controles del formulario.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Catálogos de secciones, operaciones, percepciones y niveles.
    """
    logger.info("Caché MISS: Consultando catálogos maestros en Supabase...")
    client = get_supabase_client()
    return fetch_catalogs(client)
