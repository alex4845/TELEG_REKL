import sqlite3
import time
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.common.by import By


def write_to_base(hreff, l_r, screenshot_bytes):
    conn = sqlite3.connect('rekl_base.db')
    cursor = conn.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS list_1 (
       number INTEGER PRIMARY KEY, href TEXT (200), post TEXT (250), screen BLOB
        )""")
    cursor.execute('INSERT INTO list_1 (href, post, screen) VALUES (?,?,?)',
                   (hreff, l_r, sqlite3.Binary(screenshot_bytes.read()), ))
    conn.commit()
    conn.close()

def cheking(data):
    try:
        conn = sqlite3.connect('rekl_base.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM list_1 WHERE post = ?", (data,))
        res = cursor.fetchall()
        conn.close()
        if res:
            return 'дубль'
        else:
            return 'уник'
    except:
        return 'уник'

def read_from_base(c):
    conn = sqlite3.connect('rekl_base.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT number, post, href, screen FROM list_1 ORDER BY number DESC LIMIT {c}")
    res = cursor.fetchall()
    conn.close()
    return res

def parsing():
    service = webdriver.ChromeService(executable_path='/home/tg_reklama/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation")
    options.add_argument('--deny-permission-prompts')
    options.add_argument("--user-data-dir=/home/tg_reklama/selenium")
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    chat_list = ['auantonov', 'sberbank', 'dr_komarovskiy', 'shishovaolgaivanovna', 'CDP_Moscow', "bragin_co", 'mosfounders',
                 'dindex', 'startapnaya', 'startup_club24', 'zeroton', 'Theedinorogblog', 'out_of_scope', 'skolkovoleaks']
    count = 0
    for channel in chat_list:
        driver.get('https://web.telegram.org/k/#@' + channel)
        print(chat_list.index(channel) + 1, channel)
        time.sleep(10)
        driver.save_screenshot('screen0.png')
        try:
            result = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div')
            time.sleep(3)
            l_r = str(result.text).replace('sponsored', '')
            print(l_r)
            try:
                hreff = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                hreff = ''
            chek = cheking(l_r)
            print(chek)
            if chek == 'уник':
                count += 1
                screenshot = result.screenshot_as_png
                screenshot_bytes = BytesIO(screenshot)
                write_to_base(hreff, l_r, screenshot_bytes)
        except:
            print("Нет рекламы")
            continue
        driver.get('https://web.telegram.org/k/')
    driver.quit()
    print("ДОБАВЛЕНО: ", count)
parsing()
print("ВСЕГО В БАЗЕ: ", read_from_base(1)[0][0])


