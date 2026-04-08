import pickle
import os
from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name):  # ✅ исправлено: init -> __init__
        self._name = name

    def get_name(self):
        return self._name

    @abstractmethod
    def show_info(self):
        pass


class Book:
    def __init__(self, title, author, available=True):  # ✅ исправлено: init -> __init__
        self.__title = title
        self.__author = author
        self.__available = available

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def is_available(self):
        return self.__available

    def set_available(self, status):
        self.__available = status

    def show_info(self):
        status = "доступна" if self.__available else "выдана"
        return f"{self.__title} - {self.__author} ({status})"  # ✅ исправлено: self.title -> self.__title


class User(Person):
    def __init__(self, name):  # ✅ исправлено: init -> __init__
        super().__init__(name)
        self.__books = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, book):
        if book in self.__books:
            self.__books.remove(book)

    def get_books(self):
        return self.__books

    def show_info(self):
        return f"Пользователь: {self.get_name()}, книг на руках: {len(self.__books)}"


class Librarian(Person):
    def __init__(self, name):  # ✅ исправлено: init -> __init__
        super().__init__(name)

    def show_info(self):
        return f"Библиотекарь: {self.get_name()}"


class Library:
    def __init__(self):
        self._books = []        # ✅ исправлено: __books -> _books (одно подчеркивание)
        self._users = []        # ✅ исправлено: __users -> _users
        self._librarians = []   # ✅ исправлено: __librarians -> _librarians
        self.load_data()

    def save_data(self):
        data = {
            "books": self._books,      # ✅ исправлено: _books (было __books)
            "users": self._users,      # ✅ исправлено: _users
            "librarians": self._librarians  # ✅ исправлено: _librarians
        }
        with open("library_data.pkl", "wb") as file:
            pickle.dump(data, file)
        print("Данные сохранены")

    def load_data(self):
        if os.path.exists("library_data.pkl"):
            with open("library_data.pkl", "rb") as file:
                data = pickle.load(file)
                self._books = data.get("books", [])        # ✅ исправлено
                self._users = data.get("users", [])        # ✅ исправлено
                self._librarians = data.get("librarians", [])  # ✅ исправлено
        else:
            self._books = []      # ✅ исправлено
            self._users = []      # ✅ исправлено
            self._librarians = [] # ✅ исправлено

    def add_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора: ")
        book = Book(title, author)
        self._books.append(book)
        print("Книга добавлена")

    def remove_book(self):
        title = input("Введите название книги для удаления: ")
        for book in self._books:
            if book.get_title().lower() == title.lower():
                self._books.remove(book)
                print("Книга удалена")
                return
        print("Книга не найдена")

    def register_user(self):
        name = input("Введите имя пользователя: ")
        user = User(name)
        self._users.append(user)
        print("Пользователь зарегистрирован")

    def show_all_users(self):
        if not self._users:
            print("Пользователей нет")
            return
        for i, user in enumerate(self._users, 1):
            print(f"{i}. {user.show_info()}")

    def show_all_books(self):
        if not self._books:
            print("Книг нет")
            return
        for i, book in enumerate(self._books, 1):
            print(f"{i}. {book.show_info()}")

    def show_available_books(self):
        available_books = [book for book in self._books if book.is_available()]
        if not available_books:
            print("Доступных книг нет")
            return
        for i, book in enumerate(available_books, 1):
            print(f"{i}. {book.show_info()}")

    def borrow_book(self, user):
        title = input("Введите название книги: ")
        for book in self._books:
            if book.get_title().lower() == title.lower():
                if book.is_available():
                    book.set_available(False)
                    user.add_book(book)
                    print("Книга выдана")
                    return
                else:
                    print("Книга уже выдана")
                    return
        print("Книга не найдена")

    def return_book(self, user):
        title = input("Введите название книги: ")
        for book in user.get_books():
            if book.get_title().lower() == title.lower():
                book.set_available(True)
                user.remove_book(book)
                print("Книга возвращена")
                return
        print("У вас нет этой книги")

    def show_user_books(self, user):
        books = user.get_books()
        if not books:
            print("У вас нет книг")
            return
        for i, book in enumerate(books, 1):
            print(f"{i}. {book.show_info()}")

    def librarian_menu(self, librarian):
        while True:
            print("\nМеню библиотекаря")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Зарегистрировать пользователя")
            print("4. Показать всех пользователей")
            print("5. Показать все книги")
            print("0. Назад")
            choice = input("Выберите пункт: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.register_user()
            elif choice == "4":
                self.show_all_users()
            elif choice == "5":
                self.show_all_books()
            elif choice == "0":
                break
            else:
                print("Неверный выбор")

    def user_menu(self, user):
        while True:
            print("\nМеню пользователя")
            print("1. Показать доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("0. Назад")
            choice = input("Выберите пункт: ")

            if choice == "1":
                self.show_available_books()
            elif choice == "2":
                self.borrow_book(user)
            elif choice == "3":
                self.return_book(user)
            elif choice == "4":
                self.show_user_books(user)
            elif choice == "0":
                break
            else:
                print("Неверный выбор")

    def login_librarian(self):
        if not self._librarians:
            print("Библиотекарей пока нет")
            name = input("Введите имя нового библиотекаря: ")
            librarian = Librarian(name)
            self._librarians.append(librarian)
            self.librarian_menu(librarian)
            return

        print("Список библиотекарей:")
        for i, librarian in enumerate(self._librarians, 1):
            print(f"{i}. {librarian.get_name()}")
        print(f"{len(self._librarians) + 1}. Новый библиотекарь")

        choice = input("Выберите номер: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(self._librarians):
                self.librarian_menu(self._librarians[choice - 1])
            elif choice == len(self._librarians) + 1:
                name = input("Введите имя нового библиотекаря: ")
                librarian = Librarian(name)
                self._librarians.append(librarian)
                self.librarian_menu(librarian)
            else:
                print("Неверный выбор")
        else:
            print("Неверный выбор")

    def login_user(self):
        if not self._users:
            print("Пользователей нет. Сначала зарегистрируйтесь у библиотекаря")
            return

        print("Список пользователей:")
        for i, user in enumerate(self._users, 1):
            print(f"{i}. {user.get_name()}")
        
        choice = input("Выберите номер: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(self._users):
                self.user_menu(self._users[choice - 1])
            else:
                print("Неверный выбор")
        else:
            print("Неверный выбор")

    def start(self):
        while True:
            print("\nГлавное меню")
            print("1. Войти как библиотекарь")
            print("2. Войти как пользователь")
            print("3. Сохранить данные")
            print("0. Выход")

            choice = input("Выберите пункт: ")

            if choice == "1":
                self.login_librarian()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                self.save_data()
            elif choice == "0":
                self.save_data()
                print("Программа завершена")
                break
            else:
                print("Неверный выбор")


if __name__ == "__main__":
    library = Library()
    library.start()
