import aiohttp
import logging
import time
from bs4 import BeautifulSoup

import Book
from utils import utils


NAME = "BookRepublic"
BASE_URL = "https://www.bookrepublic.it"

BOOK_CLASS = "col-listato col-12 col-md-6"
TITLE_CLASS = "h4 titolo-ebook"
AUTHOR_CLASS = "autore-small pt-1 d-inline-block"
PRICE_CLASS = "current-price"
FORMAT_CLASS = "h6 pt-1 mb-0"
DRM_CLASS = "h6"


class BookRepublic():
    @staticmethod
    async def searchBook(searchedTitle: str):
        url = f"{BASE_URL}/search/?q={searchedTitle}"
        logging.debug(f"Starting {NAME} download")
        start_t = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                end_t = time.time()
                logging.debug(f"{NAME} downloaded in {end_t - start_t}")
        soup = BeautifulSoup(content, 'html.parser')
        data = soup.find_all('div', class_=BOOK_CLASS)
        booklist = []
        for book in data:
            title = book.find('div', class_=TITLE_CLASS).get_text().strip()
            author = book.find('div', class_=AUTHOR_CLASS).getText().strip()
            price = book.find('span', class_=PRICE_CLASS).get_text()
            format_ = book.find('div', class_=FORMAT_CLASS) \
                          .getText().strip("Formato: ")
            drm = book.findAll('div', class_=DRM_CLASS)[1].getText().strip()
            booklist.append(Book.Book(title, author, price,
                                      format_.upper(), drm))
        utils.store_print(searchedTitle, NAME, booklist)
