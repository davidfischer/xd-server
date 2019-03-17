Crossword Analyzer Server
=========================

A server for storing and analyzing crossword puzzles.


Usage
-----

Install requirements

::

    pip install -r requirements.txt


Running the server locally

::

    ./manage.py runserver


Import a crossword in XD format (the publisher must be known)

::

    ./manage.py importxd /path/to/*.xd


Todo list
---------

* Show some basic statistics about the known crosswords
  such as the count by publisher, the most common clues and answers,
  and the most prolific authors.
* Allow uploading crosswords and find similar ones
* Separate settings for dev and prod
* Handle Rebus crosswords
