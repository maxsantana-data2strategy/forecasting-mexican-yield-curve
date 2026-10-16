from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from statsmodels.tsa.api import VAR

root = Path(__file__).resolve().parent
raw_path = root / "data" / "raw" / "banxico_auction_rates_monthly.csv"
if not raw_path.exists():
    raise FileNotFoundError(f"Missing raw data: {raw_path}")

raw = pd.read_csv(raw_path, parse_dates=["DATE"])
order = [
    "CETEs, 28 days", "CETEs, 91 days", "CETEs, 182 days", "CETEs, 364 days",
    "MBONOs, 3 years", "MBONOs, 5 years", "MBONOs, 10 years",
    "MBONOs, 20 years", "MBONOs, 30 years",
]
plazos = ["28d", "91d", "182d", "364d", "3a", "5a", "10a", "20a", "30a"]
wide = raw.pivot(index="DATE", columns="INSTRUMENT", values="VALUE_PCT").reindex(columns=order)
wide.columns = plazos

base_original = wide.loc["2006-11-01":].ffill().dropna()
base_corregida = wide.ffill().loc["2006-11-01":].dropna()


def metricas_promedio(observado, pronostico):
    errores = observado - pronostico
    rmse_por_plazo = np.sqrt(np.mean(errores ** 2, axis=0))
    mae_por_plazo = np.mean(np.abs(errores), axis=0)
    return rmse_por_plazo.mean(), mae_por_plazo.mean()


def evaluar(base, nombre_base):
    resultados = []
    for h in (3, 12):
        ultima = base.index.max() - pd.DateOffset(months=h)
        origenes = base.index[(base.index >= "2022-10-01") & (base.index <= ultima)]
        fechas_objetivo = origenes + pd.DateOffset(months=h)
        obs = base.loc[fechas_objetivo, plazos].to_numpy()
        persistencia = base.loc[origenes, plazos].to_numpy()
        rmse, mae = metricas_promedio(obs, persistencia)
        resultados.append({"tratamiento": nombre_base, "modelo": "Persistencia", "h": h,
                           "RMSE": rmse, "MAE": mae})

        cambios = base.diff().dropna()
        pred_var, pred_pca = [], []
        for origen in origenes:
            cambios_entrenamiento = cambios.loc[:origen, plazos]
            ajuste_var = VAR(cambios_entrenamiento).fit(maxlags=1, trend="c")
            estado = cambios_entrenamiento.iloc[-ajuste_var.k_ar:].to_numpy()
            delta = ajuste_var.forecast(estado, steps=h)
            pred_var.append(base.loc[origen, plazos].to_numpy() + delta.sum(axis=0))

            niveles = base.loc[:origen, plazos].dropna()
            pca = PCA(n_components=3)
            scores = pd.DataFrame(
                pca.fit_transform(niveles), index=niveles.index,
                columns=["PC1", "PC2", "PC3"],
            )
            ajuste_pc = VAR(scores).fit(maxlags=1, trend="c")
            estado_pc = scores.iloc[-ajuste_pc.k_ar:].to_numpy()
            factores = ajuste_pc.forecast(estado_pc, steps=h)[-1].reshape(1, -1)
            pred_pca.append(pca.inverse_transform(factores)[0])

        for modelo, pred in [("VAR(1)", np.asarray(pred_var)), ("PCA + VAR(1)", np.asarray(pred_pca))]:
            rmse, mae = metricas_promedio(obs, pred)
            resultados.append({"tratamiento": nombre_base, "modelo": modelo, "h": h,
                               "RMSE": rmse, "MAE": mae})
    return pd.DataFrame(resultados)


comparacion = pd.concat([
    evaluar(base_original, "Original: recortar -> ffill"),
    evaluar(base_corregida, "Corregido: ffill -> recortar"),
], ignore_index=True)

print("Inicio original:", base_original.index.min().strftime("%Y-%m"))
print("Inicio corregido:", base_corregida.index.min().strftime("%Y-%m"))
print("Filas adicionales:", len(base_corregida) - len(base_original))
print(comparacion.round(4).to_string(index=False))

resumen = comparacion.pivot_table(index=["tratamiento", "modelo"], columns="h", values=["RMSE", "MAE"])
print("\nResumen ordenado:")
print(resumen.round(4).to_string())
