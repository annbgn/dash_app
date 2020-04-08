import mysql.connector

DB_HOST = "localhost"
DB_NAME = "dashdb"
DB_USER = "*****"
DB_PASSWORD = "*****"


class ConnectionManager:
    def __init__(self):
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD
        self.conn = None
        self.cursor = None

    def __enter__(self):
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME,
            auth_plugin="mysql_native_password",
        )
        self.conn = conn
        self.cursor = self.conn.cursor(buffered=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()
