# Guía Visual e Identidad del Sistema (`brand_book.md`)

**Proyecto:** Sistema OLTP y Cuadro de Mando — Nivel de Manejo de Excel (EECA-UCV)  
**Framework UI:** Streamlit + Matplotlib  

---

## 1. Identidad Visual y Paleta de Colores
El diseño debe proyectar rigor estadístico, limpieza editorial y modernidad académica inspirada en la Escuela de Estadística y Ciencias Actuariales (UCV):

- **Color Primario (Institucional):** Azul Profundo `#0A2540` (Encabezados y títulos principales).
- **Color de Acento (Interactivo):** Azul Real `#1D4ED8` (Botones de envío, pestañas activas).
- **Fondo Principal:** Blanco Puro `#FFFFFF`.
- **Fondo Secundario (Tarjetas y Sidebar):** Gris Neutro Suave `#F8FAFC`.
- **Paleta Comparativa Obligatoria para Gráficos (Sección 11 vs. Sección 12):**
  - **Sección 11 (Cohorte Joven ~19 años):** Azul Cobalto `#2563EB`.
  - **Sección 12 (Cohorte Adulta/Laboral ~29 años):** Verde Esmeralda `#059669`.
  - **Alerta / Carencia de Herramientas:** Ámbar/Rojo Suave `#DC2626`.

---

## 2. Estructura de Navegación (Layout en Streamlit)
La aplicación en `main.py` debe estructurarse con `st.set_page_config(page_title="OLTP Excel EECA-UCV", layout="wide")` y dividirse en **2 pestañas principales (`st.tabs`)**:

### Pestaña 1: `📋 Instrumento de Recolección (Formulario OLTP)`
- Centrado o en contenedor limpio para lectura cómoda en dispositivos móviles.
- Agrupado visualmente en 3 bloques lógicos con `st.subheader`:
  1. **Perfil Demográfico:** Sección, Edad y Género[cite: 2].
  2. **Dominio Técnico de Excel:** ¿Ha usado Excel? + Selector múltiple dinámico de operaciones básicas (se deshabilita si responde "No")[cite: 2].
  3. **Viabilidad y Percepción:** Disponibilidad de herramientas en el hogar, interés en la electiva, percepción de utilidad futura y autopercepción en escala ordinal (1 al 5)[cite: 2].
- Al enviar con éxito, mostrar `st.success()` indicando cuántas operaciones fueron registradas en la transacción.

### Pestaña 2: `📊 Cuadro de Mando Estadístico (En Tiempo Real)`
- **Fila 1 — Tarjetas de Resumen Global (`st.metric` en 4 columnas):**
  1. Total de Estudiantes Encuestados ($n$).
  2. % de Uso Previo de Excel (Referencia base: ~93.3%)[cite: 2].
  3. % de Interés en la Materia Electiva (Referencia base: ~93.3%)[cite: 2].
  4. % con Déficit de Herramientas Tecnológicas en Casa[cite: 2].
- **Fila 2 — Comparativa Estadística por Sección (Sección 11 vs. Sección 12):**
  - Tabla resumen generada en Pandas mostrando para **Edad** y **Cantidad de Operaciones**: Media ($\bar{x}$), Moda ($Mo$), Desviación Estándar ($S$), Coeficiente de Variación ($CV\%$), Coeficiente de Asimetría y Curtosis[cite: 2].
- **Fila 3 — Visualizaciones en Matplotlib (2 Columnas):**
  - **Gráfico Izquierdo:** Distribución comparativa de cantidad de operaciones dominadas (Sección 11 vs. Sección 12)[cite: 2].
  - **Gráfico Derecho:** Gráfico de barras apiladas o agrupadas de Disponibilidad de Herramientas Tecnológicas en el Hogar por Sección (evidenciando la brecha económica/tecnológica de la Sección 11 frente a la 12)[cite: 2].
- **Fila 4 — Percepción y Autoevaluación:**
  - Gráfico de barras horizontales para los 4 segmentos de utilidad futura y distribución ordinal de autopercepción del nivel de Excel[cite: 2].

---

## 3. Reglas Estéticas para Gráficos en Matplotlib
- **Cero Ruido Visual:** Eliminar siempre los bordes superior y derecho de cada gráfico:
  ```python
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)