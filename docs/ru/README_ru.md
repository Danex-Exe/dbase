<h1 align="center">Документация</h1>
<div align="center">
    <a href="../README.md">English</a>
    <a href="../ru/README_ru.md">Русский</a>
    <br><br>
</div>

## Установка
```bash
pip install git+https://Danex-Exe/dbase.git
```

## Использование
### .txt (работа с текстом)
```python
from dbase import DataBase # Импорт модуля

db = DataBase('test.txt') # Инициализация базы данных
db.create() # Создание базы данных (Если создана, то игнорируется)

db.write('123') # Записываем данные
data = db.read() # Читаем данные
print(data) # Вывод данных
```

### .txt, .json (работа с json)
```python
from dbase import DataBase # Импорт модуля

db = DataBase('test.txt') # Вызов функции (Вместо .txt можно .json)
db.create() # Создание базы данных (Если создана, то игнорируется)

db.set(data=[
      ('a', '123'),
      ('b', '456')
]) # Запись нескольких переменных за один вызов
db.set(key='a', value='123') # Запись одного элемента
db.set('b', '456') # Запись второго элемента
# есть возможность обьеденить запись нескольких и одного

db.setdefault(data=[], key='', value='') # Работает точно так же, но только если этой переменной(-ых) не существует

db.get(key='a') # Возвращает значение переменной, если ее нет, то None

db.rename(last_key='a', new_key='c') # Переименовывает переменную

db.remove(key='c') # Удаляет переменную

db.delete() # Удаляет базу данных
```


### .dbase (зашифрованная база данных)
```python
from dbase import DataBase # Импорт модуля

db = DataBase('test.dbase') # Вызов функции (Вместо .txt можно .json)
db.create(password="СЕКРЕТНЫЙ_ПАРОЛЬ") # Создание базы данных (Если создана, то игнорируется), пароль хэшируется и хранится в базе данных
db.open(key='SECURITY_KEY.key') # Создает защищенную сессию, благодаря которой можно работать с базой данных. Без этой функции другие работать не будут

# все выше перечисленные функции для JSON, так же относятся к этой базе, но тут они еще автоматически кодируются
# функции .read() и .write() не работают с .dbase
db.delete(password="СЕКРЕТНЫЙ_ПАРОЛЬ") # Проверяет пароль от базы данных, если совпал то удаляет
```

### настройка логов
```python
from dbase import DataBase # Импорт модуля

db = DataBase('test.txt') # Инициализация базы данных

db.logger.title = 'Заголовок логера'
db.logger.log_file = 'Путь до файла с логами'
db.logger.time_format = 'Формат времени'
db.logger.format = 'Формат логов'
db.logger.log_dir = 'Папка с логами'
```
