""" Simple functions to handle Markdown files

Authors: Dylan MOLINIE
Contact: dylan.molinie@gmx.fr
Date: October 2026
Last revised: October 2026

License: GPLv3
"""

__all__ = [
    'check_html_anchor', 'create_html_anchor',
    'check_pandoc_anchor', 'create_pandoc_anchor',
    'clean_md_anchors', 'check_md_sec_depth',
    'get_md_list_level', 'get_md_sec_level',
    'check_md_toc_entry', 'create_md_toc_entry',
    'extract_md_section_title', 'build_md_with_toc',
    'write_md_with_toc', 'add_toc_to_md']

from pathlib import Path

from tools._text import (
    str_to_anchor_name, anchor_name_to_str, add_str_suffix, read_file)

# Default reference for Back-to-Top links
__TOP_RET = " [↑](#top)"


##############################################################################
##                      Anchor Manipulation Functions                       ##
##############################################################################

def check_html_anchor(string, return_anchor=False):
    """ Check that a string is an HTML anchor

    An HTML anchor has format:
        ``<a name='`anc-name`'></a>``

    Check that `string` contains the '<a' and '</a>' substrings; if so,
    return True, or False else. If `return_anchor` is set to True, find
    the anchor's name (the above example `anc-name` tag) and return it;
    return an empty string if such tag is not found.

    Parameters
    ----------
    string : str
        The string to check.
    [OPT] return_anchor : bool, defaults to False
        If False, return a Boolean indicating that `string` is an HTML
        anchor or not; if True, return the `name` tag of the anchor, or
        an empty string if it is not an HTML anchor.

    Returns
    -------
    anchor : bool if `return_anchor` is False, str else
        If `string` is an HTML anchor:
            { True (bool)           if `return_anchor` is False
            { `name` tag (str)      else
        else:
            { False (bool)          if `return_anchor` is False
            { '' (empty str)        else

    Examples
    --------
    # Check a simple HTML anchor
    >>> check_html_anchor("<a name='title'></a>", False)
    True
    >>> check_html_anchor("<a name='title'></a>", True)
    'title'

    # Create an HTML anchor and check it
    >>> title = "*White-Fang*, Jack London"
    >>> anchor = create_html_anchor(str_to_anchor_name(title))
    >>> check_html_anchor(anchor, False)
    True
    >>> check_html_anchor(anchor, True)
    'white-fang-jack-london'
    """

    # Search the first '<a' and last '</a>' substrings
    a, b = string.find('<a'), string.rfind('</a>')
    # Check that the string is an HTML anchor
    check = a != -1 and b != -1 and a < b

    # Return a Boolean as the `check` result
    if not return_anchor:
        return check

    # Return a string as the `name` tag of the HTML anchor
    if check:
        # Extract the substring between 'name' and first '>'
        name = string[string.find('name')+4:string.find('>')].strip(' ')
        # Remove the '=' mark and the surrounding spaces, if any
        name = name.lstrip('=').lstrip(' ')
        # Remove the opening and closing quotation marks
        return name[1:-1]

    # The string is not an HTML anchor
    return ''

def create_html_anchor(name):
    r""" Take an anchor name and wrap it into an HTML anchor element

    An HTML anchor has format:
        ``<a name='`name`'></a>``

    Take the `name` argument and wrap it around the above anchor syntax.

    Parameters
    ----------
    name : str
        The name of the anchor.

    Returns
    -------
    anchor : str
        The HTML-formatted anchor.

    Examples
    --------
    >>> create_html_anchor('title')
    "<a name='title'></a>\n"

    # Build an anchor from a full string
    >>> title = "*White-Fang*, Jack London"
    >>> anchor_name = str_to_anchor_name(title)
    >>> create_html_anchor(anchor_name)
    "<a name='white-fang-jack-london'></a>\n"
    """
    return f"<a name='{name}'></a>\n"

def check_pandoc_anchor(string, return_entry=False):
    """ Check that a string contains a Pandoc anchor

    A Pandoc anchor has format:
        ``Section title {#anc-name}``

    Check that `string` contains the '{', '#' and '}' characters; if so,
    return True, or False else. If `return_entry` is set to True, find
    the anchor's name (`anc-name` in the example above), and return a
    1-item dictionary whose key is this anchor and whose value is the
    rest of the string, subtracted by the anchor (`Section title` in
    the above example); return an empty dictionary if no anchor found.

    Parameters
    ----------
    string : str
        The string to check.
    [OPT] return_entry : bool, defaults to False
        If False, return a Boolean indicating that `string` contains a
        Pandoc anchor or not; if True, return a dictionary whose key is
        the anchor's name and the value is the rest of the string, or
        return an empty dictionary else.

    Returns
    -------
    anchor : bool if `return_entry` is False, dict else
        If `string` contains a Pandoc anchor:
            { True (bool)               if `return_entry` is False
            { {anchor: title} (dict)    else
        else:
            { False (bool)              if `return_entry` is False
            { {} (empty dict)           else

    Examples
    --------
    # Check a simple Pandoc anchor
    >>> check_pandoc_anchor("# Document title {#anchor}", False)
    True
    >>> check_pandoc_anchor("# Document title {#anchor}", True)
    {'anchor': '# Document title'}

    # Check a string with text after the Pandoc anchor
    >>> check_pandoc_anchor("# Document {#anchor} title", True)
    {'anchor': '# Document title'}
    """

    # Search the last '{', '#' and '}' characters
    a, b, c = string.rfind('{'), string.rfind('#'), string.rfind('}')
    # Check that the string contains a Pandoc anchor
    check = a != -1 and b != -1 and c != -1 and a < b < c

    # Return a Boolean as the `check` result
    if not return_entry:
        return check

    # Return a dict as {anchor: rest_of_string}
    if check:
        # Retrieve the anchor's name
        anc = string[b+1:c].strip()
        # Remove the anchor's name from the string
        sec = string[:a].strip(' ') + string[c+1:]
        # Build the dictionary
        return {anc:sec.rstrip(' ')}

    # The string is not a Pandoc anchor
    return {}

def create_pandoc_anchor(title, name):
    r""" Take an anchor name and wrap it into an HTML anchor element

    A Pandoc anchor has format:
        ``Section title {#anc-name}``

    Wrap the `name` argument into a Pandoc anchor and append it to the
    `title` argument using the `add_str_suffix` function. The returned
    string is: '`title` {#`name`}', with a space between the two items.

    Parameters
    ----------
    title : str
        The base string to which add the Pandoc anchor.
    name : str
        The name of the anchor.

    Returns
    -------
    title_pandoc : str
        The Pandoc-formatted sentence.

    Examples
    --------
    # Simple title with its anchor
    >>> create_pandoc_anchor('Title', 'anc-name')
    'Title {#anc-name}'

    # Title with a trailing line-breaking '\n'
    >>> create_pandoc_anchor('Section title\n', 'anc-name')
    'Section title {#anc-name}\n'
    """
    return add_str_suffix(title, ' {#' + name + '}')

##############################################################################



##############################################################################
##                     Markdown Manipulation Functions                      ##
##############################################################################

def clean_md_anchors(lines, toc=True, html=True, pandoc=True, backtop=True):
    r""" Remove the TOC, HTML and Pandoc anchors from Markdown content

    Take the content of a Markdown document, wrapped line by line in a
    list, and possibly remove the Table of Contents, the HTML anchors,
    the Pandoc anchors and the back-to-top references. For the two last
    ones, remove only the anchors and references while keeping the rest
    of the lines. Any other line is left unchanged.

    Parameters
    ----------
    lines : list of str
        The Markdown text content, one line per item.
    [OPT] toc : bool, defaults to True
        If the Table of Contents should be removed.
        See the `create_md_toc_entry` function.
    [OPT] html : bool, defaults to True
        If the HTML anchors should be removed.
        See the `create_html_anchor` function.
    [OPT] pandoc : bool, defaults to True
        If the Pandoc anchors should be removed.
        See the `create_pandoc_anchor` function.
    [OPT] backtop : bool, defaults to True
        If the back-to-top references should be removed.
        See the `top_returns` option of the `build_md_with_toc` function.

    Returns
    -------
    text : list of str
        The content of the Markdown file with the TOC, anchors and back-
        to-top references removed, with respect to the optional arguments.

    Examples
    --------
    >>> lines = [
    ...     "<a name='top'></a>\n",
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "- [Section 1](#section-1)\n",
    ...     "- [Section 2](#section-2)\n",
    ...     "- [Section 3](#section-3)\n",
    ...     "\n",
    ...     "<a name='section-1'></a>\n",
    ...     "## Section 1\n",
    ...     "Some text\n",
    ...     "\n",
    ...     "## Section 2 {#section-2}\n",
    ...     "Some text\n",
    ...     "\n",
    ...     "## Section 3 [↑](#top)\n",
    ...     "Some text\n"]

    >>> clean_md_anchors(lines)
    ['# TITLE OF THE MARKDOWN\n',
     '\n',
     '\n',
     '## Section 1\n',
     'Some text\n',
     '\n',
     '## Section 2\n',
     'Some text\n',
     '\n',
     '## Section 3\n',
     'Some text\n']
    """

    text = []
    for line in lines:

        # Remove (skip) the TOC entries
        if toc and check_md_toc_entry(line, False):
            continue

        # Remove (skip) the HTML anchors
        if html and check_html_anchor(line, False):
            continue

        # Remove the Pandoc anchors (but keep the rest of the line)
        pan = check_pandoc_anchor(line, True)
        if pandoc and pan:
            line = pan.popitem()[1]

        # Remove the back-to-top references (but keep the rest of the line)
        if backtop:
            line = line.replace(__TOP_RET, '')

        # Append the line to the valid ones
        text.append(line)

    return text

def check_md_sec_depth(line, depth):
    """ Check that `line` is a Markdown section (make sure it is stripped
    from spaces before) and that the number of heading '#' is <= `depth`

    Parameters
    ----------
    line : str
        The line to test. If it is a section, make sure it starts with
        heading '#' and not spaces (it must be stripped prior).
    depth : int
        The maximal allowed section depth.

    Returns
    -------
    check : bool
        True if `line` has at most `depth` heading '#'; False else.

    Examples
    --------
    >>> check_md_sec_depth("## Section title", 1)
    False
    >>> check_md_sec_depth("## Section title", 2)
    True
    """
    return line.startswith('#', 0, 1) and len(line)-len(line.lstrip('#')) <= depth

def get_md_list_level(line):
    r""" Get the level of a Markdown list entry

    To increase the level of an entry, it should be added four heading
    spaces '    ' or a tabulation '\t'. To get the depth of the list
    entry `line`, count the number of heading sets of four spaces or
    the number of tabulations. Take the maximum between the two values.

    Parameters
    ----------
    line : str
        The Markdown list entry to test.

    Returns
    -------
    level : int
        The level of the list entry `line`.

    Examples
    --------
    >>> level = get_md_list_level("- Entry")            # 0
    >>> level = get_md_list_level("    - Entry")        # 1
    >>> level = get_md_list_level("        - Entry")    # 2
    >>> level = get_md_list_level("\t- Entry")          # 1
    >>> level = get_md_list_level("\t\t- Entry")        # 2
    """
    return max((len(line) - len(line.lstrip('    '))) //4,
                len(line) - len(line.lstrip('\t')))

def get_md_sec_level(line, offset=1):
    r""" Get the level of a Markdown section title

    The level of a Markdown title is defined by the number of heading '#';
    find how many they are to get the section level of `line`. Since
    numbering starts from 1 (one '#' is the Markdown title), subtract
    `offset` from the number of heading '#' to start from any value.

    Parameters
    ----------
    line : str
        The Markdown section title to test.
    [OPT] offset : int, defaults to 1
        The value by which to subtract the number of heading '#' found
        in `line`, so that '##' can be considered as level 0 for instance.

    Returns
    -------
    level : int
        The level of the section title `line`.

    Examples
    --------
    >>> level = get_md_sec_level("# Title", 0)      # 1
    >>> level = get_md_sec_level("# Title", 1)      # 0
    >>> level = get_md_sec_level("## Section", 0)   # 2
    >>> level = get_md_sec_level("## Section", 2)   # 0
    """
    line = line.strip()
    return len(line) - len(line.lstrip('#')) - offset

def check_md_toc_entry(line, return_entry=False):
    r""" Check that a line is a Markdown TOC entry

    A Markdown TOC entry has format:
        ``- [Title](#anchor)``

    First, check that `line` starts with a number or symbol in list:
    (1, ..., 9, -, +, *, [); then, check that it contains the '(', '#'
    and ')' characters; if so, return True, or return False else. If
    `return_entry` is set to True, find the anchor's name (`anchor` in
    the example above) and return a 1-item dictionary whose key is this
    anchor and whose value is a tuple organized as the text of the TOC
    entry (`Title` in the example above) and the list depth (given by
    the `get_md_list_level` function); return an empty dictionary if
    no anchor is found.

    Parameters
    ----------
    line : str
        The Markdown TOC entry line.
    [OPT] return_entry : bool, defaults to False
        If False, return a Boolean indicating that `line` is a TOC entry
        or not; if True, return a 1-item dictionary whose key is the name
        of the anchor and the value is a tuple of the rest of the line and
        the level of the list entry; return an empty dictionary else.

    Returns
    -------
    anchor : bool if `return_entry` is False, dict else
        If `line` is a TOC entry:
            { True (bool)                       if `return_entry` is False
            { {anchor: (title, depth)} (dict)   else
        else:
            { False (bool)                      if `return_entry` is False
            { {} (empty dict)                   else

    Returns
    -------
    entry : dict
        The TOC entry; the anchor is used as a key, and the 2-tuple
        (title, depth) as value. Both `anchor` and `title` are str,
        and `depth` is an int.

    Examples
    --------
    # Check that a string is a TOC entry
    >>> check_md_toc_entry("- [*White-Fang*](#white-fang)\n")
    True

    # Get the anchor, title and depth
    >>> check_md_toc_entry("- [*White-Fang*](#white-fang)\n", True)
    {'white-fang': ('*White-Fang*', 0)}

    # TOC entry of level 1
    >>> check_md_toc_entry("    - [*White-Fang*](#white-fang)\n", True)
    {'white-fang': ('*White-Fang*', 1)}
    """

    # A TOC entry is a list entry that starts with a number or a symbol
    # (1, 2, ..., 9, -, +, *); if it starts with '[', it may be a reference,
    # e.g. '[link](#anc)'
    check = line.strip().startswith((*'0123456789', *'-+*', '['), 0, 1)

    # Search the last '(', '#' and ')' characters
    a, b, c = line.rfind('('), line.rfind('#'), line.rfind(')')
    # Check that the line is a TOC entry
    check = check and a != -1 and b != -1 and c != -1 and a < b < c

    # Return a Boolean as the `check` result
    if not return_entry:
        return check

    if check:
        # Anchor between (#...) and Title between [...]
        return {line[b+1:c].strip():
                (line[line.find('[')+1:line.rfind(']')], get_md_list_level(line))}

    # The line is not a TOC entry
    return {}

def create_md_toc_entry(anchor, title, depth=0):
    r""" Take a set of (anchor, title) and rewrite it as a Markdown TOC entry

    A Markdown TOC entry has format:
        ``- [`title`](#`anchor`)``

    To increase the depth of the list entry, heading sets of four spaces
    must be added at the beginning of the string; add `depth` such sets.

    Parameters
    ----------
    anchor : str
        The name of the anchor.
    title : str
        The title of the TOC entry.
    [OPT] depth : int, defaults to 0
        The level of the list, i.e. the number of heading sets of four
        spaces added at the very beginning of the TOC entry.

    Returns
    -------
    toc_entry : str
        The TOC entry that can be written in the Markdown file.

    Examples
    --------
    # Generate a title and an anchor
    >>> title = "*White-Fang*, Jack London"
    >>> print(anchor := str_to_anchor_name(title))
    white-fang-jack-london

    # Build a TOC entry (no depth)
    >>> create_md_toc_entry(anchor, title)
    '- [*White-Fang*, Jack London](#white-fang-jack-london)\n'

    # Build a TOC entry (with depth)
    >>> create_md_toc_entry(anchor, title, 1)
    '    - [*White-Fang*, Jack London](#white-fang-jack-london)\n'
    """
    return f"{'    '*depth}- [{title}](#{anchor})\n"

def extract_md_section_title(line):
    """ Extract the title of a Markdown section

    A Markdown section title has format:
        ``#[#...#] Title [{#pandoc-ref}]``

    Remove the left-side '#' from `line` and its Pandoc anchor, if any,
    and strip the resulting string from surrounding spaces.

    N.B.: `line` must be stripped from spaces (it must start with '#').

    Parameters
    ----------
    line : str
        The section line for which to extract the title.

    Returns
    -------
    title : str
        The section's title.

    Examples
    --------
    # Extract the titles from regular sections
    >>> extract_md_section_title("## Section Title")
    'Section Title'
    >>> extract_md_section_title("### Subsection Title {#reference}")
    'Subsection Title'

    # The title must be stripped from spaces prior
    >>> extract_md_section_title("  ## Section Title")
    '## Section Title'
    >>> extract_md_section_title("  ## Section Title".lstrip())
    'Section Title'
    """
    # Remove the heading '#' from the title
    line = line.lstrip('#')
    # Remove the Pandoc anchor, if any
    if pan:=check_pandoc_anchor(line, True):
        line = pan.popitem()[1]
    # Remove the heading and trailing spaces left
    return line.strip()

def build_md_with_toc(lines, depth=2, top_returns=True, pandoc=False):
    r""" Build the TOC from the content of a Markdown document

    Take the content of a Markdown document, retrieve its existing TOC
    (cf. the `check_md_toc_entry` function), and rebuild the text line
    by line as follows:
      - if a line is a section (cf. function `extract_md_section_title`),
        if it already has an anchor attached to it (either an HTML ele-
        ment placed in the line right before or after, or a Pandoc tag),
        check if it already has an entry in the TOC; if so, retrieve it;
        if not, create an anchor from the section's title, and add a TOC
        entry for it. The newly created anchor is either an HTML element
        placed in the line right before the section if `pandoc` option
        is False, or a Pandoc tag appended to the section's title else.
      - if a line is an HTML anchor (cf. function `check_html_anchor`),
        if it already has an entry in the TOC, retrieve it; else, if it
        is not directly preceded or followed by a section, build a title
        from its name (cf. function `anchor_name_to_str`) and add a TOC
        entry for it. This case aims to handle the lone HTML anchors.

    Use the `depth` option to specify the depth of the TOC; this value
    sets the maximum number of `#` symbols a section should start with
    to get an entry in the TOC. For instance, `depth=2` includes only
    the sections ('##'), whilst `depth=3` includes both sections ('##')
    and subsections ('###'). The Markdown title ('#') is always ignored.

    Use the `pandoc` option to use either HTML anchor elements, added as
    separate lines right above the section titles, or Pandoc anchor tags,
    appended to the section titles, on the same line. The Pandoc anchors
    are shorter, but are not supported by any Markdown rendering engines;
    on the contrary, the HTML anchors are almost always supported.

    In addition, if the `top_returns` option is True, add an anchor at
    the top of the text content, and append back-to-top links that lead
    to this anchor to any sections that got a TOC entry. If there is a
    document title ('#'), the newly added top anchor follows the `pandoc`
    option; else, it is an HTML anchor that is added.

    Return the content text lines, updated with the newly added anchors
    and with the original TOC removed; return also the new TOC.

    Parameters
    ----------
    lines : list of str
        The Markdown text content, one line per item.
    [OPT] depth : int, defaults to 2
        The depth of the TOC; in practice, the maximum number of heading
        '#' symbols in a line for a section to get a TOC entry. The Mark-
        down title ('#') is always ignored; a value below 2 means no TOC.
    [OPT] top_returns : bool, defaults to True
        If True, append back-to-top references to the sections that got
        a TOC entry, and add an anchor at the very top of the document,
        that is a Pandoc anchor appended to the document title if the
        `pandoc` option is set to True, or an HTML anchor else or if
        there is no such document title. Do nothing if False.
    [OPT] pandoc : bool, defaults to False
        If True, use Pandoc anchors, appended to the sections that got
        a TOC entry; use HTML anchors else, placed before the sections.

    Returns
    -------
    text : list of str
        The text, line by line, of the reworked Markdown file, with the
        new anchors and links, and with its TOC removed. The other lines
        are left unchanged (paragraphs, comments, etc.).
    entry : dict
        The TOC entries; the anchors' names are used as keys, and the
        titles as values.

    Examples
    --------
    # Consider the Markdown content below; notice the `lone-anc-1` anchor
    # that has a TOC entry, that will be retrieved for the new TOC
    >>> lines = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "- [Lone Anchor 1](#lone-anc-1)\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text\n",
    ...     "<a name='lone-anc-1'></a>\n",
    ...     "\n",
    ...     "### Subsection 1.1\n",
    ...     "Some text\n",
    ...     "<a name='lone-anc-2'></a>\n"]

    # Include only the sections ('##'), add an anchor to the top of the
    # document and append links to it to the sections' titles
    >>> text, toc = build_md_with_toc(lines, depth=2, top_returns=True)

    >>> print(text)
    ["<a name='top'></a>\n",
     '# TITLE OF THE MARKDOWN\n',
     '\n',
     '\n',
     "<a name='section-1'></a>\n",
     '## Section 1 [↑](#top)\n',
     'Some text\n',
     "<a name='lone-anc-1'></a>\n",
     '\n',
     '### Subsection 1.1\n',
     'Some text\n',
     "<a name='lone-anc-2'></a>\n"]

    >>> print(toc)
    {'section-1': ('Section 1', 0),
     'lone-anc-1': ('Lone Anchor 1', 0),
     'lone-anc-2': ('Lone anc 2', 0)}
    """
    #pylint: disable=R0912,C0201

    def build_toc_entry(anc, line, old_toc):
        """ Take the name of an anchor, a section line and the dict. of
        the already-existing TOC entries; if this anchor already had an
        entry in the TOC, keep this entry; else, build an entry from the
        line (extract its title and its depth) """
        # Check that `anc` already had an entry in `old_toc`
        if anc in old_toc.keys():
            return old_toc.pop(anc)
        # Else, build a new entry from `line` (title + depth)
        if anc:
            return (extract_md_section_title(line), get_md_sec_level(line, 2))
        # Return an empty tuple else
        return ()

    def build_header(lines, top_returns, pandoc):
        """ Take a set of lines and the `top_returns` & `pandoc` options
        from the main function; first, skip the heading newlines; then,
        if `top_returns`, add an anchor as the first line of the content:
        if `pandoc`, append it to the title, or add an HTML anchor else """
        # Retrieve the `__TOP_RET` (global) anchor's name
        anc = check_md_toc_entry(__TOP_RET, True).popitem()[0]
        # Skip the heading newlines
        i = 0
        while len(lines[i]) < 2:
            i += 1
        # First line is an HTML or Pandoc anchor, so just retrieve it
        if lines[i].find(anc) != -1:
            return lines[i+1:], [lines[i]]
        # First line is the title, so create an anchor if `top_returns`
        if top_returns and lines[i][0] == '#' and lines[i][1] != '#':
            # Append a Pandoc anchor at the end of the line
            if pandoc:
                return lines[i+1:], [create_pandoc_anchor(lines[i], anc)]
            # Or create and add an HTML anchor before the title
            return lines[i+1:], [create_html_anchor(anc), lines[i]]
        # First line is neither an anchor nor a title, so add an HTML anchor
        # if `top_returns`, and add a newline before the rest of the text
        if top_returns:
            return ['\n']+lines[i:], [create_html_anchor(anc)]
        # Else, just skip the heading newlines
        return lines[i:], []

    # Already-existing TOC and new TOC to be built from the section titles
    old_toc, new_toc = {}, {}

    # Skip the heading newlines, and add an anchor (HTML or Pandoc) at the
    # very top of the content (`text`)
    lines, text = build_header(lines, top_returns, pandoc)

    # Add an item to ensure lines[i+1] always exists when accessing it from
    # a line that starts with '##' or that is an HTML anchor
    # (this additional cell is removed at the very end of the function)
    lines = lines.copy() + ['']

    for i, line in enumerate(lines):

        # Retrieve the current table of contents, if any
        if entry:=check_md_toc_entry(line, True):
            old_toc.update(entry)
            continue

        # Clean the current line for further testing (strip the spaces
        # and remove the possible back-to-top references)
        ltmp = line.replace(__TOP_RET, '').strip(' ')

        # If the line is a section whose depth should be included in the TOC
        if ltmp.startswith('##', 0, 2) and check_md_sec_depth(ltmp, depth):

            # If `top_returns`, append a back-to-top reference to the line
            if top_returns and line.find(__TOP_RET) == -1:
                line = add_str_suffix(line, __TOP_RET)

            # If the line already contains a Pandoc anchor
            if entry:=check_pandoc_anchor(ltmp, True):
                anc = entry.popitem()[0]
                new_toc[anc] = build_toc_entry(anc, ltmp, old_toc)
            # If the previous line is an HTML anchor
            elif anc:=check_html_anchor(lines[i-1], True):
                new_toc[anc] = build_toc_entry(anc, ltmp, old_toc)
            # If the next line is an HTML anchor
            elif anc:=check_html_anchor(lines[i+1], True):
                new_toc[anc] = build_toc_entry(anc, ltmp, old_toc)

            # If the section does not already have an anchor attached to it,
            # in the line directly above or below, build a new anchor
            else:
                title = extract_md_section_title(ltmp)
                anc = str_to_anchor_name(title)
                new_toc[anc] = (title, get_md_sec_level(ltmp, 2))
                # If `pandoc`, append the anchor to the current line
                if pandoc:
                    line = create_pandoc_anchor(line, anc)
                # Else, add an HTML anchor right before the current line
                else:
                    text.append(create_html_anchor(anc))

        # If the line is an HTML anchor (to avoid duplicates)
        elif anc:=check_html_anchor(ltmp, True):
            # If the anchor already is in the old TOC, retrieve its title
            if anc in old_toc.keys():
                new_toc[anc] = old_toc.pop(anc)
            # If the anchor is unknown, skip it if either the line directly
            # above or below is a section (handled in the `if` case); else,
            # rebuild a title from the anchor and add it to the new TOC
            elif not (lines[i-1].strip(' ').startswith('##', 0, 2)
                      or lines[i+1].strip(' ').startswith('##', 0, 2)):
                new_toc[anc] = (anchor_name_to_str(anc), 0)

        # Add the current line to those to write
        text.append(line)

#    # Append any remaining items in the old TOC to the new TOC
#    if old_toc:
#        new_toc.update(old_toc)

    # Remove the dummy [''] added prior
    return text[:-1], new_toc

def write_md_with_toc(filename, text, toc_entries):
    r""" Write a Markdown text content and its TOC in a file

    Skip the heading line breaking ('\n'); if the first non-empty line
    is an HTML anchor (to index the document top), write it; then, if
    the next line is the title (starting with a single '#'), write it.
    Then, add an empty line, write the TOC (every item of `toc_entries`
    is passed to the `create_md_toc_entry` function) and add two empty
    lines directly below; skip any additional empty lines until the next
    non-empty one, write any remaining item of `text` and close the file.

    N.B.: it is though to be fed with the outputs of `build_md_with_toc`.

    Parameters
    ----------
    filename : str
        The name of the Markdown file to write.
    text : list/tuple of str
        The text to write in the Markdown, one item per line.
    toc_entries : dict
        The entries of the TOC, as a dictionary whose keys are the names
        of the (HTML/Pandoc) anchors, and the values are the TOC titles.

    Returns
    -------
    None : directly write the Markdown file.

    Examples
    --------
    >>> text = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text\n",
    ...     "\n",
    ...     "## Section 2\n",
    ...     "Some text\n"]

    >>> toc_entries = {
    ...     'section-1': ("Section 1", 0),
    ...     'section-2': ("Section 2", 0)}

    >>> write_md_with_toc("file.md", text, toc_entries)

    # Cat command with IPython on GNU/Linux
    >>> !cat file.md
    # TITLE OF THE MARKDOWN

    - [Section 1](#section-1)
    - [Section 2](#section-2)


    ## Section 1
    Some text

    ## Section 2
    Some text
    """

    # Retrieve the `__TOP_RET` (global) anchor's name
    anc = check_md_toc_entry(__TOP_RET, True).popitem()[0]

    with open(filename, 'w', encoding='utf-8') as mdfile:

        # Skip the heading newlines
        i = 0
        while text[i] == '\n':
            i += 1

        # Write the anchor (HTML) to return to the top of the document, if any
        if text[i].find(f"name='{anc}'") != -1:
            mdfile.write(text[i])       # HTML anchor
            i += 1

        # Write the title of the Markdown document, if any
        if text[i].startswith('#', 0, 1):
            mdfile.write(text[i])       # Possibly with a Pandoc anchor
            i += 1

        # Add 1 empty line below the title (or at the very top of the file if
        # there is no title), write the TOC, and add two empty lines after
        mdfile.write('\n')
        for item in toc_entries.items():
            if isinstance(item[1], str):
                mdfile.write(create_md_toc_entry(item[0], item[1], 0))
            else:
                mdfile.write(create_md_toc_entry(item[0], item[1][0], item[1][1]))
        mdfile.write('\n\n')

        # Skip the empty lines between the TOC and the next line text
        while text[i] == '\n':
            i += 1

        # Write the rest of the file
        for line in text[i:]:
            mdfile.write(line)

def add_toc_to_md(filename, depth=3, top_returns=True, pandoc=False):
    r""" Open a Markdown file, add anchors and links to its sections,
    build the new TOC and write the updated file (TOC, text and anchors)

    Call the `read_file` function to read the `filename` Markdown file,
    add the anchors and build the new TOC with `build_md_with_toc`, and
    write in a new file the updated content with `write_md_with_toc`.
    See these three functions for details.

    The name of the new file is the base name (i.e. without extension)
    of `filename` appended with the '-toc' suffix.

    Parameters
    ----------
    filename : str
        The name of the Markdown file to read.
    [OPT] depth : int, defaults to 2
        The depth of the TOC; in practice, the maximum number of heading
        '#' symbols in a line for a section to get a TOC entry. The Mark-
        down title ('#') is always ignored; a value below 2 means no TOC.
    [OPT] top_returns : bool, defaults to True
        If True, append back-to-top references to the sections that got
        a TOC entry, and add an anchor at the very top of the document,
        that is a Pandoc anchor appended to the document title if the
        `pandoc` option is set to True, or an HTML anchor else or if
        there is no such document title. Do nothing if False.
    [OPT] pandoc : bool, defaults to False
        If True, use Pandoc anchors, appended to the sections that got
        a TOC entry; use HTML anchors else, placed before the sections.

    Returns
    -------
    None : directly write in a file the updated Markdown content.

    Examples
    --------
    # Name of the example Markdown file to read and update
    filename = "example.md"

    # Dummy text to write in a Markdown file
    >>> text = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text\n",
    ...     "\n",
    ...     "### Subsection 1.1\n",
    ...     "Some text\n",
    ...     "\n",
    ...     "## Section 2\n",
    ...     "Some text\n"]

    # Write the test text in a Markdown file
    >>> with open(filename, 'w', encoding='utf-8') as mdfile:
    ...     for line in text:
    ...         mdfile.write(line)

    # Update the Markdown file
    >>> add_toc_to_md(filename, depth=2)

    # Cat command with IPython on GNU/Linux
    >>> !cat example-toc.md
    <a name='top'></a>
    # TITLE OF THE MARKDOWN

    - [Section 1](#section-1)
    - [Section 2](#section-2)


    <a name='section-1'></a>
    ## Section 1 [↑](#top)
    Some text

    ### Subsection 1.1
    Some text

    <a name='section-2'></a>
    ## Section 2 [↑](#top)
    Some text
    """

    # Read and load the Markdown file
    lines = read_file(filename)

    # Rebuild the Markdown with the section anchors and the TOC
    text, new_toc = build_md_with_toc(lines, depth, top_returns, pandoc)

    # Write the new file
    path = Path(filename)
    write_md_with_toc(f"{path.stem}-toc{path.suffix}", text, new_toc)

##############################################################################
