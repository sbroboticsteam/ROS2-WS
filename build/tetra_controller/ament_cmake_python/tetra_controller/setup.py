from setuptools import find_packages
from setuptools import setup

setup(
    name='tetra_controller',
    version='0.0.0',
    packages=find_packages(
        include=('tetra_controller', 'tetra_controller.*')),
)
