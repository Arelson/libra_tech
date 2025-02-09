import mysql.connector
import questionary
from abc import ABC, abstractmethod

# Singleton para conexão com o banco de dados
class ConectBD:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            try:
                cls._inst = super().__new__(cls)
                cls._inst.conect = mysql.connector.connect(
                    host="127.0.0.1",
                    user="user",
                    password="user123",
                    database="mysqlDatabase",
                    port=3307
                )
                cls._inst.cursor = cls._inst.conect.cursor()
                print("Conexão com o banco de dados estabelecida.")  # Depuração
            except mysql.connector.Error as err:
                print(f"Erro ao conectar ao banco de dados: {err}")  # Depuração
                return None
        return cls._inst

    def get_cursor(self):
        return self._inst.cursor if self._inst else None

    def commit(self):
        if self._inst:
            self._inst.conect.commit()

    def close(self):
        if self._inst:
            if self._inst.cursor:
                self._inst.cursor.close()
            self._inst.conect.close()
            print("Conexão com o banco de dados fechada.")  # Depuração

# Classe abstrata para ações
class Action(ABC):
    @abstractmethod
    def execute(self):
        pass

# Cadastro de livro
class RegistrarLivro(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()
        if cursor is None:
            print("Erro ao obter o cursor.")
            return

        livro_nome = input("Qual o nome do livro: ")
        categoria = questionary.select(
            "Qual a categoria do livro?",
            choices=['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
        ).ask()
        autor = input("Qual o nome do autor?: ")

        try:
            cursor.execute(
                'INSERT INTO books (name, category, author) VALUES (%s, %s, %s)',
                (livro_nome, categoria, autor)
            )
            db.commit()
            print("✅ Livro cadastrado com sucesso!")
        except mysql.connector.Error as err:
            print(f"❌ ERRO ao cadastrar: {err}")

# Cadastro de usuário
class RegistrarUser(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()
        if cursor is None:
            print("Erro ao obter o cursor.")
            return

        nomeUser = input("Digite seu nome: ")
        emailUser = input("Digite seu email: ")
        telUser = input("Digite seu telefone: ")

        try:
            cursor.execute(
                'INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)',
                (nomeUser, emailUser, telUser)
            )
            db.commit()
            print("✅ Usuário cadastrado com sucesso!")
        except mysql.connector.Error as err:
            print(f"❌ ERRO ao cadastrar usuário: {err}")

# Reserva de livros
class FazerReserva(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()
        if cursor is None:
            print("Erro ao obter o cursor.")
            return

        user_name = input("Digite o nome do usuário: ")
        cursor.execute('SELECT id FROM users WHERE name = %s', (user_name,))
        user = cursor.fetchone()

        if not user:
            print("❌ Usuário não encontrado.")
            return

        book_title = input("Digite o título do livro: ")
        cursor.execute('SELECT id FROM books WHERE name = %s', (book_title,))
        book = cursor.fetchone()

        if not book:
            print("❌ Livro não encontrado.")
            return

        try:
            cursor.execute('INSERT INTO reservations (bookId, userId) VALUES (%s, %s)', (book[0], user[0]))
            db.commit()
            print('✅ Reserva feita com sucesso!')
        except mysql.connector.Error as err:
            print(f"❌ Erro ao realizar reserva: {err}")

# Saída do sistema
class Sair(Action):
    def execute(self):
        db = ConectBD()
        db.close()
        print("👋 Saindo...")
        exit()

# Estratégia de busca
class SearchStrategy(ABC):
    @abstractmethod
    def pesquisa(self, cursor):
        pass

class BuscaPorTitulo(SearchStrategy):
    def pesquisa(self, cursor):
        titulo = input("Título do livro: ")
        cursor.execute('SELECT * FROM books WHERE name = %s', (titulo,))
        return cursor.fetchall()

class BuscaPorAutor(SearchStrategy):
    def pesquisa(self, cursor):
        autor = input("Nome do autor: ")
        cursor.execute('SELECT * FROM books WHERE author = %s', (autor,))
        return cursor.fetchall()

class BuscaPorCategoria(SearchStrategy):
    def pesquisa(self, cursor):
        categoria = questionary.select(
            "Escolha a categoria do livro:",
            choices=['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
        ).ask()
        cursor.execute('SELECT * FROM books WHERE category = %s', (categoria,))
        return cursor.fetchall()

class LivroBusca:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, cursor):
        return self.strategy.pesquisa(cursor)

# Menu principal
def main():
    actions = {
        'Cadastrar livro': RegistrarLivro(),
        'Cadastrar usuario': RegistrarUser(),
        'Fazer uma reserva': FazerReserva(),
        'Sair': Sair()
    }

    while True:
        acao = questionary.select(
            "O que deseja fazer?",
            choices=list(actions.keys()) + ['Buscar um livro']
        ).ask()

        if acao == "Buscar um livro":
            db = ConectBD()
            cursor = db.get_cursor()
            tipoBusca = questionary.select(
                "Como deseja buscar o livro?",
                choices=['Por título', 'Por autor', 'Por categoria']
            ).ask()

            strategy = {
                'Por título': BuscaPorTitulo(),
                'Por autor': BuscaPorAutor(),
                'Por categoria': BuscaPorCategoria()
            }[tipoBusca]

            busca = LivroBusca(strategy)
            resultados = busca.execute_search(cursor)
            for livro in resultados:
                print(f"📖 {livro}")
        else:
            actions[acao].execute()

if __name__ == "__main__":
    main()
