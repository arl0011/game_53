import sqlite3


def create_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
        return None


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area REAL DEFAULT 0.0,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        );
    ''')

    conn.commit()


def insert_data(conn):
    cursor = conn.cursor()

    countries = [("Кыргызстан",), ("Германия",), ("Китай",)]
    cursor.executemany("INSERT INTO countries (title) VALUES (?)", countries)

    cities = [
        ("Бишкек", 127.0, 1),
        ("Ош", 182.0, 1),
        ("Берлин", 891.8, 2),
        ("Мюнхен", 310.7, 2),
        ("Пекин", 16410.54, 3),
        ("Шанхай", 6340.5, 3),
        ("Гуанчжоу", 7434.4, 3),
    ]
    cursor.executemany("INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)", cities)

    students = [
        ("Айжан", "Асанова", 1),
        ("Нурлан", "Иманкулов", 2),
        ("Алмаз", "Токтогулов", 3),
        ("Саада", "Шерматова", 3),
        ("Гульнара", "Джумаева", 4),
        ("Аман", "Токобаев", 1),
        ("Элнура", "Карагулова", 5),
        ("Динара", "Сариев", 6),
        ("Эльдар", "Бекешов", 6),
        ("Айбек", "Курманбеков", 2),
        ("Эмиль", "Ниязов", 1),
        ("Анара", "Турганбаева", 4),
        ("Саида", "Чотбаев", 7),
        ("Мария", "Кунце", 3),
        ("Жанара", "Дуйшеева", 5)
    ]
    cursor.executemany("INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)", students)

    conn.commit()
    print("✅ Данные добавлены.")


def list_cities(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM cities")
    return cursor.fetchall()


def show_students_by_city_id(conn, city_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.first_name, s.last_name, c.title AS city, c.area, ct.title AS country
        FROM students s
        JOIN cities c ON s.city_id = c.id
        JOIN countries ct ON c.country_id = ct.id
        WHERE s.city_id = ?
    ''', (city_id,))
    students = cursor.fetchall()

    if students:
        print("\n📋 Ученики в выбранном городе:")
        for s in students:
            print(f"{s[0]} {s[1]} — {s[4]}, {s[2]} (площадь: {s[3]} км²)")
    else:
        print("❌ В этом городе нет учеников.")


def main():
    conn = create_connection("students.db")

    if conn:
        create_tables(conn)

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM countries")
        if cursor.fetchone()[0] == 0:
            insert_data(conn)

        while True:
            print("\nВы можете отобразить список учеников по выбранному ID города из перечня ниже.")
            print("Для выхода из программы введите 0:\n")

            cities = list_cities(conn)
            for city in cities:
                print(f"{city[0]}. {city[1]}")

            try:
                user_input = int(input("\nВведите ID города: "))
                if user_input == 0:
                    print("👋 До свидания!")
                    break
                show_students_by_city_id(conn, user_input)
            except ValueError:
                print("⚠️ Введите корректный ID (число).")

        conn.close()


if __name__ == "__main__":
    main()