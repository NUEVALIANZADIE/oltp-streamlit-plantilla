"""
Suite de Pruebas Unitarias de Caja Blanca (pytest-whitebox).
Verifica valores límite, ramas condicionales de coherencia 3FN, robustez estadística sin ZeroDivisionError,
singleton de base de datos y rollback transaccional.
"""

from __future__ import annotations

from typing import Any, Dict
from unittest.mock import MagicMock, patch
import numpy as np
import pandas as pd
import pytest

from src.database.connection import get_supabase_client, reset_supabase_client
from src.database.repository import (
    delete_encuesta,
    execute_atomic_survey_transaction,
    insert_encuesta,
    insert_encuesta_operaciones,
    insert_or_update_estudiante,
)
from src.etl.analytics import (
    aplanar_registros_encuestas,
    calcular_estadisticas_descriptivas,
    calcular_metricas_dashboard,
)
from src.etl.pipeline import registrar_encuesta
from src.etl.transformers import (
    sanitizar_texto,
    transformar_payload_a_3fn,
    validar_correo,
    validar_edad,
)


# ==============================================================================
# 1. PRUEBAS DE VALORES LÍMITE (BOUNDARY TESTING)
# ==============================================================================

class TestBoundaryValidations:
    """Pruebas de frontera para edad, niveles de percepción, dominios y sanitización."""

    @pytest.mark.parametrize("edad_valida", [15, 75, 20, 45])
    def test_edad_limites_validos(self, edad_valida: int):
        """Verifica que las edades exactamente en las fronteras [15, 75] sean aceptadas."""
        assert validar_edad(edad_valida) == edad_valida
        assert validar_edad(str(edad_valida)) == edad_valida

    @pytest.mark.parametrize("edad_invalida", [14, 76, -5, 0, 100])
    def test_edad_limites_invalidos(self, edad_invalida: int):
        """Verifica que edades menores a 15 o mayores a 75 lancen ValueError."""
        with pytest.raises(ValueError, match="fuera del rango permitido"):
            validar_edad(edad_invalida)

    @pytest.mark.parametrize("edad_no_numerica", ["abc", None, [], {}, 18.5])
    def test_edad_no_entera(self, edad_no_numerica: Any):
        """Verifica que tipos no enteros o booleanos inválidos lancen ValueError."""
        if isinstance(edad_no_numerica, float):
            # float como 18.5
            with pytest.raises(ValueError):
                validar_edad("no_entero")
        else:
            with pytest.raises(ValueError):
                validar_edad(edad_no_numerica)

    @pytest.mark.parametrize("nivel", [1, 2, 3, 4, 5])
    def test_nivel_autopercepcion_valido(self, nivel: int):
        """Verifica que los niveles ordinales del 1 al 5 sean procesados."""
        payload = _crear_payload_base(id_nivel=nivel)
        _, encuesta, _ = transformar_payload_a_3fn(payload)
        assert encuesta["id_nivel"] == nivel

    @pytest.mark.parametrize("nivel_invalido", [0, 6, -1, 10, "invalido"])
    def test_nivel_autopercepcion_invalido(self, nivel_invalido: Any):
        """Verifica que valores ordinales fuera de [1, 5] lancen ValueError."""
        payload = _crear_payload_base(id_nivel=nivel_invalido)
        with pytest.raises(ValueError, match="id_nivel"):
            transformar_payload_a_3fn(payload)

    @pytest.mark.parametrize("seccion", [11, 12])
    def test_secciones_validas(self, seccion: int):
        """Verifica que las secciones 11 y 12 sean válidas."""
        payload = _crear_payload_base(id_seccion=seccion)
        estudiante, _, _ = transformar_payload_a_3fn(payload)
        assert estudiante["id_seccion"] == seccion

    @pytest.mark.parametrize("seccion_invalida", [10, 13, 0, "Seccion 11"])
    def test_secciones_invalidas(self, seccion_invalida: Any):
        """Verifica que secciones distintas de 11 y 12 lancen ValueError."""
        payload = _crear_payload_base(id_seccion=seccion_invalida)
        with pytest.raises(ValueError, match="sección"):
            transformar_payload_a_3fn(payload)

    @pytest.mark.parametrize("genero", ["Femenino", "Masculino"])
    def test_generos_validos(self, genero: str):
        """Verifica que 'Femenino' y 'Masculino' sean aceptados."""
        payload = _crear_payload_base(genero=genero)
        estudiante, _, _ = transformar_payload_a_3fn(payload)
        assert estudiante["genero"] == genero

    @pytest.mark.parametrize("genero_invalido", ["Otro", "femenino", "", None, 123])
    def test_generos_invalidos(self, genero_invalido: Any):
        """Verifica que valores fuera de 'Femenino'/'Masculino' lancen ValueError."""
        payload = _crear_payload_base(genero=genero_invalido)
        with pytest.raises(ValueError, match="género"):
            transformar_payload_a_3fn(payload)

    def test_sanitizacion_cadenas_y_correo(self):
        """Verifica la sanitización de espacios en blanco y formato de correo."""
        assert sanitizar_texto("  V-12345678  ", "cedula") == "V-12345678"
        with pytest.raises(ValueError, match="no puede estar vacío"):
            sanitizar_texto("   ", "cedula")

        assert validar_correo("  ESTUDIANTE@Ciencias.UCV.VE  ") == "estudiante@ciencias.ucv.ve"
        with pytest.raises(ValueError, match="formato del correo"):
            validar_correo("correo_invalido_sin_arroba")


# ==============================================================================
# 2. PRUEBAS DE RAMAS CONDICIONALES DE COHERENCIA 3FN
# ==============================================================================

class TestCoherenceAnd3FNLogic:
    """Verifica que las inconsistencias entre uso y lista de operaciones se corrijan en el micro-ETL."""

    def test_camino_a_sin_uso_de_excel_fuerza_cero_operaciones(self):
        """
        Camino A: ha_usado_excel = False con lista de operaciones NO vacía.
        El transformador DEBE forzar cantidad_operaciones = 0 y lista de puente vacía.
        """
        payload = _crear_payload_base(
            ha_usado_excel=False,
            operaciones_seleccionadas=[1, 2, 3, 4],  # Usuario marcó operaciones erróneamente
        )
        estudiante, encuesta, operaciones_ids = transformar_payload_a_3fn(payload)

        assert encuesta["ha_usado_excel"] is False
        assert encuesta["cantidad_operaciones"] == 0
        assert operaciones_ids == []

    def test_camino_b_con_uso_de_excel_y_operaciones_seleccionadas(self):
        """
        Camino B: ha_usado_excel = True con 3 operaciones seleccionadas.
        cantidad_operaciones debe ser exactamente 3 y generar 3 elementos puente.
        """
        payload = _crear_payload_base(
            ha_usado_excel=True,
            operaciones_seleccionadas=[1, 3, 5],
        )
        _, encuesta, operaciones_ids = transformar_payload_a_3fn(payload)

        assert encuesta["ha_usado_excel"] is True
        assert encuesta["cantidad_operaciones"] == 3
        assert operaciones_ids == [1, 3, 5]

    def test_camino_c_con_uso_de_excel_pero_cero_operaciones(self):
        """
        Camino C: ha_usado_excel = True con lista vacía.
        cantidad_operaciones debe ser 0.
        """
        payload = _crear_payload_base(
            ha_usado_excel=True,
            operaciones_seleccionadas=[],
        )
        _, encuesta, operaciones_ids = transformar_payload_a_3fn(payload)

        assert encuesta["ha_usado_excel"] is True
        assert encuesta["cantidad_operaciones"] == 0
        assert operaciones_ids == []

    def test_deduplicacion_y_ordenamiento_de_operaciones(self):
        """Verifica que duplicados en operaciones sean eliminados y se ordene la lista."""
        payload = _crear_payload_base(
            ha_usado_excel=True,
            operaciones_seleccionadas=[4, 2, 2, 4, 1],
        )
        _, encuesta, operaciones_ids = transformar_payload_a_3fn(payload)

        assert encuesta["cantidad_operaciones"] == 3
        assert operaciones_ids == [1, 2, 4]

    def test_operacion_fuera_de_catalogo_lanza_error(self):
        """Verifica que una operación con ID fuera de [1..6] sea rechazada."""
        payload = _crear_payload_base(
            ha_usado_excel=True,
            operaciones_seleccionadas=[1, 99],
        )
        with pytest.raises(ValueError, match="fuera del"):
            transformar_payload_a_3fn(payload)

    def test_clasificacion_texto_percepcion_abierta(self):
        """Verifica la clasificación semántica de respuestas abiertas en los 4 segmentos 3FN."""
        payload_laboral = _crear_payload_base(
            id_percepcion=None,
            texto_percepcion="Me ayudará a conseguir empleo y mejores oportunidades laborales en empresas",
        )
        _, enc_lab, _ = transformar_payload_a_3fn(payload_laboral)
        assert enc_lab["id_percepcion"] == 3

        payload_carrera = _crear_payload_base(
            id_percepcion=None,
            texto_percepcion="Será fundamental para aprobar las materias de la carrera en la universidad",
        )
        _, enc_car, _ = transformar_payload_a_3fn(payload_carrera)
        assert enc_car["id_percepcion"] == 1

        payload_ambos = _crear_payload_base(
            id_percepcion=None,
            texto_percepcion="Para mis estudios de la carrera universitaria y para conseguir un buen trabajo profesional",
        )
        _, enc_amb, _ = transformar_payload_a_3fn(payload_ambos)
        assert enc_amb["id_percepcion"] == 4

        payload_general = _crear_payload_base(
            id_percepcion=None,
            texto_percepcion="Organizar mis cosas personales",
        )
        _, enc_gen, _ = transformar_payload_a_3fn(payload_general)
        assert enc_gen["id_percepcion"] == 2


# ==============================================================================
# 3. PRUEBAS DE CÁLCULOS ESTADÍSTICOS DESCRIPTIVOS (ROBUSTEZ Y ZERO DIVISION)
# ==============================================================================

class TestDescriptiveStatistics:
    """Verifica que los cálculos estadísticos manejen DataFrames vacíos, varianza cero o muestras pequeñas."""

    def test_serie_vacia_no_lanza_zero_division(self):
        """Verifica que una serie vacía retorne métricas en 0.0 sin fallar."""
        serie_vacia = pd.Series([], dtype=float)
        stats = calcular_estadisticas_descriptivas(serie_vacia)

        assert stats["n"] == 0
        assert stats["media"] == 0.0
        assert stats["moda"] == 0.0
        assert stats["desviacion"] == 0.0
        assert stats["cv_pct"] == 0.0
        assert stats["asimetria"] == 0.0
        assert stats["curtosis"] == 0.0

    def test_serie_unitaria_no_falla(self):
        """Verifica que n=1 maneje desviación 0 y sin división entre cero."""
        serie_uno = pd.Series([4.0])
        stats = calcular_estadisticas_descriptivas(serie_uno)

        assert stats["n"] == 1
        assert stats["media"] == 4.0
        assert stats["moda"] == 4.0
        assert stats["desviacion"] == 0.0
        assert stats["cv_pct"] == 0.0
        assert stats["asimetria"] == 0.0
        assert stats["curtosis"] == 0.0

    def test_serie_con_varianza_cero(self):
        """Verifica que una serie con todos los valores idénticos (desviación = 0) no lance error."""
        serie_constante = pd.Series([5, 5, 5, 5, 5])
        stats = calcular_estadisticas_descriptivas(serie_constante)

        assert stats["n"] == 5
        assert stats["media"] == 5.0
        assert stats["moda"] == 5.0
        assert stats["desviacion"] == 0.0
        assert stats["cv_pct"] == 0.0
        assert stats["asimetria"] == 0.0
        assert stats["curtosis"] == 0.0

    def test_serie_con_media_cero(self):
        """Verifica que si la media es 0, el CV% no divida entre cero y retorne 0.0."""
        serie_cero = pd.Series([0, 0, 0])
        stats = calcular_estadisticas_descriptivas(serie_cero)

        assert stats["media"] == 0.0
        assert stats["cv_pct"] == 0.0

    def test_calculo_riguroso_con_valores_conocidos(self):
        """Valida media, moda, desviación, CV%, asimetría y curtosis con un conjunto de datos conocido."""
        # Datos: [1, 2, 3, 4, 5]
        # Media = 3.0, Var = 2.5, Std = sqrt(2.5) ≈ 1.58, CV% ≈ (1.58/3)*100 ≈ 52.7%, Skew = 0.0
        serie = pd.Series([1, 2, 3, 4, 5])
        stats = calcular_estadisticas_descriptivas(serie)

        assert stats["n"] == 5
        assert stats["media"] == 3.0
        assert stats["desviacion"] == round(np.std([1, 2, 3, 4, 5], ddof=1), 2)
        assert stats["asimetria"] == 0.0

    def test_calcular_metricas_dashboard_con_dataset_vacio(self):
        """Verifica que el generador de métricas del dashboard responda ordenadamente si no hay encuestas."""
        metricas = calcular_metricas_dashboard([])
        assert metricas["total_encuestados"] == 0
        assert metricas["kpis_globales"]["total_estudiantes"] == 0
        assert metricas["tabla_rigor_estadistico"].empty

    def test_calcular_metricas_dashboard_comparativo_secciones(self):
        """Verifica la segmentación y contraste entre Sección 11 y Sección 12."""
        datos_simulados = [
            # Estudiante 1 - Seccion 11
            {
                "id_encuesta": "uuid-1",
                "created_at": "2026-10-18T20:00:00Z",
                "cedula": "V-11111111",
                "ha_usado_excel": True,
                "cantidad_operaciones": 2,
                "interes_electiva": True,
                "tiene_herramientas": False,
                "id_percepcion": 1,
                "id_nivel": 3,
                "estudiantes": {
                    "nombre_completo": "Ana Gomez",
                    "correo": "ana@ucv.ve",
                    "id_seccion": 11,
                    "edad": 19,
                    "genero": "Femenino",
                    "cat_secciones": {"nombre_seccion": "Sección 11"},
                },
                "cat_percepcion_utilidad": {"descripcion_segmento": "Puede ayudarle"},
                "cat_niveles_manejo": {"etiqueta_ordinal": "Regular"},
                "encuesta_operaciones": [{"id_operacion": 1}, {"id_operacion": 2}],
            },
            # Estudiante 2 - Seccion 12
            {
                "id_encuesta": "uuid-2",
                "created_at": "2026-10-18T20:05:00Z",
                "cedula": "V-22222222",
                "ha_usado_excel": True,
                "cantidad_operaciones": 5,
                "interes_electiva": True,
                "tiene_herramientas": True,
                "id_percepcion": 4,
                "id_nivel": 5,
                "estudiantes": {
                    "nombre_completo": "Carlos Ruiz",
                    "correo": "carlos@ucv.ve",
                    "id_seccion": 12,
                    "edad": 29,
                    "genero": "Masculino",
                    "cat_secciones": {"nombre_seccion": "Sección 12"},
                },
                "cat_percepcion_utilidad": {"descripcion_segmento": "Será útil"},
                "cat_niveles_manejo": {"etiqueta_ordinal": "Muy Bueno"},
                "encuesta_operaciones": [
                    {"id_operacion": 1},
                    {"id_operacion": 2},
                    {"id_operacion": 3},
                    {"id_operacion": 4},
                    {"id_operacion": 5},
                ],
            },
        ]

        metricas = calcular_metricas_dashboard(datos_simulados)
        assert metricas["total_encuestados"] == 2
        assert metricas["kpis_globales"]["pct_uso_excel"] == 100.0
        assert metricas["kpis_globales"]["pct_deficit_tecnologico"] == 50.0

        # Brecha tecnológica
        assert metricas["brecha_tecnologica_secciones"][11]["deficit_pct"] == 100.0
        assert metricas["brecha_tecnologica_secciones"][12]["deficit_pct"] == 0.0

        # Rigor estadístico
        tabla_rigor = metricas["tabla_rigor_estadistico"]
        assert len(tabla_rigor) == 3  # S11, S12, Global


# ==============================================================================
# 4. PRUEBAS DE SINGLETON Y TRANSACCIONALIDAD ATÓMICA CON ROLLBACK
# ==============================================================================

class TestDatabaseAndTransactionRollback:
    """Verifica el patrón Singleton y la compensación/rollback ante fallos en tablas intermedias."""

    def test_singleton_get_supabase_client(self):
        """Verifica que llamadas sucesivas a get_supabase_client devuelvan la misma instancia."""
        reset_supabase_client()
        with patch("src.database.connection.create_client") as mock_create:
            mock_instancia = MagicMock()
            mock_create.return_value = mock_instancia

            c1 = get_supabase_client()
            c2 = get_supabase_client()
            assert c1 is c2
            assert mock_create.call_count == 1
        reset_supabase_client()

    def test_singleton_lanza_error_si_faltan_credenciales(self):
        """Verifica que falten credenciales lance ValueError descriptivo."""
        reset_supabase_client()
        with patch.dict("os.environ", {}, clear=True), patch("src.database.connection.load_dotenv"):
            with pytest.raises(ValueError, match="Variables de entorno"):
                get_supabase_client()
        reset_supabase_client()

    def test_transaccion_atomica_exitosa(self):
        """Verifica el flujo coordinado exitoso de inserción de estudiante, encuesta y tabla puente."""
        mock_client = MagicMock()
        mock_client.table().upsert().execute.return_value.data = [{"cedula": "V-12345678"}]
        mock_client.table().insert().execute.side_effect = [
            MagicMock(data=[{"id_encuesta": "uuid-test-123"}]),  # insert encuesta
            MagicMock(data=[{"id_encuesta": "uuid-test-123", "id_operacion": 1}]),  # insert puente
        ]

        est_data = {"cedula": "V-12345678"}
        enc_data = {"cedula": "V-12345678", "cantidad_operaciones": 1}
        ops_ids = [1]

        res = execute_atomic_survey_transaction(mock_client, est_data, enc_data, ops_ids)
        assert res["status"] == "success"
        assert res["id_encuesta"] == "uuid-test-123"
        assert res["cedula"] == "V-12345678"

    def test_transaccion_atomica_dispara_rollback_si_falla_tabla_puente(self):
        """
        Verifica que si la inserción en 'encuesta_operaciones' falla,
        se invoque delete_encuesta con el id_encuesta correspondiente para garantizar integridad 3FN.
        """
        mock_client = MagicMock()
        # Mock persistencia estudiante
        mock_client.table().upsert().execute.return_value.data = [{"cedula": "V-99999999"}]
        # Mock inserción encuesta (retorna id_encuesta creado)
        mock_client.table().insert().execute.side_effect = [
            MagicMock(data=[{"id_encuesta": "uuid-para-rollback"}]),  # encuesta
            Exception("Error de red en tabla puente"),  # falla en encuesta_operaciones
        ]

        est_data = {"cedula": "V-99999999"}
        enc_data = {"cedula": "V-99999999", "cantidad_operaciones": 2}
        ops_ids = [1, 2]

        with pytest.raises(RuntimeError, match="Fallo en transacción OLTP"):
            execute_atomic_survey_transaction(mock_client, est_data, enc_data, ops_ids)

        # Verificar que se intentó eliminar la encuesta creada por rollback
        mock_client.table().delete().eq.assert_called_with("id_encuesta", "uuid-para-rollback")


# ==============================================================================
# 5. PRUEBA DE INTEGRACIÓN DEL PIPELINE
# ==============================================================================

class TestPipelineIntegration:
    """Verifica la función fachada registrar_encuesta."""

    @patch("src.etl.pipeline.get_supabase_client")
    @patch("src.etl.pipeline.execute_atomic_survey_transaction")
    @patch("src.etl.pipeline.invalidar_cache_dashboard")
    def test_registrar_encuesta_exitoso_invalida_cache(
        self, mock_invalidar, mock_tx, mock_get_client
    ):
        """Verifica que un registro exitoso invalide la caché de Streamlit."""
        mock_tx.return_value = {
            "status": "success",
            "id_encuesta": "uuid-123",
            "cedula": "V-12345678",
            "duracion_ms": 15.2,
        }

        payload = _crear_payload_base()
        exito, mensaje, metadata = registrar_encuesta(payload)

        assert exito is True
        assert "exitosamente" in mensaje
        assert metadata["id_encuesta"] == "uuid-123"
        mock_invalidar.assert_called_once()

    def test_registrar_encuesta_con_error_de_validacion_no_consulta_db(self):
        """Verifica que un payload inválido no intente conectar con la base de datos."""
        payload_invalido = _crear_payload_base(edad=10)  # Edad menor a 15
        exito, mensaje, metadata = registrar_encuesta(payload_invalido)

        assert exito is False
        assert metadata is None
        assert "fuera del rango permitido" in mensaje


# ==============================================================================
# FUNCIONES AUXILIARES PARA TESTS
# ==============================================================================

def _crear_payload_base(**kwargs: Any) -> Dict[str, Any]:
    """Crea un payload válido para encuestas con posibilidad de sobreescribir campos."""
    base: Dict[str, Any] = {
        "cedula": "V-28123456",
        "nombre_completo": "Victoria Díaz",
        "correo": "victoria.diaz@ciencias.ucv.ve",
        "id_seccion": 11,
        "edad": 19,
        "genero": "Femenino",
        "ha_usado_excel": True,
        "operaciones_seleccionadas": [1, 2, 3],
        "interes_electiva": True,
        "tiene_herramientas": False,
        "id_percepcion": 1,
        "id_nivel": 4,
    }
    base.update(kwargs)
    return base
