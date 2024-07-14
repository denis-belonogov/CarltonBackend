from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import datetime


def get_offers(arrival_date, departure_date, n_persons):
    arrival_date = datetime.datetime.strptime(arrival_date, "%Y-%m-%d").date()
    departure_date = datetime.datetime.strptime(departure_date, "%Y-%m-%d").date()
    #n_persons = int(input('Amount  of persons: '))

    URL = f"https://onhotels.de/#/booking/results?propertyId=CARLTON&arrival={arrival_date.strftime('%Y-%m-%d')}&departure={departure_date.strftime('%Y-%m-%d')}&adults={n_persons}&"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(1)
    try:
        driver.find_element(By.LINK_TEXT, "Alle akzeptieren").click()
    except:
        pass

    time.sleep(6)
    html = re.sub(r'<!.*?->','', driver.page_source)
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    rooms = soup.body.find('div', attrs={'class':'ibe-room-results-list'})

    offer_text =f'Sehr geehrter Gast, \nwie von Ihnen gewünscht sende ich Ihnen ein Angebot für ein Zimmer für {n_persons} {"Personen" if n_persons > 1 else "Person"} vom {arrival_date.strftime("%d.%m.%Y")} zum {departure_date.strftime("%d.%m.%Y")}.\n\n'

    for room in rooms.contents:
        room_prices = room.contents[0].find('div', attrs={'class':'ibe-rate-options'}).contents

        room_name = room.contents[0].find('div', attrs={'class':'ibe-room-title'}).contents[0]
        for room_price in room_prices:
            if "Nicht erstattbare" not in room_price.contents[0].text:
                with_breakfast = "mit Frühstück" in room_price.contents[0].text
                price = room_price.contents[0].text.split('€')[0].strip()
                city_tax = round(float(price.replace(',', '.')) * 0.075, 2)
                offer_text += f"{room_name}, {'inkl. Frühstück ' if with_breakfast else ''}zum Preis von {price} € + {str(city_tax).replace('.', ',')} € City-Tax je Zimmer\n"
    return offer_text