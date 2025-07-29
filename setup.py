from setuptools import setup, find_packages

setup(
    name="dbase",
    description='Database Library',
    long_description='The Python module provides classes for simplified file management and synchronization. The `DataFile` class allows you to create, read, write, rename, and delete files, as well as get their information. It supports working with files in JSON format and with the ability to keep logs',
    author='Daniil Alekseev',
    author_email='dan.d.alekseev@gmail.com',
    version="2.0.4",
    packages=find_packages(),
    install_requires=["cryptography"],
    python_requires=">=3.8",
)
