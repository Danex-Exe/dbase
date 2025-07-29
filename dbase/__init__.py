from ._imports import *
from .logger import Logger
from .errors import *
from .security import SecurityManager

__version__ = "2.0.5"
__all__ = ['DataBase']

class DataBase:
    ALLOWED_EXTENSIONS = ('.txt', '.json', '.dbase')

    def __init__(self, name: str, show_logs: bool = True) -> None:
        self.name = name
        self.show_logs = show_logs
        self.logger = Logger(title="DBASE", log_file="dbase.log")
        self._data: Union[str, Dict] = {}
        self._encryption_key: Optional[bytes] = None
        self._requires_password = False
        self._password_hash: Optional[str] = None
        self._opened = False

        _, ext = os.path.splitext(name)
        if ext not in self.ALLOWED_EXTENSIONS:
            if name != ":temp:":
                raise InvalidExtensionError("ext", self.ALLOWED_EXTENSIONS)

        self._extension = ext
        self.is_encrypted = ext == '.dbase'
        self.is_temp = name == ":temp:"

        if not self.is_temp:
            self.file_exists = os.path.exists(name)
            self.log(str(self.file_exists))
            if not self.is_encrypted and self.file_exists:
                with open(self.name, "r") as f:
                    self._data = json.load(f)
        else:
            self.file_exists = False

    def create(self, password: Optional[str] = None) -> None:
        if self.name == ":temp:":
            raise TempDatabaseCreatedError('create')

        if self.file_exists:
            self.log("Database already exists")

        if self.is_encrypted:
            if not password:
                raise ValueError("Password is required for encrypted databases")

            self._encryption_key = SecurityManager.generate_key()
            SecurityManager.save_key(self._encryption_key)
            self._password_hash = self.hash(password)
            self._requires_password = True
            self._data = {"$password": self._password_hash}
            self._save_data()
            self.log(f"Created encrypted database: {self.name}")
        else:
            with open(self.name, "w") as f:
                json.dump({} if self._extension == '.json' else '', f)
            self.log(f"Created database: {self.name}")

        self.file_exists = True

    def open(self, key_file: str = "SECURITY_KEY.key") -> None:
        if not self.is_encrypted:
            raise OperationNotAllowedError("open", "Only encrypted databases require opening")

        try:
            self._encryption_key = SecurityManager.load_key(key_file)
            with open(self.name, "rb") as f:
                encrypted_data = f.read()
            self._data = SecurityManager.decrypt(encrypted_data, self._encryption_key)
            self._opened = True
            self.log(f"Database opened: {self.name}")
        except Exception as e:
            raise SecurityError(f"Failed to open database: {str(e)}")

    def set(self, data: list = None, key: Optional[str] = None, value: Any = None) -> None:
        self._check_access()

        if data:
            for i in data:
                k, v = i
                self._set_single(k, v)
        elif key is not None:
            self._set_single(key, value)

        if self.is_encrypted:
            self._save_data()

    def _set_single(self, key: str, value: Any) -> None:
        if isinstance(value, str) and value.startswith("#"):
            value = self.hash(value[1:])
        self._data[key] = value
        self.log(f"Set key: {key}")

    def setdefault(self, data: list = None,  key: str = None, value: Any = None) -> None:
        self._check_access()

        if data:
            for i in data:
                k, v = i
                if k not in self._data:
                    self.set(key=k, value=v)

        if key is None:
            if data is not None: return
            raise DataError("setdefault", "There must be a key")

        if key not in self._data:
            self.set(key=key, value=value)

        if self.is_encrypted:
            self._save_data()

    def get(self, key: str, default_response: Any = None) -> Any:
        self._check_access()
        return self._data.get(key, default_response)

    def rename(self, last_key: str, new_key: str) -> None:
        self._check_access()

        if last_key not in self._data:
            raise KeyNotFoundError(f"Key not found: {last_key}")

        self._data[new_key] = self._data.pop(last_key)
        self.log(f"Renamed key: {last_key} -> {new_key}")

        if self.is_encrypted:
            self._save_data()

    def remove(self, key: str) -> None:
        self._check_access()
        if key not in self._data:
            raise KeyNotFoundError(f"Key not found: {key}")

        del self._data[key]
        self.log(f"Removed key: {key}")

        if self.is_encrypted:
            self._save_data()

    def delete(self, password: str = None) -> None:
        if self.is_encrypted:
            if not password:
                raise ValueError("Password is required for encrypted databases")

            if not self._verify_password(password):
                raise PasswordVerificationError()

        if not self.is_temp:
            os.remove(self.name)
            self.log(f"Deleted database: {self.name}")
            if self.is_encrypted and self._encryption_key:
                os.remove("SECURITY_KEY.key")
                self.log("Deleted security key")

        self._data = {}
        self.file_exists = False

    def read(self) -> Union[str, Dict]:
        if self.is_encrypted:
            raise OperationNotAllowedError("read", "Cannot read encrypted databases directly")

        if self.is_temp:
            return self._data

        with open(self.name, "r") as f:
            self._data = json.load(f)
            return self._data

    def write(self, data: Union[str, Dict]):
        if self.is_encrypted:
            raise OperationNotAllowedError("write", "Cannot write encrypted databases directly")

        self._data = data

        if self.is_temp:
            return

        with open(self.name, "w") as f:
            if isinstance(data, str):
                f.write(data)
            else:
                json.dump(data, f)
        self.log("Data written to file")

    @staticmethod
    def hash(value: str) -> str:
        # Простая хеш-функция для демонстрации
        import hashlib
        return hashlib.sha256(value.encode()).hexdigest()

    def _save_data(self) -> None:
        if not self.is_temp:
            if self.is_encrypted:
                encrypted_data = SecurityManager.encrypt(self._data, self._encryption_key)
                with open(self.name, "wb") as f:
                    f.write(encrypted_data)
            else:
                self.write('')

    def _verify_password(self, password: str) -> bool:
        return self._password_hash or self.get('$password') == self.hash(password)

    def _check_access(self) -> None:
        if self.is_encrypted and not self._opened:
            raise OperationNotAllowedError('check_access', "Database not opened")
        if not self.file_exists and not self.is_temp:
            raise OperationNotAllowedError("check_access", "Database not created")

    def log(self, message: str) -> None:
        if self.show_logs:
            self.logger.info(message)
