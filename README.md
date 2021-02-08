# ebpc
I was tired of searching and comparing eBooks on all my favourite sites, so i made this to automate it. 
I'm mainly interested in low prices and permissive (ideally none) DRMs for ebooks.

Example:

```
$ python main.py "Guida galattica per gli autostoppisti"

Searching for book: Guida galattica per gli autostoppisti
librerie.coop
+-----------------------------------------+---------------+---------+----------+-----------+
|                  Title                  |    Author     |  Price  |  Format  |    DRM    |
+-----------------------------------------+---------------+---------+----------+-----------+
| Guida galattica per gli autostoppisti   | Douglas Adams | € 7,99  |   EPUB   | Adobe DRM |
| Guida galattica per gli autostoppist... | Douglas Adams | € 9,99  |   EPUB   | Adobe DRM |
| Guida galattica per autostoppisti - ... |  Neil Gaiman  | € 10,99 |   EPUB   | Adobe DRM |
+-----------------------------------------+---------------+---------+----------+-----------+
```

## Stores supported
- [BookRepublic](https://www.bookrepublic.it/)
- [Libraccio](https://www.libraccio.it/)
- [librerie.coop](https://www.librerie.coop/)

## ToDo
- Logging

## Known problems(?)
- Search is limited to first page, but who needs >25 results for a book?
