from ._imports import *
from .errors import EncryptionError

class SecurityManager:
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, filename: str = "SECURITY_KEY.key"):
        with open(filename, "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(filename: str) -> bytes:
        try:
            with open(filename, "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise EncryptionError("Key file not found")

    @staticmethod
    def encrypt(data: dict, key: bytes) -> bytes:
        try:
            f = Fernet(key)
            json_data = json.dumps(data).encode()
            return f.encrypt(json_data)
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> dict:
        try:
            f = Fernet(key)
            json_data = f.decrypt(encrypted_data)
            return json.loads(json_data.decode())
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {str(e)}")