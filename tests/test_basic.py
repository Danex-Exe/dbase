import pytest
import os
from dbase.errors import *
from dbase import DataBase


def test_json_db():
    db = DataBase("test.json")
    db.create()

    db.set(key="key", value="value")
    assert db.read()["key"] == "value"
    assert db.get("key") == "value"

    db.remove("key")
    assert db.get('key') is None

    db.set(data=[('key1', 'value1'), ('key2', 'value2')])
    assert db.get('key1') == "value1"
    assert db.get('key2') == "value2"
    db.remove("key1")
    db.remove("key2")

    db.set(data=[('key1', 'value1'), ('key2', 'value2')], key='key3', value='value3')
    assert db.get('key1') == "value1"
    assert db.get('key2') == "value2"
    assert db.get('key3') == "value3"
    db.remove("key1")
    db.remove("key2")
    db.remove("key3")

    db.set(key="key", value="value")
    db.setdefault(key="key", value="value1")
    assert db.get("key") == "value"
    db.remove("key")

    db.setdefault(key="key", value="value1")
    assert db.get('key') == "value1"
    db.remove("key")

    db.set(key='key1', value="value2")
    db.setdefault(data=[('key1', 'value1'), ('key2', 'value2')])
    assert db.get('key1') == "value2"
    assert db.get('key2') == "value2"
    db.remove("key1")
    db.remove("key2")

    db.write("text")
    assert db.read() == "text"

    db.delete()
    assert not os.path.exists("test.json")


def test_encrypted_db():
    db = DataBase("test.dbase", show_logs=False)
    db.create(password="secret")

    with pytest.raises(OperationNotAllowedError):
        db.get("key")

    db.open()
    db.set(key="data", value={"important": True})
    assert db.get("data")["important"] is True

    db.delete(password="secret")
    assert not os.path.exists("test.dbase")
    assert not os.path.exists("SECURITY_KEY.key")


def test_temp_db():
    db = DataBase(":temp:", show_logs=False)

    with pytest.raises(TempDatabaseCreatedError):
        db.create()

    db.set(key="temp", value=True)
    assert db.get("temp") is True