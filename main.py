import asyncio
import time

from bot import interval
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.common.by import By
from reklama_data import *


async def parsing():
    service = webdriver.ChromeService(executable_path='chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--in-process-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation")
    options.add_argument('--deny-permission-prompts')
    options.add_argument("--user-data-dir=C:/Users/ivano/PycharmProjects/TELEG_REKL/selenium")
    #options.add_argument('--headless=new')

    # options.add_argument(
    #     "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    # options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})

    driver = webdriver.Chrome(service=service, options=options)

    chat_list = await read_from_base_channels()
    c = 0
    driver.implicitly_wait(15)
    for channel in chat_list:
        print(channel[1])
        driver.get('https://web.telegram.org/k/#@' + str(channel[1]))
        time.sleep(30)
        try:
            result = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div')
            #time.sleep(2)
            l_r = str(result.text).replace('sponsored', '')
            if 'VIEW CHANNEL' in l_r: l_r = l_r.replace('VIEW CHANNEL', '')
            if 'VIEW POST' in l_r: l_r = l_r.replace('VIEW POST', '')
            if 'VIEW BOT' in l_r: l_r = l_r.replace('VIEW BOT', '')
            if 'Open Link' in l_r: l_r = l_r.replace('Open Link', '')
            lines = l_r.split('\n')
            non_empty_lines = [line for line in lines if line.strip() != '']
            l_r = '\n'.join(non_empty_lines)
            l_r = l_r + f"\nИз канала: @{str(channel[1])}"
            l_r = l_r + f"\nКатегория: #{str(channel[2])}\n"
            chek = await cheking(l_r)
            print(chek)
            if chek == 'уник':
                c += 1
                screenshot = result.screenshot_as_png
                screenshot_bytes = BytesIO(screenshot)
                try:
                    hreff = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                except:
                    try:
                        result.find_element(By.TAG_NAME, 'button').click()
                        time.sleep(3)
                        hreff = driver.current_url
                        hreff = hreff.split('#')[1]
                    except:
                        hreff = ""
                await write_to_base(hreff, l_r, screenshot_bytes)
        except:
            continue
        driver.get('https://web.telegram.org/k/')
    driver.quit()
    await interval(c)

async def main():
    while True:
        await parsing()
        await asyncio.sleep(10000)

if __name__ == "__main__":
    asyncio.run(main())



#driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]/div').click()
# time.sleep(3)

# el = driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]')
# action.click(on_element=el)
# action.send_keys("293984845")
# action.perform()
# driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/button[1]/div').click()
#
# api_id = 28929953
# api_hash = '309496be9f464d543be027c2f8461dca'
# phone_number = '375293984845'
# with TelegramClient('session_name', api_id, api_hash) as client:
#     client.start(phone_number)
#     last_message = client.get_messages(777000, limit=1)[0]
#     kod_str = last_message.text
#     kod = [i for i in str(kod_str) if i.isdigit() == True]
#     kod_s = ''.join(kod)

# time.sleep(5)
# el_1 = driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[4]/div/div[3]/div/input')
# action.click(on_element=el_1)
# action.send_keys(kod_s)
# action.perform()



