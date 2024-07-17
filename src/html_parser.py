import datetime
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_offers(request_args):
    URL = "https://ibe-server.uphotel.agency/ibe-preview/79579851-938d-441c-b6b9-9e24d15aa192#/booking/results?"
    for key, value in request_args.items():
        URL += f"{key}={value}&"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ibe-room-results-list'))
        )
        html = re.sub(r'<!.*?->', '', driver.page_source)
        soup = BeautifulSoup(html, "html.parser")
        rooms = soup.find('div', attrs={'class': 'ibe-room-results-list'})

    offer_text = f'Sehr geehrter Gast, \nwie von Ihnen gewünscht sende ich Ihnen ein Angebot für ein Zimmer für {request_args["adults"]}  {"Personen" if int(request_args["adults"]) > 1 else "Person"} vom {datetime.datetime.strptime(request_args["arrival"], "%Y-%m-%d").strftime("%d.%m.%Y")} zum {datetime.datetime.strptime(request_args["departure"], "%Y-%m-%d").strftime("%d.%m.%Y")}.\n\n'

    for room in rooms.find_all('div', recursive=False):
        room_prices = room.find('div', attrs={'class': 'ibe-rate-options'}).find_all('div', recursive=False)
        room_name = room.find('div', attrs={'class': 'ibe-room-title'}).text.strip()
        for room_price in room_prices:
            if "Nicht erstattbare" not in room_price.text:
                with_breakfast = "mit Frühstück" in room_price.text
                price = room_price.text.split('€')[0].strip()
                city_tax = round(float(price.replace(',', '.')) * 0.075, 2)
                offer_text += f"{room_name}, {'inkl. Frühstück ' if with_breakfast else ''}zum Preis von {price} € + {str(city_tax).replace('.', ',')} € City-Tax je Zimmer\n"
    return offer_text
