Sonos skill for Snips
=====================

|Build Status| |PyPI| |MIT License|


Installation
------------

The skill is on `PyPI <https://pypi.python.org/pypi/snipshue>`_, so you can just install it with `pip <http://www.pip-installer.org>`_:

.. code-block:: console

    $ pip install snipssonos

Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    skills:
      - pip: https://github.com/snipsco/snips-skills-sonos
        package_name: snipssonos
        class_name: SnipsSonos
        

Usage with Spotify
------------------

The skill allows you to control `Sonos <http://musicpartners.sonos.com/docs?q=node/442>`_ speakers. You can use it as follows:

.. code-block:: python

    from snipssonos.snipssonos import SnipsSonos

    sonos = SnipsSonos(SPOTIFY_REFRESH_TOKEN)
    sonos.play_artist("John Coltrane")

The ``SPOTIFY_REFRESH_TOKEN`` is used for playing music from Spotify. You can obtain it from the `Snips Spotify Login <https://snips-spotify-login.herokuapp.com>`_ page.

Useage with Sonos Local Music Library
-------------------------------------

If you would like to use your local music (e.g. on a NAS) you can specify this in the `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_. The get_local_library_data.py allows you to pull your local artists, playlists etc. to include as custom slots in your assistant.

.. code-block:: yaml

    skills:
      - url: https://github.com/darioce/snips-skills-sonos
        package_name: snipssonos
        class_name: SnipsSonos
        params:
                spotify_refresh_token: XXXXXXXXXX
                speaker_index: 0
                use_local_library: True
                sonos_ip: XXX.XXX.XXX.XXX

Copyright
---------

This skill is provided by `Snips <https://www.snips.ai>`_ as Open Source software. See `LICENSE.txt <https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt>`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skill-sonos.svg
   :target: https://travis-ci.org/snipsco/snips-skill-sonos
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipssonos.svg
   :target: https://pypi.python.org/pypi/snipssonos
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt
   :alt: MIT License
