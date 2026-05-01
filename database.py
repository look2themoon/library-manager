import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="library.db"):
        """Инициализация подключения к базе данных"""
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Создание таблиц в базе данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Создаем таблицу книг
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                is_read BOOLEAN DEFAULT 0,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating INTEGER DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def add_book(self, title, author, year=None, genre=None):
        """Добавление новой книги в базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Алгоритм проверки данных
        if not title or not author:
            return "Ошибка: Название и автор обязательны"

        cursor.execute('''
            INSERT INTO books (title, author, year, genre)
            VALUES (?, ?, ?, ?)
        ''', (title, author, year, genre))

        conn.commit()
        book_id = cursor.lastrowid
        conn.close()

        return f"Книга успешно добавлена с ID: {book_id}"

    def get_all_books(self):
        """Получение всех книг из базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books ORDER BY date_added DESC')
        books = cursor.fetchall()

        conn.close()
        return books

    def search_books(self, query):
        """Поиск книг по названию или автору"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Алгоритм поиска с LIKE
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
        ''', (f'%{query}%', f'%{query}%'))

        books = cursor.fetchall()
        conn.close()
        return books

    def update_book_status(self, book_id, is_read):
        """Обновление статуса прочтения книги"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE books 
            SET is_read = ? 
            WHERE id = ?
        ''', (is_read, book_id))

        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        return affected_rows > 0

    def set_rating(self, book_id, rating):
        """Установка рейтинга книги (алгоритм валидации)"""
        # Алгоритм проверки корректности рейтинга
        if not 1 <= rating <= 10:
            return False, "Рейтинг должен быть от 1 до 10"

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE books 
            SET rating = ? 
            WHERE id = ?
        ''', (rating, book_id))

        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        return affected_rows > 0, "Рейтинг обновлен"

    def delete_book(self, book_id):
        """Удаление книги из базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))

        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        return affected_rows > 0

    def get_statistics(self):
        """Получение статистики по библиотеке (алгоритм агрегации данных)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Алгоритм подсчета статистики
        cursor.execute('SELECT COUNT(*) FROM books')
        total_books = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM books WHERE is_read = 1')
        read_books = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(rating) FROM books WHERE rating > 0')
        avg_rating = cursor.fetchone()[0]

        cursor.execute('''
            SELECT genre, COUNT(*) as count 
            FROM books 
            GROUP BY genre 
            ORDER BY count DESC
        ''')
        genres = cursor.fetchall()

        conn.close()

        return {
            'total_books': total_books,
            'read_books': read_books,
            'unread_books': total_books - read_books,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'genres': genres
        }