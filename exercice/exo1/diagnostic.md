# Diagnostic des six figures

| # | Question à laquelle la figure doit répondre | Défaut(s) nommé(s) | Correction prévue 

| 1 | **Composition** : quelle part des transactions chaque commune représente-t-elle ? 

**Encodage trop bas dans la hiérarchie de Cleveland et McGill** : angles et aires, avec trop de parts pour être comparées ; aucune valeur affichée. 

Barres horizontales triées (encodage par **longueur**), axe à 0, valeurs en %, une seule couleur ; titre-message qui nomme la commune la plus active et sa part. |



| 2 | **Comparaison** : le taux de résiliation diffère-t-il selon la région ? 

 **Axe tronqué** (barres partant de 12 %) qui grossit des écarts de quelques points, et **titre mensonger** (« écarts énormes »), accentué par un rouge alarmiste. 
 
 Barres horizontales triées, **axe à zéro**, valeurs affichées, couleur neutre ; titre qui donne le min, le max et l'écart réel en points. |



| 3 | **Relation / évolution** : ozone et température évoluent-ils ensemble au fil de l'année ? 

**Double axe** avec une échelle de droite choisie arbitrairement (-45 à 25 °C) pour fabriquer un décrochage, et **titre mensonger** ; pas de noms d'axes ni de légende. 

**Deux panneaux superposés** partageant l'axe du temps, chacun avec son unité et son échelle naturelle ; titre avec le coefficient de corrélation r. |



| 4 | **Distribution sur deux dimensions** : à quels jours et à quelles heures le NO2 est-il le plus élevé ?

**Palette inadaptée** (`jet` : non perceptuellement uniforme, fausses frontières, illisible pour les daltoniens) ; axes non étiquetés (0-6, 0-23) ; barre de couleur sans unité. 

Heatmap en **viridis**, noms des jours, axe « heure », unité sur la barre de couleur ; titre qui donne le jour et l'heure du pic, avec sa valeur. 



| 5 | **Comparaison** : quelles communes ont le prix au m2 le plus élevé ou le plus bas ? 

**Continuité fausse** (une ligne relie des catégories rangées par ordre alphabétique) et **titre mensonger** (« Évolution » alors qu'il n'y a pas de temps). 

Barres horizontales **triées par valeur**, axe à 0 ; titre qui donne la fourchette (min, max) et les communes concernées. 



| 6 | **Distribution comparée** : les clients qui résilient ont-ils une ancienneté différente de ceux qui restent ? 

**Chartjunk** (fond gris, grille noire épaisse, graduations secondaires, hachures) ; **occlusion** (alpha 0.9, un histogramme cache l'autre) ; **palette inadaptée** (rouge/vert, non sûr pour les daltoniens) ; effectifs bruts alors que les groupes n'ont pas la même taille. 

Deux histogrammes en contour (`step`) normalisés (`density=True`), couleurs **Okabe-Ito**, médianes en pointillés, grille légère ; titre qui compare les deux médianes. |