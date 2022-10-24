from pymongo import MongoClient
from passlib.context import CryptContext

# connect to cluster and create client of mock_database db (db_); within db_ "users" collection will be created
def get_db(mongo_url,verbose=False):

    try:
        db = MongoClient(mongo_url)
        print("Connected to MongoDB Atlas")
        if verbose:
            print(db.server_info())
    except Exception:
        print("Unable to connect MongoDB Atlas.")
    return db.appdb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)