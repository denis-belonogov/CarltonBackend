import datetime
import re
import time

import URLSearchParams
from bs4 import BeautifulSoup
from selenium import webdriver


def get_offers(request_args):
    URL = str(URLSearchParams.URLSearchParams(
        "https://ibe-server.uphotel.agency/ibe-preview/79579851-938d-441c-b6b9-9e24d15aa192#/booking/results?").append(
        request_args))
    URL += "&"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(1)
    html = re.sub(r'<!.*?->', '', driver.page_source)
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    rooms = soup.body.find('div', attrs={'class': 'ibe-room-results-list'})

    offer_text = f'Sehr geehrter Gast, \nwie von Ihnen gewünscht sende ich Ihnen ein Angebot für ein Zimmer für {request_args["adults"]}  {"Personen" if int(request_args["adults"]) > 1 else "Person"} vom {datetime.datetime.strptime(request_args["arrival"], "%Y-%m-%d").strftime("%d.%m.%Y")} zum {datetime.datetime.strptime(request_args["departure"], "%Y-%m-%d").strftime("%d.%m.%Y")}.\n\n'

    for room in rooms.contents:
        room_prices = room.contents[0].find(
            'div', attrs={'class': 'ibe-rate-options'}).contents

        room_name = room.contents[0].find(
            'div', attrs={'class': 'ibe-room-title'}).contents[0]
        for room_price in room_prices:
            if "Nicht erstattbare" not in room_price.contents[0].text:
                with_breakfast = "mit Frühstück" in room_price.contents[0].text
                price = room_price.contents[0].text.split('€')[0].strip()
                city_tax = round(float(price.replace(',', '.')) * 0.075, 2)
                offer_text += f"{room_name}, {'inkl. Frühstück ' if with_breakfast else ''}zum Preis von {price} € + {str(city_tax).replace('.', ',')} € City-Tax je Zimmer\n"
    return offer_text
