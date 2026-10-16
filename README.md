# Generally-oriented tools


## Contents
1. [Description](#Description)
2. [Download](#Download)
3. [Installation](#Installation)
4. [Modules Description](#Modules-Description)
5. [Example of Use](#Example-of-Use)


## Description
The `tools` package is a small toolbox that provides simple tools to handle files, text, format Markdown or BibTeX files, etc., that may be accessed from anywhere on the system.

When dealing with a certain simple task, one typically writes a standalone script somewhere and leaves it alone then, until a similar task reappears; in such a case, the common action is often to copy-paste the script anywhere it is needed, even though the functions are the exact same, or with just minor adjustments. For instance, to reorganize a BibTeX file, one may write a small script doing that, place it in the same folder than the BibTeX file, and then copy-paste it anywhere a new BibTeX file would need reorganization.

However, since the task is the same, there is no need to duplicate code, that would pollute the system; instead, a much better practice is to split the script into modular functions, and place them somewhere in the system from where they can be easily accessed and called. A good solution is to create a small package with these common functions.

This is the purpose of this small package, that aims to provide some simple functions for general-purpose tasks, and make them available from anywhere on the system. In particular, it provides the base structure on which additional functions can be added, so that they can be accessed from anywhere on the system.

### Authors & Support
This is a personal project, developed by:

- Dylan MOLINIE (<dylan.molinie@gmx.fr>)

### License
The project is distributed under GPLv3 license.


## Download
To download the project, either go to the project page:  
https://github.com/dmolinie/tools

Or download it directly with the following command:

```bash
git clone https://github.com/dmolinie/tools.git
```


## Installation
To install the `tools` package, run the following command when in the package root folder:

```bash
pip install .
```

See the
[INSTALL.rst](INSTALL.rst)
file for further explanation on the requirements and options on installation.


## Modules Description
The different modules and their functions are briefly described in the
[MODULES.rst](MODULES.rst)
file.


## Example of Use
Here is a an example of use of the main functionalities of the `tools` package: it shows how to use the main functions actually available. This script is provided in the `scripts` folder of the package sources.

```python
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
```
