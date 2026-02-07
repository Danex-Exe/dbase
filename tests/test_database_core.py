import json
import os

import pytest

from dbase import DataBase


def test_basic_crud_and_iteration(tmp_path):
    path = tmp_path / 'db.json'
    db = DataBase(str(path), show_logs=False)

    db.name = 'Alice'
    db['age'] = 30

    assert db.name == 'Alice'
    assert db['age'] == 30
    assert len(db) == 2
    assert sorted(db.keys()) == ['age', 'name']
    assert ('name', 'Alice') in db.items()


def test_missing_attribute_raises_attribute_error(tmp_path):
    db = DataBase(str(tmp_path / 'db.json'), show_logs=False)
    with pytest.raises(AttributeError):
        _ = db.unknown_key


def test_encryption_roundtrip(tmp_path):
    path = tmp_path / 'secure.json'
    db = DataBase(str(path), show_logs=False, encryption_key='secret-key')
    db.token = 'abc123'
    db.close()

    raw = path.read_text(encoding='utf-8')
    assert 'abc123' not in raw

    data = json.loads(raw)
    assert data['__dbase_encrypted__'] is True

    reopened = DataBase(str(path), show_logs=False, encryption_key='secret-key')
    assert reopened.token == 'abc123'


def test_temp_file_cleanup():
    with DataBase(is_temp=True, show_logs=False) as db:
        db_key_path = db.get_file_path()
        assert os.path.exists(db_key_path)
    assert not os.path.exists(db_key_path)


def test_save_closes_file_before_replace(tmp_path, monkeypatch):
    path = tmp_path / 'win-safe.json'
    db = DataBase(str(path), show_logs=False)

    original_replace = os.replace

    def checked_replace(src, dst):
        assert db.get_file().closed is True
        return original_replace(src, dst)

    monkeypatch.setattr(os, 'replace', checked_replace)
    db.key = 'value'
    assert db.key == 'value'
