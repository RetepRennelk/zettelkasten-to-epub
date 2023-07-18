# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

from setuptools import setup, find_packages

setup(
    name='Zettelkasten-to-EPUB',
    version='0.0.1',
    packages=find_packages(include=['z2e.src']),
    entry_points={
        'console_scripts': ['z2e=z2e.src.main:main']
    }
)