CREATE SCHEMA IF NOT EXISTS staging;

-- patients (depuis XML)
CREATE TABLE IF NOT EXISTS staging.patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    sexe CHAR(1),
    date_naissance DATE,
    ville VARCHAR(100),
    telephone VARCHAR(20),
    groupe_sanguin VARCHAR(5),
    date_creation DATE
);

-- medecins (depuis EXCEL)
CREATE TABLE IF NOT EXISTS staging.medecins (
    medecin_id VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    specialite VARCHAR(100),
    service_id VARCHAR(10),
    telephone VARCHAR(20),
    email VARCHAR(100)
);

-- services (depuis CSV)
CREATE TABLE IF NOT EXISTS staging.services (
    service_id VARCHAR(10) PRIMARY KEY,
    nom_service VARCHAR(100),
    capacite INTEGER,
    batiment VARCHAR(50),
    etage INTEGER
);

-- consultations (depuis TXT, séparateur |)
CREATE TABLE IF NOT EXISTS staging.consultations (
    consultation_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(10),
    medecin_id VARCHAR(10),
    service_id VARCHAR(10),
    date_consultation DATE,
    diagnostic VARCHAR(200),
    duree_minutes INTEGER,
    cout_consultation NUMERIC(10, 2),
    urgence VARCHAR(5),
    medicament_id VARCHAR(12)
);

-- medicaments (depuis CSV)
CREATE TABLE IF NOT EXISTS staging.medicaments (
    medicament_id VARCHAR(12) PRIMARY KEY,
    nom_medicament VARCHAR(150),
    categorie VARCHAR(100),
    prix_unitaire NUMERIC(10, 2),
    stock INTEGER,
    fournisseur VARCHAR(150)
);

-- urgences (depuis JSON / Kafka)
CREATE TABLE IF NOT EXISTS staging.urgences (
    urgence_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(10),
    service_id VARCHAR(10),
    niveau_urgence VARCHAR(20),
    timestamp_event TIMESTAMP,
    symptomes VARCHAR(200),
    temperature NUMERIC(4, 1),
    tension VARCHAR(10),
    statut VARCHAR(30)
);

-- analyses (depuis CSV)
CREATE TABLE IF NOT EXISTS staging.analyses (
    analyse_id VARCHAR(12) PRIMARY KEY,
    consultation_id VARCHAR(12),
    patient_id VARCHAR(10),
    type_analyse VARCHAR(100),
    resultat VARCHAR(50),
    valeur NUMERIC(10, 2),
    unite VARCHAR(20),
    date_analyse DATE
);