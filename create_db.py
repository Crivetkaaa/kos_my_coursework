from utils.database import DB

def create_table():
    DB.execute("""CREATE TABLE IF NOT EXISTS input_invoice (
    type_purchase TEXT,
    supplier      TEXT,
    postponement  TEXT,
    product_name  TEXT,
    count         INT,
    price         INT,
    from_country  TEXT,
    date          TEXT,
    number        TEXT UNIQUE ON CONFLICT IGNORE
    );""")

    DB.execute("""CREATE TABLE IF NOT EXISTS send_product (
    buyer        TEXT,
    product_name TEXT,
    number       TEXT UNIQUE ON CONFLICT IGNORE,
    count        INT,
    price        INT,
    date         TEXT,
    receipt INT
);""")
    print('Таблицы успешно созданы!')

if __name__ == '__main__':
    create_table()