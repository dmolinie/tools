""" Miscellaneous tools (files, text, Markdown, BibTeX, etc.) """

# Package version & author
__version__ = '1.0'
__author__ = "Dylan MOLINIE"

from importlib.util import find_spec as _find_spec
from importlib import import_module as _import_module


##############################################################################
##                       Local Scripts (Package Root)                       ##
##############################################################################

# Local scripts that require third-part libraries (listed as
# "dependencies" in the '.toml' installation file)
__scripts__ = {
    '_text',
    '_markdown',
}

# Local scripts that require additional third-part libraries (listed
# as optional dependencies ("extras") in the '.toml' installation file)
__opt_scripts__ = {
    '_bibtex': ['bibtexparser']
}

# For any optional script, check if its dependencies are installed;
# if so, add this script to the list of the available scripts
for _module in __opt_scripts__.items():
    if all(_find_spec(_mod) is not None for _mod in _module[1]):
        __scripts__.add(_module[0])

# Add the local scripts to the `__all__` set
__all__ = list(__scripts__)


# Load the local scripts and add their global variables to those of
# the package, so that they can be accessed from root
for _module in __scripts__:
    # Load the module (`from <pkg> import <mod>`)
    _mod = _import_module(f"{__name__}.{_module}")
    # Load the module's global variables (`from . <mod> import *`)
    for _name in _mod.__all__:
        globals()[_name] = getattr(_mod, _name)
    # Add the module's `__all__` set to that of the package
    __all__ += _mod.__all__.copy()

##############################################################################



##############################################################################
##                            Package Submodules                            ##
##############################################################################

## Modules that require third-part libraries (listed as
## "dependencies" in the '.toml' installation file)
#__submodules__ = {
#    'mod',        # numpy
#}

## Modules that require additional third-part libraries (listed as
## optional dependencies ("extras") in the '.toml' installation file)
#__opt_submodules__ = {
#    'module': ['dep']
#}

## For any optional submodule, check if its dependencies are installed;
## if so, add this submodule to the list of the available submodules
#for _module in __opt_submodules__.items():
#    if all(_find_spec(_mod) is not None for _mod in _module[1]):
#        __submodules__.add(_module[0])

## Add the installed submodules to the `__all__` set
#__all__ += list(__submodules__)


#def __getattr__(attr):
#    """ Return the correct module from its name, if it exists """
#    # pylint: disable=C0415, R0402, R0911
##    # Short version based on importlib (a little less efficient)
##    if module in __submodules__:
##        return _import_module(f"{__name__}.{module}")
#    if attr == 'module':
#        import tools.module as module
#        return module
#    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")

#def __dir__():
#    """ Add the modules of `submodules` to the list of callable variables"""
#    public_symbols = globals().keys() | __submodules__
#    return list(public_symbols)

##############################################################################
