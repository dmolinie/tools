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

* ``create_html_anchor``  
        Take an anchor name and wrap it into an HTML anchor element.

* ``is_html_anchor``  
        Check that a string is an HTML anchor.

* ``split_md_toc_entry``  
        Split a Markdown TOC entry into its title and its anchor.

* ``build_md_with_toc``  
        Build the TOC of a Markdown file.

* ``create_md_toc_entry``  
        Take a set of (anchor, title) and rewrite into a Markdown TOC entry.

* ``write_md_with_toc``  
        Write a text and its TOC in a Markdown file.

* ``add_toc_to_md``  
        Open a Markdown file, add HTML anchors to above sections, build the new TOC and write the updated file (TOC, text and anchors).

..
  _bibtex.py.

* ``sort_bibtex``  
        Reorganize a BibTeX file in a standardized manner.

