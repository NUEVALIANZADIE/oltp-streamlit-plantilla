# Guía Visual e Identidad del Sistema (`brand_book.md`)

**Proyecto:** Sistema OLTP y Cuadro de Mando — Nivel de Manejo de Excel (EECA-UCV)  
**Framework UI:** Streamlit + Matplotlib  
**Directorio de Recursos:** `assets/img/` (Logos, banners, íconos y referencias visuales)

---

## 1. Identidad Visual y Paleta de Colores

El diseño debe proyectar rigor estadístico, pulcritud editorial y modernidad académica inspirada en la Escuela de Estadística y Ciencias Actuariales (EECA - UCV):

- **Color Primario (Institucional):** Azul Profundo `#0A2540` (Títulos principales, encabezados de tablas, branding).
- **Color de Acento (Interactivo):** Azul Real `#1D4ED8` (Botones de envío, pestañas activas, elementos destacados).
- **Color Secundario de Contraste:** Verde Esmeralda `#059669` (Indicadores de éxito, métricas positivas, Sección 12).
- **Fondo Principal de la Aplicación:** Blanco Puro `#FFFFFF`.
- **Fondo Secundario (Cards y Sidebar):** Gris Neutro Suave `#F8FAFC`.
- **Bordes y Delimitadores:** Gris Claro `#E2E8F0`.
- **Color de Alerta / Carencia:** Rojo Suave `#DC2626` (Déficit de herramientas tecnológicas, alertas de validación).

### Paleta Comparativa para Gráficos Estadísticos (Sección 11 vs. Sección 12)
Para garantizar consistencia visual a lo largo de todo el Cuadro de Mando:
- **Sección 11 (Cohorte Joven ~19 años):** Azul Cobalto `#2563EB`.
- **Sección 12 (Cohorte Adulta/Laboral ~29 años):** Verde Esmeralda `#059669`.
- **Promedio Global / Referencia:** Gris Pizarra `#64748B`.

---

## 2. Tipografía y Jerarquía Visual

Para lograr una apariencia premium y académica, la aplicación en Streamlit utilizará fuentes de Google Fonts inyectadas vía CSS:

- **Tipografía Principal (Titulares y Encabezados):** `Inter` o `Montserrat` (Pesos: 600 SemiBold, 700 Bold). Proporciona autoridad visual, geometría moderna y legibilidad en pantallas retina y móviles.
- **Tipografía Secundaria (Cuerpo y Formularios):** `Inter` o `Roboto` (Pesos: 400 Regular, 500 Medium). Diseñada para lectura cómoda de preguntas, labels de formulario y descripciones.
- **Tipografía Numérica (Métricas y Tablas Estadísticas):** `JetBrains Mono` o `Roboto Mono` (Para valores numéricos, promedios $\bar{x}$, modas, desviaciones y tablas de Pandas). Asegura que los números queden alineados con ancho fijo (*tabular numbers*).

---

## 3. Estructura del Directorio de Assets (`assets/img/`)

Todos los recursos gráficos se organizan en la raíz del proyecto dentro de `assets/img/`:

```
assets/
└── img/
    ├── logo_eeca.png            <-- Logo oficial de la EECA / UCV (transparente)
    ├── banner_formulario.png    <-- Header ilustrado o banner superior del formulario
    ├── icons/                   <-- Íconos temáticos (Flaticon / SVG o PNG)
    │   ├── excel_icon.png       <-- Ícono distintivo de Microsoft Excel
    │   ├── student_profile.png  <-- Ícono de perfil de estudiante
    │   ├── statistics_chart.png <-- Ícono del cuadro de mando
    │   └── computer_wifi.png    <-- Ícono de disponibilidad de equipo
    └── references/              <-- Diseños y maquetas de referencia aportadas por el equipo
        └── dashboard_ref.png    <-- Referencia visual del layout deseado para el Dashboard
```

---

## 4. Estructura de Navegación y Layout en Streamlit

La aplicación en `main.py` se configura con:
```python
st.set_page_config(
    page_title="OLTP Excel EECA-UCV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

La interfaz se divide en **2 pestañas principales (`st.tabs`)**:

### Pestaña 1: `📋 Instrumento de Recolección (Formulario OLTP)`
- **Header:** Logo institucional de la EECA (`assets/img/logo_eeca.png`) y título claro del estudio.
- **Diseño Mobile-First:** Ancho controlado y centrado para completarlo con una mano desde un teléfono móvil.
- **Bloques Visuales con `st.subheader`:**
  1. **Datos de Identificación y Demografía:** Cédula, Nombre Completo, Correo, Sección (11 o 12), Edad (control discreto 15-75) y Género.
  2. **Dominio Técnico de Excel:** Pregunta de uso previo + `st.multiselect` reactivo con las 6 operaciones básicas (se desactiva automáticamente si responde "No").
  3. **Factores Socio-Académicos:** Disponibilidad de PC/Internet en casa, interés en materia electiva, percepción de utilidad futura y autoevaluación (Likert 1-5).
- **Retroalimentación:** Al enviar, muestra `st.success()` con el resumen de la transacción registrada.

### Pestaña 2: `📊 Cuadro de Mando Estadístico (En Tiempo Real)`
- **Fila 1 — KPIs Globales (`st.metric` en 4 columnas):**
  1. Total de Estudiantes Encuestados ($n$).
  2. % de Uso Previo de Excel.
  3. % de Interés en Materia Electiva.
  4. % con Déficit Tecnológico en Casa.
- **Fila 2 — Tabla de Rigor Estadístico por Sección:**
  - Tabla generada en Pandas comparando Sección 11 vs. Sección 12 con formato tabular monoespaciado: Media ($\bar{x}$), Moda ($Mo$), Desviación Estándar ($S$), Coeficiente de Variación ($CV\%$), Asimetría y Curtosis.
- **Fila 3 — Gráficos Comparativos en Matplotlib (2 Columnas):**
  - **Izquierda:** Distribución de frecuencia de cantidad de operaciones dominadas (Sección 11 en azul vs. Sección 12 en verde).
  - **Derecha:** Brecha de herramientas tecnológicas en el hogar por sección (destacando alertas).
- **Fila 4 — Percepciones:**
  - Gráfico horizontal de utilidad esperada y distribución ordinal de autoevaluación.

---

## 5. Reglas Estéticas para Gráficos en Matplotlib

Para que los gráficos mantengan nivel de publicación académica:
- **Sin Ruido Visual:** Eliminar bordes superior y derecho:
  ```python
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_color('#CBD5E1')
  ax.spines['bottom'].set_color('#CBD5E1')
  ```
- **Líneas Guía Suaves:** Cuadrículas solo en el eje numérico con `alpha=0.25`, estilo punteado y color gris neutro.
- **Tipografías en los Gráficos:** Texto en `DejaVu Sans` o fuente sans-serif legible, títulos con peso bold en `#0A2540` y etiquetas en `#475569`.
- **Etiquetas de Datos Directas:** Preferir valores sobre las barras en vez de obligar al lector a estimar en el eje Y.