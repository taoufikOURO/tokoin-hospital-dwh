CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_patients (
    sk_patient SERIAL PRIMARY KEY,
    patient_id VARCHAR(10) UNIQUE,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    sexe CHAR(1),
    date_naissance DATE,
    ville VARCHAR(100),
    groupe_sanguin VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS dwh.dim_medecins (
    sk_medecin SERIAL PRIMARY KEY,
    medecin_id VARCHAR(10) UNIQUE,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    specialite VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dwh.dim_services (
    sk_service SERIAL PRIMARY KEY,
    service_id VARCHAR(10) UNIQUE,
    nom_service VARCHAR(100),
    capacite INTEGER,
    batiment VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dwh.dim_medicaments (
    sk_medicament SERIAL PRIMARY KEY,
    medicament_id VARCHAR(12) UNIQUE,
    nom_medicament VARCHAR(150),
    categorie VARCHAR(100),
    prix_unitaire NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS dwh.dim_dates (
    sk_date SERIAL PRIMARY KEY,
    date_full DATE UNIQUE,
    jour INTEGER,
    mois INTEGER,
    annee INTEGER,
    trimestre INTEGER,
    nom_mois VARCHAR(20),
    jour_semaine VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS dwh.dim_consultations (
    sk_consultation SERIAL PRIMARY KEY,
    consultation_id VARCHAR(12) UNIQUE,
    diagnostic VARCHAR(200),
    duree_minutes INTEGER
);