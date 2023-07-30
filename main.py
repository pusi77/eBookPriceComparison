import sys
import asyncio
import logging

from utils import printing
from stores import BookRepublic
from stores import Libraccio
from stores import LibrerieCoop
from stores import Unilibro

DEBUG = False


async def concurrent_search(book_name: str):
    await asyncio.gather(
        # BookRepublic.BookRepublic.searchBook(book_name),
        # Libraccio.Libraccio.searchBook(book_name),
        # LibrerieCoop.LibrerieCoop.searchBook(book_name),
        Unilibro.Unilibro.searchBook(book_name)
    )

if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(filename='debug.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

    printing.checkUsage(sys.argv)
    print("Searching for book: " + sys.argv[1])

    asyncio.run(concurrent_search(sys.argv[1]))
