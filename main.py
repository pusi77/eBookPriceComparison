import sys

from utils import printing
from stores import BookRepublic
from stores import Libraccio
from stores import LibrerieCoop


if __name__ == "__main__":
    printing.checkUsage(sys.argv)

    print("Searching for book: " + sys.argv[1])

    store_name, books = LibrerieCoop.LibrerieCoop.searchBook(sys.argv[1])
    printing.store_print(store_name, books)

    store_name, books = BookRepublic.BookRepublic.searchBook(sys.argv[1])
    printing.store_print(store_name, books)

    store_name, books = Libraccio.Libraccio.searchBook(sys.argv[1])
    printing.store_print(store_name, books)
