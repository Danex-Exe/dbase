from ._imports import *


__all__ = ['get_message', 'set_language', 'get_available_languages']


class _MessageManager:
    
    _instance = None
    _messages: Dict[str, Dict[str, str]] = {}
    _current_language: str = 'eng'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_messages()
        return cls._instance
    
    def _load_messages(self) -> None:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            messages_file = os.path.join(current_dir, 'messages.json')
            
            with open(messages_file, 'r', encoding='utf-8') as f:
                loaded_messages = json.load(f)
                
            self._messages = loaded_messages
            
            default_messages = {
                'eng': {
                    'test': 'test!',
                    'invalid_file_path_type': 'File path must be a string',
                    'invalid_show_logs_type': 'Show logs must be a boolean value',
                    'invalid_is_temp_type': 'Is temp must be a boolean value',
                    'file_path_required_for_non_temp': 'File path is required for non-temporary database',
                    'invalid_data_format': 'Invalid data format in file',
                    'json_decode_error': 'Error decoding JSON from file',
                    'data_load_error': 'Error loading data',
                    'invalid_level_type': 'Level must be a string',
                    'invalid_message_type': 'Message must be a string',
                    'file_open_error': 'Error opening file',
                    'save_data_error': 'Error saving data',
                    'invalid_attribute_name': 'Attribute name must be a string',
                    'protected_attribute_deletion': 'Cannot delete protected attribute',
                    'attribute_not_found': 'Attribute not found: {name}',
                    'protected_attribute_modification': 'Cannot modify protected attribute',
                    'invalid_key_type': 'Key must be a string',
                    'protected_key_access': 'Cannot access protected key',
                    'protected_key_modification': 'Cannot modify protected key',
                    'protected_key_deletion': 'Cannot delete protected key',
                    'invalid_item_type': 'Item must be a string',
                    'invalid_docstring_type': 'Docstring must be a string',
                    'language_not_supported': 'Language not supported',
                    'message_not_found': 'Message not found',
                    'invalid_encryption_key_type': 'Encryption key must be a string',
                    'invalid_auto_cleanup_temp_type': 'Auto cleanup flag must be a boolean value',
                    'encryption_key_required': 'Encryption key is required to read encrypted data',
                    'invalid_encrypted_payload': 'Encrypted payload format is invalid',
                    'decrypt_data_error': 'Error decrypting data'
                },
                'ru': {
                    'test': 'тест!',
                    'invalid_file_path_type': 'Путь к файлу должен быть строкой',
                    'invalid_show_logs_type': 'Параметр show_logs должен быть логическим значением',
                    'invalid_is_temp_type': 'Параметр is_temp должен быть логическим значением',
                    'file_path_required_for_non_temp': 'Для невременной базы данных требуется указать путь к файлу',
                    'invalid_data_format': 'Неверный формат данных в файле',
                    'json_decode_error': 'Ошибка декодирования JSON из файла',
                    'data_load_error': 'Ошибка загрузки данных',
                    'invalid_level_type': 'Уровень должен быть строкой',
                    'invalid_message_type': 'Сообщение должно быть строкой',
                    'file_open_error': 'Ошибка открытия файла',
                    'save_data_error': 'Ошибка сохранения данных',
                    'invalid_attribute_name': 'Имя атрибута должно быть строкой',
                    'protected_attribute_deletion': 'Нельзя удалять защищённый атрибут',
                    'attribute_not_found': 'Атрибут не найден: {name}',
                    'protected_attribute_modification': 'Нельзя изменять защищённый атрибут',
                    'invalid_key_type': 'Ключ должен быть строкой',
                    'protected_key_access': 'Нельзя обращаться к защищённому ключу',
                    'protected_key_modification': 'Нельзя изменять защищённый ключ',
                    'protected_key_deletion': 'Нельзя удалять защищённый ключ',
                    'invalid_item_type': 'Элемент должен быть строкой',
                    'invalid_docstring_type': 'Строка документации должна быть строкой',
                    'language_not_supported': 'Язык не поддерживается',
                    'message_not_found': 'Сообщение не найдено',
                    'invalid_encryption_key_type': 'Ключ шифрования должен быть строкой',
                    'invalid_auto_cleanup_temp_type': 'Флаг автоочистки должен быть логическим значением',
                    'encryption_key_required': 'Для чтения зашифрованных данных требуется ключ шифрования',
                    'invalid_encrypted_payload': 'Неверный формат зашифрованного содержимого',
                    'decrypt_data_error': 'Ошибка расшифровки данных'
                }
            }
            
            for lang in ['eng', 'ru']:
                if lang in self._messages:
                    for key, value in default_messages.get(lang, {}).items():
                        if key not in self._messages[lang]:
                            self._messages[lang][key] = value
                else:
                    self._messages[lang] = default_messages.get(lang, {})
                
        except FileNotFoundError:
            self._messages = {
                'eng': {
                    'test': 'test!',
                    'invalid_file_path_type': 'File path must be a string',
                    'invalid_show_logs_type': 'Show logs must be a boolean value',
                    'invalid_is_temp_type': 'Is temp must be a boolean value',
                    'file_path_required_for_non_temp': 'File path is required for non-temporary database',
                    'invalid_data_format': 'Invalid data format in file',
                    'json_decode_error': 'Error decoding JSON from file',
                    'data_load_error': 'Error loading data',
                    'invalid_level_type': 'Level must be a string',
                    'invalid_message_type': 'Message must be a string',
                    'file_open_error': 'Error opening file',
                    'save_data_error': 'Error saving data',
                    'invalid_attribute_name': 'Attribute name must be a string',
                    'protected_attribute_deletion': 'Cannot delete protected attribute',
                    'attribute_not_found': 'Attribute not found: {name}',
                    'protected_attribute_modification': 'Cannot modify protected attribute',
                    'invalid_key_type': 'Key must be a string',
                    'protected_key_access': 'Cannot access protected key',
                    'protected_key_modification': 'Cannot modify protected key',
                    'protected_key_deletion': 'Cannot delete protected key',
                    'invalid_item_type': 'Item must be a string',
                    'invalid_docstring_type': 'Docstring must be a string',
                    'language_not_supported': 'Language not supported',
                    'message_not_found': 'Message not found',
                    'invalid_encryption_key_type': 'Encryption key must be a string',
                    'invalid_auto_cleanup_temp_type': 'Auto cleanup flag must be a boolean value',
                    'encryption_key_required': 'Encryption key is required to read encrypted data',
                    'invalid_encrypted_payload': 'Encrypted payload format is invalid',
                    'decrypt_data_error': 'Error decrypting data'
                },
                'ru': {
                    'test': 'тест!',
                    'invalid_file_path_type': 'Путь к файлу должен быть строкой',
                    'invalid_show_logs_type': 'Параметр show_logs должен быть логическим значением',
                    'invalid_is_temp_type': 'Параметр is_temp должен быть логическим значением',
                    'file_path_required_for_non_temp': 'Для невременной базы данных требуется указать путь к файлу',
                    'invalid_data_format': 'Неверный формат данных в файле',
                    'json_decode_error': 'Ошибка декодирования JSON из файла',
                    'data_load_error': 'Ошибка загрузки данных',
                    'invalid_level_type': 'Уровень должен быть строкой',
                    'invalid_message_type': 'Сообщение должно быть строкой',
                    'file_open_error': 'Ошибка открытия файла',
                    'save_data_error': 'Ошибка сохранения данных',
                    'invalid_attribute_name': 'Имя атрибута должно быть строкой',
                    'protected_attribute_deletion': 'Нельзя удалять защищённый атрибут',
                    'attribute_not_found': 'Атрибут не найден: {name}',
                    'protected_attribute_modification': 'Нельзя изменять защищённый атрибут',
                    'invalid_key_type': 'Ключ должен быть строкой',
                    'protected_key_access': 'Нельзя обращаться к защищённому ключу',
                    'protected_key_modification': 'Нельзя изменять защищённый ключ',
                    'protected_key_deletion': 'Нельзя удалять защищённый ключ',
                    'invalid_item_type': 'Элемент должен быть строкой',
                    'invalid_docstring_type': 'Строка документации должна быть строкой',
                    'language_not_supported': 'Язык не поддерживается',
                    'message_not_found': 'Сообщение не найдено',
                    'invalid_encryption_key_type': 'Ключ шифрования должен быть строкой',
                    'invalid_auto_cleanup_temp_type': 'Флаг автоочистки должен быть логическим значением',
                    'encryption_key_required': 'Для чтения зашифрованных данных требуется ключ шифрования',
                    'invalid_encrypted_payload': 'Неверный формат зашифрованного содержимого',
                    'decrypt_data_error': 'Ошибка расшифровки данных'
                }
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in messages file: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load messages: {e}")
    
    def get(self, message_title: str, language: str = None) -> str:
        if not isinstance(message_title, str):
            raise ValueError("message_title must be a string")
            
        if language is None:
            language = self._current_language
            
        if not isinstance(language, str):
            raise ValueError("language must be a string")
            
        if language not in self._messages:
            if 'eng' in self._messages:
                eng_messages = self._messages['eng']
                if message_title in eng_messages:
                    return eng_messages[message_title]
                else:
                    return message_title
            else:
                return message_title
            
        lang_messages = self._messages[language]
        
        if message_title in lang_messages:
            return lang_messages[message_title]
        else:
            if 'eng' in self._messages:
                eng_messages = self._messages['eng']
                if message_title in eng_messages:
                    return eng_messages[message_title]
        
        return message_title
    
    def set_language(self, language: str) -> None:
        if language not in self._messages:
            raise ValueError(f"Language '{language}' not supported. "
                           f"Available: {list(self._messages.keys())}")
        self._current_language = language
    
    def get_available_languages(self) -> list:
        return list(self._messages.keys())


_message_manager = _MessageManager()


def get_message(message_title: str, language: str = None) -> str:
    return _message_manager.get(message_title, language)


def set_language(language: str) -> None:
    _message_manager.set_language(language)


def get_available_languages() -> list:
    return _message_manager.get_available_languages()