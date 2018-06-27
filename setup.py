#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

required = [
    "apiwrapper", 
    "requests",
    "paho-mqtt",
    "requests-futures",
    "hermes-python"
]

extras_require = {
    "test": [
        "mock",
        "pytest",
        "coverage",
        "pytest-cov"
    ],
}



setup(
    name='snipssonos',
    version='2.0.0',
    description="Snips action code for your Sonos speaker(s)",
    long_description=readme,
    author="The Als",
    url='https://github.com/snipsco/snips-skill-sonos',
    packages=[
        'snipssonos'
    ],
    include_package_data=True,
    install_requires=required,
    extras_require=extras_require,
    license="MIT",
    keywords=['snips','sonos'],
    test_suite='tests',
)
