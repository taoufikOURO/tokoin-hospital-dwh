"""Module for running MongoDB aggregation queries on the patient dossiers collection."""

from connections.mongodb import get_mongo_db


def run_mongo_queries():
    """ "Run various MongoDB aggregation queries on the patient dossiers collection."""
    db = get_mongo_db()
    col = db["dossiers_patients"]

    # 1. Nombre de patients par service
    print("\n=== 1. Patients par service ===")
    pipeline = [
        {"$unwind": "$consultations"},
        {
            "$group": {
                "_id": "$consultations.service",
                "nb_patients": {"$addToSet": "$patient_id"},
            }
        },
        {"$project": {"service": "$_id", "nb_patients": {"$size": "$nb_patients"}}},
        {"$sort": {"nb_patients": -1}},
    ]
    for r in col.aggregate(pipeline):
        print(f"  {r['service']} : {r['nb_patients']} patients")

    # 2. Urgences critiques
    print("\n=== 2. Urgences critiques ===")
    pipeline = [
        {"$unwind": "$urgences"},
        {"$match": {"urgences.niveau": "Élevé"}},
        {"$group": {"_id": "$urgences.niveau", "nb": {"$sum": 1}}},
    ]
    for r in col.aggregate(pipeline):
        print(f"  Niveau {r['_id']} : {r['nb']} urgences")

    # 3. Coût moyen par service
    print("\n=== 3. Coût moyen par service ===")
    pipeline = [
        {"$unwind": "$consultations"},
        {
            "$group": {
                "_id": "$consultations.service",
                "cout_moyen": {"$avg": "$consultations.cout"},
            }
        },
        {"$project": {"service": "$_id", "cout_moyen": {"$round": ["$cout_moyen", 0]}}},
        {"$sort": {"cout_moyen": -1}},
    ]
    for r in col.aggregate(pipeline):
        print(f"  {r['service']} : {r['cout_moyen']} FCFA")

    # 4. Consultations par médecin
    print("\n=== 4. Consultations par médecin (top 10) ===")
    pipeline = [
        {"$unwind": "$consultations"},
        {"$group": {"_id": "$consultations.medecin", "nb_consultations": {"$sum": 1}}},
        {"$sort": {"nb_consultations": -1}},
        {"$limit": 10},
    ]
    for r in col.aggregate(pipeline):
        print(f"  {r['_id']} : {r['nb_consultations']} consultations")

    # 5. Patients les plus critiques
    print("\n=== 5. Patients les plus critiques ===")
    pipeline = [
        {
            "$project": {
                "nom": 1,
                "prenom": 1,
                "nb_urgences": {"$size": "$urgences"},
                "nb_consultations": 1,
            }
        },
        {"$match": {"nb_urgences": {"$gt": 0}}},
        {"$sort": {"nb_urgences": -1}},
        {"$limit": 10},
    ]
    for r in col.aggregate(pipeline):
        print(f"  {r['nom']} {r['prenom']} : {r['nb_urgences']} urgences")


if __name__ == "__main__":
    run_mongo_queries()
