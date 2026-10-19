# Especificación del Sistema ETL y Modelo de Datos OLTP (`etl_system_design.md`)

**Proyecto:** Sistema OLTP de Evaluación del Nivel de Manejo de Excel — Propedéutico EECA-UCV[cite: 1, 2]  
**Arquitectura de Datos:** Tercera Forma Normal (3FN) en PostgreSQL (Supabase Cloud)[cite: 1]  
**Stack de Integración:** Python, SDK Oficial de Supabase (`supabase-py`), Pandas, Matplotlib y Streamlit[cite: 1]  

---

## 1. Mapeo de Operacionalización de Variables al Modelo Relacional (3FN)

El instrumento de recolección de datos evalúa 10 variables estadísticas sobre los estudiantes del propedéutico de la Escuela de Estadística y Ciencias Actuariales (Sección 11 y Sección 12)[cite: 2], además de los datos de identidad y autenticidad del estudiante:

| N° | Variable / Atributo | Tipo y Escala | Regla de Negocio e Implementación en 3FN |
| :-: | :--- | :--- | :--- |
| **0** | Identificación del Estudiante | Identidad / Dimensión | **Entidad Maestra `estudiantes`:** `cedula VARCHAR(20) PRIMARY KEY`, `nombre_completo VARCHAR(120)`, `correo VARCHAR(150) UNIQUE` y restricción de unicidad compuesta `(cedula, correo)`. |
| **1** | Sección del propedéutico[cite: 2] | Cualitativa Dicotómica (Nominal)[cite: 2] | Clave foránea (`id_seccion`) referenciando al catálogo `cat_secciones` (`Sección 11`, `Sección 12`)[cite: 2]. |
| **2** | Edad en años[cite: 2] | Cuantitativa Discreta (Razón)[cite: 2] | Atributo entero (`SMALLINT`) en `estudiantes` validado en el rango `15 <= edad <= 75`. |
| **3** | Género[cite: 2] | Cualitativa Dicotómica (Nominal)[cite: 2] | Atributo `VARCHAR(15)` en `estudiantes` restringido a `'Femenino'` o `'Masculino'`[cite: 2]. |
| **4** | Si ha usado o no Excel[cite: 2] | Cualitativa Dicotómica (Nominal)[cite: 2] | Atributo booleano (`ha_usado_excel BOOLEAN NOT NULL`) en `encuestas_estudiantes`. |
| **5** | Cuántas operaciones básicas realiza[cite: 2] | Cuantitativa Discreta (Razón: 0 a 6) | **Atributo Calculado por el ETL (`cantidad_operaciones`):** No se solicita manualmente al usuario para evitar contradicciones con la Pregunta 6. El ETL calcula `len(operaciones_seleccionadas)` de forma automática. |
| **6** | Operaciones básicas que puede realizar[cite: 2] | Cualitativa Politómica (Nominal)[cite: 2] | **Desacoplamiento $N:M$ (1FN a 3FN):** Se normaliza mediante el catálogo `cat_operaciones_excel` y la tabla puente `encuesta_operaciones`. |
| **7** | Interés en materia electiva de Excel[cite: 2] | Cualitativa Dicotómica (Nominal)[cite: 2] | Atributo booleano (`interes_electiva BOOLEAN NOT NULL`). |
| **8** | Disponibilidad de herramientas tecnológicas[cite: 2] | Cualitativa Dicotómica (Nominal)[cite: 2] | Atributo booleano (`tiene_herramientas BOOLEAN NOT NULL`). |
| **9** | Percepción de beneficio profesional y académico[cite: 2] | Cualitativa Politómica (Nominal)[cite: 2] | Clave foránea (`id_percepcion`) hacia `cat_percepcion_utilidad` (tipificando los 4 segmentos cerrados del estudio)[cite: 2]. |
| **10** | Percepción respecto a su manejo de Excel[cite: 2] | Cualitativa Politómica (Ordinal)[cite: 2] | Clave foránea (`id_nivel`) hacia `cat_niveles_manejo`, conservando el orden jerárquico del `1` (Muy Malo) al `5` (Muy Bueno)[cite: 2]. |

---

## 2. Diagrama Entidad-Relación (DER en 3FN)

```mermaid
erDiagram
    CAT_SECCIONES ||--o{ ESTUDIANTES : "agrupa (1:N)"
    ESTUDIANTES ||--|| ENCUESTAS_ESTUDIANTES : "registra (1:1)"
    CAT_PERCEPCION_UTILIDAD ||--o{ ENCUESTAS_ESTUDIANTES : "clasifica (1:N)"
    CAT_NIVELES_MANEJO ||--o{ ENCUESTAS_ESTUDIANTES : "pondera (1:N)"
    ENCUESTAS_ESTUDIANTES ||--o{ ENCUESTA_OPERACIONES : "detalla (1:N)"
    CAT_OPERACIONES_EXCEL ||--o{ ENCUESTA_OPERACIONES : "clasifica (1:N)"

    CAT_SECCIONES {
        smallint id_seccion PK "11 | 12"
        varchar nombre_seccion UK "Sección 11 | Sección 12"
    }

    ESTUDIANTES {
        varchar cedula PK "Cédula de Identidad"
        varchar nombre_completo "Nombre y Apellido"
        varchar correo UK "Correo electrónico"
        smallint id_seccion FK
        smallint edad "15 a 75"
        varchar genero "Femenino | Masculino"
        timestamptz created_at
    }

    CAT_OPERACIONES_EXCEL {
        smallint id_operacion PK "1 al 6"
        varchar nombre_operacion UK "Sumar, Restar, Multiplicar, Dividir, Gráficos, Tablas dinámicas"
    }

    CAT_PERCEPCION_UTILIDAD {
        smallint id_percepcion PK "1 al 4"
        varchar descripcion_segmento UK "4 categorías cerradas de utilidad"
    }

    CAT_NIVELES_MANEJO {
        smallint id_nivel PK "1 al 5 (Escala Ordinal)"
        varchar etiqueta_ordinal UK "Muy Malo, Malo, Regular, Bueno, Muy Bueno"
    }

    ENCUESTAS_ESTUDIANTES {
        uuid id_encuesta PK
        timestamptz created_at
        varchar cedula FK, UK "1:1 con Estudiante"
        boolean ha_usado_excel
        smallint cantidad_operaciones "Calculada por ETL"
        boolean interes_electiva
        boolean tiene_herramientas
        smallint id_percepcion FK
        smallint id_nivel FK
    }

    ENCUESTA_OPERACIONES {
        uuid id_encuesta PK, FK
        smallint id_operacion PK, FK
    }
```

---

## 3. Especificación del Esquema Relacional en PostgreSQL (Supabase)

Toda interacción en la aplicación debe ejecutarse con el SDK de Supabase (`supabase-py`). Las sentencias DDL se gestionan en [`src/database/schema.sql`](file:///c:/Users/vicoa/oltp-streamlit-plantilla/src/database/schema.sql).