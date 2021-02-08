import sys
import asyncio

from utils import printing
from stores import BookRepublic
from stores import Libraccio
from stores import LibrerieCoop


async def concurrent_search(book_name: str):
    await asyncio.gather(
        LibrerieCoop.LibrerieCoop.searchBook(book_name),
        BookRepublic.BookRepublic.searchBook(book_name),
        Libraccio.Libraccio.searchBook(book_name)
    )

if __name__ == "__main__":
    printing.checkUsage(sys.argv)
    print("Searching for book: " + sys.argv[1])

    asyncio.run(concurrent_search(sys.argv[1]))
