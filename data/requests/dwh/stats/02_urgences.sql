# 1. Total urgences (KPI card)
SELECT COUNT(*) AS total_urgences
FROM dwh.fact_consultations
WHERE est_urgence = TRUE

# 2. Urgences par niveau (camembert)
SELECT niveau_urgence, COUNT(*) AS nb
FROM dwh.fact_consultations
WHERE niveau_urgence IS NOT NULL
GROUP BY niveau_urgence
ORDER BY nb DESC

# 3. Urgences par service (barres)

SELECT s.nom_service, COUNT(*) AS nb_urgences
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
WHERE f.est_urgence = TRUE
GROUP BY s.nom_service
ORDER BY nb_urgences DESC

# 4. Température moyenne par niveau d'urgence
SELECT niveau_urgence, ROUND(AVG(temperature), 1) AS temp_moyenne
FROM dwh.fact_consultations
WHERE niveau_urgence IS NOT NULL
AND temperature IS NOT NULL
GROUP BY niveau_urgence
ORDER BY temp_moyenne DESC

# 5. Évolution urgences par mois (courbe)

SELECT d.nom_mois, d.mois, COUNT(*) AS nb_urgences
FROM dwh.fact_consultations f
JOIN dwh.dim_dates d ON d.sk_date = f.sk_date
WHERE f.est_urgence = TRUE
GROUP BY d.nom_mois, d.mois
ORDER BY d.mois
