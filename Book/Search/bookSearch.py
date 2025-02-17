from Book.Search.base import SearchStrategy

class BookSearch:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, cursor):
        return self.strategy.search(cursor)