from tabulate import tabulate

HEADERS = ("Title", "Author", "Price", "Format", "DRM")

def filterRandomTitles(title: str, books: list, args) -> list:
    if args.unfiltered:
        return books
    less_random_books = []
    for book in books:
        random = False
        for word in title.lower().split(' '):
            if word not in book.title.lower():
                random = True
                break
        if not random:
            less_random_books.append(book)
    return less_random_books


def store_print(title: str, store_name: str, books: list, args):
    books = filterRandomTitles(title, books, args)
    book_infos = []
    print("\U0001F56E  " + store_name)
    if not books:
        print("Book not found!")
    else:
        for book in books:
            book_infos.append(book.infos())
        print(tabulate(book_infos, headers=HEADERS, tablefmt="pretty",
                       colalign="left"))
        