import sys
from utilities import get_db
import hashlib


db_url = sys.argv[1]
db = get_db(db_url)

# pipeline steps
stage_1 = {'username': {'$function': {'lang': 'js', 'args': ['$_id'], 'body': hashlib.md5}}}
pipeline = [{'$set': stage_1}]
pipeline.push(
    {'$merge': {'into': { 'db': 'testdata', 'coll': 'payments'}, 'on': '_id',  'whenMatched': 'replace', 'whenNotMatched': 'fail'}}
)
db.users.aggregate(pipeline)
db.users.find()
