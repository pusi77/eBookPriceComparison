import requests
from bs4 import BeautifulSoup

import Book
from stores import AbstractStore

NAME = "BookRepublic"
BASE_URL = "https://www.bookrepublic.it"


class BookRepublic(AbstractStore.AbstractStore):
    @staticmethod
    def searchBook(title: str):
        url = f"{BASE_URL}/search/?q={title}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('div', class_="col-listato col-12 col-md-6")
        booklist = []

        for book in data:
            title = book.find('div', class_="h4 titolo-ebook") \
                .get_text().strip()
            author = book.find('div',
                               class_="autore-small pt-1 d-inline-block") \
                .getText().strip()
            price = book.find('span', class_="current-price").get_text()
            format_ = book.find('div', class_="h6 pt-1 mb-0") \
                .getText().strip("Formato: ")
            drm = book.findAll('div', class_="h6")[1].getText().strip()
            booklist.append(Book.Book(title, author, price,
                            format_.upper(), drm))
        return NAME, booklist
