"""
Módulo de análisis estadístico descriptivo y cálculo de métricas para el Cuadro de Mando.
Opera exclusivamente con Pandas, implementando rigor matemático y protección total contra ZeroDivisionError.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CAT_OPERACIONES = {
    1: "Sumar",
    2: "Restar",
    3: "Multiplicar",
    4: "Dividir",
    5: "Crear gráficos",
    6: "Crear tablas dinámicas",
}

CAT_NIVELES = {
    1: "1: Muy Malo",
    2: "2: Malo",
    3: "3: Regular",
    4: "4: Bueno",
    5: "5: Muy Bueno",
}

CAT_PERCEPCIONES = {
    1: "Puede ayudarle y facilitarle la carrera",
    2: "Le será útil para diversos fines generales",
    3: "Brindará mejores oportunidades en el ámbito laboral",
    4: "Será útil tanto en la carrera como en el ámbito laboral",
}


def calcular_estadisticas_descriptivas(serie: pd.Series) -> Dict[str, Any]:
    """
    Calcula las medidas formales de la estadística descriptiva:
    Media, Moda, Desviación Estándar, Coeficiente de Variación, Asimetría y Curtosis.

    Garantiza robustez matemática frente a series vacías, muestras unitarias o varianza nula.

    Args:
        serie: Serie de Pandas con valores numéricos discretos o continuos.

    Returns:
        Dict[str, Any]: Diccionario con las métricas calculadas y redondeadas:
            - 'n': Tamaño muestral.
            - 'media': Media aritmética (x̄).
            - 'moda': Moda más frecuente (Mo).
            - 'desviacion': Desviación estándar muestral (S, ddof=1).
            - 'cv_pct': Coeficiente de variación porcentual (CV%).
            - 'asimetria': Coeficiente de asimetría de Fisher-Pearson.
            - 'curtosis': Coeficiente de curtosis de Fisher (exceso de curtosis).
    """
    if serie is None or serie.empty:
        return {
            "n": 0,
            "media": 0.0,
            "moda": 0.0,
            "desviacion": 0.0,
            "cv_pct": 0.0,
            "asimetria": 0.0,
            "curtosis": 0.0,
        }

    s_clean = pd.to_numeric(serie.dropna(), errors="coerce").dropna()
    n = len(s_clean)

    if n == 0:
        return {
            "n": 0,
            "media": 0.0,
            "moda": 0.0,
            "desviacion": 0.0,
            "cv_pct": 0.0,
            "asimetria": 0.0,
            "curtosis": 0.0,
        }

    media = float(s_clean.mean())

    # Cálculo seguro de la moda
    modes = s_clean.mode()
    moda = float(modes.iloc[0]) if not modes.empty else media

    # Desviación estándar muestral (requiere n >= 2)
    std = float(s_clean.std(ddof=1)) if n > 1 else 0.0
    if np.isnan(std):
        std = 0.0

    # Coeficiente de Variación porcentual (CV%)
    # Evita división entre cero si la media es nula o la desviación es cero
    if media != 0.0 and std > 0.0:
        cv_pct = float((std / abs(media)) * 100.0)
    else:
        cv_pct = 0.0

    # Asimetría (requiere n >= 3 y varianza > 0)
    skew = float(s_clean.skew()) if n >= 3 and std > 0.0 else 0.0
    if np.isnan(skew):
        skew = 0.0

    # Curtosis (requiere n >= 4 y varianza > 0)
    kurt = float(s_clean.kurt()) if n >= 4 and std > 0.0 else 0.0
    if np.isnan(kurt):
        kurt = 0.0

    return {
        "n": n,
        "media": round(media, 2),
        "moda": round(moda, 2),
        "desviacion": round(std, 2),
        "cv_pct": round(cv_pct, 2),
        "asimetria": round(skew, 2),
        "curtosis": round(kurt, 2),
    }


def aplanar_registros_encuestas(surveys_raw: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Desanida la estructura relacional proveniente de Supabase PostgREST en un DataFrame plano.

    Args:
        surveys_raw: Lista de diccionarios retornados por la consulta con relaciones anidadas.

    Returns:
        pd.DataFrame: DataFrame consolidado con una fila por encuesta.
    """
    if not surveys_raw:
        return pd.DataFrame(
            columns=[
                "id_encuesta",
                "created_at",
                "cedula",
                "nombre_completo",
                "correo",
                "id_seccion",
                "nombre_seccion",
                "edad",
                "genero",
                "ha_usado_excel",
                "cantidad_operaciones",
                "interes_electiva",
                "tiene_herramientas",
                "id_percepcion",
                "descripcion_percepcion",
                "id_nivel",
                "etiqueta_nivel",
                "operaciones_ids",
            ]
        )

    filas: List[Dict[str, Any]] = []
    for item in surveys_raw:
        est = item.get("estudiantes") or {}
        sec = est.get("cat_secciones") or {}
        perc = item.get("cat_percepcion_utilidad") or {}
        niv = item.get("cat_niveles_manejo") or {}
        ops_rels = item.get("encuesta_operaciones") or []

        ops_ids = [op.get("id_operacion") for op in ops_rels if op.get("id_operacion")]

        fila = {
            "id_encuesta": item.get("id_encuesta"),
            "created_at": item.get("created_at"),
            "cedula": item.get("cedula"),
            "nombre_completo": est.get("nombre_completo", ""),
            "correo": est.get("correo", ""),
            "id_seccion": est.get("id_seccion"),
            "nombre_seccion": sec.get("nombre_seccion", f"Sección {est.get('id_seccion')}"),
            "edad": est.get("edad"),
            "genero": est.get("genero"),
            "ha_usado_excel": bool(item.get("ha_usado_excel", False)),
            "cantidad_operaciones": item.get("cantidad_operaciones", 0),
            "interes_electiva": bool(item.get("interes_electiva", False)),
            "tiene_herramientas": bool(item.get("tiene_herramientas", False)),
            "id_percepcion": item.get("id_percepcion"),
            "descripcion_percepcion": perc.get(
                "descripcion_segmento", CAT_PERCEPCIONES.get(item.get("id_percepcion"), "")
            ),
            "id_nivel": item.get("id_nivel"),
            "etiqueta_nivel": niv.get(
                "etiqueta_ordinal", CAT_NIVELES.get(item.get("id_nivel"), "")
            ),
            "operaciones_ids": ops_ids,
        }
        filas.append(fila)

    return pd.DataFrame(filas)


def calcular_metricas_dashboard(
    data: Union[pd.DataFrame, List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    Calcula el consolidado integral de métricas analíticas para el Cuadro de Mando.

    Args:
        data: DataFrame procesado o lista cruda de encuestas provenientes de Supabase.

    Returns:
        Dict[str, Any]: Estructura jerárquica con:
            - 'kpis_globales': Total estudiantes, % uso de excel, % interés electiva, % déficit tecnológico.
            - 'tabla_rigor_estadistico': DataFrame comparativo con Media, Moda, Std, CV%, Asimetría y Curtosis.
            - 'frecuencia_operaciones_por_seccion': Desglose de 0 a 6 operaciones para Sección 11 y 12.
            - 'operaciones_especificas_pct': Porcentaje de dominio para cada una de las 6 operaciones básicas.
            - 'brecha_tecnologica_secciones': % de disponibilidad tecnológica en Sección 11 vs. Sección 12.
            - 'distribucion_percepcion': Distribución de los 4 segmentos de utilidad esperada.
            - 'distribucion_autoevaluacion': Distribución ordinal de autoevaluación (1 al 5).
    """
    if isinstance(data, list):
        df = aplanar_registros_encuestas(data)
    else:
        df = data.copy()

    total_estudiantes = len(df)

    if total_estudiantes == 0:
        tabla_vacia = pd.DataFrame(
            columns=["Sección", "n", "Media (x̄)", "Moda (Mo)", "Desv. Est. (S)", "CV (%)", "Asimetría", "Curtosis"]
        )
        return {
            "total_encuestados": 0,
            "kpis_globales": {
                "total_estudiantes": 0,
                "pct_uso_excel": 0.0,
                "pct_interes_electiva": 0.0,
                "pct_deficit_tecnologico": 0.0,
            },
            "tabla_rigor_estadistico": tabla_vacia,
            "frecuencia_operaciones_por_seccion": pd.DataFrame({"Cantidad Operaciones": list(range(7))}),
            "operaciones_especificas_pct": {op_name: 0.0 for op_name in CAT_OPERACIONES.values()},
            "brecha_tecnologica_secciones": {
                11: {"con_herramientas_pct": 0.0, "deficit_pct": 0.0, "n": 0},
                12: {"con_herramientas_pct": 0.0, "deficit_pct": 0.0, "n": 0},
            },
            "distribucion_percepcion": {desc: 0 for desc in CAT_PERCEPCIONES.values()},
            "distribucion_autoevaluacion": {CAT_NIVELES[i]: 0 for i in range(1, 6)},
        }

    # 1. KPIs Globales
    pct_uso = (df["ha_usado_excel"].sum() / total_estudiantes) * 100.0
    pct_interes = (df["interes_electiva"].sum() / total_estudiantes) * 100.0
    pct_deficit = ((~df["tiene_herramientas"]).sum() / total_estudiantes) * 100.0

    kpis_globales = {
        "total_estudiantes": total_estudiantes,
        "pct_uso_excel": round(float(pct_uso), 2),
        "pct_interes_electiva": round(float(pct_interes), 2),
        "pct_deficit_tecnologico": round(float(pct_deficit), 2),
    }

    # 2. Tabla de Rigor Estadístico Comparativa (Sección 11 vs Sección 12 vs Global)
    df_s11 = df[df["id_seccion"] == 11]
    df_s12 = df[df["id_seccion"] == 12]

    stats_s11 = calcular_estadisticas_descriptivas(df_s11["cantidad_operaciones"])
    stats_s12 = calcular_estadisticas_descriptivas(df_s12["cantidad_operaciones"])
    stats_global = calcular_estadisticas_descriptivas(df["cantidad_operaciones"])

    filas_tabla = [
        {
            "Sección": "Sección 11 (Cohorte Joven)",
            "n": stats_s11["n"],
            "Media (x̄)": stats_s11["media"],
            "Moda (Mo)": stats_s11["moda"],
            "Desv. Est. (S)": stats_s11["desviacion"],
            "CV (%)": stats_s11["cv_pct"],
            "Asimetría": stats_s11["asimetria"],
            "Curtosis": stats_s11["curtosis"],
        },
        {
            "Sección": "Sección 12 (Cohorte Adulta)",
            "n": stats_s12["n"],
            "Media (x̄)": stats_s12["media"],
            "Moda (Mo)": stats_s12["moda"],
            "Desv. Est. (S)": stats_s12["desviacion"],
            "CV (%)": stats_s12["cv_pct"],
            "Asimetría": stats_s12["asimetria"],
            "Curtosis": stats_s12["curtosis"],
        },
        {
            "Sección": "Global Propedéutico",
            "n": stats_global["n"],
            "Media (x̄)": stats_global["media"],
            "Moda (Mo)": stats_global["moda"],
            "Desv. Est. (S)": stats_global["desviacion"],
            "CV (%)": stats_global["cv_pct"],
            "Asimetría": stats_global["asimetria"],
            "Curtosis": stats_global["curtosis"],
        },
    ]
    tabla_rigor = pd.DataFrame(filas_tabla)

    # 3. Frecuencia de Cantidad de Operaciones (0 al 6) por Sección
    rango_operaciones = list(range(7))
    conteo_s11 = df_s11["cantidad_operaciones"].value_counts().to_dict() if len(df_s11) > 0 else {}
    conteo_s12 = df_s12["cantidad_operaciones"].value_counts().to_dict() if len(df_s12) > 0 else {}

    df_frec_ops = pd.DataFrame({
        "Cantidad Operaciones": rango_operaciones,
        "Sección 11": [conteo_s11.get(k, 0) for k in rango_operaciones],
        "Sección 12": [conteo_s12.get(k, 0) for k in rango_operaciones],
    })

    # 4. Porcentaje de Dominio por Operación Específica (1 al 6)
    operaciones_especificas: Dict[str, float] = {}
    todas_ops_list = []
    for ops in df["operaciones_ids"]:
        if isinstance(ops, list):
            todas_ops_list.extend(ops)

    for op_id, op_nombre in CAT_OPERACIONES.items():
        if total_estudiantes > 0:
            count_op = sum(1 for ops in df["operaciones_ids"] if isinstance(ops, list) and op_id in ops)
            pct_op = (count_op / total_estudiantes) * 100.0
            operaciones_especificas[op_nombre] = round(float(pct_op), 2)
        else:
            operaciones_especificas[op_nombre] = 0.0

    # 5. Brecha Tecnológica por Sección
    def _calcular_brecha_seccion(sub_df: pd.DataFrame) -> Dict[str, Any]:
        n_sec = len(sub_df)
        if n_sec == 0:
            return {"con_herramientas_pct": 0.0, "deficit_pct": 0.0, "n": 0}
        con_herramientas = sub_df["tiene_herramientas"].sum()
        con_pct = (con_herramientas / n_sec) * 100.0
        deficit_pct = 100.0 - con_pct
        return {
            "con_herramientas_pct": round(float(con_pct), 2),
            "deficit_pct": round(float(deficit_pct), 2),
            "n": n_sec,
        }

    brecha_tecnologica = {
        11: _calcular_brecha_seccion(df_s11),
        12: _calcular_brecha_seccion(df_s12),
    }

    # 6. Distribución de Percepciones de Utilidad
    conteo_percepcion = df["id_percepcion"].value_counts().to_dict()
    dist_percepcion = {
        CAT_PERCEPCIONES[k]: conteo_percepcion.get(k, 0) for k in sorted(CAT_PERCEPCIONES.keys())
    }

    # 7. Distribución Ordinal de Autoevaluación (1 al 5)
    conteo_niveles = df["id_nivel"].value_counts().to_dict()
    dist_autoevaluacion = {
        CAT_NIVELES[k]: conteo_niveles.get(k, 0) for k in sorted(CAT_NIVELES.keys())
    }

    return {
        "total_encuestados": total_estudiantes,
        "kpis_globales": kpis_globales,
        "tabla_rigor_estadistico": tabla_rigor,
        "frecuencia_operaciones_por_seccion": df_frec_ops,
        "operaciones_especificas_pct": operaciones_especificas,
        "brecha_tecnologica_secciones": brecha_tecnologica,
        "distribucion_percepcion": dist_percepcion,
        "distribucion_autoevaluacion": dist_autoevaluacion,
    }
