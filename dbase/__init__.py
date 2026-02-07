import base64
import json
import os
from tempfile import NamedTemporaryFile
from typing import Any

from .logger import Logger
from .messages import get_message


__all__ = ['DataBase', 'Logger']
__version__ = '3.1.0'


class DataBase:
    __all__ = ['create', 'check_file_exists']
    _BAN_NAMES = (
        '_file_path',
        '_show_logs',
        '_is_temp',
        '_file',
        '_encryption_key',
        '_auto_cleanup_temp',
        'logger',
    )
    _ENCRYPTION_MARKER = '__dbase_encrypted__'

    def __init__(
        self,
        file_path: str = None,
        show_logs: bool = True,
        is_temp: bool = False,
        encryption_key: str = None,
        auto_cleanup_temp: bool = True,
    ):
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(get_message('invalid_file_path_type'))
        if not isinstance(show_logs, bool):
            raise TypeError(get_message('invalid_show_logs_type'))
        if not isinstance(is_temp, bool):
            raise TypeError(get_message('invalid_is_temp_type'))
        if encryption_key is not None and not isinstance(encryption_key, str):
            raise TypeError(get_message('invalid_encryption_key_type'))
        if not isinstance(auto_cleanup_temp, bool):
            raise TypeError(get_message('invalid_auto_cleanup_temp_type'))
        if file_path is None and not is_temp:
            raise ValueError(get_message('file_path_required_for_non_temp'))

        object.__setattr__(self, '_file_path', file_path)
        object.__setattr__(self, '_show_logs', show_logs)
        object.__setattr__(self, '_is_temp', is_temp)
        object.__setattr__(self, '_encryption_key', encryption_key)
        object.__setattr__(self, '_auto_cleanup_temp', auto_cleanup_temp)
        object.__setattr__(self, 'logger', Logger())
        object.__setattr__(self, '_file', None)

        self.db_create_file()
        self._data_compliance_check()

    def _public_data_keys(self) -> list[str]:
        return [
            key
            for key in self.__dict__.keys()
            if not key.startswith('_') and key not in self._BAN_NAMES
        ]

    def _collect_public_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for key in self._public_data_keys():
            value = self.__dict__[key]
            try:
                json.dumps(value)
                data[key] = value
            except TypeError:
                self._log(f"Skipped non-JSON value for key '{key}'", 'WARNING')
        return data

    def _encrypt_text(self, text: str) -> str:
        if not self._encryption_key:
            return text
        key_bytes = self._encryption_key.encode('utf-8')
        text_bytes = text.encode('utf-8')
        encrypted = bytes(
            value ^ key_bytes[index % len(key_bytes)] for index, value in enumerate(text_bytes)
        )
        return base64.b64encode(encrypted).decode('ascii')

    def _decrypt_text(self, text: str) -> str:
        if not self._encryption_key:
            raise ValueError(get_message('encryption_key_required'))
        key_bytes = self._encryption_key.encode('utf-8')
        try:
            encrypted = base64.b64decode(text.encode('ascii'))
        except Exception as error:
            raise ValueError(get_message('decrypt_data_error')) from error
        decrypted = bytes(
            value ^ key_bytes[index % len(key_bytes)]
            for index, value in enumerate(encrypted)
        )
        return decrypted.decode('utf-8')

    def _encode_payload(self, data: dict[str, Any]) -> dict[str, Any]:
        if not self._encryption_key:
            return data
        plain_json = json.dumps(data, ensure_ascii=False)
        encrypted_payload = self._encrypt_text(plain_json)
        return {
            self._ENCRYPTION_MARKER: True,
            'algorithm': 'xor-base64-v1',
            'payload': encrypted_payload,
        }

    def _decode_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            return {}

        if payload.get(self._ENCRYPTION_MARKER):
            encrypted_payload = payload.get('payload')
            if not isinstance(encrypted_payload, str):
                raise ValueError(get_message('invalid_encrypted_payload'))
            decrypted = self._decrypt_text(encrypted_payload)
            loaded_data = json.loads(decrypted)
            if isinstance(loaded_data, dict):
                return loaded_data
            raise ValueError(get_message('invalid_data_format'))

        return payload

    def _data_compliance_check(self) -> None:
        if self._file is None:
            return

        try:
            self._file.seek(0)
            content = self._file.read().strip()
            if not content:
                return

            raw_data = json.loads(content)
            data = self._decode_payload(raw_data)

            if isinstance(data, dict):
                for key, value in data.items():
                    if key not in self._BAN_NAMES and not key.startswith('_'):
                        object.__setattr__(self, key, value)
            else:
                self._log(get_message('invalid_data_format'), 'WARNING')

        except json.JSONDecodeError:
            self._log(get_message('json_decode_error'), 'ERROR')
            self._file.truncate(0)
        except Exception as error:
            self._log(f"{get_message('data_load_error')}: {str(error)}", 'ERROR')

    def _log(self, message: str, level: str = 'INFO') -> None:
        if not isinstance(level, str):
            raise TypeError(get_message('invalid_level_type'))
        if not isinstance(message, str):
            raise TypeError(get_message('invalid_message_type'))
        if self._show_logs:
            self.logger.log(message, level)

    def get_show_logs(self) -> bool:
        return self._show_logs

    def get_is_temp(self) -> bool:
        return self._is_temp

    def get_file(self):
        return self._file

    def get_file_path(self) -> str:
        return self._file_path

    def db_create_file(self) -> None:
        if self._is_temp:
            file = NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8')
            object.__setattr__(self, '_file', file)
            object.__setattr__(self, '_file_path', file.name)
            return

        if self.check_file_exists(self._file_path):
            try:
                file = open(self._file_path, 'r+', encoding='utf-8')
                object.__setattr__(self, '_file', file)
            except Exception as error:
                self._log(f"{get_message('file_open_error')}: {str(error)}", 'ERROR')
                file = open(self._file_path, 'w+', encoding='utf-8')
                object.__setattr__(self, '_file', file)
        else:
            file = open(self._file_path, 'w+', encoding='utf-8')
            object.__setattr__(self, '_file', file)

    @staticmethod
    def check_file_exists(file_path: str) -> bool:
        if not isinstance(file_path, str):
            raise TypeError(get_message('invalid_file_path_type'))
        try:
            return os.path.isfile(file_path)
        except Exception:
            return False

    def _save_data(self) -> None:
        if self._file is None or self._file_path is None:
            return

        data = self._collect_public_data()

        try:
            payload = self._encode_payload(data)
            tmp_path = f"{self._file_path}.tmp"
            with open(tmp_path, 'w', encoding='utf-8') as tmp_file:
                json.dump(payload, tmp_file, indent=2, ensure_ascii=False)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            os.replace(tmp_path, self._file_path)

            if self._file and not self._file.closed:
                self._file.close()
            object.__setattr__(self, '_file', open(self._file_path, 'r+', encoding='utf-8'))
        except Exception as error:
            self._log(f"{get_message('save_data_error')}: {str(error)}", 'ERROR')

    def close(self) -> None:
        self._save_data()
        if self._file and not self._file.closed:
            self._file.close()
        if self._is_temp and self._auto_cleanup_temp and self._file_path:
            try:
                if os.path.exists(self._file_path):
                    os.remove(self._file_path)
            except Exception as error:
                self._log(f"Temp cleanup failed: {error}", 'WARNING')

    def __repr__(self) -> str:
        return f"DataBase({self._collect_public_data()})"

    def __str__(self) -> str:
        return str(self._collect_public_data())

    def __bytes__(self) -> bytes:
        return str(self).encode('utf-8')

    def __format__(self, format_spec: str) -> str:
        if format_spec == '':
            return str(self)
        if format_spec == 'repr':
            return repr(self)
        if format_spec == 'json':
            return json.dumps(self._collect_public_data(), ensure_ascii=False)
        return str(self).__format__(format_spec)

    def __delattr__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(get_message('invalid_attribute_name'))
        if name in self._BAN_NAMES:
            raise AttributeError(get_message('protected_attribute_deletion'))
        if name not in self.__dict__:
            self._log(get_message('attribute_not_found').format(name=name), 'WARNING')
            return
        super().__delattr__(name)
        self._save_data()

    def __setattr__(self, name: str, value) -> None:
        if not isinstance(name, str):
            raise TypeError(get_message('invalid_attribute_name'))
        if name in self._BAN_NAMES and name in self.__dict__:
            raise AttributeError(get_message('protected_attribute_modification'))
        super().__setattr__(name, value)
        if name not in self._BAN_NAMES and not name.startswith('_'):
            self._save_data()

    def __getattr__(self, name: str):
        raise AttributeError(get_message('attribute_not_found').format(name=name))

    def __getattribute__(self, name: str):
        return super().__getattribute__(name)

    def __dir__(self) -> list[str]:
        return sorted(self._public_data_keys())

    def __getitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_access'))
        return self.get(key, None)

    def __setitem__(self, key: str, value) -> None:
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_modification'))
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_deletion'))
        delattr(self, key)

    def __len__(self) -> int:
        return len(self._public_data_keys())

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            raise TypeError(get_message('invalid_item_type'))
        return item in self.__dict__ and item not in self._BAN_NAMES and not item.startswith('_')

    def __iter__(self):
        return iter(self.keys())

    def items(self):
        return [(key, self.__dict__[key]) for key in self.keys()]

    def keys(self):
        return self._public_data_keys()

    def values(self):
        return [self.__dict__[key] for key in self.keys()]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __copy__(self):
        from copy import copy

        new_db = DataBase(
            file_path=self._file_path,
            show_logs=self._show_logs,
            is_temp=self._is_temp,
            encryption_key=self._encryption_key,
            auto_cleanup_temp=self._auto_cleanup_temp,
        )
        for key, value in self.items():
            setattr(new_db, key, copy(value))
        return new_db

    def __deepcopy__(self, memo):
        from copy import deepcopy

        new_db = DataBase(
            file_path=self._file_path,
            show_logs=self._show_logs,
            is_temp=self._is_temp,
            encryption_key=self._encryption_key,
            auto_cleanup_temp=self._auto_cleanup_temp,
        )
        for key, value in self.items():
            setattr(new_db, key, deepcopy(value, memo))
        return new_db

    def __hash__(self) -> int:
        data_tuple = tuple(sorted(self.items()))
        return hash(data_tuple)

    def __eq__(self, other) -> bool:
        if isinstance(other, DataBase):
            return dict(self.items()) == dict(other.items())
        if isinstance(other, dict):
            return dict(self.items()) == other
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __bool__(self) -> bool:
        if self._is_temp:
            return self._file is not None
        return self.check_file_exists(self._file_path) if self._file_path else False

    def __matmul__(self, other: str) -> None:
        if not isinstance(other, str):
            raise TypeError(get_message('invalid_docstring_type'))
        self.__doc__ = other

    def __and__(self, other) -> bool:
        return bool(self) and bool(other)

    def __or__(self, other) -> bool:
        return bool(self) or bool(other)

    def __rand__(self, other) -> bool:
        return bool(other) and bool(self)

    def __ror__(self, other) -> bool:
        return bool(other) or bool(self)

    def clear(self) -> None:
        for key in list(self.keys()):
            delattr(self, key)
        self._save_data()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key not in self._BAN_NAMES and not key.startswith('_'):
                setattr(self, key, value)
        self._save_data()

    def get(self, key: str, default=None):
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        if key in self._BAN_NAMES or key.startswith('_'):
            return default
        return self.__dict__.get(key, default)

    def pop(self, key: str, default=None):
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        if key in self._BAN_NAMES or key.startswith('_'):
            return default
        if key in self.__dict__:
            value = self.__dict__[key]
            delattr(self, key)
            return value
        return default
