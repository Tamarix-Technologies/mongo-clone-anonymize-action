import random
import sys
from utilities import get_db,get_password_hash
import hashlib
import string


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
        user_map[username] = str(random.randint(0,10000000000))
        user['username'] = user_map[username]
    user['hashed_password'] = get_password_hash('ciao')
    db['users'].replace_one({'_id':user['_id']}, user, upsert=False)

# anonymize portfolios
portfolios = db['portfolios'].find({})
port_map = {}
letters = string.ascii_lowercase
for portfolio in portfolios:
    portfolio['username'] = user_map[portfolio['username']]
    port_name = portfolio['port_name']
    if port_name in port_map:
        portfolio['port_name'] = port_map[portfolio['port_name']]
    else:
        port_map[port_name] = ''.join(random.choice(letters) for i in range(20))
        portfolio['port_name'] = port_map[port_name]

    portfolio['port_data']['fund_name'] = [str(i) for i in range(len(portfolio['port_data']['fund_name']))]
    db['portfolios'].replace_one({'_id':portfolio['_id']}, portfolio, upsert=False)

# anonymize figures
figures = db['portfolios'].find({})
for figure in figures:
    print(figure['username'])
    figure['username'] = user_map[figure['username']]
    figure['port_name'] = port_map[figure['port_name']]
    for subfigure in figure['figures']:
        subfigure['username'] = user_map[subfigure['username']]
        subfigure['port_name'] = port_map[subfigure['port_name']]
    db['figures'].replace_one({'_id':figure['_id']}, figure, upsert=False)

# anonymize scenarios
scenarios = db['scenarios'].find({})
for scenario in scenarios:
    scenario['username'] = user_map[scenario['username']]
    scenario['port_name'] = port_map[scenario['port_name']]
    if 'overrides' in scenario['scenario_data']:
        scenario['scenario_data']['overrides'] = {}
    if 'overrides_yields' in scenario['scenario_data']:
        scenario['scenario_data']['overrides_yields'] = {}
    db['scenarios'].replace_one({'_id':scenario['_id']}, scenario, upsert=False)

# anonymize targets
targets = db['targets'].find({})
for target in targets:
    target['username'] = user_map[target['username']]
    target['port_name'] = port_map[target['port_name']]
    db['targets'].replace_one({'_id':target['_id']}, target, upsert=False)

# anonymize roadmaps
roadmaps = db['roadmaps'].find({})
for roadmap in roadmaps:
    roadmap['username'] = user_map[roadmap['username']]
    roadmap['port_name'] = port_map[roadmap['port_name']]
    db['roadmaps'].replace_one({'_id':roadmap['_id']}, roadmap, upsert=False)

