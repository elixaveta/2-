import os
import pickle
from abc import ABC, abstractmethod

# ========== АБСТРАКЦИЯ ==========
class Storage(ABC):
    @abstractmethod
    def save(self, data): pass
    @abstractmethod
    def load(self): pass

# ========== ИНКАПСУЛЯЦИЯ ==========
class Book:
    def __init__(self, title, author):
        self.__title = title
        self.__author = author
        self.__available = True
    
    def get_title(self): return self.__title
    def get_author(self): return self.__author
    def is_available(self): return self.__available
    def set_available(self, val): self.__available = val

class User:
    def __init__(self, name):
        self.__name = name
        self.__books = []
    
    def get_name(self): return self.__name
    def get_books(self): return self.__books
    def add_book(self, book): self.__books.append(book)
    def remove_book(self, book): self.__books.remove(book)

class Librarian:
    def __init__(self, name): self.__name = name
    def get_name(self): return self.__name

# ========== НАСЛЕДОВАНИЕ ==========
class PickleStorage(Storage):
    def __init__(self, filename):
        self.filename = filename
    
    def save(self, data):
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        return None

# ========== ПОЛИМОРФИЗМ ==========
class Entity(ABC):
    @abstractmethod
    def display(self): pass

class BookEntity(Book, Entity):
    def display(self): return f"{self.get_title()} - {self.get_author()}"

class UserEntity(User, Entity):
    def display(self): return f"{self.get_name()} ({len(self.get_books())} книг)"

# ========== ОСНОВНАЯ СИСТЕМА ==========
class Library:
    def __init__(self):
        # Инициализация хранилищ
        self.book_storage = PickleStorage('books.pkl')
        self.user_storage = PickleStorage('users.pkl')
        self.lib_storage = PickleStorage('librarians.pkl')
        
        # Загрузка данных
        self.books = self.book_storage.load()
        self.users = self.user_storage.load()
        self.libs = self.lib_storage.load()
        
        # Если данные не загрузились, создаём тестовые
        if self.books is None:
            self.books = [BookEntity("Война и мир", "Толстой"), 
                         BookEntity("Преступление и наказание", "Достоевский")]
        if self.users is None:
            self.users = [UserEntity("Иван")]
        if self.libs is None:
            self.libs = [Librarian("Админ")]
    
    def save_all(self):
        """Сохраняет все данные с помощью pickle"""
        self.book_storage.save(self.books)
        self.user_storage.save(self.users)
        self.lib_storage.save(self.libs)
        print("💾 Все данные сохранены в .pkl файлы")
    
    # Библиотекарь
    def add_book(self):
        t = input("Название: "); a = input("Автор: ")
        self.books.append(BookEntity(t, a)); print("✅ Книга добавлена")
    
    def remove_book(self):
        t = input("Название: ")
        for b in self.books:
            if b.get_title().lower() == t.lower():
                if b.is_available():
                    self.books.remove(b); print("✅ Книга удалена")
                else: print("❌ Книга выдана, нельзя удалить")
                return
        print("❌ Книга не найдена")
    
    def reg_user(self):
        n = input("Имя: ")
        if not any(u.get_name().lower() == n.lower() for u in self.users):
            self.users.append(UserEntity(n)); print("✅ Пользователь зарегистрирован")
        else: print("❌ Пользователь уже существует")
    
    def all_users(self):
        print("\n📋 СПИСОК ПОЛЬЗОВАТЕЛЕЙ:")
        for i,u in enumerate(self.users,1): print(f"{i}. {u.display()}")
    
    def all_books(self):
        print("\n📚 ВСЕ КНИГИ:")
        for i,b in enumerate(self.books,1):
            status = "✅" if b.is_available() else "❌"
            print(f"{i}. {b.display()} [{status}]")
    
    # Пользователь
    def avail_books(self):
        avail = [b for b in self.books if b.is_available()]
        print("\n📖 ДОСТУПНЫЕ КНИГИ:")
        for i,b in enumerate(avail,1): print(f"{i}. {b.display()}")
    
    def borrow(self, user):
        t = input("Название книги: ")
        for b in self.books:
            if b.get_title().lower() == t.lower() and b.is_available():
                b.set_available(False)
                user.add_book(b)
                print("✅ Книга взята"); return
        print("❌ Книга недоступна или не найдена")
    
    def ret(self, user):
        t = input("Название книги: ")
        for b in user.get_books():
            if b.get_title().lower() == t.lower():
                b.set_available(True)
                user.remove_book(b)
                print("✅ Книга возвращена"); return
        print("❌ У вас нет такой книги")
    
    def my_books(self, user):
        print(f"\n📚 КНИГИ {user.get_name()}:")
        for i,b in enumerate(user.get_books(),1): print(f"{i}. {b.display()}")
    
    # Меню
    def menu_lib(self, lib):
        while True:
            print(f"\n=== 👤 БИБЛИОТЕКАРЬ {lib.get_name()} ===")
            print("1.➕ Добавить книгу")
            print("2.➖ Удалить книгу")
            print("3.👥 Зарегистрировать пользователя")
            print("4.📋 Все пользователи")
            print("5.📚 Все книги")
            print("0.🔙 Назад")
            c = input("Выбор: ")
            if c=='1': self.add_book()
            elif c=='2': self.remove_book()
            elif c=='3': self.reg_user()
            elif c=='4': self.all_users()
            elif c=='5': self.all_books()
            elif c=='0': break
    
    def menu_user(self, user):
        while True:
            print(f"\n=== 👤 ПОЛЬЗОВАТЕЛЬ {user.get_name()} ===")
            print("1.📖 Доступные книги")
            print("2.📥 Взять книгу")
            print("3.📤 Вернуть книгу")
            print("4.📚 Мои книги")
            print("0.🔙 Назад")
            c = input("Выбор: ")
            if c=='1': self.avail_books()
            elif c=='2': self.borrow(user)
            elif c=='3': self.ret(user)
            elif c=='4': self.my_books(user)
            elif c=='0': break
    
    def start(self):
        print("📚 ДОБРО ПОЖАЛОВАТЬ В БИБЛИОТЕЧНУЮ СИСТЕМУ")
        print(f"Загружено: {len(self.books)} книг, {len(self.users)} пользователей")
        
        while True:
            print("\n=== ГЛАВНОЕ МЕНЮ ===")
            print("1.👤 Войти как библиотекарь")
            print("2.👥 Войти как пользователь")
            print("3.💾 Сохранить данные")
            print("0.🚪 Выход")
            c = input("Выбор: ")
            
            if c=='1':
                print("\nДоступные библиотекари:")
                for i,l in enumerate(self.libs,1): print(f"{i}. {l.get_name()}")
                print(f"{len(self.libs)+1}. ➕ Новый библиотекарь")
                n = input("Выберите номер или введите имя: ")
                
                if n.isdigit() and 1 <= int(n) <= len(self.libs):
                    self.menu_lib(self.libs[int(n)-1])
                elif n.isdigit() and int(n) == len(self.libs)+1:
                    name = input("Имя нового библиотекаря: ")
                    self.libs.append(Librarian(name))
                    self.menu_lib(self.libs[-1])
                else:
                    self.libs.append(Librarian(n))
                    self.menu_lib(self.libs[-1])
            
            elif c=='2':
                if not self.users: 
                    print("❌ Нет пользователей. Сначала зарегистрируйтесь у библиотекаря.")
                    continue
                
                print("\nДоступные пользователи:")
                for i,u in enumerate(self.users,1): print(f"{i}. {u.get_name()}")
                n = input("Выберите номер: ")
                
                if n.isdigit() and 1 <= int(n) <= len(self.users):
                    self.menu_user(self.users[int(n)-1])
                else:
                    print("❌ Неверный выбор")
            
            elif c=='3':
                self.save_all()
            
            elif c=='0':
                self.save_all()
                print("👋 До свидания!")
                break

if __name__ == "__main__":
    Library().start()