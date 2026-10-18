---

### 8. `docs/target_audience.md`
```markdown
# Perfil de Público Objetivo y Usuarios del Sistema (`target_audience.md`)

**Proyecto:** Sistema OLTP y Cuadro de Mando — Nivel de Manejo de Excel (EECA-UCV)  

---

## 1. Usuario Primario: El Estudiante Encuestado (Vista del Formulario)
Corresponde a la unidad estadística del estudio: estudiantes del curso propedéutico de la Escuela de Estadística y Ciencias Actuariales de la UCV[cite: 2]. La investigación de referencia identifica dos subgrupos demográficos claramente diferenciados que utilizan el mismo formulario[cite: 2]:

1. **Perfil Sección 11 (Cohorte Joven / Recién Egresados de Secundaria):**
   - **Edad promedio:** ~19.12 años (grupo muy homogéneo en edad, $CV = 5.35\%$)[cite: 2].
   - **Características técnicas y socioeconómicas:** Alta dispersión en su manejo de Excel ($CV = 70.18\%$, moda de `0` operaciones realizadas) y un **23.52% no cuenta con herramientas tecnológicas propias (PC/Internet) en casa**[cite: 2].
2. **Perfil Sección 12 (Cohorte Adulta / Con Experiencia Laboral):**
   - **Edad promedio:** ~28.69 años (grupo heterogéneo en edad, $CV = 33.99\%$)[cite: 2].
   - **Características técnicas y socioeconómicas:** Mayor dominio y homogeneidad en Excel (promedio y moda de `5` operaciones básicas) y un **92.30% cuenta con herramientas tecnológicas en casa**[cite: 2].

### Requerimientos de UX/UI Derivados para el Formulario:
- **Diseño Mobile-First:** Dado que el enlace del formulario se difunde principalmente a través de grupos de WhatsApp estudiantiles y casi una cuarta parte de la Sección 11 no posee computadora en casa, el formulario debe ser 100% funcional, ligero y cómodo de responder desde la pantalla de un teléfono móvil[cite: 2].
- **Lenguaje Claro y Cero Fricción:** No usar términos técnicos de bases de datos. Prevenir errores de entrada usando controles cerrados (botones de radio, selectores numéricos acotados y casillas de verificación reactivas).

---

## 2. Usuario Secundario: Coordinación Académica, Profesores e Investigadores (Vista del Dashboard)
Corresponde a los docentes de la cátedra de Estadística, la coordinación del Curso Propedéutico de la EECA-UCV y los líderes estudiantiles que consultan el Cuadro de Mando para la toma de decisiones institucionales[cite: 2].

### Requerimientos Analíticos Derivados para el Cuadro de Mando:
- **Rigor Estadístico Descriptivo:** Un profesor de la EECA no toma decisiones solo con un gráfico de torta simple. El dashboard debe presentar las métricas formales de la estadística descriptiva: **Media, Moda, Desviación Estándar, Coeficiente de Variación ($CV$), Asimetría y Curtosis** desglosadas por sección[cite: 2].
- **Visibilidad de Brechas para Toma de Decisiones:** El dashboard debe permitir contrastar de un vistazo:
  1. Que el interés por la materia electiva es masivo en ambas secciones (>88% en Sección 11 y 100% en Sección 12)[cite: 2].
  2. Que la apertura de la materia electiva requiere considerar laboratorios en la escuela, dado el 23.52% de estudiantes de la Sección 11 que no tienen equipos en su hogar[cite: 2].