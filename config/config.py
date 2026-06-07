"""Configuration file for the project.
It loads environment variables and sets up configurations for PostgreSQL, MongoDB, Kafka, and data directory.
"""

import os
from dotenv import load_dotenv

load_dotenv()

PG_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "dbname": os.getenv("PG_DB"),
}

MONGO_URI = f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = "urgences"

DATA_DIR = "data/files"
