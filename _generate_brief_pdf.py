from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "outputs" / "figures"
OUT = ROOT / "docs" / "brief_curva_banxico.pdf"

NAVY = "#0e2942"
ORANGE = "#c26a23"
INK = "#17202a"
MUTED = "#607080"
RULE = "#d8e0e8"
PALE = "#f3f6f8"


def page(section, number):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.065, 0.965, "Curva de rendimientos nominal de México",
             fontsize=14, weight="bold", color=NAVY, va="top")
    fig.text(0.935, 0.965, f"Brief ejecutivo  |  {number}/5",
             fontsize=8.5, color=MUTED, ha="right", va="top")
    fig.text(0.065, 0.928, section.upper(), fontsize=8.2, weight="bold",
             color=ORANGE, va="top")
    fig.add_artist(plt.Line2D([0.065, 0.935], [0.909, 0.909],
                              transform=fig.transFigure, color=RULE, lw=0.8))
    fig.text(0.065, 0.035,
             "Assessment de Estadístico Jr.  |  14 de octubre de 2026  |  Tasas en puntos porcentuales",
             fontsize=7.1, color=MUTED, va="bottom")
    return fig


def paragraph(fig, text, x, y, width=102, size=9.2, leading=0.0165,
              color=INK):
    lines = []
    for chunk in text.split("\n"):
        if not chunk.strip():
            lines.append("")
        else:
            lines.extend(wrap(chunk, width=width, break_long_words=False))
    for line in lines:
        if line:
            fig.text(x, y, line, fontsize=size, color=color, va="top")
        y -= leading
    return y


def heading(fig, text, x, y, size=11.2):
    fig.text(x, y, text, fontsize=size, weight="bold", color=NAVY, va="top")
    return y - 0.03


def table(fig, rows, x, y, w, h, col_widths, font_size=8.1,
          best_cells=()):
    ax = fig.add_axes([x, y, w, h])
    ax.axis("off")
    tab = ax.table(cellText=rows, colWidths=col_widths, cellLoc="left",
                   bbox=[0, 0, 1, 1])
    tab.auto_set_font_size(False)
    tab.set_fontsize(font_size)
    for (row, _), cell in tab.get_celld().items():
        cell.set_edgecolor(RULE)
        cell.PAD = 0.018
        if row == 0:
            cell.set_facecolor(NAVY)
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif row % 2 == 0:
            cell.set_facecolor(PALE)
        if (row, _) in best_cells:
            cell.set_facecolor("#dcefe3")
            cell.get_text().set_weight("bold")
    return ax


def image(fig, path, box, caption, caption_y=None):
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró la visualización requerida: {path}")
    x, y, w, h = box
    ax = fig.add_axes([x, y, w, h])
    with Image.open(path) as source:
        ax.imshow(source, interpolation="none")
    ax.axis("off")
    if caption_y is None:
        caption_y = y - 0.018
    fig.text(x, caption_y, caption, fontsize=7.2, color=MUTED,
             ha="left", va="top", wrap=True)


vector_figures = []


with PdfPages(OUT) as pdf:
    fig = page("Resumen ejecutivo / visión general del proyecto", 1)
    fig.text(0.065, 0.875, "Estructura y pronóstico de la curva mexicana",
             fontsize=20, weight="bold", color=NAVY, va="top")
    fig.text(0.065, 0.842, "Preparado por: Max Santana",
             fontsize=9.3, color=MUTED, va="top")
    y = paragraph(
        fig,
        "El análisis estudia las tasas mensuales promedio de subasta de nueve instrumentos: CETES a 28, 91, 182 y 364 días, y MBONOS a 3, 5, 10, 20 y 30 años. La base cubre octubre de 2006 a septiembre de 2026 (1,936 registros y 240 meses).",
        0.065, 0.812, width=105, size=9.4, leading=0.018)
    y -= 0.012
    y = paragraph(
        fig,
        "El objetivo fue identificar una estructura común entre plazos y evaluar si esta ayuda a pronosticar a 3 y 12 meses. Se aplicó PCA en niveles y se compararon persistencia, VAR(1) directo y PCA + VAR(1), con una prueba temporal de ventana creciente.",
        0.065, y, width=105, size=9.4, leading=0.018)
    y -= 0.024
    y = heading(fig, "Hallazgos clave", 0.065, y)
    y = paragraph(
        fig,
        "- Tres componentes resumen 99.38% de la variación (PC1: 94.09%).\n- La prueba temporal incluye 45 orígenes a 3 meses y 36 a 12 meses.",
        0.065, y, width=105, size=9.0, leading=0.018)
    y -= 0.014
    y = heading(fig, "Comparación de modelos y benchmark", 0.065, y)
    rows = [
        ["Modelo", "h=3 RMSE", "h=3 MAE", "h=12 RMSE", "h=12 MAE"],
        ["Persistencia (benchmark)", "0.5499", "0.4450", "1.2723", "1.0584"],
        ["VAR(1) directo", "0.5103", "0.3992", "1.2808", "1.0680"],
        ["PCA + VAR(1)", "0.5266", "0.4193", "1.1630", "0.9384"],
    ]
    table(fig, rows, 0.065, y - 0.195, 0.87, 0.18,
          [0.31, 0.17, 0.17, 0.175, 0.175], font_size=7.9,
          best_cells={(2, 1), (2, 2), (3, 3), (3, 4)})
    fig.text(0.065, y - 0.215,
             "RMSE y MAE promedio en puntos porcentuales. Verde: menor error por horizonte y métrica.",
             fontsize=7.4, color=MUTED, va="top")
    paragraph(
        fig,
        "A 3 meses, VAR(1) directo presenta el menor error; a 12 meses, lo obtiene PCA + VAR(1). La evidencia es exploratoria y debe leerse junto con las limitaciones de los datos.",
        0.065, y - 0.25, width=105, size=8.7, leading=0.016)
    pdf.savefig(fig)
    plt.close(fig)

    fig = page("Decisiones de procesamiento de datos", 2)
    y = paragraph(fig,
        "La fuente en formato largo se reorganizó como matriz mensual, con un plazo por columna. No se encontraron duplicados ni faltantes en el archivo largo; los faltantes aparecen al alinear fechas, especialmente en los MBONOS de mayor plazo.",
        0.065, 0.875, width=105)
    y -= 0.012
    y = paragraph(fig,
        "La cobertura faltante fue de 1.7% para 3 años, 6.7% para 5 años, 26.2% para 10 años, 28.7% para 20 años y 30.0% para 30 años. Solo 40 de 240 meses tienen los nueve plazos observados; eliminar los meses incompletos habría dejado una muestra conjunta muy reducida.",
        0.065, y, width=105)
    y -= 0.012
    y = paragraph(fig,
        "Se conservó el calendario mensual y se aplicó forward-fill causal: cada faltante usa la última observación pasada, nunca información futura. El primer faltante a 20 años se mantuvo como NaN. Para el pronóstico, el relleno se hizo antes de recortar desde noviembre de 2006: la base completa contiene 239 niveles y 238 cambios mensuales.",
        0.065, y, width=105)
    y -= 0.012
    y = paragraph(fig,
        "Como control descriptivo, la correlación mínima entre plazos fue 0.73 en la muestra completada y 0.70 usando solo los 40 meses originalmente completos. La tasa objetivo de Banxico se usó solo para validar el factor de nivel, no como predictor.",
        0.065, y, width=105)
    y -= 0.035
    y = heading(fig, "Diseño de la evaluación de pronósticos", 0.065, y)
    paragraph(fig,
        "La prueba respeta el orden temporal: el entrenamiento inicial termina en septiembre de 2022 y los orígenes de evaluación comienzan en octubre de 2022, con ventana creciente.",
        0.065, y, width=105, size=8.9, leading=0.016)
    pdf.savefig(fig)
    plt.close(fig)

    fig = page("Estructura de la curva: análisis de componentes principales", 3)
    y = paragraph(fig,
        "El PCA se estimó sobre las nueve tasas en niveles, sin estandarizar, para conservar las diferencias de variabilidad entre plazos. Los tres primeros componentes explican 99.38% de la variación: PC1 94.09%, PC2 4.60% y PC3 0.69%.",
        0.065, 0.875, width=105)
    y -= 0.012
    paragraph(fig,
        "Las cargas permiten interpretar PC1 como nivel, PC2 como pendiente y PC3 como curvatura. La reconstrucción con tres componentes tiene un RMSE de 15.07 puntos base.",
        0.065, y, width=105)
    pdf.savefig(fig)
    plt.close(fig)

    fig = page("Estrategia de pronóstico y comparación", 4)
    y = paragraph(fig,
        "La persistencia mantiene el último nivel observado y fue el benchmark más competitivo. El VAR(1) directo modela conjuntamente los cambios mensuales de los nueve plazos; los cambios pronosticados se acumulan sobre el último nivel.",
        0.065, 0.875, width=105)
    y -= 0.010
    y = paragraph(fig,
        "PCA + VAR(1) reestima el PCA en cada origen, conserva tres factores y pronostica sus puntajes con un VAR(1); luego reconstruye los nueve plazos. En ambos casos se usa una ventana creciente y solo la información disponible hasta cada origen.",
        0.065, y, width=105)
    y -= 0.016
    y = heading(fig, "Lectura de los resultados", 0.065, y)
    paragraph(fig,
        "Como resume la tabla de la portada, el VAR(1) directo es el mejor promedio a 3 meses, mientras PCA + VAR(1) obtiene el menor error a 12 meses.",
        0.065, y, width=105, size=8.8, leading=0.016)
    pdf.savefig(fig)
    plt.close(fig)

    fig = page("Conclusiones, limitaciones y pasos futuros", 5)
    y = paragraph(fig,
        "La curva presenta una estructura común fuerte: nivel, pendiente y curvatura resumen casi toda la variación. La persistencia constituye una referencia exigente, en particular para los plazos largos.",
        0.065, 0.875, width=105)
    y -= 0.035
    heading(fig, "Conclusión operativa", 0.065, y)
    y = paragraph(fig,
        "Seleccionar el modelo según el horizonte, no asumir que uno domina en todos los casos: VAR(1) directo a 3 meses y PCA + VAR(1) a 12 meses bajo el diseño de evaluación utilizado.",
        0.065, y, width=105)
    y -= 0.035
    heading(fig, "Limitación principal", 0.065, y)
    y = paragraph(fig,
        "El forward-fill conserva la continuidad, pero puede introducir cambios mensuales iguales a cero y hacer que algunos valores evaluados representen la última subasta disponible, no una nueva subasta.",
        0.065, y, width=105)
    y -= 0.035
    heading(fig, "Siguientes pasos propuestos", 0.065, y)
    y = paragraph(fig,
        "1. Estimar la curva transversalmente en los meses sin observación.\n2. Distinguir meses con subasta efectiva al calcular cambios y errores.\n3. Comparar otros órdenes del VAR y probar formalmente la significancia de las diferencias predictivas.",
        0.065, y, width=105, size=9.0, leading=0.018)
    y -= 0.035
    paragraph(fig,
        "La prioridad para validar estos hallazgos es mejorar el tratamiento de la disponibilidad de subastas y repetir la evaluación fuera de muestra antes de usar los pronósticos para decisiones.",
        0.065, y, width=105, size=9.0, leading=0.018)
    pdf.savefig(fig)
    plt.close(fig)

print(f"PDF creado: {OUT}")
