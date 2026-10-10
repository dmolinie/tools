""" Simple functions to handle BibTeX files

Authors: Dylan MOLINIE
Contact: dylan.molinie@gmx.fr
Date: October 2026
Last revised: October 2026

License: GPLv3
"""

__all__ = ['sort_bibtex']

from pathlib import Path

import bibtexparser
#from iso4 import abbreviate


##############################################################################
##                          BibTeX File Functions                           ##
##############################################################################

def sort_bibtex(filename):
    """ Reorganize a BibTeX file in a standardized manner

    Take a BibTeX file, read it, extract its entries and reorganize them
    in a standardized order: for any entry, place the 'title', 'author'
    and 'year' items first, and place the remaining item's entries next.
    For any entry, align the different items, and wrap their values into
    curly brackets. Export the reformatted file into a new file with the
    same name, appended with the '-fmt' suffix.

    Parameters
    ----------
    filename : str
        The name of the BibTeX file to format.

    Returns
    -------
    None : directly write the reformatted BibTeX file.

    Examples
    --------
    # Consider the BibTeX `bib.bib` containing this single entry:
    >>> !cat bib.bib
    @conference{conf_ref,
        keywords = {keywords},
        booktitle = {Name of the book},
        title = "Article title",
        year = {2026},
        url = {https://...},
        author = "Authors",
    }

    # Reformat the BibTeX file and export it to `bib-fmt.bib`
    >>> sort_bibtex("bib.bib")

    >>> !cat bib-fmt.bib
    @conference{conf_ref,
    	title	=	{Article title},
    	author	=	{Authors},
    	year	=	{2026},
    	booktitle	=	{Name of the book},
    	keywords	=	{keywords},
    	url		=	{https://...},
    }
    """

    # Parse the name of the file
    path = Path(filename)

    # Load the BibTeX bibliography
    lib = bibtexparser.parse_file(filename)

    # Get the references' names (ID)
    keys = [entry['ID'] for entry in lib.entries]
    keys.sort() # Sort them by alphabetical order

    # Get all entries (dict (IDs) of dict (items))
    biblio = lib.entries_dict

    # First items to write
    claves = ('title', 'author', 'year')

    # Rewrite the ordered bibliography
    with open(f"{path.stem}-fmt{path.suffix}", 'w', encoding='utf-8') as bibfile:
        for key in keys[::-1]:
            entry = biblio[key]

            # Write type and entry (ID) of the current reference
            string = '@' + entry['ENTRYTYPE'] + '{' + entry['ID'] + ',\n'

            # Write the first items of the current reference
            for item in claves:
                string += '\t' + item + '\t=\t{' + entry[item] + '},\n'

            items = [item for item in entry.fields_dict.keys() if item not in claves]
#            if entry['ENTRYTYPE'] == 'article':
#                string += ('\tjournal\t=\t{'
#                           + abbreviate(entry['jfull'], disambiguation_langs=['eng'])
#                           + '},\n')

            for item in items:
                # +1 tab for 3-character long entries (e.g. 'doi' & 'url')
                esp = '\t\t=\t{' if len(item) == 3 else '\t=\t{'
                string += '\t' + item + esp + entry[item] + '},\n'

            bibfile.write(string + '}\n\n')

##############################################################################
