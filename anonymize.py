import random
import sys
from utilities import get_db,get_password_hash
import hashlib


db_url = sys.argv[1]
db = get_db(db_url)

# anonymize users data
users = db['users'].find({})
user_map = {}
for user in users:
    username = user['username']
    if username in user_map:
        user['username'] = user_map[username]
    else:
        user_map[username] = random.randint(0,10000000000)
        user['username'] = user_map[username]
    user['hashed_password'] = get_password_hash('ciao')
    db['users'].replace_one({'_id':user['_id']}, user, upsert=False)

# anonymize portfolios data
portfolios = db['portfolios'].find({})
for portfolio in portfolios:
    portfolio['username'] = user_map[portfolio['username']]

users = db['users'].find({})
for user in users:
    print(user)
portfolios = db['portfolios'].find({})
for portfolio in portfolios:
    print(portfolio)

