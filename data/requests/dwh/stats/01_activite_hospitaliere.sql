# 1. Total consultations (KPI card)
SELECT COUNT(*) AS total_consultations
FROM dwh.fact_consultations


# 2. Consultations par mois (courbe)
SELECT d.nom_mois, d.mois, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_dates d ON d.sk_date = f.sk_date
GROUP BY d.nom_mois, d.mois
ORDER BY d.mois


# 3. Répartition urgences vs normales (camembert)
SELECT
    CASE WHEN est_urgence = TRUE THEN 'Urgence' ELSE 'Normale' END AS type_consultation,
    COUNT(*) AS nb
FROM dwh.fact_consultations
GROUP BY est_urgence


# 4. Consultations par service (barres)
SELECT s.nom_service, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY nb_consultations DESC


# 5. Durée moyenne par service (barres)
SELECT s.nom_service, ROUND(AVG(f.duree_minutes), 0) AS duree_moyenne
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY duree_moyenne DESC