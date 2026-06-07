"""Module for exporting patient dossiers from PostgreSQL to MongoDB."""
from connections.postgresql import get_pg_connection
from connections.mongodb import get_mongo_db


def export_dossiers_patients():
    """Export patient dossiers from PostgreSQL to MongoDB."""
    conn = get_pg_connection()
    db = get_mongo_db()
    collection = db["dossiers_patients"]
    collection.drop()  # repart de zéro à chaque export

    cur = conn.cursor()

    # récupère tous les patients
    cur.execute(
        "SELECT patient_id, nom, prenom, sexe, date_naissance, ville, groupe_sanguin FROM dwh.dim_patients"
    )
    patients = cur.fetchall()

    for pat in patients:
        patient_id = pat[0]

        # consultations du patient
        cur.execute(
            """
            SELECT
                c.consultation_id, c.diagnostic, c.duree_minutes,
                f.cout_consultation, f.est_urgence,
                f.niveau_urgence, f.temperature, f.tension,
                d.date_full,
                m.nom || ' ' || m.prenom AS medecin, m.specialite,
                s.nom_service,
                med.nom_medicament, med.categorie
            FROM dwh.fact_consultations f
            JOIN dwh.dim_consultations c   ON c.sk_consultation = f.sk_consultation
            JOIN dwh.dim_dates         d   ON d.sk_date         = f.sk_date
            JOIN dwh.dim_medecins      m   ON m.sk_medecin      = f.sk_medecin
            JOIN dwh.dim_services      s   ON s.sk_service      = f.sk_service
            JOIN dwh.dim_medicaments   med ON med.sk_medicament = f.sk_medicament
            JOIN dwh.dim_patients      p   ON p.sk_patient      = f.sk_patient
            WHERE p.patient_id = %s
        """,
            (patient_id,),
        )
        consultations_raw = cur.fetchall()

        consultations = []
        for row in consultations_raw:
            consultations.append(
                {
                    "consultation_id": row[0],
                    "diagnostic": row[1],
                    "duree_minutes": row[2],
                    "cout": float(row[3]) if row[3] else None,
                    "est_urgence": row[4],
                    "niveau_urgence": row[5],
                    "temperature": float(row[6]) if row[6] else None,
                    "tension": row[7],
                    "date": str(row[8]),
                    "medecin": row[9],
                    "specialite": row[10],
                    "service": row[11],
                    "medicament": row[12],
                    "categorie_med": row[13],
                }
            )

        # analyses du patient
        cur.execute(
            """
            SELECT type_analyse, resultat, valeur, unite, date_analyse
            FROM staging.analyses
            WHERE patient_id = %s
        """,
            (patient_id,),
        )
        analyses_raw = cur.fetchall()

        analyses = []
        for row in analyses_raw:
            analyses.append(
                {
                    "type_analyse": row[0],
                    "resultat": row[1],
                    "valeur": float(row[2]) if row[2] else None,
                    "unite": row[3],
                    "date": str(row[4]),
                }
            )

        # urgences du patient
        cur.execute(
            """
            SELECT urgence_id, niveau_urgence, symptomes,
                   temperature, tension, statut, timestamp_event
            FROM staging.urgences
            WHERE patient_id = %s
        """,
            (patient_id,),
        )
        urgences_raw = cur.fetchall()

        urgences = []
        for row in urgences_raw:
            urgences.append(
                {
                    "urgence_id": row[0],
                    "niveau": row[1],
                    "symptomes": row[2],
                    "temperature": float(row[3]) if row[3] else None,
                    "tension": row[4],
                    "statut": row[5],
                    "timestamp": str(row[6]),
                }
            )

        # document final
        dossier = {
            "patient_id": pat[0],
            "nom": pat[1],
            "prenom": pat[2],
            "sexe": pat[3],
            "date_naissance": str(pat[4]),
            "ville": pat[5],
            "groupe_sanguin": pat[6],
            "nb_consultations": len(consultations),
            "consultations": consultations,
            "analyses": analyses,
            "urgences": urgences,
        }

        collection.insert_one(dossier)

    cur.close()
    conn.close()
    print(f"[OK] {len(patients)} dossiers patients exportés vers MongoDB.")
