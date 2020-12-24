class Book:

    def __init__(self, title, author, price, format_, drm=None):
        self.title = title
        self.author = author
        self.price = price
        self.format_ = format_
        self.drm = drm

    def infos(self):
        return (self.title, self.author, self.price, self.format_,
                self.drm)
