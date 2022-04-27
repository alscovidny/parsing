from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib

client = MongoClient('mongodb://localhost:27017')
db = client['news']['mailru']
db.drop({})
url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

main_tag = dom.xpath("//div[contains(@data-counter-type, 'topmail')]")[0]

main_table = main_tag.xpath("./*//div[@class ='js-module']/*//a[contains(@class, 'js-topnews__item')]/@href")
main_undertable = main_tag.xpath("./*//div[@class ='js-module']/*//a[contains(@class, 'list__text')]/@href")
region_topics_news = main_tag.xpath("./../*//div[contains(@data-logger, 'news__MainRegionNews')"
                        "or contains(@data-logger, 'news__MainRubricNews')]/*"
                      "//div[@class='cols__wrapper']/*"
                      "//a[contains(@class, 'link')]/@href")

href_list = main_table + main_undertable + region_topics_news

for ref in href_list:

    if 'sportmail.ru' in ref: # пропустил новости спорта, поскольку для них не указывается источник и используется
        pass                  # совершенно другая верстка

    response = requests.get(ref, headers=header)
    dom = html.fromstring(response.text)
    cur_path = dom.xpath("//div[contains(@class, 'breadcrumbs_article')]")

    news = {}
    news['_id'] = hashlib.sha1(ref.encode('utf_8')).hexdigest()

    news['дата публикации'] = str(*cur_path[0].xpath("./*//span[contains(@class, 'js-ago')]/@datetime")).split('T')[0]
    # print(cur_path[0].xpath("./*//span[contains(@class, 'link__text')]/text()"), ref)
    if cur_path[0].xpath("./*//span[contains(@class, 'link__text')]/text()"):
        news['источник'] = cur_path[0].xpath("./*//span[contains(@class, 'link__text')]/text()")[0]
    else:
        news['источник'] = None
    news['заголовок'] = str(*cur_path[0].xpath("./../*//h1[contains(@class, 'hdr__inner')]/text()"))
    news['ссылка'] = ref

    try:
        db.insert_one(news)
    except DuplicateKeyError:
        pass
