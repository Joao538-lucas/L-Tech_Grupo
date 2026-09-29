import mysql.connector


class Database:
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="l_tech",
            port=3306,
            use_pure=True
        )