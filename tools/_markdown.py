""" Simple functions to handle Markdown files

Authors: Dylan MOLINIE
Contact: dylan.molinie@gmx.fr
Date: October 2026
Last revised: October 2026

License: GPLv3
"""

__all__ = [
    'str_to_html_anchor_name', 'create_html_anchor', 'is_html_anchor',
    'split_md_toc_entry', 'build_md_with_toc', 'create_md_toc_entry',
    'write_mdfile_with_toc', 'add_toc_to_mdfile']

from pathlib import Path

from tools._text import strip_str_accents, strip_str, read_file


##############################################################################
##                         HTML-oriented Functions                          ##
##############################################################################

def str_to_html_anchor_name(string):
    r""" Normalize a string to a standard HTML anchor name

    Take a string, lowercase it and clean it as follows:
      - replace 'œ' and 'æ' with 'oe' and 'ae';
      - replace '&' with hyphen '-';
      - remove the spaces before and after hyphens;
      - replace spaces ' ' with hyphens '-';
      - remove the symbols and punctuation;
      - remove the accents from the accentuated characters.
    Then, return the stripped string that contains HTML anchor name
    standard characters only.

    Parameters
    ----------
    string : str
        The string to standardize.

    Returns
    -------
    string_std : str
        The string standardized to HTML anchor name.

    Examples
    --------    
    >>> str_to_html_anchor_name("*White-Fang*, Jack London")
    'white-fang-jack-london'

    >>> str_to_html_anchor_name("I love cafés!")
    'i-love-cafes'

    >>> str_to_html_anchor_name("« C'est la vie ! » is a French expression.")
    "c-est-la-vie---is-a-french-expression"
    """
    # Lowercase the string
    string = string.lower()
    # Replace the apostrophes with hyphens
    string = string.replace("'", '-')
    string = string.replace("’", '-')
    # Split the 'æ' and 'œ' letters
    string = string.replace('æ', 'ae')
    string = string.replace('œ', 'oe')
    # Replace and symbol '&' with an hyphen
    string = string.replace('&', '-')
    # Remove the spaces before and after hyphens
    string = string.replace(' -', '-')
    string = string.replace('- ', '-')
    # Replace the spaces with hyphens
    string = string.replace(' ', '-')
    # Keep only the letters, numbers and hyphens (+ spaces and apostrophes)
    string = strip_str(string)
    # Remove the accents from the accentuated letters
    string = strip_str_accents(string)
#    string = string.replace('--', '-')
    # Remove the leading and trailing hyphens, if any
    return string.strip('-')

def create_html_anchor(name):
    r""" Take the HTML anchor name and wrap it into an anchor element

    An HTML anchor has format:
        <a name=`name`></a>\n

    Take the `name` argument and wrap it around the above anchor syntax.

    Parameters
    ----------
    name : str
        The referring name of the anchor.

    Returns
    -------
    anchor : str
        The formatted anchor, as a string.

    Examples
    --------
    >>> create_html_anchor('title')
    "<a name='title'></a>\n"

    # Build an anchor from a full string
    >>> title = "*White-Fang*, Jack London"
    >>> anchor_name = str_to_html_anchor_name(title)
    >>> create_html_anchor(anchor_name)
    "<a name='white-fang-jack-london'></a>\n"
    """
    return f"<a name='{name}'></a>\n"

def is_html_anchor(string):
    r""" Check that a string is an HTML anchor

    An HTML anchor has format:
        <a name=`name`></a>\n

    Take the `string` argument and check it contains both '<a' and '</a>'
    substrings, indicating it is an HTML anchor.

    Parameters
    ----------
    string : str
        The string to check.

    Returns
    -------
    is_anchor : bool
        True if `string` is an HTML anchor; False else.

    Examples
    --------
    >>> is_html_anchor("<a name='title'></a>\n")
    True

    # Build an anchor from a full string
    >>> title = "*White-Fang*, Jack London"
    >>> anchor = create_html_anchor(str_to_html_anchor_name(title))
    >>> is_html_anchor(anchor)
    True
    """
    return "<a" in string and "</a>" in string

##############################################################################



##############################################################################
##                       Markdown Handling Functions                        ##
##############################################################################

def split_md_toc_entry(s):
    r""" Split a Markdown TOC entry into its title and its anchor

    A Markdown TOC entry has format:
        - [Title](#anchor)

    As such, retrieve the part between brackets and use it as `title`,
    and the part between parentheses as `anchor`; wrap both into a dict-
    ionary, whose key is `anchor`, and the value is `title`, and return
    this dictionary.

    Parameters
    ----------
    s : str
        The Markdown TOC entry line.

    Returns
    -------
    entry : dict
        The TOC entry; the anchor is used as key, and the title as value.

    Examples
    --------
    >>> toc_ent = "- [*White-Fang*, Jack London](#white-fang-jack-london)\n"
    >>> split_md_toc_entry(toc_ent)
    {'white-fang-jack-london': '*White-Fang*, Jack London'}
    """
    # Anchor between (#...) and Title between [...]
    return {s[s.find('(#')+2:s.rfind(')')]: s[s.find('[')+1:s.rfind(']')]}

def build_md_with_toc(lines, depth=2):
    r""" Build the TOC of a Markdown file

    Take the text of a Markdown file, retrieve its existing TOC, if any,
    and rebuild the file with a new TOC as follows:
      - if a line is an HTML anchor, if it already had an entry in the
        original TOC, do nothing; if is directly preceded or followed
        by a section title, link this anchor and this title as an entry
        to the new TOC; else, link it to the generic name 'Anchor {i}';
        ignore the anchors with empty `name` tags.
      - if a line is a section, i.e. starting with one or more '#', if
        it is already directly preceded or followed by an anchor, link
        them both; else, add an HTML anchor in the line directly above
        the section title (to ensure correct displaying), link this new
        anchor to the section title and add this entry to the new TOC.

    Return the original text lines, updated with the newly added HTML
    anchors and with the original TOC removed; return also the new TOC.

    Use the `depth` argument to specify the the depth of the TOC; this
    value indicate maximum number of `#` symbols that a section should
    have. For instance, `depth=2` will include the sections '##' only;
    `depth=3` will include both sections ('##') and subsections ('###').
    The Markdown title ('#') is always ignored in the TOC.

    Parameters
    ----------
    lines : list of str
        The Markdown file text, one line per item.
    [OPT] depth : int, defaults to 2
        The depth of the TOC; in practice, the maximum number of heading
        '#' symbols in a line for a section to get a TOC entry. The Mark-
        down title ('#') is always ignored; a value below 2 means no TOC.

    Returns
    -------
    text : list of str
        The text, line by line, of the reworked Markdown file, with the
        added HTML anchors, and with its original TOC removed. The other
        lines are left unchanged (paragraphs, titles, comments, etc.)
    entry : dict
        The new TOC entries; the HTML anchors are used as keys, and the
        section titles as values.

    Examples
    --------
    # Consider the Markdown file contains the lines below
    >>> text_org = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text for the first line\n",
    ...     "Some new paragraph\n",
    ...     "\n",
    ...     "### Subsection 1.1\n",
    ...     "Some additional text\n",
    ...     "\n",
    ...     "## Section 2\n",
    ...     "Some additional text\n"]

    >>> text, toc = build_md_with_toc(text_org, depth=2)

    >>> print(text)
    ['# TITLE OF THE MARKDOWN\n',
     '\n',
     "<a name='section-1'></a>\n",
     '## Section 1\n',
     'Some text for the first line\n',
     'Some new paragraph\n',
     '\n',
     '### Subsection 1.1\n',
     'Some additional text\n',
     '\n',
     "<a name='section-2'></a>\n",
     '## Section 2\n',
     'Some additional text\n']

    >>> print(toc)
    {'section-1': 'Section 1',
     'section-2': 'Section 2'}
    """

    def check_depth(s, depth):
        """ Check that `s` is a section (make sure it is stripped from
        spaces) and check that the number of heading '#' is <= depth """
        return s[:1] == '#' and len(s) - len(s.lstrip('#')) <= depth

    last_anc = ''   # Last seen HTML anchor
    prev_toc = {}   # Already-existing TOC
    new_toc = {}    # New TOC, built from the section titles
    text = []       # The text to write, with the new HTML anchors

    # Add an item to ensure lines[i+1] always exists
    # This is sufficient since this cell is accessed only when a line
    # starts with '##' or is an HTML anchor
    lines = lines.copy() + ['']

    cpt = 0
    for i, line in enumerate(lines):

        # Retrieve the current table of contents, if any
        if '(#' in line:
            prev_toc.update(split_md_toc_entry(line))
            continue

        # Strip the heading and trailing spaces from the line to test it
        # (it is the original line which is written)
        ltmp = line.strip()

        # Build the HTML anchors from section titles
        if ltmp[:2] == '##' and check_depth(ltmp, depth):
            ln_abv, ln_blw = lines[i-1], lines[i+1]
            # If the section does not already have an anchor attached to it,
            # in the line directly above or below, build a new anchor
            if ln_abv.find('name=') == -1 and ln_blw.find('name=') == -1:
                title = line.lstrip('#').strip()        # Extract section title
                anc = str_to_html_anchor_name(title)    # Title to anchor name
                new_toc[anc] = title                    # Add the entry to TOC
                anc = create_html_anchor(anc)           # Format the HTML anchor
                # Avoid duplicates (when same file processed several times)
                if anc != last_anc:
                    last_anc = anc      # Update last-seen anchor
                    text.append(anc)    # Add the anchor above the title

        # Retrieve the last HTML anchor already-present in the text
        # (when an anchor is above a section title)
        elif is_html_anchor(ltmp):
            last_anc = line             # Update last-seen anchor
            ln_abv, ln_blw = lines[i-1].strip(), lines[i+1].strip()
            anc = line[line.find('name=')+6:line.find('>')-1]   # Anchor name
            # If the anchor is already listed in the already-existing TOC,
            # retrieve the title associated with it
            # pylint: disable-next=C0201
            if anc in prev_toc.keys():
                new_toc[anc] = prev_toc.pop(anc)
            # If the anchor is unknown, check if a section is directly below
            # or above; if so, use the section title as TOC entry associated
            # with this anchor. Ignore it if section depth > `depth`.
            elif not (check_depth(ln_abv, depth)
                      or check_depth(ltmp, depth)
                      or check_depth(ln_blw, depth)):
                pass
            elif anc and ln_abv[:2] == '##':
                new_toc[anc] = ln_abv.lstrip('#').strip()
            elif anc and ln_blw[:2] == '##':
                new_toc[anc] = ln_blw.lstrip('#').strip()
            # Else, add the anchor to the new TOC with a general entry title
            elif anc:
                new_toc[anc] = f"Anchor {cpt}"
                cpt += 1
#            # In the case of the the anchor has no name, remove it from the
#            # file (skip the line appending below)
#            else:
#                continue

        # Add the current line to those to write
        text.append(line)

#    # Stack any remaining items in the original TOC
#    if prev_toc:
#        new_toc.update(prev_toc)

    # Remove the dummy [''] added prior
    return text[:-1], new_toc

def create_md_toc_entry(entry):
    r""" Take a set of (anchor, title) and rewrite into a Markdown TOC entry

    A Markdown TOC entry has format:
        "- [Title](#anchor)"

    Take the `entry` argument, assumed to be formatted as:
        (anchor, title)
    rewrite it to match the above format and return the so-built string.

    Parameters
    ----------
    entry : 2-tuple of str
        The set of the referring name of the (HTML) anchor and the TOC
        entry title, organized as (anchor, title).

    Returns
    -------
    toc_entry : str
        The TOC entry that can be written in the Markdown file.

    Examples
    --------
    >>> title = "*White-Fang*, Jack London"
    >>> anchor_name = str_to_html_anchor_name(title)

    >>> create_md_toc_entry((anchor_name, title))
    '- [*White-Fang*, Jack London](#white-fang-jack-london)\n'
    """
    return f"- [{entry[1]}](#{entry[0]})\n"

def write_mdfile_with_toc(filename, text, toc_entries):
    r""" Write a text and its TOC in a Markdown file

    Take a text (set of strings) and the TOC entries (dict. of titles
    indexed by their anchors) and write them in a Markdown file.

    Skip the heading spacing ('\n') lines and write the document title
    (the first line starting with '#'), if any, at the very top of it;
    then, add an empty line, write the TOC (every item of `toc_entries`
    is passed to the `create_md_toc_entry` function) and add two empty
    lines directly below; skip any additional empty lines until the next
    non-empty one, write any remaining item of `text` and close the file.

    Parameters
    ----------
    filename : str
        The name of the Markdown file to write.
    text : list/tuple of str
        The text to write in the Markdown, one item per line.
    toc_entries : dict
        The entries of the TOC, as a dictionary whose keys are the names
        of the (HTML) anchors, and the values are the TOC titles.

    Returns
    -------
    None : directly write the Markdown file.

    Examples
    --------
    >>> text = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text for the first line\n",
    ...     "Some new paragraph\n",
    ...     "\n",
    ...     "## Section 2\n",
    ...     "Some additional text\n"]

    >>> toc_entries = {
    ...     'section-1': "Section 1",
    ...     'section-2': "Section 2"}

    >>> write_mdfile_with_toc("file.md", text, toc_entries)

    # Cat command with IPython on GNU/Linux
    >>> !cat file.md
    # TITLE OF THE MARKDOWN

    - [Section 1](#section-1)
    - [Section 2](#section-2)


    ## Section 1
    Some text for the first line
    Some new paragraph

    ## Section 2
    Some additional text
    """

    with open(filename, 'w', encoding='utf-8') as mdfile:

        # Skip the heading newlines
        i = 0
        while text[i] == '\n':
            i += 1

        # If the Markdown contains a title (i.e. a line that starts with '#'),
        # place it at the very top of the document
        if text[i].startswith('#'):
            # First row, assumed to be the title
            mdfile.write(text[i])
            i += 1

        # Add 1 empty line below the title (or at the very top of the file if
        # there is no title), write the TOC, and add two empty lines after
        mdfile.write('\n')
        for item in toc_entries.items():
            mdfile.write(create_md_toc_entry(item))
        mdfile.write('\n\n')

        # Skip the empty lines between the TOC and the next line text
        while text[i] == '\n':
            i += 1

        # Write the rest of the file
        for line in text[i:]:
            mdfile.write(line)

def add_toc_to_mdfile(filename, depth=2):
    r""" Open a Markdown file, add HTML anchors to above sections, build
    the new TOC and write the updated file (TOC, text and anchors)

    Call the `read_file` function to read the `filename` Markdown file,
    add the HTML anchors and build the new TOC with `build_md_with_toc`,
    and write the updated Markdown file with `write_mdfile_with_toc`.
    See these three functions for details.

    The name of the new file is the base name (i.e. without extension)
    of `filename` appended with the '-toc' suffix.

    Parameters
    ----------
    filename : str
        The name of the Markdown file to write.
    [OPT] depth : int, defaults to 2
        The depth of the TOC; in practice, the maximum number of heading
        '#' symbols in a line for a section to get a TOC entry. The Mark-
        down title ('#') is always ignored; a value below 2 means no TOC.

    Returns
    -------
    None : directly write the updated Markdown file.

    Examples
    --------
    # Name of the Markdown file to write and update then
    filename = "example.md"

    # Dummy text to write in a Markdown file
    >>> text = [
    ...     "# TITLE OF THE MARKDOWN\n",
    ...     "\n",
    ...     "## Section 1\n",
    ...     "Some text for the first line\n",
    ...     "Some new paragraph\n",
    ...     "\n",
    ...     "### Subsection 1.1\n",
    ...     "Some additional text\n",
    ...     "\n",
    ...     "## Section 2\n",
    ...     "Some additional text\n"]

    # Write the test text in a Markdown file
    >>> with open(filename, 'w', encoding='utf-8') as mdfile:
    ...     for line in text:
    ...         mdfile.write(line)

    # Update the Markdown file
    >>> add_toc_to_mdfile(filename, depth=2)

    # Cat command with IPython on GNU/Linux
    >>> !cat example-toc.md
    # TITLE OF THE MARKDOWN

    - [Section 1](#section-1)
    - [Section 2](#section-2)


    <a name='section-1'></a>
    ## Section 1
    Some text for the first line
    Some new paragraph

    ### Subsection 1.1
    Some additional text

    <a name='section-2'></a>
    ## Section 2
    Some additional text
    """

    # Read and load the Markdown file
    lines = read_file(filename)

    # Rebuild the Markdown with the section anchors and the TOC
    text, new_toc = build_md_with_toc(lines, depth)

    # Write the new file
    path = Path(filename)
    write_mdfile_with_toc(f"{path.stem}-toc{path.suffix}", text, new_toc)

##############################################################################
