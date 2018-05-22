#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pip

from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

parsed_requirements = parse_requirements(
    'requirements/prod.txt',
    session=pip.download.PipSession()
)

parsed_test_requirements = parse_requirements(
    'requirements/test.txt',
    session=pip.download.PipSession()
)


requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]


setup(
    name='snipssonos',
    version='1.1.0',
    description="Snips action code for your Sonos speaker(s)",
    long_description=readme,
    author="The Als",
    url='https://github.com/snipsco/snips-skill-sonos',
    packages=[
        'snipssonos'
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords=['snips','sonos'],
    test_suite='tests',
    tests_require=test_requirements
)
