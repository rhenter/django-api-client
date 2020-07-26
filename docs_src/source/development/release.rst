Release
-------

To release a new version, a few steps are required:

* Add entry to ``CHANGES.rst`` following the same standard

Example:

.. code-block:: rst

  0.1.0
  -----

  - What was changed


* Review changes in test requirements ``requirements.txt``

* Commit and push changes

* Run the Release command that will run the tests, build the code and upload to Pypi.

.. code-block:: bash

    $ make release
