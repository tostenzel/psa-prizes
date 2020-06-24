=======
Summary
=======

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


Install the dependency manager `Poetry <https://github.com/python-poetry/poetry>`_:

.. code:: console

    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

Change directory to ``/psa-prizes/`` and install dependencies:

.. code:: console

    $ cd psa_prizes
    $ poetry install

Example
=======

Specify the cards and grades of interest in ``/input/input.csv`` (`Click <https://github.com/tostenzel/psa-prizes/blob/master/input/input.csv>`_ for an example):

 - Paste the respective `item link <https://www.psacard.com/auctionprices>`_ to the first column
 - Write the respective grades to the second column as a list in Python syntax

If you write in the file through a GUI-based program, make sure to keep **;** as the only column delimeter.

Run *PSA-prizes*:

.. code:: console

    $ poetry run psa-prizes

Data, information and plots are saved to ``/output/``. Additionally, the information is printed to the terminal and the plot is pictured for each card-grade pair. An example output is shown below.

.. code:: console

    – The compound annual growth rate from 2016 to 2020 is 61.13%.
    – The number of cards with grade 8.0 is 119 of 562 cards. That is 21.17%.
    – Over all grades, 6 of 562 cards do not receive standard grades. These grades are in {'Authentic', 'nan'}


.. raw:: html

    <p align="center">
    <img src="../pokemon-game-charizard-holo-1st-edition-grade-8.0.png" height="450px">
    </p>