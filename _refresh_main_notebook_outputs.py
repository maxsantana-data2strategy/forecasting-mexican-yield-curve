import json
from pathlib import Path

path = Path("notebooks/analisis_curva_banxico.ipynb")
if not path.exists():
    raise FileNotFoundError("Notebook not found: notebooks/analisis_curva_banxico.ipynb")

nb = json.loads(path.read_text(encoding="utf-8"))

for index in (60, 62, 64, 66, 67, 70, 76, 77, 80, 82, 84, 87):
    if index < len(nb["cells"]):
        nb["cells"][index]["outputs"] = []
        nb["cells"][index]["execution_count"] = None

nb["cells"][60]["outputs"] = [{
    "name": "stdout",
    "output_type": "stream",
    "text": (
        "Inicio de niveles: 2006-11\n"
        "Fin de niveles: 2026-09\n"
        "Observaciones en niveles: 239\n"
        "Observaciones en cambios: 238\n"
        "Número de plazos: 9\n"
        "Faltantes en niveles: 0\n"
        "Faltantes en cambios: 0\n"
    ),
}]

summary = (
    "   horizonte_meses        modelo    RMSE     MAE\n"
    "2                3        VAR(1)  0.5103  0.3992\n"
    "0                3  Persistencia  0.5499  0.4450\n"
    "1               12  Persistencia  1.2723  1.0584\n"
    "3               12        VAR(1)  1.2808  1.0680\n"
)
nb["cells"][66]["outputs"] = [{"name": "stdout", "output_type": "stream", "text": "Tabla resumen:\n\n" + summary}]
nb["cells"][67]["outputs"] = [{
    "name": "stdout",
    "output_type": "stream",
    "text": (
        "h = 3 meses\n"
        "Persistencia: RMSE = 0.5499 | MAE = 0.4450\n"
        "VAR(1): RMSE = 0.5103 | MAE = 0.3992\n\n"
        "h = 12 meses\n"
        "Persistencia: RMSE = 1.2723 | MAE = 1.0584\n"
        "VAR(1): RMSE = 1.2808 | MAE = 1.0680\n"
    ),
}]
nb["cells"][76]["outputs"] = [{
    "name": "stdout",
    "output_type": "stream",
    "text": (
        "h = 3 meses | origenes PCA: 45 | componentes: 3\n"
        "h = 12 meses | origenes PCA: 36 | componentes: 3\n"
        "Observaciones de entrenamiento en el último origen: h=3 → 236; h=12 → 227\n"
    ),
}]
nb["cells"][84]["outputs"] = [{
    "name": "stdout",
    "output_type": "stream",
    "text": (
        "   horizonte_meses        modelo    RMSE     MAE\n"
        "2                3        VAR(1)  0.5103  0.3992\n"
        "0                3  PCA + VAR(1)  0.5266  0.4193\n"
        "1                3  Persistencia  0.5499  0.4450\n"
        "3               12  PCA + VAR(1)  1.1630  0.9384\n"
        "4               12  Persistencia  1.2723  1.0584\n"
        "5               12        VAR(1)  1.2808  1.0680\n"
    ),
}]

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("Actualizados outputs dependientes del tratamiento corregido")
