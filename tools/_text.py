""" Simple functions to handle text (strings, files, etc.)

Authors: Dylan MOLINIE
Contact: dylan.molinie@gmx.fr
Date: October 2026
Last revised: October 2026

License: GPLv3
"""

__all__ = [
    'strip_str_punctuation', 'strip_str_symbols', 'strip_str_accents',
    'strip_str', 'read_file', 'write_file']

import unicodedata


##############################################################################
##                        String Handling Functions                         ##
##############################################################################
#https://www.unicode.org/reports/tr44/tr44-34.html#General_Category_Values

def _strip_cat_from_str(s, cat):
    """ Remove any character from a general category (first letter);
    see: https://www.unicode.org/reports/tr44/tr44-34.html """
    return ''.join(c for c in s if unicodedata.category(c)[0] != cat)

def _strip_subcat_from_str(s, cat):
    """ Remove any character from a specific category (two letters);
    see: https://www.unicode.org/reports/tr44/tr44-34.html """
    return ''.join(c for c in s if unicodedata.category(c) != cat)

def strip_str_punctuation(s):
    """ Remove punctuation (', ", ;, !, *, %, (), [], {}, ...) from a string """
    return _strip_cat_from_str(s, 'P')

def strip_str_symbols(s):
    """ Remove symbols (+, =, ~, |, $, €, ...) from a string """
    return _strip_cat_from_str(s, 'S')

def strip_str_accents(s):
    """ Remove the accents from the characters of a string

    An accentuated character can be seen as a set of two items: the base
    letter and its diacritic. Using the `unicodedata` library, one can
    observe it as follows:
        >>> s = unicodedata.normalize('NFD', 'â')
        >>> print(f"letter: `{s[0]}` -- diacritic: `{s[1]} `")
        letter: `a` -- diacritic: `̂ `

    As such, to remove the accents from a string, split any accentuated
    characters into a letter and a diacritic, and return only the letters
    as a new string. Leave the unaccentuated characters unchanged.

    Parameters
    ----------
    s : string
        The string from which to remove the accents.

    Returns
    -------
    s_norm : string
        The string whose characters are stripped from their accents.

    Examples
    --------
    >>> strip_str_accents("Coffee") # Unaccentuated string (left unchanged)
    'Coffee'
    >>> strip_str_accents("Café")   # Accentuated string
    'Cafe'
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)  # Split accentuated characs
        if unicodedata.category(c) != 'Mn')         # Ignore diacritics

def strip_str(s):
    """ Keep letters, numbers, spaces, hyphens and apostrophes

    Take a string and remove any character that is not a letter, number,
    hyphen or apostrophe. Return the so-stripped string.

    Parameters
    ----------
    string : str
        The string to strip.

    Returns
    -------
    string_stripped : str
        The string stripped from the punctuation, symbols, etc.

    Examples
    --------    
    >>> strip_str("*White-Fang*, Jack London")
    'White-Fang Jack London'

    >>> strip_str("I'd like 1 café, please!")
    "I'd like 1 café please"

    >>> strip_str("« C'est la vie ! » is a French expression.")
    " C'est la vie   is a French expression"
    """
    # 'Lx': letters ; 'Nx': numbers ; 'Zx': spaces
    return ''.join(c for c in s
        if c in ('-', "'", "’")
        or unicodedata.category(c)[0] in ('L', 'N', 'Z'))

##############################################################################



##############################################################################
##                            File I/O Functions                            ##
##############################################################################

def read_file(filename):
    r""" Read and load the content of a file

    Parameters
    ----------
    filename : str
        The name of the file to read.

    Returns
    -------
    text : list
        The content of the file, line by line (any item of the list is
        a full line from the file).

    Examples
    --------
    # Write a dummy text file
    >>> with open("file.txt", 'w', encoding='utf-8') as file:
    ...     file.write("This is a dummy text file.\n")
    ...     file.write("It contains some example text.\n")
    ...     file.write("You can use it for testing purposes.\n")

    # Read the file and load its content
    >>> text = read_file("file.txt")
    >>> print(text)
    ['This is a dummy text file.\n',
     'It contains some example text.\n',
     'You can use it for testing purposes.\n']
    """
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line)
    return lines

def write_file(filename, text):
    r""" Write a set of lines into a file

    Parameters
    ----------
    filename : str
        The name of the file to read.
    text : list of str
        The lines of text to write; one item of the list is one line
        in the text file.

    Returns
    -------
    None : directly write the text lines in the file.

    Examples
    --------
    >>> text = ['This is a dummy text file.\n',
    ...         'It contains some example text.\n',
    ...         'You can use it for testing purposes.\n']

    # Write the text lines in a file
    >>> write_file("file.txt", text)

    # Cat command with IPython on GNU/Linux
    >>> !cat file.txt
    This is a dummy text file.
    It contains some example text.
    You can use it for testing purposes.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for line in text:
            file.write(line)

##############################################################################
