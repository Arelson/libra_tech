import mysql.connector

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._instance.connection = mysql.connector.connect(
                    host="127.0.0.1",
                    user="user",
                    password="user123",
                    database="mysqlDatabase",
                    port=3307
                )
                cls._instance.cursor = cls._instance.connection.cursor()
                print("Conexão com o banco de dados estabelecida.")
            except mysql.connector.Error as err:
                print(f"Erro ao conectar ao banco de dados: {err}")
                return None
        return cls._instance

    def get_cursor(self):
        return self._instance.cursor if self._instance else None

    def commit(self):
        if self._instance:
            self._instance.connection.commit()

    def close(self):
        if self._instance:
            if self._instance.cursor:
                self._instance.cursor.close()
            self._instance.connection.close()
            print("Conexão com o banco de dados fechada.")