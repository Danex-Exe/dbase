from setuptools import setup, find_packages

setup(
    name="dbase",
    description='Database Library',
    long_description='DBase - Secure Python DB library. Manage text/JSON/encrypted databases with built-in logging and error handling. Military-grade encryption, temp DBs, atomic ops. Ideal for secure local storage',
    author='Daniil Alekseev',
    author_email='sevenaspects.mail@gmail.com',
    version="2.0.6",
    packages=find_packages(),
    install_requires=["cryptography"],
    python_requires=">=3.8",
)
