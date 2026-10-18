# Reglas Estandarizadas de Arquitectura y Agentes — Sistema OLTP + Streamlit

## 1. Stack Tecnológico e Intolerancias de Arquitectura
- El proyecto utiliza exclusivamente Python (3.10+), Streamlit, Pandas, Matplotlib y el SDK oficial de Supabase (`supabase-py`).
- PROHIBIDO el uso de consultas SQL directas o concatenadas en cadenas de texto; toda transacción debe ejecutarse mediante los métodos del cliente SDK de Supabase.
- PROHIBIDO agregar otros gestores de bases de datos, ORMs adicionales o librerías de visualización fuera de Matplotlib.

## 2. Separación de Roles Agénticos y Seguridad
- **Agente Backend (DBA & ETL):** Responsable exclusivo de `src/database/`, `src/etl/` y `tests/`. Garantiza la Tercera Forma Normal (3FN), la integridad referencial y la protección de la capa gratuita de Supabase.
- **Agente Frontend (UI & Despliegue):** Responsable exclusivo de `src/ui/` y `main.py`. Construye el formulario dinámico y el Cuadro de Mando siguiendo estrictamente `docs/brand_book.md` y `docs/target_audience.md`.
- **Auditoría Cruzada Obligatoria:** El Agente Backend DEBE auditar cada entrega del Agente Frontend antes de cualquier commit para verificar:
  1. Sanitización de inputs (cero vulnerabilidades de inyección HTML/XSS en Streamlit).
  2. Cero exposición de credenciales (`SUPABASE_URL`, `SUPABASE_KEY`) en el cliente o logs.
  3. Cero llamadas al cliente de Supabase desde `src/ui/` que se salten la capa de caché de `src/etl/`.

## 3. Protección de Capa Gratuita y Telemetría
- El Cuadro de Mando (Dashboard) NO puede consultar a Supabase en cada re-renderizado de Streamlit.
- Es obligatorio encapsular las lecturas del dashboard con `@st.cache_data(ttl=900)` e invalidar la caché únicamente tras una inserción transaccional exitosa.
- Cada módulo principal de transformación e inserción debe registrar eventos básicos de telemetría (éxito/fallo de transacción y tiempo de respuesta) mediante el módulo `logging` de Python.

## 4. Gestión de Contexto, Flujo Incremental y Guardarraíles Humanos
- Antes de iniciar cualquier tarea, los agentes DEBEN leer los 4 documentos de la carpeta `docs/` (`research_design.md`, `etl_system_design.md`, `brand_book.md`, `target_audience.md`).
- Los agentes NO tienen permitido modificar archivos clave de configuración (`.env`, `requirements.txt`, `.antigravity/rules.md`).
- El desarrollo se ejecuta por etapas modulares. Ninguna etapa pasa a fusión (`merge`) sin aprobar todas las pruebas de caja blanca en `pytest` y recibir aprobación humana explícita.