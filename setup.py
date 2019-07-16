from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='ev_reduce',
    description='message handling framework',
    version='0.1',
    license='MIT',

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    python_requires='>=3.7',

    install_requires = ['pyzmq'],
    setup_requires = ['pytest-runner'],
    tests_require  = ['pytest'],

    test_suite='tests',
)
