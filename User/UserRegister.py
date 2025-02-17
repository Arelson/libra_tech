import Database.Conection as cnt
from Actions.base import Action
import mysql.connector

class RegisterUser(Action):
    def execute(self):
        db = cnt.DatabaseConnection()
        cursor = db.get_cursor()
        if cursor is None:
            print("Erro ao obter o cursor.")
            return

        user_name = input("Digite seu nome: ")
        user_email = input("Digite seu email: ")
        user_phone = input("Digite seu telefone: ")

        try:
            cursor.execute(
                'INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)',
                (user_name, user_email, user_phone)
            )
            db.commit()
            print("✅ Usuário cadastrado com sucesso!")
        except mysql.connector.Error as err:
            print(f"❌ ERRO ao cadastrar usuário: {err}")
