import asyncio
import time
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.common.by import By
from reklama_data import *
from bot import interval

async def parsing():
    service = webdriver.ChromeService(executable_path='chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--in-process-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation")
    options.add_argument('--deny-permission-prompts')
    options.add_argument("--user-data-dir=C:/Users/ivano/PycharmProjects/TELEG_REKL/selenium")
    #options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)

    chat_list = ['Theedinorogblog', 'physics_lib', 'engslov', 'slovar_psikhologia', 'englishfordeveloper',
                 'ultra_business', 'sportazarto', 'myachPRO', 'sportsmens1', 'Barcelona_Catalonia', 'CDP_Moscow ', 'bragin_co', 'mosfounders',
                 'skolkovoleaks', 'out_of_scope']
    driver.implicitly_wait(15)
    count = 0
    first = await read_from_base(1)
    for channel in chat_list:
        count += 1
        print(count, channel)
        driver.get('https://web.telegram.org/k/#@' + channel)
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
    lost = await read_from_base(1)
    diff = int(lost[0][0]) - int(first[0][0])
    await interval(diff)

async def main():
    while True:
        await parsing()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

