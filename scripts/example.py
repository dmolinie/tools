""" Example of use of the `tools` package

Authors: Dylan MOLINIE
Contact: dylan.molinie@gmx.fr
Date: October 2026
Last revised: October 2026

License: GPLv3
"""

import tools as tls


#-------------------------   String Manipulation   --------------------------#

# Remove punctuation (', ", ;, !, *, %, (), [], {}, ...) from a string
print(tls.strip_str_punctuation("This (sentence) is a 'punctuated' string!"))

# Remove symbols (+, =, ~, |, $, €, ...) from a string
print(tls.strip_str_symbols("This cost +€10 or ~$12"))

# Remove the accents from the characters of a string
print(tls.strip_str_accents("Developers drink much café"))

# Keep letters, numbers, spaces, hyphens and apostrophes in a string
print(tls.strip_str("*White-Fang*, Jack London"))
print(tls.strip_str("« C'est la vie ! » is a French expression."))

#----------------------------------------------------------------------------#

#--------------------------   Read & Write Files   --------------------------#

# Generate a dummy text
text = ['This is a dummy text file.\n',
        'It contains some example text.\n',
        'You can use it for testing purposes.\n']

# Write the text lines in a file
tls.write_file("file.txt", text)

# Read the file and load its content
print(text2 := tls.read_file("file.txt"))

#----------------------------------------------------------------------------#

#----------------------   Add TOC to Markdown Files   -----------------------#

# Generate a dummy Markdown text and write it in a file
md_text_ex = [
    "# TITLE OF THE MARKDOWN\n",
    "\n",
    "## Section 1\n",
    "Some text\n",
    "Some new paragraph\n",
    "\n",
    "### Subsection 1.1\n",
    "Some text\n",
    "\n",
    "## Section 2\n",
    "Some text\n"]
tls.write_file("file.md", md_text_ex)

# Load the Markdown file
md_text = tls.read_file("file.md")

# Add the HTML anchors and add the TOC of the Markdown
md_text_up, md_toc = tls.build_md_with_toc(md_text, depth=2)

# Write the Markdown with the new HTML anchors and the TOC
tls.write_md_with_toc("file-toc.md", md_text_up, md_toc)

# The three previous steps (read, TOC & write) can be replaced with this one
tls.add_toc_to_md("file.md", depth=2)

#----------------------------------------------------------------------------#

#-----------------------   Reorganize BibTeX Files   ------------------------#

# Generate a dummy BibTeX text and write it in a file
bib_text = [
    "@conference{conf_ref,\n",
    "    author = \"Authors\",\n",
    "    booktitle = {Name of the book},\n",
    "    keywords = {keywords},\n",
    "    year = {2026},\n",
    "    url = {https://...},\n",
    "    title = \"Article title\",\n",
    "}\n"]
tls.write_file("file.bib", bib_text)

# Reformat the BibTeX file and export it to `bib-fmt.bib`
tls.sort_bibtex("file.bib")

#----------------------------------------------------------------------------#
