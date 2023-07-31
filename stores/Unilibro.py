import aiohttp
import logging
import time
import urllib.parse
import re
from bs4 import BeautifulSoup

import Book
from utils import utils


NAME = "Unilibro"
BASE_URL = "https://www.unilibro.it"


BOOK_CLASS = "block-vet bv-cinque"
PRICE_CLASS = "prezzo-vet"

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

async def ebookDRM(url: str, cookies):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
    drm = [li.text for li in soup.find_all("li") if 'Protezione:' in li.text][0].replace("Protezione:", "")
    drm = drm.replace(" (richiede Adobe Digital Editions)", "")
    return drm

class Unilibro():
    @staticmethod
    async def searchBook(searchedTitle: str, args):
        url = f"{BASE_URL}/libri/ff"
        logging.debug(f"Starting {NAME} download")
        start_t = time.time()
        async with aiohttp.ClientSession() as session:
            # Get cookies
            async with session.get(BASE_URL, headers=headers):
                cookies = session.cookie_jar.filter_cookies(BASE_URL)

            safe_title = urllib.parse.quote_plus(searchedTitle)
            data = f"search=%2FUnilibro%2FSearch.ff%3Fquery%3D{safe_title}%26filterProdGroup%3D09%26channel%3Dit%26productsPerPage%3D20%26xml%3Dtrue"
            async with session.post(url, data=data, headers=headers, cookies=cookies) as response:
                # Handle the response as needed
                content = await response.text()
                end_t = time.time()
                logging.debug(f"{NAME} downloaded in {end_t - start_t}")

            soup = BeautifulSoup(content, 'html.parser')
            data = soup.find_all('div', class_=BOOK_CLASS)
            booklist = []
            for book in data:
                book_title_string = book.find('h5').get_text().strip()
                title = book_title_string.split(". E-book.")[0]
                author = book.find('h6').get_text().strip()
                price = book.find('div', class_=PRICE_CLASS).get_text()
                format_ = book_title_string.split("Formato ")[1]

                book_url = book.find('a', class_="c-")['href']
                drm = await ebookDRM(book_url, cookies)
                booklist.append(Book.Book(title, author, price,
                                        format_, drm))
            utils.store_print(searchedTitle, NAME, booklist, args)
