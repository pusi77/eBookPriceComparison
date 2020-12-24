import sys

from utils import printing
from stores import LibrerieCoop
from stores import Libraccio


if __name__ == "__main__":
    printing.checkUsage(sys.argv)

    print("Searching for book: " + sys.argv[1])

    store_name, books = LibrerieCoop.LibrerieCoop.searchBook(sys.argv[1])
    printing.store_print(store_name, books)

    store_name, books = Libraccio.Libraccio.searchBook(sys.argv[1])
    printing.store_print(store_name, books)
