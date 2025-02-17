from base import Action
from Database.Conection import DatabaseConnection
import mysql.connector

class FazerReserva(Action):
    def execute(self):
        db = DatabaseConnection()
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