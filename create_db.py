import sqlite3
def create_table():
    conn = sqlite3.connect('bot_db.sqlite')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS input_invoice (
    type_purchase TEXT,
    supplier TEXT,
    postponement TEXT,
    product_name TEXT,
    count INT,
    price INT,
    from_country TEXT,
    date_input TEXT,
    date_guarantee TEXT,
    receipt TEXT,
    number TEXT UNIQUE ON CONFLICT IGNORE
    );""")

    cur.execute("""CREATE TABLE send_product (
    buyer TEXT,
    product_name TEXT,
    count INT,
    price INT,
    date_output TEXT,
    data_guarantee TEXT,
    receipt TEXT,
    receipt_check TEXT,
    number TEXT UNIQUE ON CONFLICT IGNORE
    );""")
    print('Таблицы успешно созданы!')
    conn.commit()
    cur.close()
    conn.close()
if __name__ == '__main__':
    create_table()