from Book.Search.bookSearch import SearchStrategy

class buscaPorTitulo(SearchStrategy):
    def search(self, cursor):
        title = input("Título do livro: ")
        cursor.execute('SELECT * FROM books WHERE name = %s', (title,))
        return cursor.fetchall()