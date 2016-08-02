******************************
Pyramid/React Learning Journal
******************************

This package implements a multi-user learning journal using the `Pyramid <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_ web framework.
The front-end will evolve to be implemented with `ReactJS <https://facebook.github.io/react/>`_.

The journal features user authentication via GitHub, with whitelisting via configuration.

Installation
============

Some rough notes on getting this up and running.

Pyramid Application
-------------------

.. code-block:: bash

    $ git clone git@github.com:cewing/pyramid-react-journal.git
    $ cd pyramid-react-journal
    $ python3 -m venv ./
    $ . bin/activate
    (pyramid-react-journal)$ pip install -r requirements.pip
    ...
    $ pip install -e .
    ...
    $ bin/pserve development.ini

React Application and CSS
-------------------------

.. code-block:: bash

    $ npm install
    ...
    $ gulp

Deployment
==========

This application comes with an ansible-based deployment strategy.

* Begin by installing `ansible <https://www.ansible.com/>`_ (note that ansible is **not** compatible with Python 3 as of this writing).
* Set up a remove server of your choice.  The configuration for ansible is slanted toward using an Ubuntu 14.04 instance on AWS, but that is not a strict requirement.
* ensure that you have set the ``hosts`` property in ``ansible/playbook.yml`` properly.
* verify the host vars for your host. Standard vars for an AWS Ubuntu deployment are in ``ansible/group_vars/tag_Name_Class_Learning_Journal.yml``.

The to execute the deployment playbook, run:

.. code-block:: bash

    $ ansible-playbook -i <your inventory file> playbook.yml

For the standard deployment (AWS, Ubuntu 14.04), the incantation uses an EC2 dynamic inventory script, and looks like this:

.. code-block:: bash

    $ ansible-playbook -i plugins/inventory/ playbook.yml
