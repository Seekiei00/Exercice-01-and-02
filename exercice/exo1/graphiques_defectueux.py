"""Exercice 1 — six graphiques défectueux (à lancer depuis la racine du projet).

Produit sortie/defaut-1.png à sortie/defaut-6.png. Ne corrigez pas ce
fichier : écrivez vos corrections dans graphiques_corriges.py.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
SORTIE = Path("sortie")
SORTIE.mkdir(exist_ok=True)

immo = pd.read_csv("data/immobilier_transactions.csv")
immo["prix_m2"] = immo["valeur_fonciere"] / immo["surface_bati"]
air = pd.read_csv("data/qualite_air_hdf.csv", parse_dates=["horodatage"])
air = air[air["pm10"] < 900]
churn = pd.read_csv("data/telecom_churn.csv")

# Défaut 1 : parts de transactions par commune
parts = immo["commune"].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
ax.pie(parts.values, labels=parts.index, startangle=90)
ax.set_title("Répartition des transactions par commune")
fig.savefig(SORTIE / "defaut-1.png", dpi=150, bbox_inches="tight")

# Défaut 2 : taux de résiliation par région
taux = churn.groupby("region")["resilie"].mean() * 100
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(taux.index, taux.values, color="#d62728")
ax.set_ylim(12, 15.5)
ax.set_ylabel("Taux de résiliation (%)")
ax.set_title("Résiliation : des écarts énormes entre régions")
fig.savefig(SORTIE / "defaut-2.png", dpi=150, bbox_inches="tight")

# Défaut 3 : ozone et température, Lille Fives
lil = (air[air["station"] == "Lille Fives"].set_index("horodatage")
       [["o3", "temperature"]].resample("W").mean())
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(lil.index, lil["o3"], color="tab:blue", label="O3")
ax2 = ax.twinx()
ax2.plot(lil.index, lil["temperature"], color="tab:red", label="Température")
ax2.set_ylim(-45, 25)
ax.set_title("L'ozone décroche de la température à l'automne")
fig.savefig(SORTIE / "defaut-3.png", dpi=150, bbox_inches="tight")

# Défaut 4 : NO2 par jour de semaine et heure, Roubaix
rbx = air[air["station"] == "Roubaix Centre"].copy()
rbx["heure"] = rbx["horodatage"].dt.hour
rbx["jour"] = rbx["horodatage"].dt.dayofweek
tab = rbx.pivot_table(index="jour", columns="heure", values="no2")
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(tab.values, cmap="jet", aspect="auto")
fig.colorbar(im, ax=ax)
ax.set_title("NO2 moyen (µg/m3), Roubaix Centre")
fig.savefig(SORTIE / "defaut-4.png", dpi=150, bbox_inches="tight")

# Défaut 5 : prix au m2 médian par commune
med = immo.groupby("commune")["prix_m2"].median()       # ordre alphabétique
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(med.index, med.values, marker="o")
ax.set_ylabel("Prix au m2 médian (€)")
ax.set_title("Évolution du prix au m2 par commune")
ax.tick_params(axis="x", rotation=60)
fig.savefig(SORTIE / "defaut-5.png", dpi=150, bbox_inches="tight")

# Défaut 6 : ancienneté selon la résiliation
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor("#e6e6e6")
for val, couleur, nom in ((0, "green", "reste"), (1, "red", "résilie")):
    ax.hist(churn.loc[churn["resilie"] == val, "anciennete_mois"], bins=30,
            color=couleur, alpha=0.9, label=nom, edgecolor="black",
            hatch="xx")
ax.grid(True, which="both", color="black", linewidth=1)
ax.minorticks_on()
ax.legend()
ax.set_title("Ancienneté des clients selon la résiliation")
fig.savefig(SORTIE / "defaut-6.png", dpi=150, bbox_inches="tight")
print("Six figures écrites dans sortie/")
