import aiohttp
import logging
import time
from bs4 import BeautifulSoup

import Book
from utils import printing


NAME = "Unilibro"
BASE_URL = "https://www.unilibro.it"


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "97",
    "Origin": "https://www.unilibro.it",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.unilibro.it/",
    "Cookie": "visid_incap_1099613=EPSZU0iwQyGZB3B3/kJSsWqcd2QAAAAAQUIPAAAAAACXm9VUg4ddotUcX8gI3/w6; incap_ses_475_1099613=yfLoAXg5IT9RklHf9IqXBmqcd2QAAAAAgG2vta9kV2JBFElFFytI7g==; frzbt.user=%7B%22properties%22%3A%7B%22createdAt%22%3A1685560427503%7D%2C%22anonymous_id%22%3A%223d969fec-d651-4fd4-9c49-9c34acc9000c%22%2C%22distinct_id%22%3A%223d969fec-d651-4fd4-9c49-9c34acc9000c%22%7D; frzbt.session=%7B%22session_id%22%3A%228a0b8eef-4684-4bee-9a4b-c1249133f8ce%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Wed+May+31+2023+21%3A14%3A58+GMT%2B0200+(Central+European+Summer+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0391bac2-bcfc-48d0-9e81-950ea064182b&interactionCount=1&landingPath=https%3A%2F%2Fwww.unilibro.it%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A0%2CC0004%3A0; _ga_JRSZ4Q84EQ=GS1.1.1685560427.1.0.1685560427.0.0.0; _ga=GA1.1.2078838253.1685560428",
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
            async with session.post(url, headers=headers) as response:
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
