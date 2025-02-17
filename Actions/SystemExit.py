from Database.Conection import DatabaseConnection
from Actions.base import Action

class ExitSystem(Action):
    def execute(self):
        db = DatabaseConnection()
        db.close()
        print("👋 Saindo...")
        exit()