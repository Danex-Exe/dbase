# DBase

Лёгкая JSON-based библиотека для хранения данных с интерфейсом, похожим на словарь и атрибуты объекта.

- Простая запись: `db.user = "alice"` или `db["user"] = "alice"`
- Автосохранение в файл JSON
- Контекстный менеджер (`with DataBase(...) as db:`)
- Временные БД (`is_temp=True`)
- Опциональное простое шифрование при сохранении (`encryption_key`)

---

## Содержание

1. [Установка](#установка)
2. [Быстрый старт](#быстрый-старт)
3. [Как работает хранение](#как-работает-хранение)
4. [Шифрование данных](#шифрование-данных)
5. [Основной API](#основной-api)
6. [Практические примеры](#практические-примеры)
7. [Запуск тестов и CI/CD](#запуск-тестов-и-cicd)
8. [Docker и docker-compose](#docker-и-docker-compose)
9. [Ограничения и рекомендации](#ограничения-и-рекомендации)

---

## Установка

### 1) Установка из PyPI

```bash
pip install dbase
```

Проверка, что модуль установлен:

```bash
python -c "from dbase import DataBase; print(DataBase)"
```

### 2) Установка для разработки (из исходников)

```bash
git clone https://github.com/Danex-Exe/dbase.git
cd dbase
python -m pip install -e .[dev]
```

Что это даёт:
- `-e` — editable mode (изменения в коде сразу доступны без переустановки)
- `.[dev]` — устанавливает dev-зависимости (pytest, black, flake8, mypy)

### 3) Установка в виртуальном окружении (рекомендуется)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install --upgrade pip
pip install dbase
```

---

## Быстрый старт

```python
from dbase import DataBase

# Создать или открыть БД
with DataBase(file_path="data.json", show_logs=False) as db:
    db.user = "alice"
    db["score"] = 95

# Повторно открыть и прочитать
with DataBase(file_path="data.json", show_logs=False) as db:
    print(db.user)      # alice
    print(db["score"])  # 95
```

---

## Как работает хранение

- Библиотека хранит публичные ключи/атрибуты в JSON-файле.
- Защищённые служебные поля (внутренние) не сериализуются.
- При каждом изменении значения данные сохраняются в файл.
- Сохранение выполняется атомарно (через временный файл и замену), чтобы уменьшить риск повреждения данных.

---

## Шифрование данных

Можно включить простое шифрование при сохранении:

```python
from dbase import DataBase

db = DataBase(
    file_path="secure.json",
    encryption_key="my-secret-key",
    show_logs=False,
)

db.api_token = "token-123"
db.close()
```

Что важно:
- Шифрование включается **только** если указан `encryption_key`.
- Для чтения зашифрованного файла нужно открыть БД с тем же ключом.
- Текущая схема — lightweight (XOR + Base64): подходит для базовой обфускации, но не для хранения высокочувствительных данных.

---

## Основной API

### Инициализация

```python
DataBase(
    file_path: str | None = None,
    show_logs: bool = True,
    is_temp: bool = False,
    encryption_key: str | None = None,
    auto_cleanup_temp: bool = True,
)
```

### Полезные методы

- `get(key, default=None)` — безопасное чтение с fallback
- `update(**kwargs)` — массовое обновление
- `pop(key, default=None)` — извлечение и удаление
- `clear()` — очистка всех пользовательских ключей
- `items()`, `keys()`, `values()` — как у словаря
- `close()` — явное закрытие файла (и cleanup temp-файла для `is_temp=True`)

### Поддерживаемые операции

- `db.key = value`
- `db["key"] = value`
- `value = db.key`
- `value = db["key"]`
- `"key" in db`
- `len(db)`
- `del db["key"]`

---

## Практические примеры

### 1) Настройки приложения

```python
from dbase import DataBase

cfg = DataBase("config.json", show_logs=False)
cfg.app_name = "my-service"
cfg.debug = True
cfg.port = 8080
cfg.close()
```

### 2) Временное хранилище

```python
from dbase import DataBase

with DataBase(is_temp=True, show_logs=False) as cache:
    cache.session_id = "abc123"
    cache.ttl = 300
```

### 3) Работа как со словарём

```python
from dbase import DataBase

db = DataBase("users.json", show_logs=False)
db["u1"] = {"name": "Alice", "age": 30}
print(db.get("u1"))
print(db.keys())
```

---

## Запуск тестов и CI/CD

Локально:

```bash
python -m pip install -e .[dev]
pytest -q
```

В репозитории настроены GitHub Actions:
- **CI**: запускает тесты для Python 3.8 / 3.11 / 3.12
- **CD**: собирает wheel/sdist по тегам `v*`

---

## Docker и docker-compose

### Docker build + test

```bash
docker build -t dbase:local .
docker run --rm dbase:local
```

### docker-compose

```bash
docker compose up --build
```

Команда запускает тесты проекта в контейнере.

---

## Ограничения и рекомендации

1. Храните только JSON-сериализуемые значения.
2. Для production-секретов используйте полноценную криптографию (а не lightweight-обфускацию).
3. Используйте `with DataBase(...)` или `close()` для корректного завершения работы с файлами.
4. Для больших объёмов/конкурентной записи рассмотрите переход на СУБД.

---

## Лицензия

MIT License. Подробности в файле `LICENSE`.
