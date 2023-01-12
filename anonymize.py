import random
import sys
from utilities import get_db,get_password_hash
import hashlib
import string
import json


db_url = sys.argv[1]
db = get_db(db_url)
raise Exception
# anonymize users data
users = db['users'].find({})
username_map = {}
password_map = {}
letters = string.ascii_lowercase
numbers = string.digits
for user in users:
    username = user['username']
    print(username)
    if username in username_map:
        user['username'] = username_map[username]
        user['hashed_password'] = get_password_hash(password_map[username])
    else:
        username_map[username] = ''.join(random.choice(numbers) for i in range(6))
        password_map[username] = ''.join(random.choice(letters) for i in range(10))
        user['username'] = username_map[username]
        user['hashed_password'] = get_password_hash(password_map[username])
    db['users'].replace_one({'_id':user['_id']}, user, upsert=False)

# anonymize portfolios
portfolios = db['portfolios'].find({})
port_map = {}
i = 0
print(username_map)
for portfolio in portfolios:
    print(portfolio)
    portfolio['username'] = username_map[portfolio['username']]
    port_name = portfolio['port_name']
    if portfolio['username'] in port_map:
        pass
    else:
        port_map[portfolio['username']] = {}

    i = len(port_map[portfolio['username']])

    port_map[portfolio['username']][port_name] = f'portfolio_{i}'
    portfolio['port_name'] = port_map[portfolio['username']][port_name]

    portfolio['port_data']['fund_name'] = [str(i) for i in range(len(portfolio['port_data']['fund_name']))]
    db['portfolios'].replace_one({'_id':portfolio['_id']}, portfolio, upsert=False)

# anonymize figures
figures = db['figures'].find({})
for figure in figures:
    figure['username'] = username_map[figure['username']]
    figure['port_name'] = port_map[figure['username']][figure['port_name']]
    for subfigure in figure['figures']:
        subfigure['username'] = username_map[subfigure['username']]
        subfigure['port_name'] = port_map[subfigure['username']][subfigure['port_name']]
    db['figures'].replace_one({'_id':figure['_id']}, figure, upsert=False)

# anonymize scenarios
scenarios = db['scenarios'].find({})
for scenario in scenarios:
    scenario['username'] = username_map[scenario['username']]
    scenario['port_name'] = port_map[scenario['username']][scenario['port_name']]
    if 'overrides' in scenario['scenario_data']:
        scenario['scenario_data']['overrides'] = {}
    if 'overrides_yields' in scenario['scenario_data']:
        scenario['scenario_data']['overrides_yields'] = {}
    db['scenarios'].replace_one({'_id':scenario['_id']}, scenario, upsert=False)

# anonymize targets
targets = db['targets'].find({})
for target in targets:
    target['username'] = username_map[target['username']]
    target['port_name'] = port_map[target['username']][target['port_name']]
    db['targets'].replace_one({'_id':target['_id']}, target, upsert=False)

# anonymize roadmaps
roadmaps = db['roadmaps'].find({})
for roadmap in roadmaps:
    roadmap['username'] = username_map[roadmap['username']]
    roadmap['port_name'] = port_map[roadmap['username']][roadmap['port_name']]
    db['roadmaps'].replace_one({'_id':roadmap['_id']}, roadmap, upsert=False)

out = {'username':username_map,'password':password_map}
with open('./user_map.json', 'w') as f:
    json.dump(out, f)



