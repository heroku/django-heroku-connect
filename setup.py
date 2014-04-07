#!/usr/bin/env python

import os
import sys

import connect_client

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'connect_client',
]

requires = [
    'shams==0.0.2',
    'Django>=1.6',
]

with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='connect_client',
    version=connect_client.__version__,
    description='Heroku Connect client django app',
    long_description=readme,
    author='David Gouldin',
    author_email='dgouldin@heroku.com',
    url='https://github.com/heroku/django-heroku-connect',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'connect_client': 'connect_client'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
