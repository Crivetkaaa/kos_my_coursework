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
    
    @classmethod
    def input_file(cls, data):
        for row in data:
            cls.execute(f"""INSERT INTO input_invoice (type_purchase, supplier, postponement, product_name, count, price, from_country, date, number) VALUES ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}');""")

    @classmethod
    def output_file(cls, data):
        for row in data:
            cls.execute(f"INSERT INTO send_product (buyer, product_name, number, count, price, date, receipt) VALUES ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}');")
    