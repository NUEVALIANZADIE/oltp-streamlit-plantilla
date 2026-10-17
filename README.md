# OLTP Streamlit Template (Vibecoding Base)

Este repositorio es una plantilla base diseñada para el desarrollo de aplicaciones OLTP con Streamlit, estructurada específicamente para sesiones de Vibecoding. La arquitectura permite la integración fluida de agentes de IA, separando claramente las reglas del sistema, las habilidades (skills) y el contexto del proyecto.

## Características principales de la arquitectura:
- Gestión de Contexto Aislada: Permite adaptar el proyecto modificando únicamente los documentos de contexto dentro del directorio docs/, sin necesidad de alterar las reglas base o los roles de los agentes.
- Directivas Globales: Cuenta con el archivo .antigravity/rules.md para centralizar las directivas de arquitectura, roles de los agentes y normativas de seguridad.
- Sistema Modular de Habilidades (Skills): Utiliza un directorio dedicado (.agents/skills/) para gestionar los módulos de habilidades de los agentes (tanto preinstaladas como propias), incluyendo integraciones oficiales como el supabase-sdk.

¿Cómo usar esta plantilla en tus sesiones de Vibecoding?
Esta plantilla está pensada para que no tengas que escribir el código desde cero, sino para que orquestes a tus agentes de IA (como Google Antigravity).

Clona el repositorio: Inicia tu proyecto con esta base.

Alimenta el Contexto: Antes de pedirle a la IA que programe, ve a la carpeta docs/ y actualiza los documentos con la lógica de negocio, las variables de tu formulario y los detalles del ETL que mencionas en tu documento base.

Ajusta las Reglas (Opcional): Si necesitas que el agente se comporte diferente (por ejemplo, que use una librería específica para la base de datos), modifícalo en .antigravity/rules.md.

Comienza a "Vibecodear": Pídele a tu IDE agéntico que lea el contexto y comience a generar la aplicación de Streamlit y el flujo OLTP/ETL basándose en las reglas establecidas.

Ejecuta y prueba: Corre streamlit run app.py para visualizar los cambios que la IA va generando en tiempo real.

Copia y pega esto en tu README.md
Markdown
# OLTP Streamlit Template (Vibecoding Base) 🚀

Este repositorio es una plantilla base diseñada para el desarrollo rápido de aplicaciones OLTP con Streamlit, estructurada específicamente para sesiones de **Vibecoding** utilizando IDEs agénticos (como Google Antigravity). 

La arquitectura permite la creación de un sistema interactivo para la captura de información mediante formularios dinámicos, integrando un proceso ETL (Extracción, Transformación y Carga) en la nube.

## 🎯 Objetivo de la Plantilla

Desarrollar una app de Streamlit que actúe como un sistema OLTP para la recolección de datos a través de formularios web dinámicos. Extrae las variables ingresadas por el usuario, las transforma según las reglas de negocio y las carga en la base de datos, todo orquestado mediante agentes de Inteligencia Artificial.
