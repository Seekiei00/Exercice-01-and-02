
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
SORTIE = Path("sortie_corriges")
SORTIE.mkdir(exist_ok=True)

immo = pd.read_csv("data/immobilier_transactions.csv")
immo["prix_m2"] = immo["valeur_fonciere"] / immo["surface_bati"]
air = pd.read_csv("data/qualite_air_hdf.csv", parse_dates=["horodatage"])
air = air[air["pm10"] < 900]
churn = pd.read_csv("data/telecom_churn.csv")

# Défaut 1 : parts de transactions par commune; good 
parts = immo["commune"].value_counts(normalize=True).sort_values() * 100
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(parts.index, parts.values, color="tab:blue")
ax.set_xlabel("Part des transactions (%)")
ax.set_title("Répartition des transactions par commune")
fig.savefig(SORTIE / "defaut-1.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Défaut 2 : taux de résiliation par région; good
taux = churn.groupby("region")["resilie"].mean() * 100
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(taux.index, taux.values, color="tab:blue")
ax.set_ylim(0, 20)
ax.set_ylabel("Taux de résiliation (%)")
ax.set_title("Taux de Résiliation : des niveaux proches entre régions")
fig.savefig(SORTIE / "defaut-2.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Défaut 3 : ozone et température, Lille Fives; good
lil = (air[air["station"] == "Lille Fives"].set_index("horodatage")
       [["o3", "temperature"]].resample("W").mean())
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax1.plot(lil.index, lil["o3"], color="tab:blue")
ax1.set_ylabel("O3 (µg/m3)")
ax2.plot(lil.index, lil["temperature"], color="tab:red")
ax2.set_ylabel("Température (°C)")
ax1.set_title("Ozone (moyennes hebdo), Lille Fives")
ax2.set_title("Température (moyennes hebdo), Lille Fives")
fig.savefig(SORTIE / "defaut-3.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Défaut 4 : NO2 par jour de semaine et heure, Roubaix; good
rbx = air[air["station"] == "Roubaix Centre"].copy()
rbx["heure"] = rbx["horodatage"].dt.hour
rbx["jour"] = rbx["horodatage"].dt.dayofweek
tab = rbx.pivot_table(index="jour", columns="heure", values="no2")
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(tab.values, cmap="viridis", aspect="auto")
ax.set_yticks(range(7))
ax.set_yticklabels(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])
ax.set_xticks(range(0, 24, 2))
ax.set_xlabel("Heure")
fig.colorbar(im, ax=ax, label="NO2 (µg/m3)")
fig.savefig(SORTIE / "defaut-4.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Défaut 5 : prix au m2 médian par commune; good
med = immo.groupby("commune")["prix_m2"].median().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(med.index, med.values, color="tab:blue")
ax.set_xlabel("Prix au m2 médian (€)")
ax.set_title("Prix au m2 médian par commune")
ax.tick_params(axis="x", rotation=60)
fig.savefig(SORTIE / "defaut-5.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Corrigé 6 : ancienneté selon la résiliation
restes = churn.loc[churn["resilie"] == 0, "anciennete_mois"]
resilies = churn.loc[churn["resilie"] == 1, "anciennete_mois"]
med0, med1 = restes.median(), resilies.median()

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist([restes, resilies], bins=30, density=True, label=[f"Non résiliés (médiane {med0:.0f} mois)", f"Résiliés (médiane {med1:.0f} mois)"], color=["#0072B2", "#E69F00"])          
ax.set_ylabel("Densité (proportion de clients)")
ax.grid(axis="y", color="#dddddd", linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False)
ax.set_title(f"Les clients qui résilient ont une ancienneté médiane de {med1:.0f} mois, "
             f"contre {med0:.0f} pour ceux qui restent")
fig.savefig(SORTIE / "defaut-6.png", dpi=150, bbox_inches="tight")
plt.close(fig)