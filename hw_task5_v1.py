from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())

# url = "https://e.mail.ru/inbox/0:16424325001661819630:0/"
# url = 'https://e.mail.ru/inbox/0:16424325001661819630:0/?app_id_mytracker=58519&authid=l3ke0a3z.0yi&back=1%2C1&dwhsplit=s10273.b1ss12743s&from=login%2Cnavi&x-login-auth=1&afterReload=1'
url = "https://e.mail.ru/inbox/0:16534185291795119209:0/?utm_source=portal&utm_medium=new_portal_navigation&utm_campaign=e.mail.ru&mt_sub5=37&mt_sub1=e.mail.ru&mt_click_id=mt-y7s979-1653424386-2590424396"

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get(url)
driver.find_element(By.XPATH, "//input[@name='username']").send_keys('study.ai_172@mail.ru')
driver.find_element(By.XPATH,"//button[@type='submit']").click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
field = driver.find_element(By.XPATH, "//input[@name='password']")

driver.implicitly_wait(0.2)
field.send_keys('NextPassword172#')
driver.find_element(By.XPATH,"//button[@type='submit']").click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letter__body')]")))
text_message = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__body')]").text

from_user = driver.find_element(By.XPATH, "//span[@class='letter-contact']").get_attribute("title")
when_sent = driver.find_element(By.XPATH, "//div[@class='letter__date']").text
theme = driver.find_element(By.XPATH, "//div[@class='thread__header']").text
print(theme)
print(from_user)
print(when_sent)
print(text_message)
# div class b-letter__body

driver.quit()