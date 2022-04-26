from lxml import html
import requests
from pprint import pprint

url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36'}

# response = requests.get(url, headers=header)

# dom = html.fromstring(response.text)

# href_list = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href")

# pprint(href_list)

# for ref in href_list:
ref = 'https://news.mail.ru/politics/51056244/'

response = requests.get(ref, headers=header)
dom = html.fromstring(response.text)

cur_path = dom.xpath("//div[contains(@class, 'breadcrumbs_article')]")

# print(cur_path)
for cur in cur_path:

    time = cur.xpath("./*//span[contains(@class, 'js-ago')]/@datetime")
    source = cur.xpath("./*//span[contains(@class, 'link__text')]/text()")
    name = cur.xpath("./../*//h1[contains(@class, 'hdr__inner')]/text()")


    print(str(*time).split('T')[0])