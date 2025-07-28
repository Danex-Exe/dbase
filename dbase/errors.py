from .logger import Logger

# Настройка логгера для ошибок
error_logger = Logger(title="DBASE-ERROR", log_file="dbase_errors.log")

class DBaseError(Exception):
    """Базовое исключение для всех ошибок библиотеки."""
    def __init__(self, message: str, code: int = 1000):
        self.message = message
        self.code = code
        super().__init__(f"DBASE-{code}: {message}")
        error_logger.error(f"{self.__class__.__name__}: {message} (code: {code})")

# ===== Ошибки операций =====
class OperationError(DBaseError):
    """Ошибки выполнения операций с БД"""
    def __init__(self, message: str, operation: str = None):
        super().__init__(f"Operation failed: {message}", 2000)
        self.operation = operation

class InvalidExtensionError(OperationError):
    """Недопустимое расширение файла"""
    def __init__(self, extension: str, allowed: tuple):
        super().__init__(
            f"Invalid file extension: '{extension}'. Allowed: {', '.join(allowed)}",
            "File Validation"
        )
        self.extension = extension
        self.allowed_extensions = allowed

class KeyNotFoundError(OperationError):
    """Ключ не найден в базе данных"""
    def __init__(self, key: str):
        super().__init__(f"Key '{key}' not found in database", "Data Access")
        self.key = key

class SecurityError(OperationError):
    """Базовые ошибки безопасности"""
    def __init__(self, message: str):
        super().__init__(f"Security violation: {message}", "Security")

class PasswordVerificationError(SecurityError):
    """Ошибка проверки пароля"""
    def __init__(self):
        super().__init__("Password verification failed")

class EncryptionError(SecurityError):
    """Ошибка шифрования/дешифрования"""
    def __init__(self, reason: str):
        super().__init__(f"Encryption/decryption failed: {reason}")

class OperationNotAllowedError(SecurityError):
    """Операция не разрешена в текущем состоянии"""
    def __init__(self, operation: str, reason: str):
        super().__init__(f"Operation '{operation}' not allowed: {reason}")
        self.operation = operation

# ===== Ошибки файловых операций =====
class FileSystemError(DBaseError):
    """Ошибки работы с файловой системой"""
    def __init__(self, message: str, path: str = None):
        super().__init__(f"File system error: {message}", 3000)
        self.path = path

class FileNotFoundError(FileSystemError):
    """Файл не найден"""
    def __init__(self, path: str):
        super().__init__(f"File not found: {path}", path)

class FilePermissionError(FileSystemError):
    """Ошибка прав доступа к файлу"""
    def __init__(self, path: str, operation: str):
        super().__init__(f"Permission denied for {operation} on {path}", path)
        self.operation = operation

class FileCorruptionError(FileSystemError):
    """Файл поврежден или имеет неверный формат"""
    def __init__(self, path: str, reason: str):
        super().__init__(f"File corrupted: {reason}", path)
        self.reason = reason

# ===== Ошибки данных =====
class DataError(DBaseError):
    """Ошибки обработки данных"""
    def __init__(self, message: str, data: any = None):
        super().__init__(f"Data error: {message}", 4000)
        self.data = data

class SerializationError(DataError):
    """Ошибка сериализации/десериализации"""
    def __init__(self, data_type: type, format: str = 'JSON'):
        super().__init__(f"Failed to serialize {data_type} to {format}")
        self.data_type = data_type
        self.format = format

class DataTypeError(DataError):
    """Неподдерживаемый тип данных"""
    def __init__(self, key: str, data_type: type, expected: type):
        super().__init__(
            f"Invalid type for key '{key}': got {data_type}, expected {expected}"
        )
        self.key = key
        self.actual_type = data_type
        self.expected_type = expected

class DataIntegrityError(DataError):
    """Нарушение целостности данных"""
    def __init__(self, message: str, key: str = None):
        super().__init__(f"Data integrity violated: {message}")
        self.key = key

# ===== Ошибки состояния =====
class StateError(DBaseError):
    """Ошибки недопустимого состояния системы"""
    def __init__(self, message: str, current_state: str):
        super().__init__(f"Invalid state: {message}", 5000)
        self.current_state = current_state

class DatabaseNotOpenError(StateError):
    """Попытка выполнить операцию до открытия БД"""
    def __init__(self, operation: str):
        super().__init__(
            f"Operation '{operation}' requires database to be opened first",
            "Closed"
        )
        self.operation = operation

class DatabaseNotCreatedError(StateError):
    """Попытка использовать не созданную БД"""
    def __init__(self, operation: str):
        super().__init__(
            f"Operation '{operation}' requires database to be created first",
            "Not Created"
        )
        self.operation = operation

class TempDatabaseCreatedError(StateError):
    """Попытка создать временную БД"""
    def __init__(self, operation: str):
        super().__init__(
            f"Operation '{operation}' non-temporary database required",
            "Not Created"
        )
        self.operation = operation

# ===== Критические системные ошибки =====
class CriticalSystemError(DBaseError):
    """Критические системные ошибки"""
    def __init__(self, message: str, component: str):
        super().__init__(f"Critical system failure in {component}: {message}", 9000)
        self.component = component
        error_logger.error(f"CRITICAL FAILURE: {component} - {message}")

class DiskFullError(CriticalSystemError):
    """Недостаточно места на диске"""
    def __init__(self, required: int, available: int, path: str):
        super().__init__(
            f"Insufficient disk space (required: {required}, available: {available})",
            "Storage"
        )
        self.required = required
        self.available = available
        self.path = path

class MemoryAllocationError(CriticalSystemError):
    """Ошибка выделения памяти"""
    def __init__(self, operation: str, size: int):
        super().__init__(
            f"Failed to allocate {size} bytes for {operation}",
            "Memory Management"
        )
        self.operation = operation
        self.size = size