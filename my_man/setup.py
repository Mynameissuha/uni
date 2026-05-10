from setuptools import setup

setup(
    name="filemanager",
    version="0.1",
    py_modules=["main", "manager"],
    entry_points={
        'console_scripts': [
            'filemanager = main:main', # Команда = модуль:функция
        ],
    },
)