from .connection import ConnectionManager

class PinOperations:
    def __init__(self, conn_mgr: ConnectionManager):
        self.conn, self.cursor = conn_mgr.get_connection()

    def save_pin(self, username, pin):
        self.cursor.execute("INSERT OR REPLACE INTO pins (username, pin) VALUES (?, ?)", (username, pin))
        self.conn.commit()

    def get_pin(self, username):
        self.cursor.execute("SELECT pin FROM pins WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None