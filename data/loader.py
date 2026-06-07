import pandas as pd
import xmltodict
import json
from config.config import DATA_DIR
from connections.postgresql import get_pg_connection


def insert_df(df, table, conn):
    """Insère un DataFrame dans une table staging via psycopg2."""
    if df.empty:
        print(f"[WARN] {table} : DataFrame vide, rien à insérer.")
        return

    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    query = f"""
        INSERT INTO {table} ({cols})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """
    cur = conn.cursor()
    rows = [tuple(row) for row in df.itertuples(index=False)]
    cur.executemany(query, rows)
    conn.commit()
    cur.close()
    print(f"[OK] {table} : {len(rows)} lignes insérées.")


# 1. PATIENTS (XML)
def load_patients(conn):
    with open(f"{DATA_DIR}/patients.xml", encoding="utf-8") as f:
        data = xmltodict.parse(f.read())

    patients = data["patients"]["patient"]
    if isinstance(patients, dict):
        patients = [patients]  # si un seul patient

    df = pd.DataFrame(patients)
    df = df.rename(
        columns={
            "patient_id": "patient_id",
            "nom": "nom",
            "prenom": "prenom",
            "sexe": "sexe",
            "date_naissance": "date_naissance",
            "ville": "ville",
            "telephone": "telephone",
            "groupe_sanguin": "groupe_sanguin",
            "date_creation": "date_creation",
        }
    )
    df = df[
        [
            "patient_id",
            "nom",
            "prenom",
            "sexe",
            "date_naissance",
            "ville",
            "telephone",
            "groupe_sanguin",
            "date_creation",
        ]
    ]
    insert_df(df, "staging.patients", conn)


# 2. MEDECINS (XLSX)
def load_medecins(conn):
    df = pd.read_excel(f"{DATA_DIR}/medecins.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"medecin_id": "medecin_id"})
    df = df[
        [
            "medecin_id",
            "nom",
            "prenom",
            "specialite",
            "service_id",
            "telephone",
            "email",
        ]
    ]
    insert_df(df, "staging.medecins", conn)


# 3. SERVICES (CSV)
def load_services(conn):
    df = pd.read_csv(f"{DATA_DIR}/services.csv")
    df.columns = df.columns.str.strip().str.lower()
    df = df[["service_id", "nom_service", "capacite", "batiment", "etage"]]
    insert_df(df, "staging.services", conn)


# 4. CONSULTATIONS (TXT, séparateur |)
def load_consultations(conn):
    df = pd.read_csv(
        f"{DATA_DIR}/consultations.txt",
        sep="|",
        dtype=str,
    )
    df.columns = df.columns.str.strip().str.lower()
    df["duree_minutes"] = pd.to_numeric(df["duree_minutes"], errors="coerce")
    df["cout_consultation"] = pd.to_numeric(df["cout_consultation"], errors="coerce")
    df["date_consultation"] = pd.to_datetime(
        df["date_consultation"], errors="coerce"
    ).dt.date
    df = df[
        [
            "consultation_id",
            "patient_id",
            "medecin_id",
            "service_id",
            "date_consultation",
            "diagnostic",
            "duree_minutes",
            "cout_consultation",
            "urgence",
            "medicament_id",
        ]
    ]
    insert_df(df, "staging.consultations", conn)


# 5. MEDICAMENTS (CSV)
def load_medicaments(conn):
    df = pd.read_csv(f"{DATA_DIR}/medicaments.csv")
    df.columns = df.columns.str.strip().str.lower()
    df["prix_unitaire"] = pd.to_numeric(df["prix_unitaire"], errors="coerce")
    df = df[
        [
            "medicament_id",
            "nom_medicament",
            "categorie",
            "prix_unitaire",
            "stock",
            "fournisseur",
        ]
    ]
    insert_df(df, "staging.medicaments", conn)


# 6. ANALYSES (CSV)
def load_analyses(conn):
    df = pd.read_csv(f"{DATA_DIR}/analyses.csv")
    df.columns = df.columns.str.strip().str.lower()
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    df["date_analyse"] = pd.to_datetime(df["date_analyse"], errors="coerce").dt.date
    df = df[
        [
            "analyse_id",
            "consultation_id",
            "patient_id",
            "type_analyse",
            "resultat",
            "valeur",
            "unite",
            "date_analyse",
        ]
    ]
    insert_df(df, "staging.analyses", conn)


# 7. URGENCES (JSON) — batch (pas Kafka)
def load_urgences_batch(conn):
    with open(f"{DATA_DIR}/urgences.json", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"timestamp": "timestamp_event"})
    df["timestamp_event"] = pd.to_datetime(df["timestamp_event"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df = df[
        [
            "urgence_id",
            "patient_id",
            "service_id",
            "niveau_urgence",
            "timestamp_event",
            "symptomes",
            "temperature",
            "tension",
            "statut",
        ]
    ]
    insert_df(df, "staging.urgences", conn)


# POINT D'ENTRÉE
def load_all():
    conn = get_pg_connection()
    print("=== Chargement staging ===")
    load_patients(conn)
    load_medecins(conn)
    load_services(conn)
    load_consultations(conn)
    load_medicaments(conn)
    load_analyses(conn)
    load_urgences_batch(conn)
    conn.close()
    print("=== Staging terminé ===")


def load_all():
    conn = get_pg_connection()
    print("=== Chargement staging ===")
    load_patients(conn)
    load_medecins(conn)
    load_services(conn)
    load_consultations(conn)
    load_medicaments(conn)
    load_analyses(conn)
    load_urgences_batch(conn)
    conn.close()
    print("=== Staging terminé ===")
