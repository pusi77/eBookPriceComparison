import requests
from bs4 import BeautifulSoup

import Book
from stores import AbstractStore

NAME = "Libraccio"
BASE_URL = "https://www.libraccio.it"
PAPERBACK_QUERY = "libraccio"
EBOOK_QUERY = "ebook"
# without user-agent will get 403
USERAGENT = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) "
             "Gecko/20100101 Firefox/15.0.1")


def removeFinalComma(string: str):
    # Sometimes there is a comma after author's name
    if string[-1] == ",":
        return string[:-1]
    else:
        return string


def ebookInfos(url: str):
    page = requests.get(url, headers={"User-Agent": USERAGENT})
    soup = BeautifulSoup(page.content, 'html.parser')
    format_and_drm = soup.find('td', id="ebook-value-format").get_text()
    word_list = format_and_drm.split()
    format_ = word_list[0]
    if "DRM" in word_list:
        drm = "Yes"
    else:
        drm = "None"
    return format_, drm


def scrapBook(title: str, ebook=False):
    # with this func most code is shared for books and ebooks
    if ebook:
        url = f"{BASE_URL}/src/?xy={title}&ch={EBOOK_QUERY}"
    else:
        url = f"{BASE_URL}/src/?xy={title}&ch={PAPERBACK_QUERY}"
    page = requests.get(url, headers={"User-Agent": USERAGENT})
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('div', class_="row")
    booklist = []

    for book in data:
        try:
            title = book.find('div', class_="title").find('a').get_text()
            author = book.find('div', class_="attr author") \
                .find('span', class_="data").get_text().strip()
            author = removeFinalComma(author)
            price = book.find('span', class_="sellpr").get_text()
            if ebook:
                url = book.find("a", href=lambda href:
                                href and "/ebook/" in href)
                format_, drm = ebookInfos(str(BASE_URL) + url['href'])
                booklist.append(Book.Book(title, author, price,
                                          format_.upper(), drm))
            else:
                format_ = "CARTACEO"
                booklist.append(Book.Book(title, author,
                                price, format_.upper()))
        except AttributeError:
            # idk what causes this error
            continue
    return booklist


class Libraccio(AbstractStore.AbstractStore):
    @staticmethod
    def searchBook(title: str):
        paperback_list = scrapBook(title)
        ebook_list = scrapBook(title, ebook=True)
        return NAME, paperback_list + ebook_list
