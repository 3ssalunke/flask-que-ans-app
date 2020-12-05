import sqlite3


class DatabaseConnection:
    def __init__(self, host):
        self.connection = None
        self.host = host

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, a, b, c):
        if a or b or c:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
