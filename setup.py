#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ.get('USER', '') == 'vagrant':
    del os.link

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'sleekxmpp', 'dnspython', 'pyasn1', 'pyasn1-modules', 'enum34', 'xmltodict'
]

test_requirements = [
    'mock'
]

setup(
    name='ncaplite',
    version='0.1.0',
    description="ncaplite contains a python package and reference design for implementing IEEE P21451-1 Network Capable Application Processor services",
    long_description=readme + '\n\n' + history,
    author="James Ethridge",
    author_email='jeethridge@gmail.com',
    url='https://github.com/jeethridge/ncaplite',
    packages=[
        'ncaplite',
    ],
    package_dir={'ncaplite':
                 'ncaplite'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='ncaplite',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
