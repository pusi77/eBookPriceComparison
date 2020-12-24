from abc import ABC, abstractmethod


class AbstractStore(ABC):
    # every store class must have searchBook method
    @abstractmethod
    def searchBook(title: str):
        pass
