Installing the Tools package
++++++++++++++++++++++++++++

.. Contents::


Prerequisites
=============

The ``tools`` package requires the following software:

1) **Python** 3.8.x or newer.

**Python** https://www.python.org/


Installation
============

Except the optional packages specified below, the ``tools`` project relies on standard Python libraries only. The project's modules that depend on packages that are not installed on the system will not appear as tab-completion options (but may still be accessed via direct call).


Basic Installation
------------------

To install the ``tools`` package, when in the installation folder, run the following command:

.. code-block:: sh

   pip install .

This will compile the package's sources and install them into the active environment (e.g. "site-packages").


Additional Packages
-------------------

The package includes a function to reorganize BibTeX files using the ``bibtexparser`` package; to install it, run the command:

.. code-block:: sh

   pip install .[bibtex]

This will download and install the ``bibtexparser`` package in addition to the current ``tools`` package.
