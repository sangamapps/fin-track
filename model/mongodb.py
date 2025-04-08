from pymongo import MongoClient
from bson import ObjectId
from .config import MONGO_DB_URL, MONGO_DB_NAME

client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]
users_collection = db["users"]
accounts_collection = db["accounts"]
rules_collection = db["rules"]
transactions_collection = db["transactions"]
