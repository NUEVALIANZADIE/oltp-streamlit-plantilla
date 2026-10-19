"""
Módulo de transformación y validación del micro-ETL (Transición a 3FN).
Valida tipos de datos, límites numéricos, coherencia condicional y desacoplamiento relacional.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

VALID_SECCIONES = {11, 12}
VALID_GENEROS = {"Femenino", "Masculino"}
VALID_PERCEPCIONES = {1, 2, 3, 4}
VALID_NIVELES = {1, 2, 3, 4, 5}
VALID_OPERACIONES = {1, 2, 3, 4, 5, 6}


def sanitizar_texto(texto: Any, campo: str) -> str:
    """
    Sanitiza y valida una cadena de texto eliminando espacios redundantes y caracteres de control.

    Args:
        texto: Valor de entrada.
        campo: Nombre del campo para reporte de errores.

    Returns:
        str: Texto sanitizado.

    Raises:
        ValueError: Si el texto está vacío o no es una cadena válida.
    """
    if not isinstance(texto, str):
        raise ValueError(f"El campo '{campo}' debe ser una cadena de texto.")
    limpio = texto.strip()
    if not limpio:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return limpio


def validar_correo(correo: Any) -> str:
    """
    Valida y normaliza un correo electrónico institucional o personal.

    Args:
        correo: Cadena con el correo electrónico.

    Returns:
        str: Correo en minúsculas y sin espacios.

    Raises:
        ValueError: Si el formato del correo no es válido.
    """
    correo_str = sanitizar_texto(correo, "correo").lower()
    # Patrón básico de verificación de correo
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(patron, correo_str):
        raise ValueError(f"El formato del correo '{correo_str}' es inválido.")
    return correo_str


def validar_edad(edad: Any) -> int:
    """
    Valida el límite numérico de la variable 'edad' (15 a 75 años).

    Args:
        edad: Valor numérico de la edad.

    Returns:
        int: Edad validada.

    Raises:
        ValueError: Si la edad no es entera o está fuera del rango [15, 75].
    """
    if not isinstance(edad, int) or isinstance(edad, bool):
        try:
            edad = int(edad)
        except (ValueError, TypeError):
            raise ValueError("La edad debe ser un número entero.")

    if edad < 15 or edad > 75:
        raise ValueError(f"La edad ({edad}) está fuera del rango permitido [15, 75] años.")
    return edad


def clasificar_texto_percepcion(texto: str) -> int:
    """
    Clasifica semánticamente la respuesta abierta sobre la percepción de beneficio de Excel
    en una de las 4 categorías cerradas de la Tercera Forma Normal (cat_percepcion_utilidad).

    Args:
        texto: Cadena libre redactada por el estudiante.

    Returns:
        int: Identificador de categoría (1 al 4):
            1: Ayuda en la carrera universitaria
            2: Fines generales y cotidianos
            3: Oportunidades laborales y profesionales
            4: Beneficio integral (carrera + trabajo)
    """
    t = texto.lower()

    palabras_carrera = [
        "carrera", "materia", "materias", "estudio", "estudios", "semestre",
        "profesor", "academico", "académico", "universidad", "ucv", "tarea",
        "tareas", "facultad", "eeca", "asignatura", "aprobar"
    ]
    palabras_laboral = [
        "trabajo", "laboral", "empleo", "profesion", "profesión", "profesional",
        "empresa", "empresas", "actuarial", "finanzas", "pasantia", "pasantía",
        "pasantias", "pasantías", "curriculum", "cv", "sueldo", "mercado", "futuro"
    ]

    tiene_carrera = any(p in t for p in palabras_carrera)
    tiene_laboral = any(p in t for p in palabras_laboral)

    if tiene_carrera and tiene_laboral:
        return 4
    elif tiene_laboral:
        return 3
    elif tiene_carrera:
        return 1
    else:
        return 2


def transformar_payload_a_3fn(
    payload: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any], List[int]]:
    """
    Valida el payload recibido del formulario y lo descompone en modelos de Tercera Forma Normal (3FN),
    calculando automáticamente las variables cuantitativas derivadas.

    Args:
        payload: Diccionario crudo proveniente de la interfaz de usuario con los campos:
            - cedula, nombre_completo, correo, id_seccion, edad, genero
            - ha_usado_excel, operaciones_seleccionadas (list[int])
            - interes_electiva, tiene_herramientas, id_percepcion, id_nivel

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], List[int]]:
            1. estudiante_data: Datos de dimensión personal.
            2. encuesta_data: Hecho transaccional de la encuesta (con 'cantidad_operaciones' calculada).
            3. operaciones_ids: Lista de IDs ordenados para la tabla puente 'encuesta_operaciones'.

    Raises:
        ValueError: Si alguna validación de frontera, tipo o dominio falla.
    """
    if not isinstance(payload, dict):
        raise ValueError("El payload de entrada debe ser un diccionario.")

    # 1. Validación de campos de identidad y dimensión de estudiante
    cedula = sanitizar_texto(payload.get("cedula"), "cédula")
    nombre_completo = sanitizar_texto(payload.get("nombre_completo"), "nombre_completo")
    correo = validar_correo(payload.get("correo"))

    # Sección (11 o 12)
    id_seccion = payload.get("id_seccion")
    if id_seccion not in VALID_SECCIONES:
        raise ValueError(f"La sección '{id_seccion}' es inválida. Valores permitidos: 11 o 12.")

    # Edad (15 a 75)
    edad = validar_edad(payload.get("edad"))

    # Género ('Femenino' o 'Masculino')
    genero = payload.get("genero")
    if genero not in VALID_GENEROS:
        raise ValueError(f"El género '{genero}' es inválido. Valores permitidos: {VALID_GENEROS}.")

    # 2. Validación de campos socio-académicos y de percepción
    ha_usado_excel = bool(payload.get("ha_usado_excel", False))
    interes_electiva = bool(payload.get("interes_electiva", False))
    tiene_herramientas = bool(payload.get("tiene_herramientas", False))

    id_percepcion = payload.get("id_percepcion")
    texto_percepcion = payload.get("texto_percepcion")

    if id_percepcion is None and texto_percepcion:
        id_percepcion = clasificar_texto_percepcion(sanitizar_texto(texto_percepcion, "texto_percepcion"))
    elif id_percepcion is None:
        raise ValueError("Debe proporcionar 'id_percepcion' o 'texto_percepcion'.")

    if id_percepcion not in VALID_PERCEPCIONES:
        raise ValueError(
            f"El id_percepcion '{id_percepcion}' es inválido. Valores permitidos: {VALID_PERCEPCIONES}."
        )

    id_nivel = payload.get("id_nivel")
    if id_nivel not in VALID_NIVELES:
        raise ValueError(
            f"El id_nivel ordinal '{id_nivel}' es inválido. Valores permitidos: {VALID_NIVELES}."
        )

    # 3. Lógica de Coherencia Transaccional y Cálculo Automático de Variables Derivadas
    # Camino A: Si el estudiante declara NO haber usado Excel, forzar 0 operaciones y lista vacía.
    # Camino B: Si usó Excel, validar y contar las operaciones seleccionadas únicas en [1..6].
    operaciones_raw = payload.get("operaciones_seleccionadas") or []
    if not isinstance(operaciones_raw, list):
        raise ValueError("Las operaciones seleccionadas deben proporcionarse como una lista.")

    operaciones_ids: List[int] = []
    if not ha_usado_excel:
        cantidad_operaciones = 0
        operaciones_ids = []
    else:
        # Extraer enteros válidos
        ops_set = set()
        for op in operaciones_raw:
            try:
                op_int = int(op)
            except (ValueError, TypeError) as err:
                raise ValueError(f"Identificador de operación inválido: {op}") from err

            if op_int not in VALID_OPERACIONES:
                raise ValueError(f"Operación con id {op_int} fuera del catálogo [1..6].")
            ops_set.add(op_int)

        operaciones_ids = sorted(list(ops_set))
        cantidad_operaciones = len(operaciones_ids)

    # 4. Construcción de modelos desacoplados en 3FN
    estudiante_data: Dict[str, Any] = {
        "cedula": cedula,
        "nombre_completo": nombre_completo,
        "correo": correo,
        "id_seccion": id_seccion,
        "edad": edad,
        "genero": genero,
    }

    encuesta_data: Dict[str, Any] = {
        "cedula": cedula,
        "ha_usado_excel": ha_usado_excel,
        "cantidad_operaciones": cantidad_operaciones,
        "interes_electiva": interes_electiva,
        "tiene_herramientas": tiene_herramientas,
        "id_percepcion": id_percepcion,
        "id_nivel": id_nivel,
    }

    logger.debug(
        "Payload transformado con éxito a 3FN para cédula %s (Cantidad de operaciones: %d)",
        cedula,
        cantidad_operaciones,
    )

    return estudiante_data, encuesta_data, operaciones_ids
