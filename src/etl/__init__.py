"""
Módulo ETL del Sistema OLTP.
Expone funciones públicas para transformación, cálculo estadístico y consultas cacheadas.
"""

from src.etl.analytics import (
    aplanar_registros_encuestas,
    calcular_estadisticas_descriptivas,
    calcular_metricas_dashboard,
)
from src.etl.pipeline import (
    invalidar_cache_dashboard,
    obtener_catalogos,
    obtener_datos_dashboard,
    obtener_metricas_completas,
    registrar_encuesta,
)
from src.etl.transformers import (
    sanitizar_texto,
    transformar_payload_a_3fn,
    validar_correo,
    validar_edad,
)

__all__ = [
    "sanitizar_texto",
    "validar_correo",
    "validar_edad",
    "transformar_payload_a_3fn",
    "calcular_estadisticas_descriptivas",
    "aplanar_registros_encuestas",
    "calcular_metricas_dashboard",
    "registrar_encuesta",
    "obtener_datos_dashboard",
    "obtener_metricas_completas",
    "obtener_catalogos",
    "invalidar_cache_dashboard",
]
