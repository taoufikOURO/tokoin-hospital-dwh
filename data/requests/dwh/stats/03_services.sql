# 1. Nombre de services (KPI card)
SELECT COUNT(DISTINCT sk_service) AS total_services
FROM dwh.fact_consultations

# 2. Consultations par service (barres)
SELECT s.nom_service, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY nb_consultations DESC


# 3. Capacité vs activité par service
SELECT s.nom_service, s.capacite, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service, s.capacite
ORDER BY nb_consultations DESC

# 4. Coût total par service
SELECT s.nom_service, ROUND(SUM(f.cout_consultation), 0) AS cout_total
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY cout_total DESC

# 5. Taux d'urgence par service (barres)
SELECT
    s.nom_service,
    ROUND(
        COUNT(*) FILTER (WHERE est_urgence = TRUE) * 100.0 / COUNT(*), 1
    ) AS taux_urgence_pct
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY taux_urgence_pct DESC