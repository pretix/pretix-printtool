pretix-printtool
================

This is a command-line tool for `pretix`_ that allows you to automatically print out tickets that should be sent
to the customer on paper. This requires the pretix Shipping plugin that is only available for shops hosted on
pretix.eu or for pretix Enterprise installations.

Current limitations:

* Currently only supports printing on a per-organizer level, not on a per-event level.

* Currently only supports printing systems with a *local* CUPS deamon (Linux/macOS)

* Currently uses a late-ack method: The tool polls a PDF to print, prints it, waits for the print job to complete,
  then confirms the printing to the server and then starts polling the next PDF. This is obviously slower and might
  be parallelized, but this way it is kept simple and robust to ensure an easily recoverable state after printer errors.

Installation and usage
----------------------

First, make sure you have a recent Python installation on your system. If ``python -V`` gives you a version 2.x,
try using ``python3`` instead or install a newer Python. We recommend Python 3.6+, but 3.4+ should work as well.

Then, we recommend creating a virtual environment to isolate the python dependencies of this package from other
python programs ony our system::

    $ pyvenv env
    $ source env/bin/activate

You should now see a ``(env)`` prepended to your shell prompt. You have to do this
in every shell you use to work with pretix (or configure your shell to do so
automatically). Depending on your Python version, you might need to replace ``pyvenv`` with ``python -m venv``.
If you are working on Ubuntu or Debian, we recommend upgrading your pip and setuptools installation inside
the virtual environment::

    (env)$ pip3 install -U pip setuptools

Now you can install the print tool::

    (env)$ pip3 install pretix-printtool

To configure it, run the following command::

    (env)$ pretix-printtool setup

You will be asked a number of questions on your printer as well as for the URL of your pretix
installation and your API key. The prompt will also tell you how to obtain that API key.

At the end, this command will write a config file to a location of your choice. You need to specify this config file
for all further actions. The command::

    (env)$ pretix-printtool test configfile-path.cfg

will test the connection to pretix, but will not perform any actions. To actually start printing, use::

    (env)$ pretix-printtool print configfile-path.cfg


Contributing
------------

If you like to contribute to this project, you are very welcome to do so. If you have any
questions in the process, please do not hesitate to ask us.

Please note that we have a `Code of Conduct`_ in place that applies to all project contributions, including issues,
pull requests, etc.

License
-------

Copyright 2017 Raphael Michel

Released under the terms of the GNU General Public License v3.0.

.. _pretix: https://github.com/pretix/pretix
.. _Code of Conduct: https://docs.pretix.eu/en/latest/development/contribution/codeofconduct.html
