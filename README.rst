.. |bender-skype| replace:: **bender-skype**

.. _bender: https://github.com/bender-bot/bender

============
Bender-Skype
============

.. image:: http://img.shields.io/travis/bender-bot/bender-skype.svg?style=flat
    :target: https://travis-ci.org/bender-bot/bender-skype
    :alt: Build status

Using Skype as `bender`_ backbone.

Requirements
============

* `bender`_
* Skype up and running

Install
=======

To install |bender-skype| all it takes is one command line::

    pip install bender-skype

Usage
=====

Initialize `bender`_ with |bender-skype|::

    bender --backbone skype

It will connect to current Skype instance. Anyone chatting to this account now can use `bender`_.
