import mysql.connector
import questionary
from abc import abstractclassmethod, ABC

#Singtlon com a coneção de banco de dados
## Modulo de coneção
class ConectBD:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.conect = mysql.connector.connect(
                host="localhost",
                user="user",
                password="user123",
                database="mysqlDatabase",
                port=3307
            )
            cls._inst.cursor = cls._inst.conect.cursor()
        return cls._inst
    
    def get_cursor(self):
        return self._inst.cursor
    def commit(self):
        self._inst.conect.commit()
    def close(self):
        self._inst.cursor.close()
        self._inst.conect.close()
    

#metodo factory para diferentes ações
class Action(ABC):
    @abstractclassmethod
    def execute(self):
        pass
class RegistrarLivro(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()

        livro_nome = input("Qual o nome do livro")
        categoria = questionary.select(
            "Qual a categoria do livro",
            choices = ['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
        ).ask()
        autor = input("Qual o nome do autor?: ")

        try:
            cursor.execute(
                'INSERT INTO books (name, category, author) VALUES (%s, %s, %s)',
                (livro_nome, categoria, autor)
            )
            db.commit()
            print("Livro cadastrado")
        except Exception as e:
            print("ERRO ao cadastrar: ", e)

class RegistrarUser(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()

        nomeUser = input("Digite seu nome: ")
        emailUser = input("Digite seu email: ")
        telUser = input("Digite seu telefoene: ")

        try:
            cursor.execute(
                'INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)',
                (nomeUser, emailUser, telUser)
            )
            db.commit()
            print("Usuario cadastrado: ")
        except Exception as e:
            print("ERRO ao cadastrae: ", e)
class fazerReserva(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()

        user_name = input("Digite o nome do usuário: ")
        cursor.execute('SELECT * FROM users WHERE name = %s', (user_name,))
        user_results = cursor.fetchall()

        if len(user_results) == 0:
            print('Erro: Usuário não encontrado.')
            

        book_title = input("Digite o título do livro: ")
        cursor.execute('SELECT * FROM books WHERE name = %s', (book_title,))
        book_results = cursor.fetchall()

        if len(book_results) == 0:
            print('Erro: Livro não encontrado.')
            

        book_id = book_results[0][0]  
        user_id = user_results[0][0]  

        try:
            cursor.execute('INSERT INTO reservations (bookId, userId) VALUES (%s, %s)', (book_id, user_id))
            db.commit()
            print('Reserva feita com sucesso!')
        except Exception as e:
            print("Erro ao realizar reserva:", e)
class sair(Action):
    def execute(self):
        db = ConectBD()
        cursor = db.get_cursor()

        print("Saindo...")
        cursor.close()
        db.close()

class ActionFactory:
    @staticmethod
    def get_acao(acao_nome):
        acao = {
            "Cadastrar livro: ": RegistrarLivro,
            "Cadastrar Usuario: ": RegistrarUser,
            "Fazer Reserva: ": fazerReserva,
            "Sair": sair
        }
        return acao.get(acao_nome, None)()
    
#Usando o metodo strategy
class SearchStrategy(ABC):
    @abstractclassmethod
    def pesquisa(self, cursor):
        pass

class buscaPorTitulo(SearchStrategy):
    def pesquisa(self, cursor):
        livro_titulo = input("Titulo do livro: ")
        cursor.execute('SELECT * FROM books WHERE name = %s', (livro_titulo,))
        return cursor.fetchall()
class buscaPorAutor(SearchStrategy):
    def pesquisa(self, cursor):
        author_name = input("Digite o nome do autor: ")
        cursor.execute('SELECT * FROM books WHERE author = %s', (author_name,))
        return cursor.fetchall()
class buscaPorCategoria(SearchStrategy):
    def pesquisa(self, cursor):
        category_choices = [
                'Esporte',
                'Ficção',
                'Educação',
                'Fantasia',
                'Diversa'
            ]
        category_name = questionary.select(
            "Escolha a categoria do livro:",
            choices=category_choices
        ).ask()
        cursor.execute('SELECT * FROM books WHERE category = %s', (category_name,))
        return cursor.fetchall()
class LivroBusca:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy
    def setstrategy(self, startegy: SearchStrategy):
        self.strategy = startegy
    def execute_search(self, cursor):
        return self.strategy.search(cursor)
