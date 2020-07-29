Documentation
=============

Update or Add Documentation
---------------------------

To add new or update the documentation, you must to add or change the files in RST format located on ``docs_src/source``

Note:
  If you add anything new, make sure you add the reference in the ``docs_src/source/index.rst``


Update the translation
----------------------

Today we have 2 translations, being ``en`` (english) and ``pt_BR`` Portuguese, if you want to add one more,
just add the prefix of the language that will be generated or updated in located in ``docs_src/source/locale/``

* Generate new blocks to update

.. code-block:: bash

    $ cd docs_src
    $ make gettext
    $ sphinx-intl update -p build/gettext -l pt_BR -l en


* Update the .po files in ``docs_src/source/locale/ LANGUAGE /LC_MESSAGES/``

Example:

.. code-block:: text

    #: ../../source/index.rst:28
    msgid "User Guide"
    msgstr "Guia do Usuário"


Note:
  The .mo file will be generated when you generate the HTML files

Generating documentation
------------------------

The project use GitHub pages, so all HTML files must be locate on /doc

.. code-block:: bash

    $ cd docs_src
    $ sphinx-build -b html source ../docs/en -D language='en'
    $ sphinx-build -b html source ../docs/pt-br -D language='pt_BR'
