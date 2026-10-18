# GUÍA DEFINITIVA DE VIBECODING: CREA TU PROPIO SISTEMA OLTP PARA INVESTIGACIONES ESTADÍSTICAS
## Cómo Orquestar Agentes de Inteligencia Artificial para Superar a Google Forms con Ingeniería de Datos y Rigor Metodológico

**Institución:** Escuela de Estadística y Ciencias Actuariales (EECA - UCV)  
**IDE Agéntico:** Google Antigravity  
**Stack Tecnológico Base:** Python 3.10+, Streamlit, Pandas, Matplotlib y Supabase Cloud (PostgreSQL)  
**Propósito y Visión Pedagógica:**  
Esta guía no es simplemente el instructivo de un caso particular: **es una metodología de trabajo universal y replicable**. Enseña a los estudiantes y docentes de la EECA cómo prescindir de herramientas limitadas como Google Forms y construir, mediante la orquestación de agentes de IA (*Vibecoding* con rigor), **sistemas transaccionales propios (OLTP)** con micro-ETL en tiempo real y cuadros de mando de alta precisión analítica, aplicables a cualquier investigación estadística futura.

---

## 🧭 1. El Manifiesto: Dejar de "Recoger Datos" para Empezar a "Diseñar Sistemas OLTP"

Tradicionalmente, en las investigaciones universitarias la recolección de datos se delega a hojas de cálculo planas o herramientas como Google Forms. Aunque son accesibles, presentan fallas estructurales graves para el rigor estadístico:

| Dimensión | Enfoque Empírico (Google Forms / CSV) | Enfoque de Ingeniería de Datos (OLTP + 3FN en la Nube) |
| :--- | :--- | :--- |
| **Integridad de Registros** | Respuestas duplicadas frecuentes; no hay claves primarias ni restricciones a nivel de motor. | **Blindaje relacional:** Cédula como `PRIMARY KEY`, correo `UNIQUE` y restricciones compuestas que impiden matemáticamente el doble registro. |
| **Variables de Selección Múltiple** | Se guardan como texto separado por comas (`Sumar, Restar`), violando la Primera Forma Normal (1FN) y obligando a búsquedas lentas (`LIKE %...%`). | **Desacoplamiento $N:M$:** Catálogos normalizados y tablas intermedias/puente donde cada selección es un registro atómico indexado. |
| **Inconsistencias Lógicas** | El usuario responde *"Sé 3 operaciones"* y marca 2 en la lista siguiente (error de medición humano inevitable). | **Cálculo automático en el ETL:** El usuario solo marca las opciones y el motor calcula $\text{cantidad} = \operatorname{len}(\text{items})$, garantizando coherencia absoluta. |
| **Tiempo Real y Análisis** | Requiere exportar un CSV manualmente, limpiarlo en Excel o R y rearmar gráficos estáticos. | **Micro-ETL Síncrono:** La transacción ingresa en Postgres y actualiza al instante un Cuadro de Mando con métricas formales ($\bar{x}$, $Mo$, $S$, $CV\%$, Asimetría y Curtosis). |

---

## 🎯 2. La Arquitectura Universal: Micro-ETL en Tiempo Real con Streamlit + Supabase

Todo sistema OLTP desarrollado con esta plantilla sigue un flujo de tres etapas ejecutado en milisegundos en la misma sesión:

```
┌─────────────────────────────────┐
│     1. EXTRACCIÓN (Extract)     │ ──► El encuestado responde en Streamlit (UI Mobile-First).
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   2. TRANSFORMACIÓN (Transform) │ ──► Limpieza de strings, tipificación estricta de variables
│       (En memoria RAM)          │     y cálculo de variables derivadas en Python.
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│       3. CARGA (Load - OLTP)    │ ──► Inserción atómica en Supabase vía SDK (3FN).
│       (PostgreSQL Cloud)        │     Si la cédula/correo ya existen, la BD rechaza el duplicado.
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  4. INVALIDACIÓN INTELIGENTE    │ ──► st.cache_data.clear() refresca el Dashboard
│      (Cero Gasto de Cuota)      │     sin saturar la capa gratuita de Supabase.
└─────────────────────────────────┘
```

---

## 🛑 3. Lo que Nadie te Cuenta: El Checklist Previo a la Orquestación Agéntica

> *"Antes de sentarse a escribir prompts o pedirle código a un modelo de lenguaje, hay que verificar este checklist. Si no tienes resuelto el diseño metodológico y la arquitectura de datos, el agente solo generará código basura que aparenta funcionar pero carece de rigor."*

- [x] **1. Investigación Bien Planteada:**  
  Planteamiento del problema, objetivos claros y matriz de operacionalización de variables: distinguir dimensiones, escalas de medición (nominal, ordinal, razón, intervalo) e indicadores estadísticos requeridos.
- [x] **2. Modelo Relacional en Tercera Forma Normal (3FN):**  
  Tener diseñado el Diagrama Entidad-Relación (DER), definir claves primarias naturales o subrogadas (`UUID` / Cédula), claves foráneas (`FOREIGN KEY`), tablas puente para relaciones $N:M$ y políticas de seguridad (`Row Level Security - RLS`).
- [x] **3. Stack Tecnológico Justificado:**  
  Python (3.10+), Streamlit (Frontend interactivo), Pandas (procesamiento matricial), Matplotlib (visualización científica con estilo editorial) y Supabase SDK (`supabase-py` para evitar consultas SQL concatenadas en texto).
- [x] **4. Reglas Directivas del IDE (`rules.md` / `AGENTS.md`):**  
  Restricciones claras para los agentes: qué carpetas pueden tocar, qué archivos son intocables (`.env`, `requirements.txt`) y qué convenciones de código deben obedecer.
- [x] **5. Habilidades Modulares (Agent Skills):**  
  Especializar al agente con guías de ejecución reutilizables (`SKILL.md`) para tareas críticas (Supabase SDK, convenciones de Git y pruebas de caja blanca con `pytest`).
- [x] **6. Estrategia de Gestión de Contexto:**  
  Desacoplar la memoria del proyecto en documentos de especificación dentro de `docs/`. Así, cualquier nuevo caso de estudio solo requiere cambiar los archivos de `docs/` sin alterar la arquitectura base.
- [x] **7. Guardarraíles Humanos Obligatorios:**  
  Ningún código generado por IA pasa a ramas principales sin validación de pruebas unitarias (`pytest`) y revisión humana explícita (*Code Review*).

---

## 📦 4. Anatomía del Repositorio Boilerplate Reutilizable

Esta plantilla fue diseñada para que **cualquier estudiante o equipo de investigación de la EECA pueda hacer un `Fork` en GitHub** y montar su propio sistema en minutos:

```text
oltp-streamlit-plantilla/
├── .antigravity/
│   └── rules.md                # Directivas maestras del sistema y delimitación de roles
├── .agents/
│   ├── AGENTS.md               # Catálogo de roles (@backend-dba y @frontend-ui)
│   └── skills/                 # Habilidades agénticas especializadas
│       ├── supabase/           # Buenas prácticas de Postgres y SDK de Supabase
│       ├── git-conventions/    # Convenciones semánticas de ramas y commits
│       └── pytest-whitebox/    # Automatización de pruebas de caja blanca
├── docs/                       # EL CORAZÓN DEL CONTEXTO (Se adapta para cada investigación)
│   ├── research_design.md      # Diseño metodológico y operacionalización de variables
│   ├── etl_system_design.md    # Esquema relacional en 3FN, DER y arquitectura ETL
│   ├── brand_book.md           # Identidad visual, paleta, fuentes y assets
│   ├── target_audience.md      # Perfil de usuario móvil (encuestados) y directivo (docentes)
│   └── pedagogical_guide.md    # Bitácora didáctica desarrollada durante la sesión
├── assets/                     # Recursos gráficos institucionales
│   └── img/
│       ├── icons/              # Íconos temáticos (Flaticon)
│       └── references/         # Maquetas de diseño deseadas
├── src/
│   ├── database/               # Conexión singleton y script DDL de creación de tablas
│   ├── etl/                    # Lógica de Validación (T), Inserción OLTP (L) y Métricas
│   └── ui/                     # Formulario y Cuadro de Mando interactivo
├── tests/                      # Suite de pruebas unitarias de caja blanca (pytest)
└── main.py                     # Punto de entrada de la aplicación en Streamlit
```

---

## 🛠️ 5. Paso a Paso: Cómo Crear y Configurar tu Propio Proyecto en Supabase

Supabase ofrece una base de datos PostgreSQL completa en la nube con capa gratuita para hospedar las transacciones del sistema sin costo de infraestructura. Sigue estos pasos para aprovisionar tu entorno:

### Paso 5.1: Crear la Cuenta y el Proyecto
1. Ingresa a [https://supabase.com](https://supabase.com) e inicia sesión con tu cuenta de **GitHub**.
2. En el panel principal (Dashboard), haz clic en el botón verde **"New Project"**.
3. Selecciona tu organización personal y completa el formulario:
   - **Name (Nombre del Proyecto):** Asigna un nombre representativo (ej: `oltp-eeca-excel` o el nombre de tu investigación).
   - **Database Password (Contraseña):** Define una contraseña segura y **anótala de inmediato en un lugar seguro**. La necesitarás si deseas conectar herramientas externas o el CLI.
   - **Region:** Selecciona la región geográfica más cercana (por ejemplo: `South America (São Paulo)` o `US East (North Virginia)`) para minimizar la latencia.
   - **Pricing Plan:** Elige el plan **Free** ($0/mes).
4. Haz clic en **"Create new project"** y espera aproximadamente 1 a 2 minutos mientras Supabase aprovisiona el clúster de Postgres.

### Paso 5.2: Obtener las Credenciales de Conexión (API Keys)
Una vez que el proyecto esté listo:
1. En el menú lateral izquierdo, haz clic en el icono de engranaje **Project Settings** (abajo del todo).
2. Selecciona la pestaña **API** (o en la nueva interfaz, **API Keys**):
   - **Project URL:** Es la dirección base de tu API (ej: `https://xxxxxxxxxxxxxxxxxxxx.supabase.co`). Copia este valor para tu variable `SUPABASE_URL`.
   - **Project API Keys:** 
     - Copia la clave **`anon` / `publishable`** (empieza por `sb_publishable_...` o un JWT). Esta es la que se usa para clientes públicos con políticas RLS.
     - Si requieres la clave administrativa para migraciones internas, localiza la **`service_role` / `secret key`** (empieza por `sb_secret_...`). **Nunca expongas esta clave en repositorios públicos**.

### Paso 5.3: Configurar las Variables de Entorno Locales
En la raíz de tu proyecto local, crea un archivo llamado `.env` (el cual ya está protegido en `.gitignore` para no subirse a GitHub):
```env
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_KEY=tu_clave_anon_o_publishable_aqui
SUPABASE_SECRET_KEY=tu_clave_secreta_aqui
```

### Paso 5.4: Ejecutar el Esquema Relacional (DDL) en el SQL Editor
1. En el panel de Supabase, haz clic en **SQL Editor** en el menú lateral izquierdo (icono con corchetes `>_`).
2. Haz clic en **"New Query"** (o presiona `+`).
3. Abre el archivo `src/database/schema.sql` de tu repositorio, copia todo su contenido y pégalo en el editor de Supabase.
4. Presiona el botón verde **Run** (o `Ctrl + Enter`):
   - Esto creará los catálogos con sus registros iniciales, las tablas normalizadas (`estudiantes`, `encuestas_estudiantes`), la tabla puente (`encuesta_operaciones`), los índices de rendimiento y las políticas de seguridad **RLS** (*Row Level Security*).
5. Ve a **Table Editor** en el menú izquierdo para verificar visualmente que las tablas se hayan creado con sus columnas y relaciones correctas.

---

## 🔄 6. Cómo Replicar este Método para CUALQUIER Investigación de la Escuela

Para aplicar esta arquitectura a un nuevo trabajo de grado, pasantía o estudio estadístico:

1. **Haz un Fork del repositorio base:** Tendrás toda la infraestructura de agentes y scripts lista.
2. **Crea tu proyecto en Supabase:** Siguiendo el paso a paso de la Sección 5.
3. **Actualiza únicamente la carpeta `docs/`:**
   - En `research_design.md`, describe tu problema y cuadro de variables.
   - En `etl_system_design.md`, dibuja tu DER en 3FN y las reglas de transformación.
   - En `brand_book.md`, define los colores institucionales y el layout del dashboard.
   - En `target_audience.md`, define quién llenará el formulario y qué directivos verán las métricas.
4. **Ejecuta tu DDL en Supabase:** Corre el nuevo `schema.sql` en el SQL Editor.
5. **Orquesta a los Agentes de Antigravity:** Sigue el guion de prompts en vivo de la siguiente sección.

---

## 🎭 7. Guion de Ejecución en Vivo (Orquestación Paso a Paso)

Este es el guion exacto para dirigir la sesión práctica frente a los estudiantes:

### Paso 1: Presentación del Boilerplate y Contexto (5 min)
*Explicar cómo los documentos de `docs/` y las reglas de `.antigravity/rules.md` evitan las alucinaciones de la IA.*

### Paso 2: Invocación del `@backend-dba` (15 min)
**Prompt en vivo:**
```text
Actúa bajo el rol de @backend-dba definido en .antigravity/rules.md.
Lee docs/research_design.md y docs/etl_system_design.md.
Construye en src/database/ y src/etl/ la conexión singleton con el SDK de Supabase,
la transformación y validación de datos a 3FN, la inserción transaccional atómica
y las funciones del Dashboard con caché @st.cache_data.
Luego, genera y ejecuta las pruebas de caja blanca en tests/ con pytest.
```
*Guardarraíl:* Los participantes observan la ejecución de `pytest` en la consola. Todo debe pasar en verde.

### Paso 3: Invocación del `@frontend-ui` (15 min)
**Prompt en vivo:**
```text
Actúa bajo el rol de @frontend-ui definido en .antigravity/rules.md.
Lee docs/brand_book.md y docs/target_audience.md.
Desarrolla en src/ui/ y main.py el formulario dinámico mobile-first y el Cuadro
de Mando estadístico comparativo usando Streamlit, Pandas y Matplotlib,
conectándote únicamente a las funciones de src/etl/.
```
*Demostración:* Se abre la app (`streamlit run main.py`) y se envía un registro real desde un teléfono móvil, observando la actualización inmediata en el Cuadro de Mando.

### Paso 4: Auditoría Cruzada de Seguridad y Cierre Git (10 min)
**Prompt en vivo:**
```text
Agente Backend, realiza la auditoría de seguridad sobre src/ui/ y main.py.
Verifica que los inputs estén sanitizados (cero inyecciones XSS/HTML),
que no existan credenciales expuestas y que ninguna gráfica consulte a Supabase
fuera de la capa de caché.
Una vez aprobado, aplica la skill git-conventions para crear el commit final.
```

---

## 🎓 Conclusión: El Verdadero Significado del "Vibecoding"

El *Vibecoding* profesional en la Escuela de Estadística no consiste en pedirle a un chat de IA que adivine código desordenado. Consiste en **actuar como el Arquitecto del Sistema**:
- Definir el rigor metodológico y estadístico.
- Modelar datos en Tercera Forma Normal (3FN).
- Blindar las reglas del sistema y los roles de los agentes.
- **Dejar que la IA programe los bloques modulares bajo nuestra estricta supervisión y pruebas de calidad.**
