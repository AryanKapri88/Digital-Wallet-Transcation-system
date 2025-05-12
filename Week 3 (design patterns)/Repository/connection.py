import sqlite3                      #singleton

class ConnectionManager:
    _instance = None

    @staticmethod
    def get_instance(db_name='payment.db'):
        if ConnectionManager._instance is None:
            ConnectionManager._instance = ConnectionManager(db_name)
        return ConnectionManager._instance

    def __init__(self, db_name):
        if ConnectionManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
        self.conn = sqlite3.connect(f'repository/{db_name}')
        self.cursor = self.conn.cursor()

    def get_connection(self):
        return self.conn, self.cursor

    def close(self):
        self.conn.close()