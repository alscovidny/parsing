from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')

print(client.list_database_names())

    