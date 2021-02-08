import aiohttp
from bs4 import BeautifulSoup

import Book
from utils import printing


NAME = "librerie.coop"
BASE_URL = "https://www.librerie.coop"
BOOK_URL = "/libri/"
PAPERBACK = "CARTACEO"

BOOK_CLASS = "product-info-small"
TITLE_CLASS = "titolo-prodotto"
AUTHOR_CLASS = "author"
PRICE_CLASS = "current-price"
FORMAT_CLASS = "info-formato"
DRM_CLASS = "h6 bold pl-1"


async def getProtection(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
    drm = soup.find('p', class_=DRM_CLASS).get_text()
    return drm


class LibrerieCoop():
    @staticmethod
    async def searchBook(title: str):
        url = f"{BASE_URL}/search/?q={title}&cerca_in=titolo"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
        data = soup.find_all('div', class_=BOOK_CLASS)
        booklist = []
        for book in data:
            format_ = book.find(class_=FORMAT_CLASS).get_text().strip()
            if format_ == PAPERBACK:
                continue

            title = book.find(class_=TITLE_CLASS).get_text().strip()
            author_html = book.find('a', itemprop=AUTHOR_CLASS)
            author = None
            if author_html is not None:
                # sometimes author is not displayed on webpage
                author = author_html.get_text().strip()
            price = book.find(class_=PRICE_CLASS).get_text().strip()
            book_url = book.find("a", href=lambda href:
                                 href and "/libri/" in href)
            drm = await getProtection(str(BASE_URL) + book_url['href'])
            booklist.append(Book.Book(title, author, price,
                                      format_.upper(), drm))
        printing.store_print(NAME, booklist)
