CREATE TABLE IF NOT EXISTS dwh.fact_consultations (
    id_fact SERIAL PRIMARY KEY,
    sk_patient INTEGER REFERENCES dwh.dim_patients (sk_patient),
    sk_medecin INTEGER REFERENCES dwh.dim_medecins (sk_medecin),
    sk_service INTEGER REFERENCES dwh.dim_services (sk_service),
    sk_medicament INTEGER REFERENCES dwh.dim_medicaments (sk_medicament),
    sk_date INTEGER REFERENCES dwh.dim_dates (sk_date),
    sk_consultation INTEGER REFERENCES dwh.dim_consultations (sk_consultation),
    duree_minutes INTEGER,
    cout_consultation NUMERIC(10, 2),
    est_urgence BOOLEAN,
    niveau_urgence VARCHAR(20), -- depuis urgences.json si dispo
    temperature NUMERIC(4, 1),
    tension VARCHAR(10)
);