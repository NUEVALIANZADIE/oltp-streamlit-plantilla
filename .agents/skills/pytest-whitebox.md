---
name: pytest-whitebox
description: Diseño y ejecución de pruebas unitarias de caja blanca con pytest para validar la lógica interna del ETL y las restricciones 3FN.
triggers:
  - ejecutar pruebas
  - crear tests
  - validar etl
  - pytest
---

# Skill: Pruebas de Caja Blanca Automatizadas con Pytest

## 1. Propósito
Verificar todos los caminos lógicos, ramas condicionales, límites numéricos y estructuras de datos en `src/etl/` antes de integrar con Supabase o con la interfaz de Streamlit.

## 2. Cobertura Obligatoria de Caja Blanca (`tests/test_etl_whitebox.py`)
Cada suite de pruebas debe evaluar explícitamente:
1. **Valores Límite (Boundary Testing):**
   - Edad exactamente en los bordes permitidos (`15` y `75` años -> Válido) y fuera de rango (`14`, `76`, `-5` -> Lanza `ValueError`).
   - Nivel de autopercepción ordinal entre `1` y `5`.
2. **Ramas Condicionales de Coherencia:**
   - Camino A: `ha_usado_excel = False` con lista de operaciones no vacía -> El transformador DEBE forzar `cantidad_operaciones = 0` y vaciar la lista de la tabla puente.
   - Camino B: `ha_usado_excel = True` con 3 operaciones seleccionadas -> `cantidad_operaciones` debe ser exactamente `3` y generar 3 diccionarios para `encuesta_operaciones`.
3. **Cálculos Estadísticos Descriptivos:**
   - Verificar que el cálculo de Media, Moda, Desviación Estándar, Coeficiente de Variación ($CV$), Asimetría y Curtosis maneje correctamente DataFrames vacíos o con varianza cero sin lanzar `ZeroDivisionError`.

## 3. Comando de Ejecución
El agente debe correr:
`pytest tests/ -v --tb=short`
Ninguna tarea puede darse por terminada si al menos un test falla.