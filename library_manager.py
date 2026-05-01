from database import Database


class LibraryManager:
    def __init__(self):
        """Инициализация менеджера библиотеки"""
        self.db = Database()

    def display_menu(self):
        """Отображение меню программы"""
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 50)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Поиск книги")
        print("4. Отметить книгу как прочитанную")
        print("5. Установить рейтинг книге")
        print("6. Удалить книгу")
        print("7. Статистика библиотеки")
        print("8. Выход")
        print("=" * 50)

    def add_book(self):
        """Добавление новой книги"""
        print("\n--- Добавление новой книги ---")
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = input("Введите год издания (необязательно): ")
        genre = input("Введите жанр книги (необязательно): ")

        year = int(year) if year.isdigit() else None
        genre = genre if genre else None

        result = self.db.add_book(title, author, year, genre)
        print(result)

    def display_books(self, books):
        """Отображение списка книг"""
        if not books:
            print("\nКниги не найдены!")
            return

        print("\n" + "-" * 90)
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10} {'Рейтинг':<8}")
        print("-" * 90)

        for book in books:
            book_id, title, author, year, genre, is_read, date_added, rating = book
            status = "✓ Прочитана" if is_read else "✗ Не прочитана"
            # Алгоритм форматирования вывода
            print(f"{book_id:<5} {title[:30]:<30} {author[:20]:<20} "
                  f"{year if year else 'N/A':<6} {status:<10} {rating if rating else 'N/A':<8}")

    def run(self):
        """Основной цикл программы"""
        while True:
            self.display_menu()
            choice = input("\nВыберите действие (1-8): ")

            # Алгоритм обработки выбора пользователя
            if choice == '1':
                self.add_book()

            elif choice == '2':
                books = self.db.get_all_books()
                self.display_books(books)

            elif choice == '3':
                query = input("\nВведите название или автора для поиска: ")
                books = self.db.search_books(query)
                self.display_books(books)

            elif choice == '4':
                try:
                    book_id = int(input("\nВведите ID книги: "))
                    if self.db.update_book_status(book_id, 1):
                        print("✓ Книга отмечена как прочитанная!")
                    else:
                        print("✗ Книга не найдена!")
                except ValueError:
                    print("Ошибка: Введите корректный ID")

            elif choice == '5':
                try:
                    book_id = int(input("\nВведите ID книги: "))
                    rating = int(input("Введите рейтинг (1-10): "))
                    success, message = self.db.set_rating(book_id, rating)
                    print(f"{'✓' if success else '✗'} {message}")
                except ValueError:
                    print("Ошибка: Введите корректные данные")

            elif choice == '6':
                try:
                    book_id = int(input("\nВведите ID книги для удаления: "))
                    if self.db.delete_book(book_id):
                        print("✓ Книга удалена!")
                    else:
                        print("✗ Книга не найдена!")
                except ValueError:
                    print("Ошибка: Введите корректный ID")

            elif choice == '7':
                stats = self.db.get_statistics()
                print("\n--- Статистика библиотеки ---")
                print(f"Всего книг: {stats['total_books']}")
                print(f"Прочитано: {stats['read_books']}")
                print(f"Не прочитано: {stats['unread_books']}")
                print(f"Средний рейтинг: {stats['avg_rating']}")

                if stats['genres']:
                    print("\nКниги по жанрам:")
                    for genre, count in stats['genres']:
                        print(f"  {genre if genre else 'Без жанра'}: {count}")

            elif choice == '8':
                print("\nДо свидания!")
                break

            else:
                print("\nОшибка: Выберите действие от 1 до 8")

            input("\nНажмите Enter для продолжения...")