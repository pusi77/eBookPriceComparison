import aiohttp
import logging
import time
import urllib.parse
from bs4 import BeautifulSoup

import Book
from utils import printing


NAME = "Unilibro"
BASE_URL = "https://www.unilibro.it"


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.unilibro.it",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.unilibro.it/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "TE": "trailers"
}

class Unilibro():
    @staticmethod
    async def searchBook(title: str):
        url = f"{BASE_URL}/libri/ff"
        logging.debug(f"Starting {NAME} download")
        start_t = time.time()
        async with aiohttp.ClientSession() as session:
            # Get cookies
            async with session.get(BASE_URL, headers=headers):
                cookies = session.cookie_jar.filter_cookies(BASE_URL)

            safe_title = urllib.parse.quote_plus(title)
            data = f"search=%2FUnilibro%2FSearch.ff%3Fquery%3D{safe_title}%26filterProdGroup%3D09%26channel%3Dit%26productsPerPage%3D20%26xml%3Dtrue"
            async with session.post(url, data=data, headers=headers, cookies=cookies) as response:
                # Handle the response as needed
                data = await response.text()
                end_t = time.time()
                logging.debug(f"{NAME} downloaded in {end_t - start_t}")
                print(data)

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as response:
        #         content = await response.text()
        #         end_t = time.time()
        #         logging.debug(f"{NAME} downloaded in {end_t - start_t}")
        # soup = BeautifulSoup(content, 'html.parser')
        # data = soup.find_all('div', class_=BOOK_CLASS)
        # booklist = []
        # for book in data:
        #     title = book.find('div', class_=TITLE_CLASS).get_text().strip()
        #     author = book.find('div', class_=AUTHOR_CLASS).getText().strip()
        #     price = book.find('span', class_=PRICE_CLASS).get_text()
        #     format_ = book.find('div', class_=FORMAT_CLASS) \
        #                   .getText().strip("Formato: ")
        #     drm = book.findAll('div', class_=DRM_CLASS)[1].getText().strip()
        #     booklist.append(Book.Book(title, author, price,
        #                               format_.upper(), drm))
        # printing.store_print(NAME, booklist)
