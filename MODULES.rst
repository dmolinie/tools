Tools package's modules, functions & classes
++++++++++++++++++++++++++++++++++++++++++++

This file aims to summarize all the objects implemented in the ``tools`` package; to this purpose, it briefly introduces the modules of the package, as well as their respective functions.

.. Contents::


root
====
General purpose functions to handle files, text, Markdown, BibTeX, etc.

..
  _text.py.

* ``strip_str_punctuation``
        Remove punctuation (', ", ;, !, %, (), [], {}, ...) from a string.

* ``strip_str_symbols``
        Remove symbols (+, =, ~, $, €, ...) from a string.

* ``strip_str_accents``
        Remove the accents from the characters of a string.

* ``strip_str``
        Keep only letters, numbers, spaces, hyphens and apostrophes in a string.

* ``add_str_suffix``
        Append a string to another, while keeping the any trailing '\n'.

* ``str_to_anchor_name``
        Normalize a string to a standard anchor name.

* ``anchor_name_to_str``
        Take an anchor and convert it to a human-readable string.

* ``read_file``
        Read and load the content of a file.

* ``write_file``
        Write a set of lines into a file.

..
  _markdown.py.

* ``check_html_anchor``
        Check that a string is an HTML anchor.

* ``create_html_anchor``
        Take an anchor name and wrap it into an HTML anchor element.

* ``check_pandoc_anchor``
        Check that a string contains a Pandoc anchor.

* ``create_pandoc_anchor``
        Take an anchor name and wrap it into an HTML anchor element.

* ``clean_md_anchors``
        Remove the TOC, HTML and Pandoc anchors from Markdown content.

* ``check_md_sec_depth``
        Check that a string is a Markdown section and that its level is lower than a certain depth.

* ``get_md_list_level``
        Get the level of a Markdown list entry.

* ``get_md_sec_level``
        Get the level of a Markdown section title.

* ``check_md_toc_entry``
        Check that a string is a Markdown TOC entry.

* ``create_md_toc_entry``
        Take a set of (anchor, title) and rewrite into a Markdown TOC entry.

* ``extract_md_section_title``
        Extract the title of a Markdown section.

* ``build_md_with_toc``
        Build the TOC from the content of a Markdown document.

* ``write_md_with_toc``
        Write a Markdown text content and its TOC in a file.

* ``add_toc_to_md``
        Open a Markdown file, add anchors and links to its sections, build the new TOC and write the updated file (TOC, text, anchors and links).

..
  _bibtex.py.

* ``sort_bibtex``
        Reorganize a BibTeX file in a standardized manner.

