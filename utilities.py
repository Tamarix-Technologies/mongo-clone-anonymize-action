from pymongo import MongoClient

# connect to cluster and create client of mock_database db (db_); within db_ "users" collection will be created
def get_db(mongo_url,verbose=False):

    db = MongoClient(mongo_url)
    try:
        print("Connected to MongoDB Atlas")
        if verbose:
            print(db.server_info())
    except Exception:
        print("Unable to connect MongoDB Atlas.")
    return db