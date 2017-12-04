import os

from setuptools import find_packages, setup

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''

setup(
    name='pretix-printtool',
    version='0.1.1',
    description='Command-line client for pretix that allows to print out tickets for shippinh',
    long_description=long_description,
    url='https://github.com/pretix/pretix-printtool',
    author='Raphael Michel',
    author_email='mail@raphaelmichel.de',

    install_requires=[
        'click==6.*',
        'pycups',
        'requests',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,

    entry_points={
        'console_scripts': ['pretix-printtool=pretix_printtool.main:main'],
    },
)
