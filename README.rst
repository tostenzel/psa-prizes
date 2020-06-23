==========
psa-prizes
==========

.. image:: https://badge.fury.io/py/psa-prizes.svg
  :target: https://pypi.org/project/psa-prizes

.. image:: https://github.com/tostenzel/psa-prizes/workflows/Continuous%20Integration/badge.svg?branch=master
  :target: https://github.com/tostenzel/psa-prizes/actions

.. image:: https://readthedocs.org/projects/psa-prizes/badge/?version=latest
   :target: https://psa-prizes.readthedocs.io/en/latest/?badge=latest

.. image:: https://codecov.io/gh/tostenzel/psa-prizes/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/tostenzel/psa-prizes

.. image:: https://app.codacy.com/project/badge/Grade/8b4d19500d434a18a899405d71d2654e
   :alt: Codacy Badge
   :target: https://app.codacy.com/manual/tostenzel/psa-prizes?utm_source=github.com&utm_medium=referral&utm_content=tostenzel/psa-prizes&utm_campaign=Badge_Grade_Dashboard

About
=====

PSA-prizes is a Python package for simple prize analyses of PSA-graded trading cards.

`PSA <https://www.psacard.com>`_ (Professional Sports Authenticator) grades the authenticity and condition of sport cards, such as baseball and basketball, and cards from TCGs (trading card games) like Magic, Yu-Gi-Oh! and Pokémon. These `grades <https://www.psacard.com/resources/gradingstandards#cards>`_ provide credible categories for these sensible collectibles in which prizes can be compared.

Features
========

Web Scraping
------------

- Scrape the comprehensive data recorded by PSA on public sales of certified cards from the `Auction Prizes <https://www.psacard.com/auctionprices/>`_ register on their website

Basic Analysis
--------------

- Compute the compound annual growth rate (CAGR) and numbers on the grade distribution, record unusual grade types and plot the prizes over time

Installation
============

Clone the package to a local directory:

.. code:: console

    $ git clone https://github.com/tostenzel/psa-prizes

Install the dependency manager `Poetry <https://github.com/python-poetry/poetry>`_ by downloading and running get-poetry.py:

.. code:: console

    $ python get-poetry.py

Change directory to psa-prizes and install dependencies:

.. code:: console

    $ cd psa_prizes
    $ poetry install

Example
=======

Specify the cards and grades of interest in ``input/input.csv`` (`Click <https://github.com/tostenzel/psa-prizes/blob/master/input/input.csv>`_ for an example):

 - Paste the respective `item link <https://www.psacard.com/auctionprices>`_ in the first column
 - Write the respective grades to the second column as a list in Python syntax.

If you write in the file through a GUI-based program, make sure to keep **;** as the only column delimeter.

Run psa-prizes:

.. code:: console

    $ poetry run psa-prizes

Documentation
=============

The documentation is hosted on `rtd <https://psa-prizes.readthedocs.io/en/latest>`_.
