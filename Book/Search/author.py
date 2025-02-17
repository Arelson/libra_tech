from base import SearchStrategy

class buscaPorAutor(SearchStrategy):
    def search(self, cursor):
        author = input("Nome do autor: ")
        cursor.execute('SELECT * FROM books WHERE author = %s', (author,))
        return cursor.fetchall()