# 1. Coût total global (KPI card)
SELECT ROUND(SUM(cout_consultation), 0) AS cout_total_global
FROM dwh.fact_consultations

# 2. Coût moyen par service (barres)
SELECT s.nom_service, ROUND(AVG(f.cout_consultation), 0) AS cout_moyen
FROM dwh.fact_consultations f
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
GROUP BY s.nom_service
ORDER BY cout_moyen DESC

# 3. Évolution coût total par mois (courbe)
SELECT d.nom_mois, d.mois, ROUND(SUM(f.cout_consultation), 0) AS cout_total
FROM dwh.fact_consultations f
JOIN dwh.dim_dates d ON d.sk_date = f.sk_date
GROUP BY d.nom_mois, d.mois
ORDER BY d.mois

# 4. Coût moyen urgences vs normales
SELECT
    CASE WHEN est_urgence = TRUE THEN 'Urgence' ELSE 'Normale' END AS type_consultation,
    ROUND(AVG(cout_consultation), 0) AS cout_moyen
FROM dwh.fact_consultations
GROUP BY est_urgence

# 5. Top 10 consultations les plus coûteuses
SELECT
    p.nom || ' ' || p.prenom AS patient,
    s.nom_service,
    f.cout_consultation
FROM dwh.fact_consultations f
JOIN dwh.dim_patients p ON p.sk_patient = f.sk_patient
JOIN dwh.dim_services s ON s.sk_service = f.sk_service
ORDER BY f.cout_consultation DESC
LIMIT 10