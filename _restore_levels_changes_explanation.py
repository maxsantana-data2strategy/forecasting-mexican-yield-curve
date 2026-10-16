import json
from pathlib import Path

path = Path("notebooks/analisis_curva_banxico.ipynb")
if not path.exists():
    raise FileNotFoundError("Notebook not found: notebooks/analisis_curva_banxico.ipynb")

nb = json.loads(path.read_text(encoding="utf-8"))
cell = next(
    c for c in nb["cells"]
    if c["cell_type"] == "markdown"
    and "Estructura de la curva mediante PCA" in c.get("source", [""])[0]
)
lines = cell["source"]
position = next(i for i, line in enumerate(lines) if "niveles mensuales" in line)
addition = """\n\nLa diferencia entre ambas representaciones puede verse con el CETE a 28 días:\n\n- **Octubre de 2006:** nivel = 7.05%; cambio = —\n- **Noviembre de 2006:** nivel = 7.04%; cambio = −0.01 puntos porcentuales\n- **Abril de 2007:** nivel = 7.01%; cambio = −0.03 puntos porcentuales\n- **Mayo de 2007:** nivel = 7.24%; cambio = +0.23 puntos porcentuales\n\nLos niveles describen dónde se encuentra cada plazo en un mes determinado; los cambios describen cuánto se movió desde el mes anterior. Por eso los niveles son la representación principal para estudiar la forma de la curva, mientras que los cambios se utilizan como una comprobación de la dinámica mensual.\n"""
assert not any("La diferencia entre ambas representaciones" in line for line in lines)
lines[position] = lines[position].rstrip("\n") + addition
cell["source"] = lines
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
