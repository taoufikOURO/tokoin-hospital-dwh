# 1. Total médicaments prescrits (KPI card)
SELECT COUNT(DISTINCT sk_medicament) AS total_medicaments
FROM dwh.fact_consultations


# 2. Top 10 médicaments les plus prescrits (barres)
SELECT med.nom_medicament, COUNT(*) AS nb_prescriptions
FROM dwh.fact_consultations f
JOIN dwh.dim_medicaments med ON med.sk_medicament = f.sk_medicament
GROUP BY med.nom_medicament
ORDER BY nb_prescriptions DESC
LIMIT 10


# 3. Prescriptions par catégorie (camembert)
SELECT med.categorie, COUNT(*) AS nb_prescriptions
FROM dwh.fact_consultations f
JOIN dwh.dim_medicaments med ON med.sk_medicament = f.sk_medicament
GROUP BY med.categorie
ORDER BY nb_prescriptions DESC


# 4. Prix moyen par catégorie
SELECT med.categorie, ROUND(AVG(med.prix_unitaire), 0) AS prix_moyen
FROM dwh.fact_consultations f
JOIN dwh.dim_medicaments med ON med.sk_medicament = f.sk_medicament
GROUP BY med.categorie
ORDER BY prix_moyen DESC