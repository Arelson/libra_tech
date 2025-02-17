from Actions.base import Action
import Database.Conection as cnt
import questionary
import mysql.connector

class RegisterBook(Action):
    def execute(self):
        db = cnt.DatabaseConnection()
        cursor = db.get_cursor()
        if cursor is None:
            print("Erro ao obter o cursor.")
            return

        book_name = input("Qual o nome do livro: ")
        category = questionary.select(
            "Qual a categoria do livro?",
            choices=['Esportes', 'Ficção', 'Educação', 'Fantasia', 'Diversa']
        ).ask()
        author = input("Qual o nome do autor?: ")

        try:
            cursor.execute(
                'INSERT INTO books (name, category, author) VALUES (%s, %s, %s)',
                (book_name, category, author)
            )
            db.commit()
            print("✅ Livro cadastrado com sucesso!")
        except mysql.connector.Error as err:
            print(f"❌ ERRO ao cadastrar: {err}")