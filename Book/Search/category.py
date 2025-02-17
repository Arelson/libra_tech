from Book.Search.bookSearch import SearchStrategy
import questionary

class buscaPorCategoria(SearchStrategy):
    def search(self, cursor):
        category = questionary.select(
            "Escolha a categoria do livro:",
            choices=['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
        ).ask()
        cursor.execute('SELECT * FROM books WHERE category = %s', (category,))
        return cursor.fetchall()