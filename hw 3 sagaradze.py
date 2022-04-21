from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError
import hashlib
from bs4 import BeautifulSoup as bs
import time
import requests

client = MongoClient('mongodb://localhost:27017')

db = client['hh_parsing_database']['data']



h = hashlib.new('sha256') # - нововведение

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
pattern = 'https://hh.ru'
count = 0
N = int(input('Введите количество страниц, которое хотите распарсить (0 если парсить все): '))

# with open('parsed.json', 'w', encoding='utf-8') as f:
#     f.write('стартовая ссылка:\nhttps://hh.ru/vacancies/khimik?page=0&hhtmFrom=vacancy_search_catalog\n\n')

is_next_page = 'https://hh.ru/vacancies/khimik?page=0&hhtmFrom=vacancy_search_catalog'
while is_next_page:
    if N != 0:
        if count >= N:
            break

    time.sleep(1)
    r = requests.get(is_next_page, headers=headers)
    if r.status_code == 200:
        print(f'успешный доступ к странице {count + 1}')

    soup = bs(r.text, 'html.parser')

    info_full_list = soup.find_all('div', attrs={'class' : 'vacancy-serp-item-body__main-info'})
    is_next_page = soup.find('a', attrs={'data-qa' : 'pager-next'})
    if is_next_page:
        is_next_page = pattern + is_next_page.get('href')

    for info_full in info_full_list:

        vacancy_data = {}
        vacancy = info_full.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})
        vacancy_cash = info_full.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'})

        # нововведение - даём id для объекта

        vacancy_data['вакансия'] = vacancy.text
        vacancy_data['ссылка'] = vacancy.get('href')
        #
        h.update(vacancy_data['ссылка'].encode('utf-8'))
        vacancy_data['_id'] = h.hexdigest()# - попробовать кодировать чисто по ссылке?
        #

        vacancy_data['минимальная ЗП'] = None
        vacancy_data['максимальная ЗП'] = None
        vacancy_data['валюта'] = None

        if vacancy_cash:
            cash_list = vacancy_cash.text.replace('\u202f','').split()
            vacancy_data['валюта'] = cash_list.pop()
            if 'от' in cash_list:
                vacancy_data['минимальная ЗП'] = int(cash_list.pop())
            elif 'до' in cash_list:
                vacancy_data['максимальная ЗП'] = int(cash_list.pop())
            else:
                vacancy_data['минимальная ЗП'] = int(cash_list[0])
                vacancy_data['максимальная ЗП'] = int(cash_list.pop())

        try:
            db.insert_one(vacancy_data)
        except DuplicateKeyError:
            pass

        # with open('parsed.json', 'a', encoding='utf-8') as f:
        #     json.dump(vacancy_data, f, indent=4, ensure_ascii=False)

    count += 1

print(client.list_database_names())

for doc in db.find():
    pprint(doc)