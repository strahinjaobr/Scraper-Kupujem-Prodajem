import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json
from dotenv import load_dotenv

load_dotenv()

# function that extracts all ads from a single page

def extract_data(items_list, session, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    page = session.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    ads = soup.find_all('article')
    for ad in ads:
        item = {}
        if ad['class'][0] == "CategoryPartner-module-scss-module__b_oGQG__item":
            item['title'] = ad.find('div', class_='CategoryPartnerInfoAndPrice-module-scss-module__-NI2sq__categoryPartnerTitle').text
            item['price'] = 'In the ad'
            item['link'] = ad.find('a', class_="Link-module-scss-module__1zYhVG__link")['href']
        else:
            item['title'] = ad.find('div', class_='AdItem-module-scss-module__RS9oJW__name').text
            item['price'] = ad.find('div', class_='priceText AdItem-module-scss-module__2GyMja__inlinePrice').text
            item['link'] = 'https://www.kupujemprodajem.com' + ad.find('a', class_="Link-module-scss-module__1zYhVG__link")['href']
        items_list.append(item)
    return items_list

# calls the single-page scraping function n times and returns the list
def scrape():
    items_list = []
    session = requests.Session()
    for i in range(1, 3):
        url = f"https://www.kupujemprodajem.com/pretraga?keywords=iphone%20&currency=eur&type=sell&ignoreUserId=no&page={i}&order=posted%20desc&prev_keywords=iphone%20"
        
        items_list = extract_data(items_list, session, url)
        time.sleep(2)
    return items_list

# saves the list of known ad links to a JSON file
def save_file(items_list):
    with open('known_ads.json', 'w') as f:
        json.dump(items_list, f, indent=4)

# reads the list of links saved by the function above
def load_file():
    try:
        with open('known_ads.json', 'r') as f:
            items_list = json.load(f)
            return items_list
    except FileNotFoundError:
        print('File not found!')
        return []

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': text}
    requests.get(url, params=params)

while True:
    current_items = scrape()
    item_map = {el['link']: el for el in current_items}
    current_links = [el['link'] for el in current_items]
    known_links = load_file()
    new_links = set(current_links) - set(known_links)
    known_links.extend(list(new_links))
    for ad in new_links:
        message = f"NEW AD! \n {item_map[ad]['title']} \n {item_map[ad]['price']} \n {ad}"
        send_message(message)
    save_file(known_links)
    time.sleep(120)