# 1. Total médecins (KPI card)
SELECT COUNT(DISTINCT sk_medecin) AS total_medecins
FROM dwh.fact_consultations


# 2. Top 10 médecins par consultations (barres)
SELECT m.nom || ' ' || m.prenom AS medecin, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_medecins m ON m.sk_medecin = f.sk_medecin
GROUP BY m.nom, m.prenom
ORDER BY nb_consultations DESC
LIMIT 10


# 3. Consultations par spécialité (camembert)
SELECT m.specialite, COUNT(*) AS nb_consultations
FROM dwh.fact_consultations f
JOIN dwh.dim_medecins m ON m.sk_medecin = f.sk_medecin
GROUP BY m.specialite
ORDER BY nb_consultations DESC


# 4. Durée moyenne par médecin (top 10)
SELECT m.nom || ' ' || m.prenom AS medecin,
ROUND(AVG(f.duree_minutes), 0) AS duree_moyenne
FROM dwh.fact_consultations f
JOIN dwh.dim_medecins m ON m.sk_medecin = f.sk_medecin
GROUP BY m.nom, m.prenom
ORDER BY duree_moyenne DESC
LIMIT 10


# 5. Coût moyen par spécialité
SELECT m.specialite, ROUND(AVG(f.cout_consultation), 0) AS cout_moyen
FROM dwh.fact_consultations f
JOIN dwh.dim_medecins m ON m.sk_medecin = f.sk_medecin
GROUP BY m.specialite
ORDER BY cout_moyen DESC
