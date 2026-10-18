# Diseño de la Investigación y Operacionalización de Variables (`research_design.md`)

**Título del Estudio:** Investigación acerca del nivel de manejo de Excel de los estudiantes del Propedéutico de la Escuela de Estadística y Ciencias Actuariales (EECA - UCV)[cite: 2]  
**Autores de Referencia:** Schantal Troja, Vicente Díaz y Victoria Díaz (EECA - UCV)[cite: 2]  

---

## 1. Planteamiento del Problema y Finalidad
Existe una brecha significativa entre las exigencias prácticas de la Escuela de Estadística y Ciencias Actuariales (UCV) y el dominio previo de Microsoft Excel con el que ingresan los estudiantes del curso propedéutico[cite: 2]. Esta carencia genera inseguridad estudiantil al enfrentar tareas que requieren tanto equipamiento tecnológico propio (computadora e internet en el hogar) como dominio técnico de hojas de cálculo para estadística descriptiva (ordenamiento de datos, medidas de tendencia central, dispersión, posición, asimetría, curtosis, tablas de frecuencias y gráficos)[cite: 2].

**Finalidad del Sistema:** Capturar transacciones en tiempo real (OLTP) mediante una aplicación web y procesar automáticamente los indicadores estadísticos en un Cuadro de Mando para sustentar ante la coordinación académica la apertura de una **materia electiva práctica de Excel**[cite: 1, 2].

---

## 2. Objetivos de la Investigación
### Objetivo General
Evaluar el nivel de manejo de Excel de los estudiantes del propedéutico de la carrera de Estadística y Ciencias Actuariales de la Universidad Central de Venezuela[cite: 2].

### Objetivos Específicos (Métricas del Cuadro de Mando)
1. Estudiar el nivel promedio, moda, dispersión (Desviación Estándar y Coeficiente de Variación), asimetría y curtosis del manejo de operaciones básicas en Excel segmentado por sección (Sección 11 vs. Sección 12)[cite: 2].
2. Evaluar la proporción de estudiantes que cuentan con las herramientas tecnológicas necesarias (PC/Laptop/WiFi) en su hogar para realizar prácticas[cite: 2].
3. Calcular el porcentaje de la muestra que domina cada operación básica específica (sumar, restar, multiplicar, dividir, crear gráficos y tablas dinámicas)[cite: 2].
4. Medir el porcentaje de interés estudiantil en cursar una materia electiva de Excel[cite: 2].
5. Analizar la percepción sobre la utilidad futura de Excel en el ámbito académico y profesional, así como la autopercepción del nivel de manejo tras completar el cuestionario[cite: 2].

---

## 3. Rediseño Metodológico (De Google Forms a Sistema OLTP)
En el levantamiento original mediante Google Forms se detectaron puntos de fricción que este sistema OLTP corrige de raíz[cite: 1, 2]:
- **Validación de Edad:** Pasa de ser respuesta abierta en texto a un control numérico discreto restringido (`15` a `75` años)[cite: 2].
- **Eliminación de Inconsistencia entre Pregunta 5 y Pregunta 6:** En el cuestionario original se preguntaba por separado *"¿Cuántas operaciones básicas sabes realizar?"* (0 a 7) y *"¿Qué tipo de operaciones básicas sabes realizar?"*[cite: 2]. En este sistema OLTP, el usuario únicamente marca **cuáles operaciones sabe realizar** y el pipeline ETL calcula automáticamente la variable cuantitativa discreta `cantidad_operaciones` (`0` a `6`), garantizando coherencia matemática absoluta.
- **Tipificación de Percepción de Utilidad (Pregunta 9):** Pasa de texto abierto a una variable politómica cerrada con las 4 categorías analíticas descubiertas en el estudio original[cite: 2].

---

## 4. Cuadro de Operacionalización de Variables

| N° | Variable | Tipo de Variable | Escala | Valores Permitidos / Regla en el Sistema OLTP |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Sección del propedéutico | Cualitativa Dicotómica | Nominal | `Sección 11`, `Sección 12`[cite: 2] |
| **2** | Edad en años | Cuantitativa Discreta | Razón | Entero entre `15` y `75` años[cite: 2] |
| **3** | Género | Cualitativa Dicotómica | Nominal | `Femenino`, `Masculino`[cite: 2] |
| **4** | Uso previo de Excel | Cualitativa Dicotómica | Nominal | `Sí` (`True`), `No` (`False`)[cite: 2] |
| **5** | Cantidad de operaciones básicas que realiza | Cuantitativa Discreta | Razón | `0, 1, 2, 3, 4, 5, 6` *(Calculada automáticamente por el ETL según Pregunta 6)* |
| **6** | Operaciones básicas que puede realizar | Cualitativa Politómica | Nominal | Selección múltiple: `Sumar`, `Restar`, `Multiplicar`, `Dividir`, `Crear gráficos`, `Crear tablas dinámicas`[cite: 2] |
| **7** | Interés en materia electiva de Excel | Cualitativa Dicotómica | Nominal | `Sí` (`True`), `No` (`False`)[cite: 2] |
| **8** | Disponibilidad de herramientas tecnológicas | Cualitativa Dicotómica | Nominal | `Sí` (`True`), `No` (`False`)[cite: 2] |
| **9** | Percepción de beneficio profesional y académico | Cualitativa Politómica | Nominal | 1. `Puede ayudarle y facilitarle la carrera`<br>2. `Le será útil para diversos fines generales`<br>3. `Brindará mejores oportunidades en el ámbito profesional y laboral`<br>4. `Será útil y brindará oportunidades tanto en la carrera como en el ámbito profesional`[cite: 2] |
| **10** | Autopercepción del nivel de manejo de Excel | Cualitativa Politómica | Ordinal | `1`: Muy Malo, `2`: Malo, `3`: Regular, `4`: Bueno, `5`: Muy Bueno[cite: 2] |