import requests
from bs4 import BeautifulSoup
import lxml


def get_link_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept-Language': 'en',
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    name = soup.select_one(selector="#productTitle")
    price = soup.select_one(selector="#priceblock_ourprice")
    if name and price:
        name = name.getText().strip()
        price = float(price.getText().strip()[1:])
        return name, price
    else:
        price = "unavailable"
        name = "unavailable"
        return name, price

