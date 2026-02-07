Welcome to DBase documentation. For the latest documentation, visit our [GitHub repository](https://github.com/Danex-Exe/dbase).

## Quick Links

- [Full Documentation](https://github.com/Danex-Exe/dbase#readme)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Changelog](https://github.com/Danex-Exe/dbase/blob/main/docs/CHANGELOG.md)

## Installation

```bash
pip install "git+https://github.com/Danex-Exe/dbase.git@9c5dff4"
```

## Basic Example

```python
from dbase import DataBase

# Create or open a database
db = DataBase(file_path="data.json")

# Store data
db["name"] = "Alice"
db.score = 95

# Retrieve data
print(db["name"])  # Alice
print(db.score)    # 95

# Use as context manager
with DataBase(file_path="session.json") as session:
    session.user = "admin"
    session.timestamp = "2024-01-01"
```

## API Reference

### DataBase Class

```python
class DataBase(file_path=None, show_logs=True, is_temp=False)
```

**Parameters:**
- `file_path` (str, optional): Path to JSON file for persistent storage
- `show_logs` (bool): Enable/disable logging (default: True)
- `is_temp` (bool): Create temporary in-memory database (default: False)

**Methods:**
- `get(key, default=None)`: Get value with fallback
- `pop(key, default=None)`: Remove and return value
- `update(**kwargs)`: Update multiple values
- `clear()`: Remove all data
- `items()`: Return key-value pairs
- `keys()`: Return all keys
- `values()`: Return all values

## Examples

### Example 1: Basic CRUD Operations

```python
db = DataBase("users.json")

# Create
db["user1"] = {"name": "Alice", "age": 30}

# Read
user = db["user1"]

# Update
db["user1"]["age"] = 31

# Delete
del db["user1"]
```

### Example 2: Configuration Storage

```python
config = DataBase("config.json")

# Set configuration
config.database.host = "localhost"
config.database.port = 5432
config.app.debug = True

# Get configuration
host = config.database.host
```

### Example 3: Temporary Data

```python
# Temporary in-memory database
cache = DataBase(is_temp=True)

# Store temporary data
cache.session_token = "abc123"
cache.timestamp = "2024-01-01T12:00:00"

# Data is lost when program ends
```

## Best Practices

1. **Use context managers** for automatic cleanup:
   ```python
   with DataBase("data.json") as db:
       # Work with database
   ```

2. **Handle missing keys** safely:
   ```python
   value = db.get("missing_key", default="default_value")
   ```

3. **Use appropriate storage**:
   - Persistent files for long-term storage
   - Temporary databases for caching

4. **Enable logging** during development:
   ```python
   db = DataBase("data.json", show_logs=True)
   ```

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure the directory exists before creating database
2. **Permission errors**: Check file permissions
3. **JSON decode errors**: Verify file contains valid JSON
4. **Type errors**: Ensure you're using string keys

### Getting Help

- Check the [GitHub Issues](https://github.com/Danex-Exe/dbase/issues)
- Review the source code
- Submit a bug report with reproduction steps

## License

MIT License - see LICENSE file for details.

## Support

This project is maintained by Daniil Alekseev. For support, please open an issue on GitHub.
