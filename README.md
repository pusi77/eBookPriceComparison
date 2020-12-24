# bpc
I was tired of searching (e)books on my favourite sites. I'm mainly interested in low prices and permissive (ideally none) DRMs for ebooks.

Example:

```
$ python main.py "Guida galattica per gli autostoppisti"

Searching for book: Guida galattica per gli autostoppisti
librerie.coop
+-----------------------------------------+---------------+---------+----------+-----------+
|                  Title                  |    Author     |  Price  |  Format  |    DRM    |
+-----------------------------------------+---------------+---------+----------+-----------+
|  Guida galattica per gli autostoppisti  | Douglas Adams | € 12,50 | CARTACEO |           |
|  Guida galattica per gli autostoppisti  | Douglas Adams | € 7,99  |   EPUB   | Adobe DRM |
| Guida galattica per gli autostoppist... | Douglas Adams | € 16,50 | CARTACEO |           |
| Guida galattica per gli autostoppist... | Douglas Adams | € 9,99  |   EPUB   | Adobe DRM |
| Guida galattica per gli autostoppist... | Douglas Adams | € 28,00 | CARTACEO |           |
| Niente panico. La guida galattica pe... |  Neil Gaiman  | € 19,90 | CARTACEO |           |
| Guida galattica per autostoppisti - ... |  Neil Gaiman  | € 10,99 |   EPUB   | Adobe DRM |
+-----------------------------------------+---------------+---------+----------+-----------+
```

## Stores supported
- [librerie.coop](https://www.librerie.coop/)
- [Libraccio](https://www.libraccio.it/)

### Planning to support
- [IBS](https://www.ibs.it/)
- [Amazon](https://www.amazon.it/) ?

## ToDo
- Concurrent stores analysis(?)

## Known problems(?)
- Search is limited to first page, but who needs >25 results for a book?