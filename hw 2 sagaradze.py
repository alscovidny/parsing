from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

url = 'https://hh.ru/vacancies/khimik?page=0&hhtmFrom=vacancy_search_catalog'

# url = 'https://python-scripts.com/requests'

# r = requests.get(url, headers=headers)

# with open('hh_himiki.html', 'wt', encoding='utf-8') as f:
    # f.write(r.text)

html_file = ''
with open('hh_himiki.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

soup = bs(html_file, 'html.parser')



info_full_list = soup.find_all('div', attrs={'class' : 'vacancy-serp-item-body__main-info'})

for info_full in info_full_list:

    vacancy = info_full.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})
    vacancy_cash = info_full.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'})

    a = []

    a.append(vacancy.text) #даёт название профессииa
    a.append(vacancy.get('href'))

    pprint(a)

    if vacancy_cash:
        print(vacancy_cash.text)
    else:
        print('no cash')




# pprint(info_full)
# pprint(info.text)
# print(soup.head)