from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from datetime import date, timedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
import pprint
import hashlib
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dateutil.parser import parse

client = MongoClient('mongodb://localhost:27017')
db = client['study_ai']['mail_text']
db.drop()

print('Начало выполнения скрипта')
print(datetime.datetime.now())
def autorization():
    #опции для снижения пожирания ОЗУ
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")

    url = "https://account.mail.ru/login"
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    driver.set_window_size(600, 600)
    driver.get(url)

    def send_keys():
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'username')]")))
        driver.find_element(By.XPATH, "//input[contains(@name, 'username')]").send_keys('study.ai_172@mail.ru')
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'password')]")))
        driver.find_element(By.XPATH, "//input[contains(@name, 'password')]").send_keys('NextPassword172#')
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div/a[contains(@class, 'new-selection')]")))
    try:
        send_keys()
    except ElementNotInteractableException:
        driver.refresh()
        time.sleep(0.5)
        send_keys()
    return driver

def collection_links(driver):
    with open('links.txt', 'wt', encoding='utf-8') as f:
        links = []
        find_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]")
        ActionChains(driver).click_and_hold(find_elem).perform()
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        last_elem = find_elem.get_attribute('href')
        end = 0
        start = time.time()
        prev_start_elements = [] #массив предыдущих элементов. для предотвращения повторного сканирования крайних элементов
        while (end - start) < 15:
            try:
                new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
            except StaleElementReferenceException:
                time.sleep(0.2)
                new_last_elem = driver.find_element(By.XPATH, "//div/a[contains(@class, 'new-selection')]").get_attribute('href')
            time.sleep(1)
            start_elements = driver.find_elements(By.XPATH, "//div/a[contains(@class, 'new-selection')]")
            for el in start_elements:
                if el.get_attribute('href') and el.get_attribute('href') not in prev_start_elements:
                    f.write(el.get_attribute('href') + '\n')
            if last_elem != new_last_elem:
                last_elem = new_last_elem
                start = time.time()
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.05)
            end = time.time()
            prev_start_elements = start_elements

def read_message(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letter__body')]")))
        time.sleep(0.5)
    except:
        driver.get(url)
        driver.refresh()
        # driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letter__body')]")))
        time.sleep(0.5)

    message_strings = driver.find_elements(By.XPATH, "//div[contains(@class, 'letter__body')]")
    result = ''
    for string in message_strings:
        result = result.join(string.text)
    text_message = result
    from_user = driver.find_element(By.XPATH, "//span[@class='letter-contact']").get_attribute("title")
    when_sent = driver.find_element(By.XPATH, "//div[@class='letter__date']").text

    if 'Сегодня' in when_sent:
        when_sent = when_sent.replace('Сегодня', str(date.today()))
        when_sent = parse(when_sent)
        when_sent = when_sent.strftime('%d %b, %H:%M')
    elif 'Вчера' in when_sent:
        when_sent = when_sent.replace('Вчера', str(date.today() - timedelta(days=1)))
        when_sent = parse(when_sent)
        when_sent = when_sent.strftime('%d %b, %H:%M')

    theme = driver.find_element(By.XPATH, "//div[@class='thread__header']").text
    id = hashlib.sha1(url.encode('utf_8')).hexdigest()
    return {'_id' : id,
            'from' : from_user,
            'when_sent' : when_sent,
            'theme' : theme,
            'text' : text_message
    }

def read_first_N(N=10):
    with open('links.txt', 'rt', encoding='utf-8') as f:
        driver = autorization()
        j = 0
        for line in f: # стремился сделать так, чтобы работало по принципу чтения в виде генератора
            if j >= N:
                break
            data = read_message(line.strip(), driver)
            j += 1
            try:
                db.insert_one(data)
            except DuplicateKeyError:
                pass
            print(f'обработано сообщений: {j}. Время: {datetime.datetime.now()}')
            # реконнект, чтобы не тормозилось в процессе выполнения при парсинге большого количества ссылок
            if j % 100 == 0:
                driver.quit()
                driver = autorization()

        driver.quit()

driver = autorization()
print('Выполнена авторизация')
print('Идёт сбор страниц....')
collection_links(driver) # функция собирает все ссылки на сообщения
driver.quit()
print('Страницы собраны')
print(datetime.datetime.now())
read_first_N()

print('Выполнение успешно завершено')
print(datetime.datetime.now())
