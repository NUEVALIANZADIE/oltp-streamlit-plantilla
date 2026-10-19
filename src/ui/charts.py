"""
Módulo generador de gráficos estadísticos en Matplotlib para el Cuadro de Mando.
Implementa estética limpia, eliminación de spines superiores/derechos y paleta del Brand Book.
"""

from __future__ import annotations

from typing import Any, Dict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paleta del Brand Book
COLOR_PRIMARY = "#0A2540"
COLOR_S11 = "#2563EB"       # Azul Cobalto (Sección 11 - Cohorte Joven)
COLOR_S12 = "#059669"       # Verde Esmeralda (Sección 12 - Cohorte Adulta)
COLOR_ALERT = "#DC2626"     # Rojo Suave (Déficit Tecnológico)
COLOR_NEUTRAL = "#64748B"   # Gris Pizarra
COLOR_BORDER = "#CBD5E1"    # Gris para ejes y cuadrículas
COLOR_TEXT = "#475569"


def _aplicar_estetica_base(ax: plt.Axes, titulo: str, xlabel: str = "", ylabel: str = "") -> None:
    """
    Aplica las reglas estéticas institucionales:
    - Remueve bordes superior y derecho (spines).
    - Coloriza ejes en gris tenue.
    - Cuadrícula suave punteada en el eje Y.
    - Título y etiquetas legibles.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_BORDER)
    ax.spines["bottom"].set_color(COLOR_BORDER)

    ax.grid(axis="y", linestyle="--", alpha=0.35, color=COLOR_BORDER)
    ax.set_axisbelow(True)

    ax.set_title(titulo, fontsize=13, fontweight="bold", color=COLOR_PRIMARY, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, fontweight="medium", color=COLOR_TEXT)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, fontweight="medium", color=COLOR_TEXT)
    ax.tick_params(colors=COLOR_TEXT, labelsize=9)


def plot_distribucion_operaciones(df_frecuencias: pd.DataFrame) -> plt.Figure:
    """
    Genera el gráfico comparativo de barras agrupadas para la cantidad de operaciones (0 al 6)
    dominadas por los estudiantes de la Sección 11 (Azul) vs. Sección 12 (Verde).

    Args:
        df_frecuencias: DataFrame con columnas 'Cantidad Operaciones', 'Sección 11', 'Sección 12'.

    Returns:
        plt.Figure: Objeto de figura de Matplotlib listo para renderizarse en Streamlit.
    """
    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=100)

    x = np.arange(len(df_frecuencias))
    width = 0.38

    s11_vals = df_frecuencias["Sección 11"].values
    s12_vals = df_frecuencias["Sección 12"].values

    rects1 = ax.bar(
        x - width / 2,
        s11_vals,
        width,
        label="Sección 11 (Joven)",
        color=COLOR_S11,
        alpha=0.9,
        edgecolor="none",
    )
    rects2 = ax.bar(
        x + width / 2,
        s12_vals,
        width,
        label="Sección 12 (Adulta)",
        color=COLOR_S12,
        alpha=0.9,
        edgecolor="none",
    )

    _aplicar_estetica_base(
        ax,
        titulo="Distribución de Operaciones por Sección",
        xlabel="Cantidad de Operaciones Básicas (0 a 6)",
        ylabel="N° Estudiantes",
    )

    ax.set_xticks(x)
    ax.set_xticklabels([str(op) for op in df_frecuencias["Cantidad Operaciones"]])
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")

    # Etiquetas directas sobre las barras si hay valores > 0
    if sum(s11_vals) + sum(s12_vals) > 0:
        ax.bar_label(rects1, padding=2, fontsize=8, color=COLOR_PRIMARY, fontweight="semibold")
        ax.bar_label(rects2, padding=2, fontsize=8, color=COLOR_PRIMARY, fontweight="semibold")

    fig.tight_layout()
    return fig


def plot_brecha_tecnologica(brecha_data: Dict[int, Dict[str, Any]]) -> plt.Figure:
    """
    Genera el gráfico comparativo de disponibilidad de computadora/WiFi en el hogar
    contrastando la Sección 11 frente a la Sección 12 y destacando el déficit en rojo.

    Args:
        brecha_data: Diccionario con llaves 11 y 12 con 'con_herramientas_pct' y 'deficit_pct'.

    Returns:
        plt.Figure: Objeto de figura de Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(5.4, 3.2), dpi=100)

    secciones = ["Sección 11\n(Cohorte Joven)", "Sección 12\n(Cohorte Adulta)"]
    con_herramientas = [
        brecha_data.get(11, {}).get("con_herramientas_pct", 0.0),
        brecha_data.get(12, {}).get("con_herramientas_pct", 0.0),
    ]
    deficit = [
        brecha_data.get(11, {}).get("deficit_pct", 0.0),
        brecha_data.get(12, {}).get("deficit_pct", 0.0),
    ]

    y_pos = np.arange(len(secciones))
    bar_height = 0.45

    # Barras apiladas horizontalmente al 100%
    b1 = ax.barh(
        y_pos,
        con_herramientas,
        height=bar_height,
        label="Dispone de PC/WiFi en Casa",
        color=COLOR_S12,
        alpha=0.9,
    )
    b2 = ax.barh(
        y_pos,
        deficit,
        left=con_herramientas,
        height=bar_height,
        label="Déficit Tecnológico (Sin PC/WiFi)",
        color=COLOR_ALERT,
        alpha=0.9,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_BORDER)
    ax.spines["bottom"].set_color(COLOR_BORDER)
    ax.grid(axis="x", linestyle="--", alpha=0.35, color=COLOR_BORDER)
    ax.set_axisbelow(True)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(secciones, fontsize=10, fontweight="semibold", color=COLOR_PRIMARY)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Porcentaje de la Cohorte (%)", fontsize=10, color=COLOR_TEXT)
    ax.set_title("Brecha Tecnológica en el Hogar por Sección", fontsize=13, fontweight="bold", color=COLOR_PRIMARY, pad=12)
    ax.legend(frameon=False, fontsize=9, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2)

    # Etiquetas dentro o sobre las barras
    for idx, (con_val, def_val) in enumerate(zip(con_herramientas, deficit)):
        if con_val > 10:
            ax.text(
                con_val / 2,
                idx,
                f"{con_val:.1f}%",
                va="center",
                ha="center",
                color="#FFFFFF",
                fontweight="bold",
                fontsize=9,
            )
        if def_val > 10:
            ax.text(
                con_val + (def_val / 2),
                idx,
                f"{def_val:.1f}%",
                va="center",
                ha="center",
                color="#FFFFFF",
                fontweight="bold",
                fontsize=9,
            )

    fig.tight_layout()
    return fig


def plot_distribucion_percepcion(dist_percepcion: Dict[str, int]) -> plt.Figure:
    """
    Genera un gráfico de barras horizontales mostrando la percepción de utilidad de Excel.

    Args:
        dist_percepcion: Diccionario con descripción de categoría y conteo de respuestas.

    Returns:
        plt.Figure: Objeto de figura de Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=100)

    categorias = list(dist_percepcion.keys())
    conteos = list(dist_percepcion.values())

    y_pos = np.arange(len(categorias))

    bars = ax.barh(y_pos, conteos, height=0.55, color=COLOR_PRIMARY, alpha=0.85)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_BORDER)
    ax.spines["bottom"].set_color(COLOR_BORDER)
    ax.grid(axis="x", linestyle="--", alpha=0.35, color=COLOR_BORDER)
    ax.set_axisbelow(True)

    ax.set_yticks(y_pos)
    # Acortar etiquetas para legibilidad en pantallas compactas
    etiquetas_cortas = [
        cat if len(cat) <= 38 else cat[:35] + "..." for cat in categorias
    ]
    ax.set_yticklabels(etiquetas_cortas, fontsize=9, color=COLOR_TEXT)
    ax.set_xlabel("Frecuencia Absoluta", fontsize=10, color=COLOR_TEXT)
    ax.set_title("Percepción de Beneficio Profesional y Académico", fontsize=12, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    if sum(conteos) > 0:
        ax.bar_label(bars, padding=3, fontsize=9, color=COLOR_PRIMARY, fontweight="semibold")

    fig.tight_layout()
    return fig


def plot_distribucion_autoevaluacion(dist_niveles: Dict[str, int]) -> plt.Figure:
    """
    Genera un gráfico de barras verticales para la escala ordinal de autoevaluación (1 al 5).

    Args:
        dist_niveles: Diccionario con etiqueta ordinal y frecuencia absoluta.

    Returns:
        plt.Figure: Objeto de figura de Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=100)

    etiquetas = list(dist_niveles.keys())
    conteos = list(dist_niveles.values())

    # Paleta secuencial de menor a mayor dominio
    colores = ["#EF4444", "#F97316", "#FBBF24", "#3B82F6", "#10B981"]

    bars = ax.bar(etiquetas, conteos, width=0.5, color=colores, alpha=0.9)

    _aplicar_estetica_base(
        ax,
        titulo="Autopercepción del Nivel de Manejo de Excel",
        xlabel="Escala Ordinal (1: Muy Malo a 5: Muy Bueno)",
        ylabel="Estudiantes",
    )

    if sum(conteos) > 0:
        ax.bar_label(bars, padding=2, fontsize=9, color=COLOR_PRIMARY, fontweight="semibold")

    fig.tight_layout()
    return fig
