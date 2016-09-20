.. image:: https://travis-ci.org/quiltdata/python-api.svg?branch=master
    :target: https://travis-ci.org/quiltdata/python-api
Python
======

The Quilt Python connector uses the Quilt REST API and SQL Alchemy
(http://docs.sqlalchemy.org/), if installed, to access and update data
sets in Quilt. Quilt tables are available as dictionaries or Pandas
(http://pandas.pydata.org/) DataFrames.

The Quilt Python connector is available via PyPI:
https://pypi.python.org/pypi/quilt

.. code:: python

    pip install quilt


Connection
----------

To use the Quilt Python connector, add this repository to your
PYTHONPATH and import quilt.

Connect to Quilt by creating a Connection object:

.. code:: python

    import quilt
    connection = quilt.Connection(username)
    Password: *enter your password*

The connection will contain a list of your Quilt tables:

.. code:: python

    connection.tables

Search for Data Sets
~~~~~~~~~~~~~~~~~~~~

You can also find tables by searching your own tables and Quilt’s public
data sets

.. code:: python

    connection.search('term')

Get Table
~~~~~~~~~

Get a table by Table id using get\_table:

.. code:: python

    t = connection.get_table(1234)

Create a New Table
~~~~~~~~~~~~~~~~~~

Using the connection, you can create new tables in Quilt. To create an
empty table:

.. code:: python

    t = connection.create_table(name, description)

To create a table from an input file:

.. code:: python

    t = connection.create_table(name, description, inputfile=path_to_input_file)

Or, to create a new table from a DataFrame:

.. code:: python

    t = connection.save_df(df, name, description="table description")



Table
-----

Each Table object has a list of Columns

.. code:: python

    mytable.columns

After the columns have been fetched, columns are available as table
attributes.

.. code:: python

    mytable.column1

Accessing Table Data
~~~~~~~~~~~~~~~~~~~~

Tables are iterable. To access table data:

.. code:: python

    for row in mytable:
        print row

Search
^^^^^^

Search for matching rows in a table by calling search.

.. code:: python

    for row in mytable.search('foo'):
        print row

Order By
^^^^^^^^

Sort the table by any column or set of columns. You can set the ordering
by passing a string that is the column’s field (name in the database).

.. code:: python

    mytable.order_by('column1')

You can find column field names with their “.field” attribute:

.. code:: python

    mytable.order_by(mytable.column1.field)

You can sort by multiple columns by passing a list of fields.

.. code:: python

    mytable.order_by(['column2', 'column1'])

To sort in descending order, add a “-” in front of the column field
name:

.. code:: python

    mytable.order_by('-column1')

Limit
^^^^^

Limit the number of rows returned by calling limit(number\_of\_rows).

Putting it all together
^^^^^^^^^^^^^^^^^^^^^^^

Search, order\_by and limit can be combined to return just the data you
want to see. For example, to return the top 2 finishers with the name
Sally from a table of race results (race\_results: [name\_000,
time\_001]), you could write:

.. code:: python

    for result in race_results.search('Sally').order_by('-time_001').limit(2):
        print row

Pandas DataFrame
~~~~~~~~~~~~~~~~

Access a table’s data as a Pandas DataFrame by calling mytable.df()

You can also combine the querying methods above to access particular
rows.

.. code:: python

    race_results.search('Sally').order_by('-time\_001').limit(2).df()

Gene Math
~~~~~~~~~

Quilt supports intersect and subtract for tables that store genomic
regions. Those operations assume that tables have columns storing:
Chromsome, start and end. The function get\_bed\_cols tries to infer
those columns based on column names.

If the guessing fails, or to override the guess, set the chromosome,
start, end columns explicitly with set\_bed\_cols.
mytable.set\_bed\_cols(mytable.chr\_001, mytable.start\_002,
mytable.end\_003)

Once the bed columns are set for both tables, they can be intersected
and subtracted.

.. code:: python

    result = tableA.intersect(tableB)
    result = tableA.intersect_wao(tableB)
    result = tableA.subtract(tableB)

Convert files to live data sets on Quilt
========================================

Optional prep (your steps may vary)
-----------------------------------

#. Get a list of files you want to upload (see ``get-files-to-upload/``)
#. Download the files in the list (see ``curl-all.py``)
#. Unzip downloaded files (if needed)

   .. code:: bash

       cd downloads
       gunzip *.gz

#. | Use ``data_set.py`` to create data sets on Quilt (see
     ``python data_set.py --help``).
   | You will need a Quilt username and password. Or use ``batch.py`` to
     create multiple data sets.

   .. code:: bash

       python data_set.py
         -e https://quiltdata.com
         -u USERNAME
         -n "ENCODE data"
         -d "#A549 #histone peak data #hg19"
         -f downloads/wgEncodeBroadHistoneNhaH3k36me3StdPk.broadPeak

File formats in this example
----------------------------

-  `ENCODE broadPeak format <https://genome.ucsc.edu/FAQ/FAQformat.html#format13>`_

Resources
---------

-  `ENCODE Project <https://www.encodeproject.org/>`_


Development
-----------

Python 2.7 tests in-progress. Tests run with:

.. code:: python

    pip install -r requirements.text
    pip install pytest
    pytest tests
