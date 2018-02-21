from setuptools import setup

setup(
    name='snipssonos',
    version='1.0.0',
    description='Sonos skill for Snips',
    author='The Als',
    url='https://github.com/snipsco/snips-skill-sonos',
    download_url='',
    license='MIT',
    install_requires=['soco'],
    test_suite="tests",
    keywords=['snips', 'sonos'],
    packages=['snipssonos', 'snipssonos/provider'],
    package_data={'snipssonos': ['Snipsspec']},
    include_package_data=True
)
