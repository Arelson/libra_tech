import mysql.connector
import questionary
from abc import ABC, abstractmethod

# Singleton com a conexão de banco de dados
class ConectBD:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            try:
                cls._inst = super().__new__(cls)
                cls._inst.conect = mysql.connector.connect(
                    host="localhost",
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
        return self._inst.cursor
    
    def commit(self):
        self._inst.conect.commit()
    
    def close(self):
        self._inst.cursor.close()
        self._inst.conect.close()
        print("Conexão com o banco de dados fechada.")  # Depuração

# Método factory para diferentes ações
class Action(ABC):
    @abstractmethod
    def execute(self):
        pass

class RegistrarLivro(Action):
    def execute(self):
        db = ConectBD()
        if db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        cursor = db.get_cursor()
        if cursor is None:
            print("Erro: Não foi possível obter o cursor.")
            return

        livro_nome = input("Qual o nome do livro: ")
        categoria = questionary.select(
            "Qual a categoria do livro",
            choices=['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
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
        if db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        cursor = db.get_cursor()
        if cursor is None:
            print("Erro: Não foi possível obter o cursor.")
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
            print("Usuario cadastrado")
        except Exception as e:
            print("ERRO ao cadastrar: ", e)

class fazerReserva(Action):
    def execute(self):
        db = ConectBD()
        if db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        cursor = db.get_cursor()
        if cursor is None:
            print("Erro: Não foi possível obter o cursor.")
            return

        user_name = input("Digite o nome do usuário: ")
        cursor.execute('SELECT * FROM users WHERE name = %s', (user_name,))
        user_results = cursor.fetchall()

        if len(user_results) == 0:
            print('Erro: Usuário não encontrado.')
            return

        book_title = input("Digite o título do livro: ")
        cursor.execute('SELECT * FROM books WHERE name = %s', (book_title,))
        book_results = cursor.fetchall()

        if len(book_results) == 0:
            print('Erro: Livro não encontrado.')
            return

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
        if db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        cursor = db.get_cursor()
        if cursor is None:
            print("Erro: Não foi possível obter o cursor.")
            return
        if db.get_cursor():
            db.get_cursor().close()
        db.close()
        print("Saindo...")
        exit()

# Usando o método strategy
class SearchStrategy(ABC):
    @abstractmethod
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

    def setstrategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, cursor):
        return self.strategy.pesquisa(cursor)

def main():
    while True:
        acao = questionary.select(
            'O que você deseja fazer? ',
            choices=[
                'Cadastrar livro',
                'Cadastrar usuario',
                'Fazer uma reserva',
                'Buscar um livro',
                'Sair'
            ]
        ).ask()

        print(f"Opção selecionada: {acao}")  # Depuração

        if acao == 'Cadastrar livro':
            print("Executando Cadastrar livro...")  # Depuração
            RegistrarLivro().execute()
        elif acao == 'Cadastrar usuario':
            print("Executando Cadastrar usuario...")  # Depuração
            RegistrarUser().execute()
        elif acao == 'Fazer uma reserva':
            print("Executando Fazer uma reserva...")  # Depuração
            fazerReserva().execute()
        elif acao == 'Buscar um livro':
            print("Executando Buscar um livro...")  # Depuração
            db = ConectBD()
            if db is None:
                print("Erro: Não foi possível conectar ao banco de dados.")
                return

            cursor = db.get_cursor()
            if cursor is None:
                print("Erro: Não foi possível obter o cursor.")
                return

            tipoBusca = questionary.select(
                'Como deseja buscar o livro? ',
                choices=[
                    'Por título', 
                    'Por autor', 
                    'Por categoria'
                ]
            ).ask()

            if tipoBusca == 'Por título':
                strategy = buscaPorTitulo()
            elif tipoBusca == 'Por autor':
                strategy = buscaPorAutor()
            elif tipoBusca == 'Por categoria':
                strategy = buscaPorCategoria()
            
            buscaLivro = LivroBusca(strategy)
            resultados = buscaLivro.execute_search(cursor)

            if resultados:
                print('Resultados da busca: ')
                for livro in resultados:
                    print(livro)
            else:
                print('Nenhum livro encontrado!')
        elif acao == 'Sair':
            print("Saindo...")  # Depuração
            sair().execute()
            break

if __name__ == "__main__":
    main()