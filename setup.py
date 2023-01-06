from setuptools import setup, find_packages

setup(
    name='housekeep',
    version='0.1',
    entry_points={'console_scripts': ['housekeep = housekeep.housekeep:main']},
    packages=find_packages()
)
