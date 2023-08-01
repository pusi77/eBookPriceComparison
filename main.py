import asyncio
import logging
import argparse

from stores import BookRepublic
from stores import Libraccio
from stores import LibrerieCoop
from stores import Unilibro

DEBUG = False
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--unfiltered", help="get unfiltered results", action='store_true')
parser.add_argument('title')
args = parser.parse_args()

async def concurrent_search(book_name: str):
    await asyncio.gather(
        BookRepublic.BookRepublic.searchBook(book_name, args),
        Libraccio.Libraccio.searchBook(book_name, args),
        LibrerieCoop.LibrerieCoop.searchBook(book_name, args),
        Unilibro.Unilibro.searchBook(book_name, args)
    )

if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(filename='debug.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

    print("Searching for book: " + args.title)

    asyncio.run(concurrent_search(args.title))
