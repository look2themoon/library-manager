from library_manager import LibraryManager

def main():
    """Главная функция программы"""
    print("Запуск системы управления библиотекой...")
    app = LibraryManager()
    app.run()

if __name__ == "__main__":
    main()