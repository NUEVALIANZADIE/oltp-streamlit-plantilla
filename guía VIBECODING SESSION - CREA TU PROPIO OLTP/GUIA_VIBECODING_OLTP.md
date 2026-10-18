# VIBECODING SESSION: CREA TU PROPIO SISTEMA OLTP + STREAMLIT
## Guía Metodológica, Arquitectura de Datos y Orquestación Multi-Agente

**Institución:** Escuela de Estadística y Ciencias Actuariales (EECA - UCV)  
**IDE Agéntico:** Google Antigravity  
**Stack Tecnológico:** Python 3.10+, Streamlit, Pandas, Matplotlib, Supabase Cloud (PostgreSQL)  
**Propósito Didáctico:** Documento integral de referencia para estudiantes y docentes que explica cómo construir un sistema transaccional en tiempo real (OLTP) acoplado a un micro-ETL y un Cuadro de Mando estadístico, utilizando agentes especializados de Inteligencia Artificial sin improvisación.

---

## 🎯 Meta General del Proyecto (Goal)

Desarrollar una aplicación web interactiva en **Streamlit** utilizando como IDE agéntico **Google Antigravity**, creando un sistema **OLTP** (*Online Transaction Processing*) para capturar información mediante un formulario dinámico desplegado en la nube, procesado mediante un **pipeline ETL integrado en tiempo real**:

```
 ┌──────────────────────┐       ┌────────────────────────┐       ┌──────────────────────┐
 │   EXTRACCIÓN (E)     │  ──►  │   TRANSFORMACIÓN (T)   │  ──►  │      CARGA (L)       │
 │ Formulario Streamlit │       │ Validación, Limpieza y │       │ Base 3FN en Supabase │
 │ (Widgets Reactivos)  │       │ Cálculo Automático RAM │       │ + Caché en Dashboard │
 └──────────────────────┘       └────────────────────────┘       └──────────────────────┘
```

1. **Extracción (Extract):** Captura síncrona de los datos ingresados en el formulario web de Streamlit, mapeando cada campo hacia las variables del instrumento de recolección.
2. **Transformación (Transform):** Conversión de las respuestas en registros relacionales normalizados en **Tercera Forma Normal (3FN)**. Un sistema OLTP captura transacciones del día a día con total integridad y cero redundancia.
3. **Carga (Load):** Inserción atómica en **Supabase** (PostgreSQL en la nube sin costo de servidores dedicados) y visualización en tiempo real en un Cuadro de Mando descriptivo con protección de cuota mediante `@st.cache_data`.

---

## 🛑 Lo que nadie te cuenta: El Checklist Previo Obligatorio

> *"Antes de sentarse a orquestar un agente de inteligencia artificial, hay que verificar el siguiente checklist. Sin esto, el resto del trabajo es improvisación y termina en información que no sirve para nada más que para aparentar."*

- [x] **¿La investigación está bien planteada?**  
  Se debe contar con el diseño metodológico completo: planteamiento del problema, finalidad, hipótesis u objetivos y operacionalización rigurosa de variables (diferenciando dimensiones, variables complejas e indicadores estadísticos).
- [x] **¿Tenemos claro el diseño de la base de datos?**  
  Saber cómo garantizar consistencia, restricciones de unicidad (`UNIQUE`), integridad referencial (claves foráneas) y seguridad (`Row Level Security - RLS`). Entender las reglas de cada variable y que la estructura relacional responda a la finalidad analítica del estudio.
- [x] **¿Tenemos el stack tecnológico completo y justificado?**  
  Saber bajo qué entorno trabajará el agente: Python, Streamlit, Pandas, Matplotlib y el SDK de Supabase (`supabase-py`). El SDK permite operar PostgreSQL desde la nube mediante PostgREST sin añadir drivers pesados ni exponer credenciales directas en la interfaz.
- [x] **¿Están definidos los archivos de reglas del IDE (`rules.md` / `AGENTS.md`)?**  
  Directivas inquebrantables de arquitectura, estándares de código (3FN, type hints, cero SQL concatenado) y restricciones técnicas para que el agente programe alineado y sin alucinaciones.
- [x] **¿Está estructurada la modularización mediante Agent Skills?**  
  Carpetas e instrucciones especializadas (`SKILL.md`) para desacoplar tareas (convenciones de Git, pruebas unitarias de caja blanca, buenas prácticas de Postgres).
- [x] **¿Se cuenta con una estrategia de gestión de contexto?**  
  Separar la arquitectura en documentos modulares (`docs/`) para evitar la degradación o fatiga del prompt en conversaciones largas.
- [x] **¿Está definido el flujo de pruebas y guardarraíles humanos?**  
  Pruebas unitarias de caja blanca con `pytest` y validación humana obligatoria (*Code Review*) antes de fusionar cualquier código a ramas de producción.

---

## 📋 FASE 1: Construcción del Repositorio Base (El Boilerplate Reutilizable)

El objetivo pedagógico es demostrar que **la arquitectura para agentes de IA no se improvisa desde cero en cada proyecto**. Se construye un esqueleto estandarizado una sola vez para que cualquier estudiante pueda hacer un *fork*, manteniendo intactas las reglas, los roles y las habilidades, adaptando únicamente los documentos de contexto dentro de `docs/`.

### 1.1 Estructura del Repositorio

```text
oltp-streamlit-plantilla/
├── .antigravity/
│   └── rules.md                # Directivas globales de arquitectura, roles y seguridad
├── .agents/
│   ├── AGENTS.md               # Manifiesto de orquestación y catálogo de roles
│   └── skills/                 # Habilidades modulares del agente
│       ├── supabase/           # Skill de Supabase SDK y Postgres best practices
│       ├── git-conventions/    # Convención estricta de ramas y commits
│       └── pytest-whitebox/    # Pruebas automatizadas de caja blanca
├── docs/                       # Documentos de contexto del caso de estudio
│   ├── research_design.md      # Planteamiento y operacionalización de variables
│   ├── etl_system_design.md    # Modelo relacional 3FN, DER y arquitectura ETL
│   ├── brand_book.md           # Identidad visual, tipografías y diseño del dashboard
│   ├── target_audience.md      # Perfiles de usuario (Estudiantes vs. Coordinación)
│   └── pedagogical_guide.md    # Bitácora didáctica desarrollada durante la sesión
├── assets/                     # Recursos gráficos del proyecto
│   └── img/
│       ├── icons/              # Íconos temáticos (Flaticon)
│       └── references/         # Maquetas visuales del Dashboard
├── src/
│   ├── database/               # Conexión singleton y schema DDL
│   ├── etl/                    # Validación (T), Transacción (L) y Consultas Dashboard
│   └── ui/                     # Formulario y Cuadro de Mando en Streamlit
├── tests/                      # Suite de pruebas unitarias (pytest)
├── requirements.txt            # Dependencias oficiales de Python
└── main.py                     # Punto de entrada de la aplicación Streamlit
```

### 1.2 Reglas Innegociables de Arquitectura (`.antigravity/rules.md`)
1. **Stack Exclusivo:** Python 3.10+, Streamlit, Pandas, Matplotlib y Supabase SDK. Prohibido agregar ORMs pesados o SQL concatenado en strings.
2. **División de Roles:**
   - **`@backend-dba`:** Exclusivo para `src/database/`, `src/etl/` y `tests/`.
   - **`@frontend-ui`:** Exclusivo para `src/ui/` y `main.py`.
3. **Auditoría Cruzada:** El Backend audita al Frontend línea por línea certificando cero inyecciones XSS/HTML, cero fugas de `SUPABASE_KEY` y cero consultas directas fuera del caché.
4. **Protección de Capa Gratuita:** El dashboard utiliza `@st.cache_data(ttl=900)`. Solo se invalida la memoria cuando ocurre una inserción transaccional exitosa (`st.cache_data.clear()`).
5. **Archivos Intocables por Agentes:** `.env`, `requirements.txt` y `.antigravity/rules.md`.

---

## 🔬 FASE 2: Inyección de Contexto del Caso de Estudio (`docs/`)

Hacemos un *fork* del boilerplate y adaptamos los 4 documentos base para el caso real: **Evaluación del Nivel de Manejo de Excel en el Propedéutico de la EECA-UCV (Secciones 11 y 12)**.

### 2.1 Rediseño Metodológico (De Google Forms a OLTP en 3FN)

| Variable en Estudio | Tipo y Escala | Corrección Aplicada en el Sistema OLTP |
| :--- | :--- | :--- |
| **Identificación** | Nominal / Identidad | Tabla maestra `estudiantes` con `cedula PRIMARY KEY` y `correo UNIQUE`. Impide duplicados en la base de datos. |
| **Sección** | Nominal Dicotómica | Clave foránea hacia `cat_secciones` (`11: Sección 11`, `12: Sección 12`). |
| **Edad** | Cuantitativa Discreta | Entero validado en el rango cerrado `15 <= edad <= 75` años (elimina texto libre). |
| **Género** | Nominal Dicotómica | Restricción controlada a `'Femenino'` o `'Masculino'`. |
| **Uso Previo de Excel** | Nominal Booleana | Booleano (`True` / `False`). Si es `False`, el formulario desactiva la selección de operaciones. |
| **Cantidad de Operaciones** | Cuantitativa Discreta | **Calculada automáticamente por el ETL:** $n = \operatorname{length}(\text{operaciones})$. Elimina la contradicción humana de Google Forms. |
| **Operaciones Dominadas** | Politómica ($N:M$) | Desacoplada en `cat_operaciones_excel` y tabla puente `encuesta_operaciones`. Cada operación es un registro atómico (1FN a 3FN). |
| **Interés en Electiva** | Nominal Booleana | Booleano (`True` / `False`). Mide la viabilidad de apertura académica. |
| **Herramientas en Casa** | Nominal Booleana | Booleano (`True` / `False`). Mide la disponibilidad de PC e Internet propio. |
| **Percepción de Utilidad** | Politómica Nominal | Tipificada en 4 segmentos cerrados según la investigación de referencia. |
| **Nivel de Autopercepción** | Ordinal (Likert) | Escala del `1` (Muy Malo) al `5` (Muy Bueno). |

---

## 🎭 FASE 3: Guion de Ejecución en Vivo (Orquestación Paso a Paso)

Este es el guion exacto para dirigir la sesión en vivo frente a los estudiantes:

### Paso 1: Presentación del Boilerplate y Contexto (5 min)
- Mostrar la estructura de carpetas, el archivo `.antigravity/rules.md` y explicar cómo la IA lee los documentos de `docs/` antes de tocar una sola línea de código.

### Paso 2: Invocación del Agente Backend / DBA (15 min)
**Prompt a ejecutar en vivo:**
> *"Actúa bajo el rol de `@backend-dba` definido en `.antigravity/rules.md`. Lee `docs/research_design.md` y `docs/etl_system_design.md`. Construye en `src/database/` y `src/etl/` la conexión singleton con el SDK de Supabase, la transformación y validación de datos a 3FN, la inserción transaccional atómica y las funciones del Dashboard con caché `@st.cache_data`. Luego, genera y ejecuta las pruebas de caja blanca en `tests/` con pytest."*

- **Guardarraíl Humano:** Los estudiantes observan la ejecución de `pytest` en la terminal. Ninguna prueba debe fallar.

### Paso 3: Invocación del Agente Frontend / UI (15 min)
**Prompt a ejecutar en vivo:**
> *"Actúa bajo el rol de `@frontend-ui` definido en `.antigravity/rules.md`. Lee `docs/brand_book.md` y `docs/target_audience.md`. Desarrolla en `src/ui/` y `main.py` el formulario dinámico mobile-first y el Cuadro de Mando estadístico comparativo (Sección 11 vs. Sección 12) usando Streamlit, Pandas y Matplotlib, consumiendo exclusivamente las funciones públicas de `src/etl/`."*

- Se lanza la app con `streamlit run main.py` y se prueba el envío de respuestas en vivo desde un teléfono móvil.

### Paso 4: Auditoría Cruzada de Seguridad y Cierre Git (10 min)
**Prompt a ejecutar en vivo:**
> *"Actúa como `@backend-dba` y realiza la auditoría cruzada de seguridad sobre `src/ui/` y `main.py`. Verifica que los inputs estén sanitizados (cero inyecciones XSS/HTML), que no existan credenciales expuestas y que ninguna gráfica consulte a Supabase fuera de la capa de caché. Una vez aprobado, aplica la convención de Git para crear el commit final."*

- Se genera el commit bajo la convención `feat(release): sistema oltp y dashboard eeca-ucv completado` y se abre el Pull Request.

---

## 💡 Conclusión Pedagógica

El verdadero valor del **Vibecoding** no consiste en pedirle a un modelo de lenguaje que "adivine" el código, sino en **diseñar la arquitectura, las directivas y el contexto con rigor profesional**, permitiendo que los agentes de IA ejecuten la implementación técnica bajo supervisión y validación humana continua.
