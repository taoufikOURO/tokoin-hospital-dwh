"""Module for managing MongoDB connections."""

from pymongo import MongoClient
from config.config import MONGO_URI


def get_mongo_db():
    """Establishes a connection to the MongoDB database and returns the database object."""
    client = MongoClient(MONGO_URI)
    return client["hospital_dwh"]
