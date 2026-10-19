# GUÍA DEFINITIVA DE VIBECODING: CREA TU PROPIO SISTEMA HÍBRIDO OLTP + OLAP PARA INVESTIGACIONES ESTADÍSTICAS
## Cómo Orquestar Agentes de Inteligencia Artificial para Diseñar la Captura Transaccional y la Analítica en Tiempo Real con Rigor Metodológico

**Autoría:** Victoria Andrea Díaz Duarte  
**Institución de Referencia:** Escuela de Estadística y Ciencias Actuariales (EECA - UCV)  
**IDE Agéntico:** Google Antigravity  
**Stack Tecnológico Base:** Python 3.10+, Streamlit, Pandas, Matplotlib y Supabase Cloud (PostgreSQL)  

---

### ⚠️ Una Advertencia Esencial sobre el "Vibecoding" y el Criterio Profesional

Esta guía **no es un manual para docentes ni un ejercicio teórico abstracto**: es un recurso práctico y universal diseñado para **cualquier persona —seas estudiante o no—** que quiera dar el salto definitivo de las encuestas precarias en Google Forms a la creación de sus propios **sistemas híbridos (OLTP para la captura transaccional + OLAP para la analítica en tiempo real)** con rigor metodológico para investigación estadística.

Este material te enseña el paso a paso exacto para que lo hagas por ti mismo utilizando un pipeline ETL y agentes de Inteligencia Artificial que facilitan y aceleran el trabajo repetitivo. Sin embargo, debes tener algo muy claro:

> **El uso de herramientas de Inteligencia Artificial jamás será suficiente para reemplazar el aprendizaje, el estudio de los fundamentos y el criterio analítico.**  
> 
> La IA es un multiplicador de eficiencia formidable: te permite materializar en minutos arquitecturas que antes tomaban semanas. Pero **sin criterio técnico, metodológico y de ingeniería de datos, estas herramientas te pueden meter en problemas gravísimos**. Si no sabes cómo se normaliza una base de datos en 3FN, cómo se previenen inconsistencias lógicas o qué significa matemáticamente cada indicador de tu dashboard, la IA solo construirá código que "aparenta" funcionar pero que produce información inservible. Domina los fundamentos para ser un profesional con criterio; usa la IA para ser infinitamente más ágil.

---

## 🧭 1. El Manifiesto: Dejar de "Recoger Datos" para Empezar a "Diseñar Sistemas Híbridos OLTP + OLAP"

Tradicionalmente, en el ámbito académico y profesional, la recolección de datos se delega a hojas de cálculo planas o herramientas como Google Forms. Aunque parecen cómodas a primera vista, presentan vicios estructurales severos que degradan la validez de cualquier estudio estadístico.

Para entender qué estamos construyendo, debemos diferenciar dos paradigmas fundamentales en la ingeniería de datos:
- **OLTP (*Online Transaction Processing*):** Sistemas diseñados para **capturar y registrar transacciones individuales en tiempo real** con máxima velocidad, consistencia y atomicidad (ej: cada estudiante llenando su encuesta sin colisiones ni duplicados).
- **OLAP (*Online Analytical Processing*):** Sistemas diseñados para **análisis masivo, agregaciones y reportería histórica** (ej: nuestro Cuadro de Mando calculando medias $\bar{x}$, desviaciones estándar, coeficientes de variación y asimetría).

En esta plantilla construimos un **híbrido elegante y moderno**: utilizamos PostgreSQL en Supabase como nuestro motor **OLTP transaccional**, y procesamos en memoria con Streamlit y Pandas nuestra capa **analítica OLAP en tiempo real**.

### Comparativa: ¿Por qué Google Forms no es suficiente para la investigación seria?

| Dimensión Crítica | Enfoque Empírico (Google Forms / CSV) | Enfoque Profesional (OLTP + 3FN en Supabase Cloud) |
| :--- | :--- | :--- |
| **Integridad de Identidad** | Un estudiante puede enviar 5 veces el formulario con pequeñas variaciones. La limpieza posterior es manual y subjetiva. | **Blindaje a Nivel de Motor:** La cédula actúa como `PRIMARY KEY` y el correo como `UNIQUE`. La base de datos aborta cualquier intento de duplicidad automáticamente. |
| **Variables de Selección Múltiple** | Se guardan como texto plano separado por comas (`"Sumar, Restar, Gráficos"`). Viola la **Primera Forma Normal (1FN)** y exige búsquedas lentas e imprecisas (`LIKE %...%`). | **Desacoplamiento Relacional ($N:M$):** Se crea un catálogo maestro y una **tabla puente o intermedia**. Cada opción seleccionada es una fila atómica indexada, lista para ser analizada sin procesamiento de texto sucio. |
| **Inconsistencias Lógicas** | En el cuestionario se pregunta: *"¿Cuántas operaciones sabes hacer? (0-6)"* y luego *"¿Cuáles sabes hacer?"*. El usuario responde `3` y marca `2`. El dato queda corrupto. | **Cálculo Automático en el Pipeline (Transform):** Al usuario solo se le pregunta *cuáles sabe hacer*. El código calcula automáticamente `len(seleccionadas)`, garantizando 100% de coherencia matemática. |
| **Tiempo Real y Automatización** | Requiere descargar un `.xlsx`, abrir SPSS, R o Excel, limpiar celdas vacías y rehacer gráficos manualmente cada semana. | **Micro-ETL Síncrono:** La transacción ingresa en Postgres y al instante la caché se invalida, recalculando el Cuadro de Mando en vivo frente a los ojos del investigador. |

---

## 🎯 2. La Arquitectura Universal: ¿Qué es un ETL y Cómo Opera en este Proyecto?

Un proceso **ETL** (*Extract, Transform, Load*) es el pilar de la ingeniería de datos: consiste en **extraer** datos de una o varias fuentes, **transformarlos** (limpieza, validación de reglas de negocio, cálculo de variables derivadas y tipificación) y **cargarlos** en un destino estructurado para su posterior consumo analítico.

Para un proyecto estadístico que está comenzando y que busca ser replicable para principiantes, no tiene sentido montar clusters pesados (como Apache Spark o Airflow) que demandan cientos de dólares al mes. En esta solución, el pipeline **ETL** opera integrado y en tiempo real dentro del ciclo de la aplicación:

```
┌─────────────────────────────────┐
│     1. EXTRACCIÓN (Extract)     │ ──► El encuestado llena el formulario en Streamlit
│     (Formulario Web / Móvil)    │     (widgets limpios: texto, selects, botones de radio).
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   2. TRANSFORMACIÓN (Transform) │ ──► Ocurre en Python (Memoria RAM):
│    (Validación de Negocio)      │     • Sanitiza cadenas (elimina espacios y código malicioso).
│                                 │     • Valida rangos lógicos (edad entre 15 y 75 años).
│                                 │     • Calcula variables derivadas (cantidad = len(operaciones)).
│                                 │     • Genera las tuplas relacionales normalizadas en 3FN.
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│       3. CARGA (Load - OLTP)    │ ──► Inserción atómica en Supabase Cloud vía SDK oficial:
│       (PostgreSQL en la Nube)   │     • Inserta en 'estudiantes' (identidad).
│                                 │     • Inserta en 'encuestas_estudiantes' (relación 1:1).
│                                 │     • Inserta en 'encuesta_operaciones' (tabla puente N:M).
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  4. INVALIDACIÓN INTELIGENTE    │ ──► La función de inserción dispara: st.cache_data.clear()
│      (Dashboard en Vivo)        │     El Cuadro de Mando vuelve a consultar los datos frescos
│                                 │     y recalcula las estadísticas descriptivas al instante.
└─────────────────────────────────┘
```

### ¿Qué nos ofrece Supabase a través de su API y su SDK al trabajar con PostgreSQL Cloud?
Supabase no es solo una base de datos alojada en la nube; es una plataforma que simplifica radicalmente la ingeniería de datos:
1. **API REST Automática (PostgREST):** En el mismo instante en que creas tus tablas en PostgreSQL, Supabase genera automáticamente endpoints REST documentados y seguros para cada tabla.
2. **SDK Oficial de Python (`supabase-py`):** Nos permite interactuar con la base de datos sin escribir sentencias SQL concatenadas en cadenas de texto (lo que previene inyecciones SQL por diseño). Operamos con llamadas directas y parametrizadas como `client.table("estudiantes").insert(...)`.
3. **Seguridad a Nivel de Fila (RLS):** Las reglas de acceso y privacidad las gobierna el motor de Postgres en la nube, garantizando que nadie pueda alterar o extraer información fuera de las políticas autorizadas.

### ¿Qué es la Tercera Forma Normal (3FN) y por qué debe importarte?
Normalizar una base de datos significa **organizar los datos para que cada hecho se guarde una sola vez y en el lugar que le corresponde**:
- **1FN (Atomicidad):** Cada celda contiene un solo valor. No guardamos listas de operaciones en un solo campo de texto.
- **2FN (Dependencia Total de la Clave):** Cada dato del estudiante (edad, género, correo) depende de su clave única (`cedula`), no de la encuesta particular.
- **3FN (Cero Dependencias Transitivas):** Si una categoría se repite (ej: "Sección 11", "Sección 12", "Muy Bueno", "Bueno"), no escribimos la palabra una y otra vez en cada fila; creamos un catálogo (`cat_secciones`, `cat_niveles_manejo`) y solo guardamos su identificador numérico (`id_seccion`, `id_nivel`). Esto reduce el tamaño de la base de datos, acelera las consultas por milisegundos y previene errores de tipeo.

---

## 💻 3. Justificación del Stack Tecnológico: ¿Por qué estas Herramientas y qué Beneficios Aportan?

> **En ingeniería de datos no se eligen librerías o herramientas por moda, sino por arquitectura, costos y sostenibilidad en el tiempo.**

De nada sirve diseñar una arquitectura teórica "perfecta" si requiere servidores de $500 mensuales que ni los estudiantes ni la escuela pueden pagar, o si depende de tecnologías que dentro de seis meses quedarán obsoletas. Este stack fue seleccionado bajo una premisa realista: **costo cero ($0), alta calidad técnica, curva de aprendizaje accesible para principiantes y sostenibilidad en el tiempo**:

### 🐍 1. Python (3.10+) — El Estándar de Oro en Estadística y Datos
* **¿Por qué se escoge?:** Es el lenguaje hegemónico en la Escuela de Estadística y Ciencias Actuariales. Permite unificar en un solo ecosistema el desarrollo de la aplicación web, la validación de negocio, las pruebas automatizadas y el modelado analítico sin tener que aprender frameworks externos en JavaScript.
* **Beneficio de Ingeniería de Datos:** Tipado estático con *Type Hints*, manipulación matricial nativa, logging robusto y compatibilidad total con librerías de inferencia estadística.

### 🎈 2. Streamlit — Frontend Reactivo sin Complejidad Web
* **¿Por qué se escoge?:** Desarrollar un frontend tradicional requiere HTML, CSS, JavaScript, React o Next.js, lo cual desvía la atención del rigor metodológico. Streamlit permite convertir scripts puros de Python en aplicaciones web interactivas y reactivas en minutos.
* **Beneficio de Ingeniería de Datos:** 
  - **Mobile-First nativo:** Sus componentes son automáticamente responsivos para ser respondidos desde teléfonos celulares vía WhatsApp.
  - **Manejo de estado y caché (`@st.cache_data`):** Permite aislar lecturas pesadas en memoria RAM para no degradar la base de datos ni agotar cuotas cloud.
  - **Cero código backend separado:** El formulario y la lógica ETL viven sincronizados en el mismo ciclo de ejecución.

### 🐼 3. Pandas — Motor Matricial y Agregaciones Estadísticas
* **¿Por qué se escoge?:** A diferencia de recorrer listas de diccionarios con bucles `for` lentos, Pandas opera sobre estructuras vectorizadas en C (*DataFrames*).
* **Beneficio de Ingeniería de Datos:** Permite transformar la respuesta relacional de Supabase en una matriz analítica en microsegundos, calculando al vuelo indicadores robustos de estadística descriptiva ($\bar{x}$, $Mo$, $S$, $CV\%$, Asimetría y Curtosis) y agrupaciones segmentadas (`groupby`) entre cohortes (Sección 11 vs. Sección 12).

### 📈 4. Matplotlib — Control Científico Total y Rigor Editorial
* **¿Por qué se escoge?:** Las librerías comerciales o interactivas tipo Plotly a menudo generan gráficos sobrecargados con ruido visual que no se adaptan al estándar de una publicación académica o tesis de la EECA.
* **Beneficio de Ingeniería de Datos:** Ofrece control milimétrico sobre cada elemento del plano cartesiano: eliminación de bordes innecesarios (*spines off*), paletas cromáticas académicas de alto contraste, tipografías personalizadas y exportación en alta resolución vectorial.

### ⚡ 5. Supabase Cloud (PostgreSQL) — Base de Datos Relacional de Nivel Empresarial
* **¿Por qué se escoge?:** Instalar y mantener un servidor local de PostgreSQL o MySQL requiere configuración de puertos, Docker, backups y costos de infraestructura que dificultan el trabajo colaborativo. Supabase provee una base de datos PostgreSQL administrada en la nube con capa gratuita para investigación académica.
* **Beneficio de Ingeniería de Datos:**
  - **Soporte relacional en 3FN:** Claves foráneas reales, restricciones de integridad (`CHECK`, `UNIQUE`) y cascadas relacionales.
  - **Seguridad perimetral (Row Level Security - RLS):** Las reglas de acceso y privacidad viven dentro de la propia base de datos, no en el cliente.
  - **API REST Automática vía PostgREST (SDK Oficial):** No hay necesidad de escribir endpoints HTTP manuales ni consultas SQL concatenadas en texto; el SDK de Python interactúa de manera nativa y parametrizada contra la base de datos.
  - **Sostenibilidad económica:** Permite hospedar investigaciones enteras en su capa gratuita (*Free Tier*) sin generar facturas imprevistas.

---

## 🛑 4. Lo que Nadie te Cuenta: Preguntas Clave Antes de Orquestar Agentes de Inteligencia Artificial

> *"Antes de sentarse a escribir prompts o pretender que un modelo de lenguaje programe por ti, hay que responder con absoluta honestidad el siguiente cuestionario crítico. Sin esto, el resto del trabajo es una basura y está mal dirigido. Conclusión: información basura que no sirve para nada más que para aparentar."*

1. **¿La investigación está bien planteada?**  
   Para evaluar si la investigación está bien planteada, se debe tener el trazado del diseño de la investigación completo: planteamiento del problema, finalidad, operacionalización de variables y comprender la diferencia entre una dimensión, una variable compleja y entre indicadores estadísticos.

2. **¿Tenemos claro el diseño de la base de datos?**  
   ¿Sabemos cómo garantizar la consistencia, seguridad e integridad de los registros? ¿Comprendemos las reglas de cada una de las variables y su forma de medición? ¿Las estructuras de datos satisfacen la finalidad de los mismos (métricas calculadas, conteos, proporciones)?

3. **¿Tenemos el stack tecnológico completo y justificado?**  
   ¿Sabemos bajo qué entorno de programación trabajará el agente? ¿En qué lenguaje y por qué ese es el adecuado? Librerías, métodos de programación, optimización de caché y rendimiento. En nuestro caso trabajaremos con Python, Streamlit, Pandas, Matplotlib y el SDK oficial de Supabase para operar una base de datos PostgreSQL desde la nube sin necesidad de añadir otro gestor de bases de datos.

4. **¿Están definidos los archivos de reglas del IDE (ej. `.antigravity/rules.md` o `AGENTS.md`)?**  
   Es fundamental establecer las directivas de arquitectura, estándares de código (ej: 3FN, ORM/SDK, endpoints asíncronos) y restricciones técnicas para que los agentes programen con contexto alineado y sin alucinaciones.

5. **¿Está estructurada la modularización mediante Agent Skills?**  
   Se deben definir carpetas e instrucciones especializadas (con su respectivo `SKILL.md`) para desacoplar tareas específicas (ej: convenciones de Git, buenas prácticas de Supabase, pruebas unitarias automatizadas) y permitir revelación progresiva de contexto.

6. **¿Se cuenta con una estrategia de gestión de contexto para evitar la degradación o fatiga del prompt?**  
   Es necesario establecer políticas de limpieza de sesión, resúmenes periódicos de avance e inyección de contexto bajo demanda (modularizado en la carpeta `docs/`) para mantener las respuestas del agente precisas en desarrollos largos.

7. **¿Está definido el flujo de revisión, refactorización y pruebas de caja blanca del código generado?**  
   Pytest. Para optimizar las pruebas de caja blanca lo ideal es crear una habilidad (`pytest-whitebox`). Debe contemplarse un canal de validación humana obligatoria (*Code Review*, Pull Requests y pruebas unitarias/locales) antes de fusionar el código generado por IA a las ramas de producción.

---

## 📦 5. Anatomía del Repositorio Boilerplate Reutilizable

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

> [!TIP]
> ### 💡 Regla de Oro sobre la Especificidad del Contexto (`docs/`)
> **Puedes ser tan específico, exhaustivo y detallado como quieras en el desarrollo de los documentos de contexto dentro de `docs/`, dependiendo de la complejidad y alcance de tu proyecto.**  
> 
> Mientras más compleja sea la investigación estadística (más tablas relacionales, reglas de validación compuestas, estratos muestrales, fórmulas de ponderación o requerimientos de identidad visual), más detallada debe ser la especificación. Recuerda que **el agente de IA no adivina intenciones**: su precisión y calidad de código dependerán directamente del nivel de detalle, definiciones y restricciones que hayas plasmado en estos archivos. Si tu proyecto necesita documentos adicionales puedes crearlos libremente dentro de `docs/`.

---

## 🛠️ 6. Paso a Paso: Cómo Crear y Configurar tu Propio Proyecto en Supabase

Supabase ofrece una base de datos PostgreSQL completa en la nube con capa gratuita para hospedar las transacciones del sistema sin costo de infraestructura. Sigue estos pasos para aprovisionar tu entorno:

### Paso 6.1: Crear la Cuenta y el Proyecto
1. Ingresa a [https://supabase.com](https://supabase.com) e inicia sesión con tu cuenta de **GitHub**.
2. En el panel principal (Dashboard), haz clic en el botón verde **"New Project"**.
3. Selecciona tu organización personal y completa el formulario:
   - **Name (Nombre del Proyecto):** Asigna un nombre representativo (ej: `oltp-eeca-excel` o el nombre de tu investigación).
   - **Database Password (Contraseña):** Define una contraseña segura y **anótala de inmediato en un lugar seguro**. La necesitarás si deseas conectar herramientas externas o el CLI.
   - **Region:** Selecciona la región geográfica más cercana (por ejemplo: `South America (São Paulo)` o `US East (North Virginia)`) para minimizar la latencia.
   - **Pricing Plan:** Elige el plan **Free** ($0/mes).
4. Haz clic en **"Create new project"** y espera aproximadamente 1 a 2 minutos mientras Supabase aprovisiona el clúster de Postgres.

### Paso 6.2: Obtener las Credenciales de Conexión (API Keys)
Una vez que el proyecto esté listo:
1. En el menú lateral izquierdo, haz clic en el icono de engranaje **Project Settings** (abajo del todo).
2. Selecciona la pestaña **API** (o en la nueva interfaz, **API Keys**):
   - **Project URL:** Es la dirección base de tu API (ej: `https://xxxxxxxxxxxxxxxxxxxx.supabase.co`). Copia este valor para tu variable `SUPABASE_URL`.
   - **Project API Keys:** 
     - Copia la clave **`anon` / `publishable`** (empieza por `sb_publishable_...` o un JWT). Esta es la que se usa para clientes públicos con políticas RLS.
     - Si requieres la clave administrativa para migraciones internas, localiza la **`service_role` / `secret key`** (empieza por `sb_secret_...`). **Nunca expongas esta clave en repositorios públicos**.

### Paso 6.3: Configurar las Variables de Entorno Locales
En la raíz de tu proyecto local, crea un archivo llamado `.env` (el cual ya está protegido en `.gitignore` para no subirse a GitHub):
```env
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_KEY=tu_clave_anon_o_publishable_aqui
SUPABASE_SECRET_KEY=tu_clave_secreta_aqui
```

### Paso 6.4: Ejecutar el Esquema Relacional (DDL) en el SQL Editor
1. En el panel de Supabase, haz clic en **SQL Editor** en el menú lateral izquierdo (icono con corchetes `>_`).
2. Haz clic en **"New Query"** (o presiona `+`).
3. Abre el archivo `src/database/schema.sql` de tu repositorio, copia todo su contenido y pégalo en el editor de Supabase.
4. Presiona el botón verde **Run** (o `Ctrl + Enter`):
   - Esto creará los catálogos con sus registros iniciales, las tablas normalizadas (`estudiantes`, `encuestas_estudiantes`), la tabla puente (`encuesta_operaciones`), los índices de rendimiento y las políticas de seguridad **RLS** (*Row Level Security*).
5. Ve a **Table Editor** en el menú izquierdo para verificar visualmente que las tablas se hayan creado con sus columnas y relaciones correctas.

---

---

## 🔄 7. Cómo Replicar este Método para CUALQUIER Investigación Estadística

> ### 🧠 La Regla de Oro sobre las Alucinaciones de la IA:
> **La Inteligencia Artificial alucina por falta de contexto.**  
> Cuando un modelo de lenguaje "inventa" código que no funciona, usa librerías incompatibles o mezcla la base de datos con la interfaz de usuario, no es por una limitación del modelo: **es porque no le diste las directivas correctas**. 
> 
> Todos los artefactos que diseñamos aquí —las carpetas de contexto en `docs/`, las directivas innegociables de `.antigravity/rules.md` y las habilidades especializadas (`SKILL.md`) en `.agents/skills/`— son precisamente el **antídoto contra la alucinación**. Son los rieles que obligan a la IA a entregarte un código 100% alineado, limpio y libre de errores infantiles.

Para aplicar esta arquitectura a cualquier trabajo de grado, pasantía o investigación de mercado:

1. **Haz un Fork del repositorio base:** Tendrás toda la infraestructura de agentes y scripts estandarizados lista.
2. **Crea tu proyecto en Supabase:** Siguiendo el paso a paso de la Sección 6.
3. **Inyecta tu propio Contexto en `docs/`:**
   - En `research_design.md`, describe tu problema y tu cuadro de operacionalización de variables.
   - En `etl_system_design.md`, dibuja tu DER en 3FN y las reglas del pipeline ETL.
   - En `brand_book.md`, define los colores institucionales y el layout del dashboard.
   - En `target_audience.md`, define quién responderá el formulario y qué directivos evaluarán las métricas.
4. **Ejecuta tu DDL en Supabase:** Pega y corre el nuevo `schema.sql` en el SQL Editor.
5. **Comienza a orquestar a tus agentes:** Sigue el guion interactivo de la siguiente sección.

---

## 🎭 8. ¡Comienza ya a Orquestar a tus Agentes! (Guion de Ejecución Paso a Paso)

Una vez que tengas tu repositorio configurado con los documentos en `docs/` y tu base de datos lista en Supabase, es hora de poner a trabajar a tus agentes en Google Antigravity:

### Paso 1: Verificar Comprensión de Contexto y Presentación del Equipo (5 min)
Antes de permitirle escribir una sola línea de código, debes **garantizar que la estructura de tu repositorio esté correctamente entendida** y que el agente conozca sus límites:

**Prompt en vivo para el Paso 1:**
```text
Hola. Antes de comenzar a programar, lee detenidamente '.antigravity/rules.md', 
'.agents/AGENTS.md' y todos los documentos dentro de 'docs/'. 

Confírmame si tienes claro el contexto del proyecto, las restricciones técnicas 
y la segregación de roles. Por favor, presenta al equipo completo de agentes 
especializados que participarán en la construcción, indicando el rol de cada uno 
y sus directorios autorizados de trabajo.
```
*Objetivo:* Si el agente responde explicando con precisión el rol del `@backend-dba` y del `@frontend-ui` y citando tus documentos de `docs/`, tienes la certeza absoluta de que el contexto fue inyectado con éxito y no habrá alucinaciones.

---

### Paso 2: Invocación del Agente Backend / DBA (15 min)
Una vez validada la estructura, ordenamos la construcción de la capa de datos y el pipeline ETL:

**Prompt en vivo para el Paso 2:**
```text
Actúa bajo el rol de @backend-dba definido en .antigravity/rules.md.
Lee docs/research_design.md y docs/etl_system_design.md.

Construye en src/database/ y src/etl/:
1. La conexión singleton con el SDK de Supabase (sin SQL concatenado).
2. El pipeline ETL de validación, transformación relacional a 3FN y cálculo automático de variables derivadas.
3. La inserción transaccional atómica respetando la integridad referencial.
4. Las consultas analíticas del Dashboard protegidas con caché @st.cache_data.

Luego, diseña y ejecuta la suite de pruebas de caja blanca en tests/ utilizando pytest.
```
*Guardarraíl Humano 1:* Ejecuta `pytest` en tu consola. Verifica que todas las pruebas pasen en verde antes de autorizar el paso al frontend.

---

### Paso 3: Invocación del Agente Frontend / UI & Dashboard (15 min)
Con la capa de datos blindada y probada, convocamos al diseñador de interfaces:

**Prompt en vivo para el Paso 3:**
```text
Actúa bajo el rol de @frontend-ui definido en .antigravity/rules.md.
Lee docs/brand_book.md y docs/target_audience.md.

Desarrolla en src/ui/ y main.py:
1. El formulario dinámico mobile-first para la captura transaccional.
2. El Cuadro de Mando estadístico comparativo en tiempo real utilizando Streamlit, 
   Pandas y Matplotlib (con estética limpia, spines off y rigor descriptivo).

REGLA ESTRICTA: Conéctate únicamente a las funciones públicas expuestas por src/etl/. 
Queda prohibido llamar directamente al cliente de Supabase desde la UI.
```
*Demostración:* Lanzas la aplicación localmente con `streamlit run main.py`, abres el enlace desde tu navegador o teléfono móvil y envías un registro de prueba.

---

### Paso 4: Auditoría Cruzada de Seguridad y Cierre con Git (10 min)
Para certificar que el frontend no violó las reglas del sistema:

**Prompt en vivo para el Paso 4:**
```text
Agente Backend (@backend-dba), realiza la auditoría cruzada de seguridad obligatoria 
sobre los archivos creados en src/ui/ y main.py.

Verifica línea por línea:
1. Que los campos de texto estén sanitizados contra inyecciones HTML/XSS en Streamlit.
2. Que jamás se expongan credenciales sensibles (SUPABASE_KEY) en el cliente o logs.
3. Que ninguna gráfica o widget consulte a la base de datos fuera de la capa de caché.

Una vez emitido el dictamen 'APROBADO POR SEGURIDAD DBA', aplica la convención 
de Git para registrar el commit estandarizado y dejar listo el Pull Request.
```
---

## 🚀 9. Paso a Paso: Despliegue en la Nube con Streamlit Community Cloud y GitHub

Una de las grandes ventajas de esta arquitectura es que **poner la aplicación en producción en internet es 100% gratuito** y no requiere configurar servidores Linux, Docker ni redes complejas. 

Utilizamos **Streamlit Community Cloud**, la plataforma oficial de Streamlit que se conecta directamente a tu repositorio de GitHub para ofrecer despliegue continuo (**CI/CD**): cada vez que hagas un `git push` a tu rama principal, la aplicación se actualizará automáticamente en la nube.

Sigue estos pasos para publicar tu sistema y obtener un enlace público para compartir por WhatsApp o redes:

### Paso 9.1: Asegurar los Requisitos Previos en GitHub
Antes de conectar Streamlit Cloud, verifica que en tu repositorio de GitHub:
1. El archivo `requirements.txt` esté en la raíz del proyecto con todas las librerías necesarias (`streamlit`, `pandas`, `matplotlib`, `supabase`, `python-dotenv`).
2. El archivo de entrada principal sea `main.py`.
3. Tu archivo `.env` **NO esté subido a GitHub** (revisa que esté incluido en `.gitignore`).

### Paso 9.2: Crear tu Cuenta en Streamlit Community Cloud
1. Ingresa a [https://share.streamlit.io](https://share.streamlit.io).
2. Haz clic en **"Sign in with GitHub"** (inicia sesión con la misma cuenta donde tienes el repositorio del proyecto).
3. Autoriza a Streamlit para acceder a tus repositorios públicos.

### Paso 9.3: Configurar el Nuevo Despliegue (Deploy an App)
1. En el panel de Streamlit Cloud, haz clic en el botón azul **"New app"** (o *"Deploy an app"*).
2. Selecciona la opción **"I have an app"** o escoge tu repositorio:
   - **Repository:** Selecciona tu repositorio (ej: `tu-usuario/oltp-streamlit-plantilla`).
   - **Branch:** Selecciona la rama de producción (generalmente `main` o tu rama terminada).
   - **Main file path:** Escribe `main.py` (el archivo raíz que ejecuta la aplicación).
   - **App URL (Opcional):** Puedes personalizar el subdominio público de tu app (ej: `encuesta-excel-eeca.streamlit.app`).

### Paso 9.4: Inyectar las Claves Secretas en "Advanced Settings" (Secrets)
> **⚠️ Regla Crítica de Seguridad:** Como el archivo `.env` nunca se sube a GitHub para no exponer credenciales, debemos inyectar las variables directamente en la configuración segura de Streamlit Cloud.

1. Antes de presionar Deploy, haz clic en **"Advanced settings..."** (abajo a la izquierda del formulario de despliegue).
2. En la sección **Secrets** (que utiliza formato TOML), copia y pega tus credenciales de Supabase:
   ```toml
   SUPABASE_URL = "https://tu-proyecto-id.supabase.co"
   SUPABASE_KEY = "tu_clave_anon_o_publishable_aqui"
   SUPABASE_SECRET_KEY = "tu_clave_secreta_aqui"
   ```
   *Nota técnica:* La librería `python-dotenv` lee el `.env` localmente en tu computadora, mientras que en Streamlit Cloud la función `st.secrets` y las variables de entorno inyectan estos mismos valores de forma segura sin que nadie pueda verlos en el código fuente.
3. Haz clic en **"Save"**.

### Paso 9.5: Desplegar y Monitorear en Vivo
1. Haz clic en el botón azul **"Deploy!"**.
2. Verás cómo Streamlit Cloud abre una consola en tiempo real donde:
   - Clona tu repositorio de GitHub.
   - Instala las dependencias de `requirements.txt`.
   - Inicializa el servidor web en un contenedor seguro.
3. En menos de 2 minutos, tu aplicación estará activa con un enlace HTTPS oficial (ej: `https://tu-app.streamlit.app`).
4. **¡Listo para recolectar datos!** Copia el enlace, compártelo en los grupos de estudio o redes sociales y observa cómo cada respuesta desde cualquier teléfono móvil ingresa a Supabase y actualiza tu Cuadro de Mando en vivo.

---

## 🎓 Conclusión: El Verdadero Significado del "Vibecoding" con Criterio
*(Por Victoria Andrea Díaz Duarte)*

El *Vibecoding* profesional no consiste en sentarse pasivamente a ver cómo un modelo de lenguaje adivina líneas de código desordenadas. Consiste en **asumir con madurez el rol de Arquitecto del Sistema**:

1. **El criterio humano manda:** Tú eres quien formula el rigor metodológico, quien comprende las variables estadísticas y quien decide cómo estructurar las relaciones en Tercera Forma Normal (3FN).
2. **La IA ejecuta y acelera:** El agente programa los módulos, crea las conexiones, genera las pruebas y maquetiza el frontend bajo tus reglas inquebrantables.
3. **El aprendizaje no se negocia:** Las herramientas cambian y evolucionan velozmente, pero la base teórica (estadística descriptiva, álgebra relacional, normalización y buenas prácticas de ingeniería) es lo que te protegerá de cometer errores costosos en el mundo profesional.

Aprovecha este flujo, construye tus propios sistemas, experimenta con tus investigaciones y conviértete en un profesional que no solo sabe analizar datos, sino que sabe **diseñar la ingeniería que los captura con excelencia**.
