import time

from selenium import webdriver
from selenium.webdriver.common.by import By


service = webdriver.ChromeService(executable_path='chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--enable-automation")
options.add_argument('--deny-permission-prompts')
#options.add_argument("--user-data-dir=C:/Users/ivano/PycharmProjects/TELEG_REKL/selenium")
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://web.telegram.org/k/#@' + 'auantonov')
time.sleep(5)

driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]/div').click()
time.sleep(3)
print("Кликаем по телефону")
driver.save_screenshot('screenshot1.png')
el = driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]')
el.send_keys("293984845")
time.sleep(2)
print("Вставляем телефон")
driver.save_screenshot('screenshot2.png')

driver.quit()
