Sonos skill for Snips
=====================

|Build Status| |PyPI| |MIT License|

A Snips Skill to control one Sonos on your local network.

Snips Manager
-------------

Installation
^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Manager
<https://github.com/snipsco/snipsskills>`_. Simply add the following section to
your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    skills:
      - package_name: snipssonos
        class_name: SnipsSonos
        pip: https://github.com/snipsco/snips-skills-sonos

Usage with Sonos Local Music Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you would like to use your local music (e.g. on a NAS, Itune Library, ...).
Follow the Instruction `here
<https://sonos.custhelp.com/app/answers/detail/a_id/261/~/adding-and-updating-your-music-library>`_
.

| To create a nas within your raspberry pi by following
  `this guide <https://eltechs.com/raspberry-pi-nas-guide/>`_.

| To create a local playlist follow
  `this Gist <https://gist.github.com/scarlson/944860>`_.

Usage with Spotify
^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    skills:
      - package_name: snipssonos
        class_name: SnipsSonos
        pip: https://github.com/snipsco/snips-skills-sonos
        params:
            spotify_refresh_token: SPOTIFY_REFRESH_TOKEN

The ``SPOTIFY_REFRESH_TOKEN`` is used for playing music from Spotify. You can
obtain it from the
`Snips Spotify Login <https://snips-spotify-login.herokuapp.com>`_ page.

There is an issue with the library we are using to connect to the Spotify.
To play a Spotify playlist please import your Spotify playlist to your Sonos
Playlist.

All optional parameters
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: yaml

        params:
            spotify_refresh_token: SPOTIFY_REFRESH_TOKEN
            default_speaker: 0
            sonos_ip: XXX.XXX.XXX.XXX

spotify_refresh_token
  | set spotify refresh token.
  | The ``SPOTIFY_REFRESH_TOKEN`` is used for playing music from Spotify. You
    can obtain it from the
    `Snips Spotify Login <https://snips-spotify-login.herokuapp.com>`_ page.

default_speaker
  The default speaker used with the skill.

sonos_ip
  If you already have the ip address of your Sonos, you can set it.

Standalone
----------

Installation
^^^^^^^^^^^^

The skill is on `PyPI <https://pypi.python.org/pypi/snipshue>`_, so you can just
install it with `pip <http://www.pip-installer.org>`_:

.. code-block:: console

    $ pip install snipssonos

Usage
^^^^^

The skill allows you to control
`Sonos <http://musicpartners.sonos.com/docs?q=node/442>`_ speakers. You can use
it as follows:

.. code-block:: python

    from snipssonos.snipssonos import SnipsSonos

    sonos = SnipsSonos(SPOTIFY_REFRESH_TOKEN)
    sonos.play_artist("John Coltrane")

Copyright
---------

This skill is provided by `Snips <https://www.snips.ai>`_ as Open Source
software. See `LICENSE.txt
<https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt>`_ for more
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
