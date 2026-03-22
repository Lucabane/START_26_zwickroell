import logging
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "txp_clean")


class MongoService:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        logging.info(f"Connecté à la DB: {DB_NAME}")

    def get_tests_collection(self):
        return self.db["_tests"]

    def get_values_collection(self):
        return self.db["valuecolumns_migrated"]


mongo_service = MongoService()