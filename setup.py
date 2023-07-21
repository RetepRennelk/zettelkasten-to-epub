# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

from setuptools import setup, find_packages

setup(
    name='Zettelkasten-to-EPUB',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['z2e=z2e.src.main:main']
    }
)