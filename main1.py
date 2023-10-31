import asyncio
import time
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.common.by import By
from reklama_data import *


async def parsing():
    service = webdriver.ChromeService(executable_path='/home/tg_reklama/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--crash-dumps-dir=/tmp")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--deny-permission-prompts')
    options.add_argument("--user-data-dir=/home/tg_reklama/selenium")
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=options)

    chat_list = await read_from_base_channels()
    driver.implicitly_wait(10)
    for channel in chat_list:
        #print(channel[1])
        driver.get('https://web.telegram.org/k/#@' + str(channel[1]))
        try:
            result = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div')
            l_r = str(result.text).replace('sponsored', '')
            if 'VIEW CHANNEL' in l_r: l_r = l_r.replace('VIEW CHANNEL', '')
            if 'VIEW POST' in l_r: l_r = l_r.replace('VIEW POST', '')
            if 'VIEW BOT' in l_r: l_r = l_r.replace('VIEW BOT', '')
            if 'Open Link' in l_r: l_r = l_r.replace('Open Link', '')
            lines = l_r.split('\n')
            non_empty_lines = [line for line in lines if line.strip() != '']
            l_r = '\n'.join(non_empty_lines)
            l_r = l_r + f"\nГде нашли: @{str(channel[1])}\n"
            l_r = l_r + f"\nКатегория: #{str(channel[2])}\n"
            chek = await cheking(l_r)
            #print(chek)
            if chek == 'уник':
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

async def main():
    while True:
        await parsing()
        await asyncio.sleep(13000)


if __name__ == "__main__":
    asyncio.run(main())







