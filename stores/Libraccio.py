import aiohttp
import logging
import time
from bs4 import BeautifulSoup

import Book
from utils import printing


# IMPORTANT NOTE:
# I've no idea why, but searching with ebook-only filter doesn't show some
# titles which can be found with standard search, so to find them i must
# search all books and then check if they had ebook version.
# tl;dr: website is borked, but offer some DRM-free books so..

NAME = "Libraccio"
BASE_URL = "https://www.libraccio.it"
PAPERBACK_QUERY = "libraccio"
EBOOK_QUERY = "ebook"
# without user-agent will get 403
USERAGENT = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) "
             "Gecko/20100101 Firefox/15.0.1")

BOOK_CLASS = "row"
TITLE_CLASS = "title"
AUTHOR_CLASS = "lAuthor"
PRICE_CLASS = "sellpr"
FORMAT_CLASS = "ebook-label-format"


async def ebookInfos(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": USERAGENT}) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
    format_ = soup.find('td', id=FORMAT_CLASS).find_next_sibling().get_text()
    drm = "???"
    return format_, drm


class Libraccio():
    @staticmethod
    async def searchBook(title: str):
        url = f"{BASE_URL}/src/?xy={title}&ch={EBOOK_QUERY}"
        logging.debug(f"Starting {NAME} download")
        start_t = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": USERAGENT}) as response:
                content = await response.text()
                end_t = time.time()
                logging.debug(f"{NAME} downloaded in {end_t - start_t}")
        soup = BeautifulSoup(content, 'html.parser')
        data = soup.find_all('div', class_=BOOK_CLASS)
        booklist = []
        for book in data:
            try:
                url = book.find("a", href=lambda href:
                                href and "/ebook/" in href)
                if url is None:
                    continue
                title = book.find('div', class_=TITLE_CLASS) \
                            .find('a').get_text()
                author = book.find('a', class_="lAuthor").get_text().strip()
                price = book.find('span', class_=PRICE_CLASS).get_text()
                format_, drm = await ebookInfos(str(BASE_URL) + url['href'])
                booklist.append(Book.Book(title, author, price, format_.upper(), drm))
            except AttributeError as e:
                print(f'ERROR: {e}')
                logging.debug(e)
                continue
        printing.store_print(NAME, booklist)
