from setuptools import setup

setup(
    name='mw',
    version='0.1.0',
    py_modules=['mw'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'mw = mw.__main__:main',
        ],
    },
)