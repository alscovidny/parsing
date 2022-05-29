from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import pprint
import hashlib
from bs4 import BeautifulSoup
import requests
import json
import pickle

requests.get

def autorization():
    url = "https://account.mail.ru/login"
    driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    driver.set_window_size(1000, 600)
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'username')]")))
    driver.find_element(By.XPATH, "//input[contains(@name, 'username')]").send_keys('study.ai_172@mail.ru')
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'password')]")))
    driver.find_element(By.XPATH, "//input[contains(@name, 'password')]").send_keys('NextPassword172#')
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div/a[contains(@class, 'new-selection')]")))
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    return driver

def collection_links():

    links = []
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(0.5)

    # ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    # time.sleep(0.5)
    # last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
    # end = 0
    # start = time.time()
    # while (end - start) < 5:
    for j in range(2):

        # try:
        #   new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
        # except StaleElementReferenceException:
        #   time.sleep(0.5)
        #   new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
        time.sleep(1)
        start_elements = driver.find_elements(By.XPATH, "//div/a[contains(@class, 'new-selection')]")
        for el in start_elements:
            if el.get_attribute('href') and el.get_attribute('href') not in links:
                links.append(el.get_attribute('href'))
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        #     if last_elem != new_last_elem:
        #         last_elem = new_last_elem
        #         start = time.time()
        #     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        #     time.sleep(0.05)
        #     # print(j)
        #
        #     end = time.time()
        #     # if start:
        #     print(end - start)


    return links

driver = autorization()
# cookies = pickle.load(open("cookies.pkl", "rb"))
links = collection_links()

# for cookie in cookies:
#     for key, item in cookie.items():
#         # key = str(key)
#         cookie[key] = str(item)


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}


driver.quit()


#
# 'domain': '.e.mail.ru',
#   'expiry': 1661604648,
#   'httpOnly': True,
#   'name': 'sdcs',
#   'path': '/',
#   'sameSite': 'None',
#   'secure': True,
#   'value': 'IpXri75foGlvx98R'
url = links[0]
r = requests.get(url,
                 headers=headers,
                 cookies={'domain': 'https://e.mail.ru',
                          'expiry': '1661604648',
                          'httpOnly': 'True',
                          'name': 'sdcs',
                          'path': '/',
                          'sameSite': 'None',
                          'secure': 'True',
                          'value': 'IpXri75foGlvx98R'
}
                 )

soup = BeautifulSoup(r.text, 'html.parser').find_all('div')
for elem in soup:
    print(elem.text)

# print(soup)
#



# print(r.text)
# with open('file.html', 'wt', encoding='utf-8') as f:
#     f.write(r.text)
#
# # pprint.pprint(links)
# print(len(links))
# print(len(set(links)))
# time.sleep(3)
#


# if переменна:
#     start time
#
#     в конце цикла - end time

# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)
###################################

# ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
# last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
# end = 0
# start = time.time()
# while (end - start) < 5:
#
#     try:
#         new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
#     except StaleElementReferenceException:
#         time.sleep(0.5)
#         new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
#
#     if last_elem != new_last_elem:
#         last_elem = new_last_elem
#         start = time.time()
#     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
#     time.sleep(0.05)
#     # print(j)
#
#     end = time.time()
#     # if start:
#     print(end - start)
#
# print(len(driver.find_elements(By.XPATH, "//div/a[contains(@class, 'new-selection')]")))

# ActionChains(driver).send_keys(Keys.END).perform()
# element = start_elements[1]
# element = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]")
# ActionChains(driver).scroll(0, 0, 0, 300, origin=element).perform()
# last_elem = start_elements[-1].get_attribute('href')
# new_last_elem = ''
#
# i = 0
# flag = False
# news_passed = False
# while True:
#     if flag:
#         break
#     i += 1
#     ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
#     time.sleep(0.8)
#     # print(len(driver.find_elements(By.XPATH, "//div/a[contains(@class, 'new-selection')]")))
#     elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
#     print(f'cycle 1, iteration: {i}')
#     print(elem)
#     if elem not in links:
#         while True:
#             i+=1
#             ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
#             time.sleep(0.8)
#             elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
#             print(f'cycle 2, iteration: {i}')
#             print(elem)
#             if elem not in links:
#                 links.append(elem)
#             elif elem in links:
#                 news_passed = True
#             elif elem in links and news_passed:
#                 flag = True
#                 break


#
# while True:
#     i += 1
#     print(f'iteration: {i}')
#     # time.sleep(2)
#     ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
#     time.sleep(0.6)
#     new_last_elem = driver.find_elements(By.XPATH, "//div/a[contains(@class, 'new-selection')]")[-1].get_attribute('href')
#     if new_last_elem not in links:
#         links.append(new_last_elem)
#         last_elem = new_last_elem
#     print(new_last_elem)
#     if i == 100:
#         break
#     # if new_last_elem:
#     #     links.setdefault(new_last_elem, '')
#     # if new_last_elem == last_elem:
#     #     break
#

# print(len(links))