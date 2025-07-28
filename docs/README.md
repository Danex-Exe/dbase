<h1 align="center">Documentation</h1>
<div align="center">
    <a href="README.md">English</a>
    <a href="ru/README_ru.md">Русский</a>
    <br><br>
</div>

## Installation
```bash
pip install git+https://Danex-Exe/dbase.git
```

## Usage
### .txt (text handling)
```python
from dbase import DataBase # Import the module

db = DataBase('test.txt') # Initialize the database
db.create() # Create the database (ignored if already exists)

db.write('123') # Write data
data = db.read() # Read data
print(data) # Output data
```

### .txt, .json (JSON handling)
```python
from dbase import DataBase # Import the module

db = DataBase('test.txt') # Call the function (.json can be used instead of .txt)
db.create() # Create the database (ignored if already exists)

db.set(data=[
      ('a', '123'),
      ('b', '456')
]) # Write multiple variables in one call
db.set(key='a', value='123') # Write a single element
db.set('b', '456') # Write a second element
# it's possible to combine writing multiple and single elements

db.setdefault(data=[], key='', value='') # Works the same way, but only if the variable(s) don't exist

db.get(key='a') # Returns the value of the variable, or None if it doesn't exist

db.rename(last_key='a', new_key='c') # Renames a variable

db.remove(key='c') # Deletes a variable

db.delete() # Deletes the database
```


### .dbase (encrypted database)
```python
from dbase import DataBase # Import the module

db = DataBase('test.dbase') # Call the function (.json can be used instead of .txt)
db.create(password="SECRET_PASSWORD") # Create the database (ignored if already exists), the password is hashed and stored in the database
db.open(key='SECURITY_KEY.key') # Creates a secure session, enabling interaction with the database. Other functions won't work without this.

# All the aforementioned JSON functions also apply to this database, but here they are automatically encoded
# The .read() and .write() functions do not work with .dbase
db.delete(password="SECRET_PASSWORD") # Checks the database password and deletes it if it matches
```

### Logger configuration
```python
from dbase import DataBase # Import the module

db = DataBase('test.txt') # Initialize the database

db.logger.title = 'Logger title'
db.logger.log_file = 'Path to the log file'
db.logger.time_format = 'Time format'
db.logger.format = 'Log format'
db.logger.log_dir = 'Logs directory'
```
