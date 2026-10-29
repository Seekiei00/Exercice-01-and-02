import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import ticker

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]

df = pd.read_csv(RACINE/"data"/"immobilier_transactions.csv", parse_dates=["date_mutation"])
df["prix_m2"] = df["valeur_fonciere"] / df["surface_bati"]


nb_transactions = len(df)
print(f"\nNombre de transactions : {nb_transactions}")

prix_median = df["valeur_fonciere"].median()
print(f"\nPrix médian : {prix_median:,.0f} €")

prix_moyen = df["valeur_fonciere"].mean()
print(f"\nPrix moyen : {prix_moyen:,.0f} €")

corr_surface_valeur = df["surface_bati"].corr(df["valeur_fonciere"])
print(f"\nCorrélation entre surface et valeur foncière : {corr_surface_valeur:.2f}")

corr_log_surface_valeur = np.log(df["surface_bati"]).corr(np.log(df["valeur_fonciere"]))
print(f"\nCorrélation entre log(surface) et log(valeur foncière) : {corr_log_surface_valeur:.2f}")

tri_communes = df.groupby("commune")["prix_m2"].median().round(2).sort_values()
print(f"\n10 communes les plus chères :", f"\n{tri_communes.head(10)}")

par_dpe = df.groupby("dpe")["prix_m2"].agg(mediane="median", effectif="count").reindex(list("ABCDEFG")).round(2)
print(f"\nRépartition par DPE :", f"\n{par_dpe}")


#                                                        Partie 2 : la figure


#Figure 1

fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))
ax1, ax2, ax3, ax4 = axes.flat

couleurs = {"Appartement": "#1f77b4", "Maison": "#ff7f0e"}

for type_local, groupe in df.groupby("type_local"):
    ax1.scatter(
        groupe["surface_bati"],
        groupe["valeur_fonciere"] / 1000,          
        s=6, alpha=0.3,                            
        color=couleurs[type_local],
        label=f"{type_local}, n= {len(groupe):,}".replace(",", " "),
    )

ax1.set_xscale("log")
ax1.set_yscale("log")

ax1.set_xticks([20, 50, 100, 200, 500])
ax1.set_yticks([50, 100, 200, 500, 1000])

milliers = ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))
ax1.xaxis.set_major_formatter(milliers)
ax1.yaxis.set_major_formatter(milliers)

ax1.xaxis.set_minor_formatter(ticker.NullFormatter())
ax1.yaxis.set_minor_formatter(ticker.NullFormatter())

ax1.set_xlabel("Surface bâtie (m², échelle log)")
ax1.set_ylabel("Prix de vente (k€, échelle log)")
ax1.legend()
ax1.set_title("Le prix suit la surface, quel que soit le type", loc="left")




# Figure 2

couleurs_barres = ["#9db4cc"] * len(tri_communes)   
couleurs_barres[0] = "#d62728"     
couleurs_barres[-1] = "#d62728"    

ax2.barh(tri_communes.index, tri_communes.values, color=couleurs_barres)
ax2.xaxis.set_major_formatter(milliers)

ax2.tick_params(axis="y", labelsize=8)     
ax2.set_xlabel("Prix médian au m² (€)")
ax2.set_title("Le m² est 3 fois plus cher à Lille qu'à Maubeuge", loc="left")


# Figure 3

ax3.plot(par_dpe.index, par_dpe["mediane"], marker="o", color="#0c4f7e")

for etiquette, ligne in par_dpe.iterrows():
    ax3.annotate(
        f"n={ligne['effectif']:,.0f}".replace(",", " "),   
        xy=(etiquette, ligne["mediane"]),                   
        textcoords="offset points", xytext=(0, 8),          
        ha="center", fontsize=8,
    )


ax3.set_ylim(2000, 3100)
ax3.yaxis.set_major_formatter(milliers)
ax3.set_xlabel("Étiquette énergie (DPE)")
ax3.set_ylabel("Prix médian au m² (€)")
ax3.set_title("Plus le DPE est mauvais, moins le m² vaut : −20 % de A à G", loc="left")



# Figure 4

trimestriel = (df.set_index("date_mutation").groupby("type_local")["valeur_fonciere"].resample("QE").median().unstack(level=0))
print(trimestriel)

couleurs = {"Appartement": "#1f77b4", "Maison": "#ff7f0e"}   

for type_local in trimestriel.columns:
    serie = trimestriel[type_local] / 1000          
    ax4.plot(serie.index, serie.values, marker="o", markersize=3,color=couleurs[type_local])
    ax4.annotate(
        type_local,
        xy=(serie.index[-1], serie.iloc[-1]),         
        textcoords="offset points", xytext=(0, -8),    
        ha="right", va="top",
        color=couleurs[type_local], fontweight="bold",
        )

ax4.set_ylim(bottom=0)
ax4.xaxis.set_major_locator(mdates.YearLocator())
ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax4.set_ylabel("Prix de vente médian (k€)")
ax4.set_title("Des prix quasi stables entre 2023 et 2025", loc="left")


fig.tight_layout()

SORTIE = RACINE / "sortie_exercice02"
SORTIE.mkdir(parents=True, exist_ok=True)

fig.savefig(SORTIE / "figure.png", dpi=100)