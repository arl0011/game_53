import sqlite3


def create_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
        return None


def create_products_table(connection):
    sql = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_title VARCHAR(200) NOT NULL,
        price REAL NOT NULL DEFAULT 0.0,
        quantity INTEGER NOT NULL DEFAULT 0
    )
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insert_products(connection):
    sql = '''INSERT INTO products (product_title, price, quantity)
             VALUES (?, ?, ?)'''
    products = [
        ("Мыло детское", 45.0, 20),
        ("Зубная паста", 120.5, 15),
        ("Шампунь", 230.0, 10),
        ("Гель для душа", 190.0, 12),
        ("Салфетки влажные", 55.5, 25),
        ("Туалетная бумага", 30.0, 50),
        ("Мыло жидкое", 60.0, 18),
        ("Порошок стиральный", 300.0, 8),
        ("Освежитель воздуха", 150.0, 6),
        ("Губки для мытья", 25.0, 40),
        ("Пакеты для мусора", 70.0, 30),
        ("Средство для мытья посуды", 110.0, 14),
        ("Щётка для обуви", 90.0, 9),
        ("Чистящее средство", 160.0, 7),
        ("Пена для бритья", 200.0, 11)
    ]
    try:
        cursor = connection.cursor()
        cursor.executemany(sql, products)
        connection.commit()
        print("✅ 15 товаров добавлены.")
    except sqlite3.Error as e:
        print(e)


def update_quantity_by_id(connection, product_id, new_quantity):
    sql = '''UPDATE products SET quantity = ? WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_quantity, product_id))
        connection.commit()
        print(f"🔄 Количество товара с ID={product_id} обновлено.")
    except sqlite3.Error as e:
        print(e)


def update_price_by_id(connection, product_id, new_price):
    sql = '''UPDATE products SET price = ? WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_price, product_id))
        connection.commit()
        print(f"💰 Цена товара с ID={product_id} обновлена.")
    except sqlite3.Error as e:
        print(e)


def delete_product_by_id(connection, product_id):
    sql = '''DELETE FROM products WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (product_id,))
        connection.commit()
        print(f"🗑️ Товар с ID={product_id} удалён.")
    except sqlite3.Error as e:
        print(e)


def select_all_products(connection):
    sql = '''SELECT * FROM products'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("\n📦 Все товары:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)


def filter_products_by_price_and_quantity(connection, price_limit, min_quantity):
    sql = '''SELECT * FROM products WHERE price < ? AND quantity > ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (price_limit, min_quantity))
        rows = cursor.fetchall()
        print(f"\n🔍 Товары с ценой < {price_limit} и количеством > {min_quantity}:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)


def search_products_by_name(connection, search_term):
    sql = '''SELECT * FROM products WHERE product_title LIKE ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (f"%{search_term}%",))
        rows = cursor.fetchall()
        print(f"\n🔎 Поиск по названию ('{search_term}'):")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)



database_name = 'products.db'
conn = create_connection(database_name)

if conn:
    print("✅ Подключение к базе данных установлено.")
    create_products_table(conn)
    insert_products(conn)


    update_price_by_id(conn, 1, 99.99)
    update_quantity_by_id(conn, 2, 50)


    delete_product_by_id(conn, 3)


    select_all_products(conn)


    filter_products_by_price_and_quantity(conn, 100, 10)


    search_products_by_name(conn, "мыло")

    conn.close()
    print("\n✅ Работа завершена.")