from setuptools import setup, find_packages

setup(
    name="little-manager",
    version="0.1",
    packages=find_packages(),
    py_modules=["main", "manag"],
    package_dir={"": "."},
    entry_points={
        'console_scripts': [
            'littlemanager = main:main',
        ],
    },
)