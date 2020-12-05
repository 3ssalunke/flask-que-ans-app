import sqlite3
import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect('postgres://chmuelxmudoyhe:password@ec2-52-5-176-53.compute-1.amazonaws.com:5432/dfbdt7rekv4jmj')
        return self.connection

    def __exit__(self, a, b, c):
        if a or b or c:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
