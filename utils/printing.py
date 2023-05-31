from tabulate import tabulate

HEADERS = ("Title", "Author", "Price", "Format", "DRM")

def checkUsage(argv: list):
    if len(argv) != 2:
        print('ERROR: Wrong number of arguments!\n')
        print('USAGE: main.py "bookname"')
        print('Example: main.py "the hitchhiker\'s guide to the galaxy"')
        exit()


def store_print(store_name: str, books: list):
    book_infos = []
    print("\U0001F56E  " + store_name)
    if not books:
        print("Book not found!")
    else:
        for book in books:
            book_infos.append(book.infos())
        print(tabulate(book_infos, headers=HEADERS, tablefmt="pretty",
                       colalign="left"))
