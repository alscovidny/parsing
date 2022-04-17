from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

url = 'https://hh.ru/vacancies/khimik?page=0&hhtmFrom=vacancy_search_catalog'

url_parse = bs(url, 'html.parser')
url_parse.find('page')

# r = requests.get(url, headers=headers)



# with open('hh_himiki.html', 'wt', encoding='utf-8') as f:
    # f.write(r.text)

# html_file = ''
# with open('hh_himiki.html', 'r', encoding='utf-8') as f:
#     html_file = f.read()

soup = bs(r.text, 'html.parser')

# soup = bs(html_file, 'html.parser')

info_full_list = soup.find_all('div', attrs={'class' : 'vacancy-serp-item-body__main-info'})

is_next_page = soup.find('a', attrs={'data-qa' : 'pager-next'}).get('href')

# print(is_next_page)

data = []

for info_full in info_full_list:

    vacancy_data = {}

    vacancy = info_full.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})
    vacancy_cash = info_full.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'})

    vacancy_data['1.вакансия'] = vacancy.text
    vacancy_data['5.ссылка'] = vacancy.get('href')
    vacancy_data['2.минимальная ЗП'] = None
    vacancy_data['3.максимальная ЗП'] = None
    vacancy_data['4.валюта'] = None

    if vacancy_cash:
        cash_list = vacancy_cash.text.replace('\u202f','').split()
        vacancy_data['4.валюта'] = cash_list.pop()
        # print(cash_list)
        if 'от' in cash_list:
            vacancy_data['2.минимальная ЗП'] = int(cash_list.pop())
        elif 'до' in cash_list:
            vacancy_data['3.максимальная ЗП'] = int(cash_list.pop())
        else:
            vacancy_data['2.минимальная ЗП'] = int(cash_list[0])
            vacancy_data['3.максимальная ЗП'] = int(cash_list.pop())

    data.append(vacancy_data)

pprint(data)