---
name: code-style-python
description: Reglas de estilo de código en Python, tipado estático, docstrings y desacoplamiento modular entre Supabase, Pandas y Streamlit.
triggers:
  - escribir código python
  - crear módulo
  - refactorizar función
---

# Skill: Estándares de Redacción de Código en Python

## 1. Propósito
Mantener el código modular, legible, tipado y estrictamente desacoplado entre las capas de Base de Datos, ETL e Interfaz de Usuario.

## 2. Reglas de Escritura Obligatorias
1. **Type Hints Estrictos:** Toda función debe declarar los tipos de sus argumentos y su valor de retorno usando `typing` (ej. `def transformar_encuesta(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:`).
2. **Docstrings Concisos:** Toda función pública debe incluir un docstring breve indicando: propósito, parámetros de entrada, salida y excepciones levantadas (`ValueError`).
3. **Separación de Capas (Arquitectura Limpia):**
   - `src/database/`: Solo interactúa con el cliente SDK de Supabase. No importa `streamlit` ni `matplotlib`.
   - `src/etl/`: Contiene la validación de reglas de negocio, transformación a 3FN y cálculos estadísticos en `pandas`.
   - `src/ui/`: Renderiza componentes de `streamlit` y figuras de `matplotlib`. Nunca instancia el cliente de Supabase directamente.
4. **Manejo de Excepciones y Telemetría:** Prohibido usar `except Exception: pass`. Todo error debe ser capturado, registrado con `logging.error()` y devuelto con un mensaje seguro para el usuario.

## 3. Anti-Patrones Prohibidos
- ❌ Usar `st.write()` con `unsafe_allow_html=True` recibiendo datos de entrada del usuario.
- ❌ Llamar a `supabase.table().select()` dentro de un bucle o fuera de una función decorada con `@st.cache_data`.