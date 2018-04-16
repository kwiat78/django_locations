import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_locations',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        "Django==1.8.6",
        "djangorestframework==3.6.2",
        "django-filter==1.0.1",
        "requests==2.9.0",
    ],
    tests_require=[
        "freezegun==0.3.9",
        "pytz==2015.7",
        "PyYAML==3.12",
    ],
    test_suite="runtests",
    include_package_data=True,
    description='A simple Django app for addding tracks made out of locations',
    long_description=README,
    author='Szymon Kwiatkowski',
    author_email='kwiat78@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django REST framework :: 3.6',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
