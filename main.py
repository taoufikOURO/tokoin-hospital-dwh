"""Main module to orchestrate the entire data processing workflow, including database initialization, data loading, transformation, and exporting results to MongoDB."""
from connections.db_init import init_database
from data.loader import load_all
from processing.transformer import transform_all
from processing.mongo_export import export_dossiers_patients
from processing.mongo_queries import run_mongo_queries

if __name__ == "__main__":
    init_database()
    load_all()
    transform_all()
    export_dossiers_patients()
    run_mongo_queries()
