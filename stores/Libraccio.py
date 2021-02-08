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
AUTHOR_CLASS = "attr author"
PRICE_CLASS = "sellpr"
FORMAT_DRM_CLASS = "ebook-value-format"


def removeFinalComma(string: str):
    # Sometimes there is a comma after author's name
    if string and string[-1] == ",":
        return string[:-1]
    else:
        return string


async def ebookInfos(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": USERAGENT}) as response:  # noqa: E501
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
    format_and_drm = soup.find('td', id=FORMAT_DRM_CLASS).get_text()
    word_list = format_and_drm.split()
    format_ = word_list[0]
    if "DRM" in word_list:
        drm = "Yes"
    else:
        drm = "None"
    return format_, drm


class Libraccio():
    @staticmethod
    async def searchBook(title: str):
        url = f"{BASE_URL}/src/?xy={title}&ch={EBOOK_QUERY}"
        logging.debug(f"Starting {NAME} download")
        start_t = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": USERAGENT}) as response:  # noqa: E501
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
                author = book.find('div', class_=AUTHOR_CLASS) \
                             .find('span', class_="data").get_text().strip()
                author = removeFinalComma(author)
                price = book.find('span', class_=PRICE_CLASS).get_text()
                format_, drm = await ebookInfos(str(BASE_URL) +
                                                url['href'])
                booklist.append(Book.Book(title, author, price,
                                          format_.upper(), drm))
            except AttributeError:
                # idk what causes this error
                continue
        printing.store_print(NAME, booklist)
