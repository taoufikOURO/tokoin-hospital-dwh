from connections.postgresql import get_pg_connection


# ──────────────────────────────────────────
# UTILITAIRE
# ──────────────────────────────────────────
def execute(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()


# ──────────────────────────────────────────
# 1. DIM_PATIENTS
# ──────────────────────────────────────────
def load_dim_patients(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_patients
            (patient_id, nom, prenom, sexe, date_naissance, ville, groupe_sanguin)
        SELECT DISTINCT
            patient_id, nom, prenom, sexe, date_naissance, ville, groupe_sanguin
        FROM staging.patients
        WHERE patient_id IS NOT NULL
        ON CONFLICT (patient_id) DO NOTHING
    """,
    )
    print("[OK] dim_patients chargée.")


# ──────────────────────────────────────────
# 2. DIM_MEDECINS
# ──────────────────────────────────────────
def load_dim_medecins(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_medecins
            (medecin_id, nom, prenom, specialite)
        SELECT DISTINCT
            medecin_id, nom, prenom, specialite
        FROM staging.medecins
        WHERE medecin_id IS NOT NULL
        ON CONFLICT (medecin_id) DO NOTHING
    """,
    )
    print("[OK] dim_medecins chargée.")


# ──────────────────────────────────────────
# 3. DIM_SERVICES
# ──────────────────────────────────────────
def load_dim_services(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_services
            (service_id, nom_service, capacite, batiment)
        SELECT DISTINCT
            service_id, nom_service, capacite, batiment
        FROM staging.services
        WHERE service_id IS NOT NULL
        ON CONFLICT (service_id) DO NOTHING
    """,
    )
    print("[OK] dim_services chargée.")


# ──────────────────────────────────────────
# 4. DIM_MEDICAMENTS
# ──────────────────────────────────────────
def load_dim_medicaments(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_medicaments
            (medicament_id, nom_medicament, categorie, prix_unitaire)
        SELECT DISTINCT
            medicament_id, nom_medicament, categorie, prix_unitaire
        FROM staging.medicaments
        WHERE medicament_id IS NOT NULL
        ON CONFLICT (medicament_id) DO NOTHING
    """,
    )
    print("[OK] dim_medicaments chargée.")


# ──────────────────────────────────────────
# 5. DIM_DATES
# ──────────────────────────────────────────
def load_dim_dates(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_dates
            (date_full, jour, mois, annee, trimestre, nom_mois, jour_semaine)
        SELECT DISTINCT
            date_consultation,
            EXTRACT(DAY   FROM date_consultation)::INT,
            EXTRACT(MONTH FROM date_consultation)::INT,
            EXTRACT(YEAR  FROM date_consultation)::INT,
            EXTRACT(QUARTER FROM date_consultation)::INT,
            TO_CHAR(date_consultation, 'TMMonth'),
            TO_CHAR(date_consultation, 'TMDay')
        FROM staging.consultations
        WHERE date_consultation IS NOT NULL
        ON CONFLICT (date_full) DO NOTHING
    """,
    )
    print("[OK] dim_dates chargée.")


# ──────────────────────────────────────────
# 6. DIM_CONSULTATIONS
# ──────────────────────────────────────────
def load_dim_consultations(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.dim_consultations
            (consultation_id, diagnostic, duree_minutes)
        SELECT DISTINCT
            consultation_id, diagnostic, duree_minutes
        FROM staging.consultations
        WHERE consultation_id IS NOT NULL
        ON CONFLICT (consultation_id) DO NOTHING
    """,
    )
    print("[OK] dim_consultations chargée.")


# ──────────────────────────────────────────
# 7. FACT_CONSULTATIONS
# ──────────────────────────────────────────
def load_fact_consultations(conn):
    execute(
        conn,
        """
        INSERT INTO dwh.fact_consultations (
            sk_patient, sk_medecin, sk_service, sk_medicament,
            sk_date, sk_consultation,
            duree_minutes, cout_consultation, est_urgence,
            niveau_urgence, temperature, tension
        )
        SELECT
            p.sk_patient,
            m.sk_medecin,
            s.sk_service,
            med.sk_medicament,
            d.sk_date,
            c.sk_consultation,
            st.duree_minutes,
            st.cout_consultation,
            CASE WHEN UPPER(st.urgence) = 'OUI' THEN TRUE ELSE FALSE END,
            u.niveau_urgence,
            u.temperature,
            u.tension
        FROM staging.consultations st
        JOIN dwh.dim_patients      p   ON p.patient_id      = st.patient_id
        JOIN dwh.dim_medecins      m   ON m.medecin_id      = st.medecin_id
        JOIN dwh.dim_services      s   ON s.service_id      = st.service_id
        JOIN dwh.dim_medicaments   med ON med.medicament_id = st.medicament_id
        JOIN dwh.dim_dates         d   ON d.date_full       = st.date_consultation
        JOIN dwh.dim_consultations c   ON c.consultation_id = st.consultation_id
        LEFT JOIN staging.urgences u   ON u.patient_id      = st.patient_id
    """,
    )
    print("[OK] fact_consultations chargée.")


# ──────────────────────────────────────────
# POINT D'ENTRÉE
# ──────────────────────────────────────────
def transform_all():
    conn = get_pg_connection()
    print("=== Transformation DWH ===")
    load_dim_patients(conn)
    load_dim_medecins(conn)
    load_dim_services(conn)
    load_dim_medicaments(conn)
    load_dim_dates(conn)
    load_dim_consultations(conn)
    load_fact_consultations(conn)
    conn.close()
    print("=== DWH terminé ===")
