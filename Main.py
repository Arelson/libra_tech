import questionary
from Book.BookRegister import RegisterBook
from User.UserRegister import RegisterUser
from Actions.MakeReservation import FazerReserva
from Actions.SystemExit import ExitSystem
from Book.Search.title import buscaPorTitulo
from Book.Search.author import buscaPorAutor
from Book.Search.category import buscaPorCategoria
from Book.Search.bookSearch import BookSearch
from Database.Conection import DatabaseConnection

# Menu principal
def main():
    actions = {
        'Cadastrar livro': RegisterBook(),
        'Cadastrar usuario': RegisterUser(),
        'Fazer uma reserva': FazerReserva(),
        'Sair': ExitSystem()
    }

    while True:
        action = questionary.select(
            "O que deseja fazer?",
            choices=list(actions.keys()) + ['Buscar um livro']
        ).ask()

        if action == "Buscar um livro":
            db = DatabaseConnection()
            cursor = db.get_cursor()
            search_type = questionary.select(
                "Como deseja buscar o livro?",
                choices=['Por título', 'Por autor', 'Por categoria']
            ).ask()

            strategy = {
                'Por título': buscaPorTitulo(),
                'Por autor': buscaPorAutor(),
                'Por categoria': buscaPorCategoria()
            }[search_type]

            search = BookSearch(strategy)
            results = search.execute_search(cursor)
            for book in results:
                print(f"📖 {book}")
        else:
            actions[action].execute()

if __name__ == "__main__":
    main()