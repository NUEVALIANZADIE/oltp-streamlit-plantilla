# Manifiesto de Orquestación Multi-Agente (`AGENTS.md`)

Este repositorio opera bajo una arquitectura estricta de **Dos Agentes Especializados** con responsabilidades segregadas y auditoría cruzada obligatoria. Ningún agente actúa como "todero".

---

## 1. Catálogo de Agentes Activos

| ID del Agente | Archivo de Definición | Rol Principal | Directorios de Escritura Permitidos | Directorios Prohibidos (Solo Lectura) |
| :--- | :--- | :--- | :--- | :--- |
| **`@backend-dba`** | `.agents/backend_dba_agent.md` | Arquitecto de Datos (3FN), Pipeline ETL, Caché y Auditor de Seguridad | `src/database/`, `src/etl/`, `tests/` | `src/ui/`, `main.py`, `.env`, `requirements.txt` |
| **`@frontend-ui`** | `.agents/frontend_ui_agent.md` | Diseñador de Interfaz (Streamlit), Visualización (Matplotlib) y Despliegue | `src/ui/`, `main.py` | `src/database/`, `src/etl/`, `tests/`, `.env`, `requirements.txt` |

---

## 2. Protocolo de Orquestación y Handoff (Secuencia por Etapas)

Toda funcionalidad nueva se desarrolla siguiendo estrictamente este ciclo de 4 etapas con intervención humana:

1. **Etapa 1 — Ingesta de Contexto:**
   Ambos agentes leen obligatoriamente `.antigravity/rules.md` y los 4 archivos de `docs/` (`research_design.md`, `etl_system_design.md`, `brand_book.md`, `target_audience.md`) antes de proponer cualquier cambio.
2. **Etapa 2 — Ejecución de `@backend-dba` (Datos, ETL y Pruebas):**
   - Diseña y programa los módulos en `src/database/` y `src/etl/` garantizando la Tercera Forma Normal (3FN) y el encapsulamiento de caché (`@st.cache_data`) para proteger la capa gratuita de Supabase.
   - Invoca la skill `pytest-whitebox` para generar y ejecutar las pruebas unitarias en `tests/`.
   - **Guardarraíl Humano 1:** El humano revisa el resultado de `pytest` y aprueba el contrato de funciones que consumirá el Frontend.
3. **Etapa 3 — Ejecución de `@frontend-ui` (Formulario y Cuadro de Mando):**
   - Construye la interfaz en `src/ui/` y `main.py` invocando únicamente las funciones públicas expuestas por `src/etl/`.
   - Aplica la identidad visual de `docs/brand_book.md` y la ergonomía *mobile-first* de `docs/target_audience.md`.
4. **Etapa 4 — Auditoría Cruzada de Seguridad y Cierre Git:**
   - **`@backend-dba` audita a `@frontend-ui`:** Revisa `src/ui/` y `main.py` línea por línea para certificar que NO existan vulnerabilidades de inyección HTML/XSS, que NO se filtren credenciales de Supabase y que NO existan consultas a la base de datos fuera de la capa de caché.
   - Una vez emitido el dictamen `APROBADO POR SEGURIDAD DBA`, se activa la skill `git-conventions` para crear la rama y registrar el commit antes del Pull Request final.