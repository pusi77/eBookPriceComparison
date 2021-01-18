import requests
from bs4 import BeautifulSoup

import Book
from stores import AbstractStore

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


def removeFinalComma(string: str):
    # Sometimes there is a comma after author's name
    if string and string[-1] == ",":
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


class Libraccio(AbstractStore.AbstractStore):
    @staticmethod
    def searchBook(title: str):
        url = f"{BASE_URL}/src/?xy={title}&ch={EBOOK_QUERY}"
        page = requests.get(url, headers={"User-Agent": USERAGENT})
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('div', class_="row")
        booklist = []

        for book in data:
            try:
                url = book.find("a", href=lambda href:
                                href and "/ebook/" in href)
                if url is None:
                    continue
                title = book.find('div', class_="title").find('a').get_text()
                author = book.find('div', class_="attr author") \
                    .find('span', class_="data").get_text().strip()
                author = removeFinalComma(author)
                price = book.find('span', class_="sellpr").get_text()
                format_, drm = ebookInfos(str(BASE_URL) + url['href'])
                booklist.append(Book.Book(title, author, price,
                                          format_.upper(), drm))
            except AttributeError:
                # idk what causes this error
                continue
        return NAME, booklist
