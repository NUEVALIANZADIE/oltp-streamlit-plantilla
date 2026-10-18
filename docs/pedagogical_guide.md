# Bitácora Pedagógica y Fundamentos de Arquitectura de Datos (`pedagogical_guide.md`)

**Proyecto:** Sistema OLTP y Cuadro de Mando en Tiempo Real — Nivel de Manejo de Excel (EECA-UCV)  
**Naturaleza del Documento:** Desarrollo didáctico elaborado de manera interactiva a lo largo de la sesión de *Vibecoding* por el agente de Inteligencia Artificial para los estudiantes y docentes de la Escuela de Estadística y Ciencias Actuariales (EECA - UCV).  
**Audiencia:** Estudiantes de Estadística, Ciencias Actuariales y Desarrolladores en sesiones de Vibecoding  
**Propósito:** Explicar el "por qué" detrás de cada decisión técnica de ingeniería de datos, normalización y diseño transaccional frente al enfoque empírico de hojas de cálculo o Google Forms.

---

## 1. El Salto Mental: De la Hoja de Cálculo (CSV / Google Forms) al Sistema Relacional (OLTP)

En la formación inicial en ciencias de datos y estadística, la herramienta por defecto suele ser Microsoft Excel o Google Sheets. Cuando los estudiantes diseñan su primera recolección de datos, tienden a pensar en **una sola matriz rectangular plana** (un CSV con filas y columnas).

Sin embargo, los sistemas transaccionales en producción (**OLTP** - *Online Transaction Processing*) operan con principios distintos diseñados para:
1. **Garantizar la integridad de los datos** (evitar datos corruptos, incompletos o inconsistentes).
2. **Evitar la redundancia** (no almacenar el mismo texto miles de veces).
3. **Escalar eficientemente** (consultas rápidas con indexación).

---

## 2. Decisiones de Modelado Relacional (Tercera Forma Normal - 3FN)

### 2.1 ¿Por qué desacoplar `estudiantes` de `encuestas_estudiantes`?
* **El Problema:** Si guardamos el nombre, correo y cédula directamente en cada fila de la encuesta, mezclamos la **identidad del sujeto** con el **hecho transaccional** (el acto de responder).
* **La Solución 3FN:** 
  - La tabla `estudiantes` modela la **dimensión estática** de la persona (clave primaria `cedula`, `correo UNIQUE`, datos sociodemográficos).
  - La tabla `encuestas_estudiantes` modela el **evento transaccional** (identificado por un `id_encuesta UUID`).
* **Valor Pedagógico:** Si el departamento de estadística decide hacer una medición longitudinal (por ejemplo, evaluar al mismo estudiante al inicio y al final del curso), este modelo soporta ambas encuestas sin duplicar la información personal del estudiante. Al mismo tiempo, si la regla de negocio exige una sola respuesta por persona, la base de datos lo blinda con una restricción `UNIQUE (cedula)` en la tabla de encuestas.

---

### 2.2 ¿Por qué separar `cat_operaciones_excel` y `encuesta_operaciones` (Relación $N:M$)?
* **El Error Común del Principiante:**
  - *Opción A (Lista en texto):* Guardar `"Sumar, Restar, Gráficos"` en una sola columna VARCHAR.  
    *Consecuencia:* Viola la **Primera Forma Normal (1FN)**. Para contar cuántos alumnos saben hacer gráficos, el sistema tendría que realizar búsquedas lentas de subcadenas (`LIKE '%Gráficos%'`), propensas a errores tipográficos y que anulan el uso de índices.
  - *Opción B (Columnas fijas):* Crear 6 columnas booleanas (`sabe_sumar`, `sabe_restar`, etc.).  
    *Consecuencia:* Si la cátedra decide agregar una séptima operación (ej: *"Macros"* o *"Tablas de Frecuencia"*), el desarrollador tendría que alterar la estructura de la tabla (`ALTER TABLE`) en producción, lo cual es costoso e inflexible.
* **La Solución Profesional ($N:M$ con Tabla Puente):**
  1. `cat_operaciones_excel`: Catálogo maestro cerrado con los identificadores `1` al `6`.
  2. `encuesta_operaciones`: Tabla puente o intermedia donde cada fila representa un **hecho atómico**:
     - Estudiante A domina la Operación 1 $\rightarrow$ `(id_encuesta_A, 1)`
     - Estudiante A domina la Operación 5 $\rightarrow$ `(id_encuesta_A, 5)`
* **Valor Pedagógico:** Enseña cómo las operaciones de selección múltiple se modelan formalmente en bases de datos relacionales sin redundancias ni columnas huérfanas.

---

## 3. Arquitectura del Pipeline ETL en Streamlit: ¿Por qué en Tiempo Real?

A diferencia de un Data Warehouse corporativo que corre procesos de extracción masiva en la noche (procesamiento por lotes o *batch* con Apache Airflow), este sistema utiliza un **ETL en Tiempo Real (Micro-ETL Transaccional)** embebido en la aplicación web:

```
[Formulario Web] 
       │
       ▼ (Extract)
[Payload de Entrada] ──► [Transformación en RAM] ──► [Carga Atómica en Supabase]
                               │                                    │
                     • Sanitización de cédula              • Inserción estudiantes
                     • cantidad_operaciones = len(...)     • Inserción encuestas
                     • Tipificación de tipos               • Inserción puente N:M
                                                                    │
                                                                    ▼
                                                        st.cache_data.clear()
                                                                    │
                                                                    ▼
                                                        [Dashboard Actualizado]
```

### 3.1 La Regla de Oro: Eliminar la Inconsistencia Humana en el "Transform"
En el formulario original en papel o Google Forms se hacían dos preguntas separadas:
1. *"¿Cuántas operaciones básicas sabes realizar? (0 a 6)"*
2. *"¿Cuáles operaciones sabes realizar?"*

En los datos reales, muchos encuestados marcaban que sabían realizar 3 operaciones, pero en la lista solo tildaban 2 (o viceversa).  
**Lección de Ingeniería de Software:** Los sistemas robustos no le piden al usuario que calcule datos derivados. En nuestro formulario el estudiante solo marca **cuáles sabe hacer**, y la etapa **T (Transform)** del ETL calcula automáticamente:
$$\text{cantidad\_operaciones} = \operatorname{length}(\text{operaciones\_seleccionadas})$$
Esto garantiza consistencia matemática del 100% en la base de datos.

---

## 4. Eficiencia de Costos y Recursos: El Rol del Caché (`st.cache_data`)

* **El Reto:** Streamlit re-ejecuta todo el script de Python de arriba a abajo cada vez que un usuario interactúa con un botón, pestaña o filtro. Si cada re-renderizado consultara la base de datos de Supabase, la cuota gratuita de peticiones API se agotaría rápidamente.
* **La Estrategia de Caché Inteligente:**
  - El Cuadro de Mando consulta la base de datos a través de una función protegida por `@st.cache_data(ttl=900)`. Durante 15 minutos, todas las visitas y filtros leen de la memoria RAM del servidor (tiempo de respuesta < 5 ms y cero consumo de API en Supabase).
  - **Invalidación dirigida:** Únicamente cuando alguien envía una nueva encuesta válida, el pipeline ETL dispara `st.cache_data.clear()`. Así, los gráficos y métricas descriptivas se refrescan al instante sin gastar recursos de forma ociosa.
