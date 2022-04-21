from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['hh_parsing_database']['data']

salary = int(input('Введите минимально допустимую для вас зарплату: '))

for doc in db.find(
        # {'$or': [{'author': 'Peter2'}, {'age': 29}]}
        { '$or' : [{'максимальная ЗП': {'$gt' : salary} },
                   {'минимальная ЗП' : {'$gt' : salary}}]
        }):
    pprint(doc)

print(db.count_documents({}))