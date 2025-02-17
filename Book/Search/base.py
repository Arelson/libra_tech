from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, cursor):
        pass