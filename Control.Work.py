import sqlite3


def initialize_database():
    conn = sqlite3.connect('store_database.db')
    cursor = conn.cursor()


    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS stores")


    cursor.execute("""
    CREATE TABLE categories (
        code VARCHAR(2) PRIMARY KEY,
        title VARCHAR(150)
    )""")

    cursor.execute("""
    CREATE TABLE stores (
        store_id INTEGER PRIMARY KEY,
        title VARCHAR(100)
    )""")

    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        title VARCHAR(250),
        category_code VARCHAR(2),
        unit_price FLOAT,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY (category_code) REFERENCES categories(code),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    )""")


    cursor.executemany("INSERT INTO categories (code, title) VALUES (?, ?)", [
        ('FD', 'Food products'),
        ('EL', 'Electronics'),
        ('CL', 'Clothes')
    ])


    cursor.executemany("INSERT INTO stores (store_id, title) VALUES (?, ?)", [
        (1, 'Asia'),
        (2, 'Globus'),
        (3, 'Spar')
    ])


    cursor.executemany("INSERT INTO products (id, title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?, ?)", [
        (1, 'Chocolate', 'FD', 10.5, 129, 1),
        (2, 'Jeans', 'CL', 120.0, 55, 2),
        (3, 'T-Shirt', 'CL', 0.0, 15, 1),
        (4, 'Smartphone', 'EL', 599.99, 10, 3)
    ])

    conn.commit()
    conn.close()


def connect_db():
    return sqlite3.connect('store_database.db')


def get_stores(cursor):
    cursor.execute("SELECT store_id, title FROM stores")
    return cursor.fetchall()


def get_products_by_store(cursor, store_id):
    query = """
    SELECT p.title, c.title, p.unit_price, p.stock_quantity
    FROM products p
    JOIN categories c ON p.category_code = c.code
    WHERE p.store_id = ?
    """
    cursor.execute(query, (store_id,))
    return cursor.fetchall()


def main():
    initialize_database()
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\nВы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:\n")
        stores = get_stores(cursor)
        for store in stores:
            print(f"{store[0]}. {store[1]}")

        try:
            user_input = int(input("\nВведите id магазина: "))
        except ValueError:
            print("Пожалуйста, введите корректное число.")
            continue

        if user_input == 0:
            print("Выход из программы.")
            break

        store_ids = [store[0] for store in stores]
        if user_input not in store_ids:
            print("Магазин с таким id не найден.")
            continue

        products = get_products_by_store(cursor, user_input)
        if not products:
            print("В выбранном магазине нет товаров.")
        else:
            for product in products:
                print(f"\nНазвание продукта: {product[0]}")
                print(f"Категория: {product[1]}")
                print(f"Цена: {product[2]}")
                print(f"Количество на складе: {product[3]}")

    conn.close()

if __name__ == "__main__":
    main()