import json
import os
from tempfile import NamedTemporaryFile


from .errors import *
from .security import *
from .logger import Logger
from .messages import get_message


__all__ = ['DataBase', 'Logger']
__version__ = '3.0.0'


class DataBase:
    __all__ = ['create', 'check_file_exists']
    _BAN_NAMES = ('_file_path', '_show_logs', '_is_temp', '_file', 'logger')

    def __init__(self, file_path: str = None, show_logs: bool = True, is_temp: bool = False):
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(get_message('invalid_file_path_type'))

        if not isinstance(show_logs, bool):
            raise TypeError(get_message('invalid_show_logs_type'))

        if not isinstance(is_temp, bool):
            raise TypeError(get_message('invalid_is_temp_type'))
        
        if file_path is None and not is_temp:
            raise ValueError(get_message('file_path_required_for_non_temp'))
        
        # Используем object.__setattr__ для обхода нашего __setattr__
        object.__setattr__(self, '_file_path', file_path)
        object.__setattr__(self, '_show_logs', show_logs)
        object.__setattr__(self, '_is_temp', is_temp)
        object.__setattr__(self, 'logger', Logger())
        object.__setattr__(self, '_file', None)
        
        self.db_create_file()
        self._data_compliance_check()


    def _data_compliance_check(self) -> None:
        if self._is_temp:
            for key in list(self.__dict__.keys()):
                if key not in self._BAN_NAMES:
                    delattr(self, key)
            return

        if self._file is None:
            return
            
        try:
            self._file.seek(0)
            content = self._file.read().strip()
            
            if not content:
                return
                
            data = json.loads(content)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if key not in self._BAN_NAMES:
                        object.__setattr__(self, key, value)
            else:
                self._log(get_message('invalid_data_format'), 'WARNING')
                
        except json.JSONDecodeError:
            self._log(get_message('json_decode_error'), 'ERROR')
            self._file.truncate(0)
        except Exception as e:
            self._log(f"{get_message('data_load_error')}: {str(e)}", 'ERROR')


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
            # Используем object.__setattr__ для обхода защиты
            file = NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
            object.__setattr__(self, '_file', file)
            object.__setattr__(self, '_file_path', file.name)
            return

        if self.check_file_exists(self._file_path):
            try:
                file = open(self._file_path, 'r+', encoding='utf-8')
                object.__setattr__(self, '_file', file)
            except Exception as e:
                self._log(f"{get_message('file_open_error')}: {str(e)}", 'ERROR')
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
        except Exception as e:
            return False

    
    def _save_data(self) -> None:
        if self._file is None:
            return
            
        data = {}
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    value = getattr(self, key)
                    json.dumps(value)
                    data[key] = value
                except (TypeError, AttributeError):
                    pass
        
        if not data:
            return

        try:
            self._file.seek(0)
            json.dump(data, self._file, indent=2, ensure_ascii=False)
            self._file.truncate()
            self._file.flush()
        except Exception as e:
            self._log(f"{get_message('save_data_error')}: {str(e)}", 'ERROR')


    def __repr__(self) -> str:
        data = {}
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    data[key] = getattr(self, key)
                except AttributeError:
                    pass
        return f"DataBase({data})"

    def __str__(self) -> str:
        data = {}
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    data[key] = getattr(self, key)
                except AttributeError:
                    pass
        return str(data)

    def __bytes__(self) -> bytes:
        return str(self).encode('utf-8')

    def __format__(self, format_spec: str) -> str:
        if format_spec == '':
            return str(self)
        elif format_spec == 'repr':
            return repr(self)
        elif format_spec == 'json':
            data = {}
            for key in dir(self):
                if not key.startswith('_') and key not in self._BAN_NAMES:
                    try:
                        data[key] = getattr(self, key)
                    except AttributeError:
                        pass
            return json.dumps(data, ensure_ascii=False)
        else:
            return str(self).__format__(format_spec)


    def __delattr__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(get_message('invalid_attribute_name'))

        if name in self._BAN_NAMES:
            raise AttributeError(get_message('protected_attribute_deletion'))

        if not hasattr(self, name):
            self._log(get_message('attribute_not_found').format(name=name), 'WARNING')
            return
        
        super().__delattr__(name)
        self._save_data()

    def __setattr__(self, name: str, value) -> None:
        if not isinstance(name, str):
            raise TypeError(get_message('invalid_attribute_name'))

        # Разрешаем изменение защищенных атрибутов только внутри методов класса
        # Проверяем, вызван ли из метода класса (по стеку вызовов)
        import inspect
        
        # Получаем текущий фрейм
        current_frame = inspect.currentframe()
        
        # Проверяем, вызывается ли из метода этого класса
        is_from_class_method = False
        if current_frame:
            # Получаем предыдущий фрейм (который вызвал __setattr__)
            caller_frame = current_frame.f_back
            if caller_frame:
                # Получаем имя метода, который вызвал __setattr__
                method_name = caller_frame.f_code.co_name
                # Получаем объект self из локальных переменных вызывающего фрейма
                caller_self = caller_frame.f_locals.get('self')
                if caller_self is self and method_name != '__init__':
                    is_from_class_method = True
        
        # Если это защищенный атрибут и вызывается не из метода класса, запрещаем
        if name in self._BAN_NAMES and hasattr(self, name) and not is_from_class_method:
            raise AttributeError(get_message('protected_attribute_modification'))
        
        # Если это не защищенный атрибут, сохраняем данные
        old_value = getattr(self, name, None) if name in self._BAN_NAMES else None
        super().__setattr__(name, value)
        
        # Сохраняем только если это не защищенный атрибут или значение изменилось
        if name not in self._BAN_NAMES:
            self._save_data()


    def __getattr__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(get_message('invalid_attribute_name'))

        if name in self._BAN_NAMES or name.startswith('_'):
            raise AttributeError(get_message('attribute_not_found').format(name=name))
        
        return None

    def __getattribute__(self, name: str):
        return super().__getattribute__(name)


    def __dir__(self) -> list[str]:
        public_attrs = []
        for attr in super().__dir__():
            if not attr.startswith('_') and attr not in self._BAN_NAMES:
                public_attrs.append(attr)
        return sorted(public_attrs)


    def __getitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
        
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_access'))
            
        return getattr(self, key, None)

    def __setitem__(self, key: str, value) -> None:
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
            
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_modification'))
            
        return setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError(get_message('invalid_key_type'))
            
        if key in self._BAN_NAMES or key.startswith('_'):
            raise KeyError(get_message('protected_key_deletion'))
            
        return delattr(self, key)

    def __len__(self) -> int:
        return len([attr for attr in dir(self) if not attr.startswith('_') and attr not in self._BAN_NAMES])

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            raise TypeError(get_message('invalid_item_type'))
        
        return hasattr(self, item) and item not in self._BAN_NAMES and not item.startswith('_')


    def __iter__(self):
        keys = []
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                keys.append(key)
        return iter(keys)

    def items(self):
        items = []
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    items.append((key, getattr(self, key)))
                except AttributeError:
                    pass
        return items

    def keys(self):
        return list(self.__iter__())

    def values(self):
        values = []
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    values.append(getattr(self, key))
                except AttributeError:
                    pass
        return values


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._save_data()
        if self._file and not self._file.closed:
            self._file.close()


    def __copy__(self):
        from copy import copy
        new_db = DataBase(
            file_path=self._file_path,
            show_logs=self._show_logs,
            is_temp=self._is_temp
        )
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    setattr(new_db, key, copy(getattr(self, key)))
                except AttributeError:
                    pass
        return new_db

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new_db = DataBase(
            file_path=self._file_path,
            show_logs=self._show_logs,
            is_temp=self._is_temp
        )
        for key in dir(self):
            if not key.startswith('_') and key not in self._BAN_NAMES:
                try:
                    setattr(new_db, key, deepcopy(getattr(self, key), memo))
                except AttributeError:
                    pass
        return new_db

    def __hash__(self) -> int:
        data_tuple = tuple(sorted(self.items()))
        return hash(data_tuple)


    def __eq__(self, other) -> bool:
        if isinstance(other, DataBase):
            return dict(self.items()) == dict(other.items())
        elif isinstance(other, dict):
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
        if isinstance(other, DataBase):
            return bool(self) and bool(other)
        return bool(self) and bool(other)

    def __or__(self, other) -> bool:
        if isinstance(other, DataBase):
            return bool(self) or bool(other)
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
        if key in self._BAN_NAMES or key.startswith('_'):
            return default
        return getattr(self, key, default)

    def pop(self, key: str, default=None):
        if key in self._BAN_NAMES or key.startswith('_'):
            return default
        
        value = getattr(self, key, default)
        if hasattr(self, key):
            delattr(self, key)
        return value