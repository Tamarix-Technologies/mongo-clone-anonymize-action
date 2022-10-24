import sys
from pymongo import MongoClient

db_url = sys.argv[1]
db = MongoClient(db_url)
try:
    print("Connected to MongoDB Atlas")
    print(db.server_info())
except Exception:
    print("Unable to connect MongoDB Atlas.")