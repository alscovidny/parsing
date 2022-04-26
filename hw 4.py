from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib

client = MongoClient('mongodb://localhost:27017')
db = client['news']['mailru']

url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

# main_table = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href")
main_tag = dom.xpath("//div[contains(@data-counter-type, 'topmail')]")[0]

l = main_tag

main_table = l.xpath("./*//div[@class ='js-module']/*//a[contains(@class, 'js-topnews__item')]/@href")
main_undertable = l.xpath("./*//div[@class ='js-module']/*//a[contains(@class, 'list__text')]/@href")

# main_topics = l.xpath("./../*//div[contains(@data-logger, 'news__MainRubricNews')]/*"
#                       "//div[@class='cols__wrapper']/*"
#                       "//a[contains(@class, 'link')]/@href")

region_topics_news = l.xpath("./../*//div[contains(@data-logger, 'news__MainRegionNews')"
                        "or contains(@data-logger, 'news__MainRubricNews')]/*"
                      "//div[@class='cols__wrapper']/*"
                      "//a[contains(@class, 'link')]/@href")

all_news = main_table + main_undertable + region_topics_news

# /*//a[@contains(@class, 'link')]/@href
# //div[@data-logger='news__MainRubricNews']/*
# div[@class='cols__wrapper']/*//
#
# print(main_table)
# print(main_undertable)
print(region_topics_news)
#
# for ref in href_list:
#
#     response = requests.get(ref, headers=header)
#     dom = html.fromstring(response.text)
#     cur_path = dom.xpath("//div[contains(@class, 'breadcrumbs_article')]")
#
#     news = {}
#     news['_id'] = hashlib.sha1(ref.encode('utf_8')).hexdigest()
#     news['дата публикации'] = str(*cur_path[0].xpath("./*//span[contains(@class, 'js-ago')]/@datetime")).split('T')[0]
#     news['источник'] = cur_path[0].xpath("./*//span[contains(@class, 'link__text')]/text()")[0]
#     news['заголовок'] = str(*cur_path[0].xpath("./../*//h1[contains(@class, 'hdr__inner')]/text()"))
#     news['ссылка'] = ref
#
#     try:
#         db.insert_one(news)
#     except DuplicateKeyError:
#         pass
