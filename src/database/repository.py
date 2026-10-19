"""
Módulo de repositorio para operaciones sobre Supabase SDK en 3FN.
Ejecuta transacciones atómicas, inserción desacoplada y consultas relacionales sin SQL concatenado.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional
from supabase import Client

logger = logging.getLogger(__name__)


def insert_or_update_estudiante(client: Client, estudiante_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inserta o actualiza la entidad maestra de estudiante en la tabla 'estudiantes'.

    Args:
        client: Cliente oficial de Supabase.
        estudiante_data: Diccionario con campos ('cedula', 'nombre_completo', 'correo',
                         'id_seccion', 'edad', 'genero').

    Returns:
        Dict[str, Any]: Registro del estudiante insertado o actualizado.

    Raises:
        RuntimeError: Si ocurre un error en la llamada SDK de Supabase.
    """
    try:
        response = client.table("estudiantes").upsert(
            estudiante_data, on_conflict="cedula"
        ).execute()
        if not response.data:
            raise RuntimeError("No se obtuvo respuesta al persistir estudiante.")
        return response.data[0]
    except Exception as exc:
        logger.error("Error al persistir estudiante (Cédula: %s): %s", estudiante_data.get("cedula"), exc)
        raise RuntimeError(f"Error en persistencia de estudiante: {exc}") from exc


def insert_encuesta(client: Client, encuesta_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inserta el registro de encuesta en la tabla 'encuestas_estudiantes'.

    Args:
        client: Cliente oficial de Supabase.
        encuesta_data: Diccionario con campos ('cedula', 'ha_usado_excel', 'cantidad_operaciones',
                       'interes_electiva', 'tiene_herramientas', 'id_percepcion', 'id_nivel').

    Returns:
        Dict[str, Any]: Registro de la encuesta con su 'id_encuesta' generado.

    Raises:
        RuntimeError: Si ocurre un error en la inserción de la encuesta.
    """
    try:
        response = client.table("encuestas_estudiantes").insert(encuesta_data).execute()
        if not response.data:
            raise RuntimeError("No se obtuvo datos tras la inserción de encuesta.")
        return response.data[0]
    except Exception as exc:
        logger.error("Error al insertar encuesta de estudiante: %s", exc)
        raise RuntimeError(f"Error al registrar encuesta: {exc}") from exc


def insert_encuesta_operaciones(
    client: Client, operaciones_records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Inserta registros en la tabla puente 'encuesta_operaciones' para el desacoplamiento N:M.

    Args:
        client: Cliente oficial de Supabase.
        operaciones_records: Lista de diccionarios con ('id_encuesta', 'id_operacion').

    Returns:
        List[Dict[str, Any]]: Lista de filas insertadas en la tabla intermedia.

    Raises:
        RuntimeError: Si la inserción en la tabla puente falla.
    """
    if not operaciones_records:
        return []

    try:
        response = client.table("encuesta_operaciones").insert(operaciones_records).execute()
        return response.data or []
    except Exception as exc:
        logger.error("Error al insertar operaciones en tabla puente N:M: %s", exc)
        raise RuntimeError(f"Error al registrar operaciones de encuesta: {exc}") from exc


def delete_encuesta(client: Client, id_encuesta: str) -> None:
    """
    Elimina una encuesta por su ID (usado como mecanismo de compensación/rollback).

    Args:
        client: Cliente oficial de Supabase.
        id_encuesta: Identificador UUID de la encuesta a eliminar.
    """
    try:
        client.table("encuestas_estudiantes").delete().eq("id_encuesta", id_encuesta).execute()
        logger.warning("Rollback ejecutado: Encuesta %s eliminada por compensación.", id_encuesta)
    except Exception as exc:
        logger.critical("Fallo catastrófico en compensación de encuesta %s: %s", id_encuesta, exc)


def execute_atomic_survey_transaction(
    client: Client,
    estudiante_data: Dict[str, Any],
    encuesta_data: Dict[str, Any],
    operaciones_ids: List[int],
) -> Dict[str, Any]:
    """
    Ejecuta la transacción coordinada de registro de estudiante, encuesta y tabla puente N:M.
    Incluye mecanismo de rollback/compensación y telemetría de tiempos de respuesta.

    Args:
        client: Cliente oficial de Supabase.
        estudiante_data: Datos de dimensión del estudiante.
        encuesta_data: Datos del hecho transaccional de la encuesta.
        operaciones_ids: Lista de identificadores de operaciones de Excel dominadas.

    Returns:
        Dict[str, Any]: Diccionario con la confirmación de la transacción ('id_encuesta', 'cedula', 'duracion_ms').

    Raises:
        RuntimeError: Si la transacción falla en cualquiera de sus etapas.
    """
    start_time = time.perf_counter()
    cedula = estudiante_data.get("cedula", "DESCONOCIDA")
    id_encuesta_creada: Optional[str] = None

    logger.info("Iniciando transacción OLTP para cédula: %s", cedula)

    try:
        # Paso 1: Persistir dimensión estudiante
        insert_or_update_estudiante(client, estudiante_data)

        # Paso 2: Persistir evento transaccional encuesta
        encuesta_res = insert_encuesta(client, encuesta_data)
        id_encuesta_creada = encuesta_res.get("id_encuesta")
        if not id_encuesta_creada:
            raise RuntimeError("La encuesta insertada no retornó un id_encuesta válido.")

        # Paso 3: Persistir tabla puente N:M si hay operaciones seleccionadas
        if operaciones_ids:
            operaciones_records = [
                {"id_encuesta": id_encuesta_creada, "id_operacion": op_id}
                for op_id in operaciones_ids
            ]
            try:
                insert_encuesta_operaciones(client, operaciones_records)
            except Exception as bridge_exc:
                # Mecanismo de compensación / Rollback
                logger.error(
                    "Fallo en inserción de tabla puente. Iniciando rollback de encuesta %s...",
                    id_encuesta_creada,
                )
                delete_encuesta(client, id_encuesta_creada)
                raise bridge_exc

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "Transacción OLTP EXITOSA para cédula: %s (id_encuesta: %s) en %.2f ms",
            cedula,
            id_encuesta_creada,
            elapsed_ms,
        )

        return {
            "status": "success",
            "id_encuesta": id_encuesta_creada,
            "cedula": cedula,
            "duracion_ms": round(elapsed_ms, 2),
        }

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.error(
            "Transacción OLTP FALLIDA para cédula: %s en %.2f ms. Error: %s",
            cedula,
            elapsed_ms,
            exc,
        )
        raise RuntimeError(f"Fallo en transacción OLTP: {exc}") from exc


def fetch_catalogs(client: Client) -> Dict[str, List[Dict[str, Any]]]:
    """
    Obtiene todos los catálogos maestros desde Supabase para poblar los controles de la UI.

    Args:
        client: Cliente oficial de Supabase.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Diccionario con listas de catálogos:
            - 'secciones'
            - 'operaciones'
            - 'percepciones'
            - 'niveles'
    """
    try:
        secciones = client.table("cat_secciones").select("*").order("id_seccion").execute().data or []
        operaciones = client.table("cat_operaciones_excel").select("*").order("id_operacion").execute().data or []
        percepciones = client.table("cat_percepcion_utilidad").select("*").order("id_percepcion").execute().data or []
        niveles = client.table("cat_niveles_manejo").select("*").order("id_nivel").execute().data or []

        return {
            "secciones": secciones,
            "operaciones": operaciones,
            "percepciones": percepciones,
            "niveles": niveles,
        }
    except Exception as exc:
        logger.error("Error al consultar catálogos maestros: %s", exc)
        raise RuntimeError(f"Error al obtener catálogos de base de datos: {exc}") from exc


def fetch_all_surveys_joined(client: Client) -> List[Dict[str, Any]]:
    """
    Obtiene la totalidad de encuestas con sus tablas relacionadas mediante el query builder SDK.

    Args:
        client: Cliente oficial de Supabase.

    Returns:
        List[Dict[str, Any]]: Lista de registros de encuestas estructurados con datos relacionales.
    """
    try:
        response = client.table("encuestas_estudiantes").select(
            "id_encuesta, created_at, cedula, ha_usado_excel, cantidad_operaciones, "
            "interes_electiva, tiene_herramientas, id_percepcion, id_nivel, "
            "estudiantes(*, cat_secciones(*)), "
            "cat_percepcion_utilidad(*), "
            "cat_niveles_manejo(*), "
            "encuesta_operaciones(*, cat_operaciones_excel(*))"
        ).order("created_at", desc=True).execute()

        return response.data or []
    except Exception as exc:
        logger.error("Error al consultar encuestas estructuradas: %s", exc)
        raise RuntimeError(f"Error al obtener datos analíticos de encuestas: {exc}") from exc
