===============================
Snips App Sonos
===============================

.. image:: https://travis-ci.org/snipsco/snips-app-sonos.svg?branch=dev
        :target: https://travis-ci.org/snipsco/snips-app-sonos

Snips action code for your Sonos speaker(s)

Features
--------

* Discover your Sonos devices in your local Network
* Support for Spotify and Deezer
* Search for any Artist, Song, Album on Spotify, and Deezer with your voice
* Control Music Playback with your voice
* Web Interface for authentication, and devices management


Setup Instructions
------------------

The following instructions are valid when you are setting up the app on your Raspberry Pi after the Music assistant was installed from the console.

Setting up the configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you installed your assistant with sam, the app folder should reside on your Pi at this path : `/var/lib/snips/skills/snips-app-sonos`. 
Create an empty file called `config.ini` that follows the structure below : 

        [global]
        [secret]

Setting up the Sonos API service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running tests
~~~~~~~~~~~~~

Create a virtual environment, and run:

    pip install -r requirements/test.txt
    tox

This will install the dependencies needed to run the tests, and actually run the tests. 


Copyright
---------

This action code is provided by `Snips <https://www.snips.ai>`_ as Open Source
software. See `LICENSE.txt
<https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt>`_ for more
information.

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
