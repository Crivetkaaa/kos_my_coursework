import sqlite3

class DB:
    @classmethod
    def execute_res(cls, text):
        conn, cur = cls.open_conn()
        rows = cur.execute(text)
        data = []
        for row in rows:
            data.append(row)

        cls.close_conn(conn, cur)
        return data
    
    @classmethod
    def execute(cls, text):
        conn, cur = cls.open_conn()
        cur.execute(text)
        cls.close_conn(conn, cur)
    
    @staticmethod
    def close_conn(conn, cur):
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod
    def open_conn():
        conn = sqlite3.connect('bot_db.sqlite')
        cur = conn.cursor()
        return conn, cur