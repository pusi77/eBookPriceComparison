import requests
from bs4 import BeautifulSoup

import Book
from stores import AbstractStore

NAME = "librerie.coop"
BASE_URL = "https://www.librerie.coop"
BOOK_URL = "/libri/"
PAPERBACK = "CARTACEO"


def getProtection(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    drm = soup.find('p', class_="h6 bold pl-1").get_text()
    return drm


class LibrerieCoop(AbstractStore.AbstractStore):
    @staticmethod
    def searchBook(title: str):
        url = f"{BASE_URL}/search/?q={title}&cerca_in=titolo"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('div', class_="product-info-small")
        booklist = []

        for book in data:
            title = book.find(class_="titolo-prodotto").get_text().strip()
            author_html = book.find('a', itemprop="author")
            author = None
            if author_html is not None:
                # sometimes author is not displayed on webpage
                author = author_html.get_text().strip()
            price = book.find(class_="current-price").get_text().strip()
            format_ = book.find(class_="info-formato").get_text().strip()
            if format_ != PAPERBACK:
                url = book.find("a", href=lambda href:
                                href and "/libri/" in href)
                drm = getProtection(str(BASE_URL) + url['href'])
                booklist.append(Book.Book(title, author, price,
                                format_.upper(), drm))
                continue
            booklist.append(Book.Book(title, author, price, format_.upper()))
        return NAME, booklist
