# system check
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')

db = client['news']['mailru']
for doc in db.find({}):
    pprint(doc)

print(f'\nВсего документов в базе: {db.count_documents({})}')