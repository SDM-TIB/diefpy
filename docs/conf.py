# Configuration file for the Sphinx documentation builder.
#
# For a full list of options see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import re
import subprocess
import sys
sys.path.insert(0, os.path.abspath('../'))
import diefpy
from sphinx_gallery.sorting import FileNameSortKey


# -- Project information -----------------------------------------------------
project = 'diefpy'
copyright = '2019-2022, Philipp D. Rohde and Nikoleta Themeliotou'
author = 'Philipp D. Rohde, Nikoleta Themeliotou'


# The full version, including alpha/beta/rc tags
def _get_version():
    with open('../VERSION', 'r', encoding='utf8') as version_file:
        version = version_file.read()
    return version


version = _get_version()
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_multiversion',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_gallery.gen_gallery',
    'sphinxcontrib.bibtex',
]

# bibtex configuration
bibtex_bibfiles = ['refs.bib']
bibtex_default_style = 'unsrt'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'friendly'
pygments_style = "sphinx"


# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

# Don't show the module name.
add_module_names = False

autodoc_default_flags = ['members']
autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

html_copy_source = False

# sphinx-gallery configuration
sphinx_gallery_conf = {
    # path to your example scripts
    'examples_dirs': ['../example/gallery'],
    # path to where to save gallery generated output
    'gallery_dirs': ['examples'],
    # specify that examples should be ordered according to filename
    'within_subsection_order': FileNameSortKey,
    # files to be executed
    'filename_pattern': r'/*\.py',
}

# configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(sys.version_info), None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}


# -- Options for sphinx-multiversion ------------------------------------------
# Only the latest patch release of each minor series is built (e.g., v1.2.1 for
# 1.2.x) and published as /v1.2.1/. Tags without documentation (before v1.1.0)
# are skipped automatically. The newest release is additionally served at /latest/.
def _latest_patch_tags():
    cwd = os.path.dirname(os.path.abspath(__file__))
    tags = subprocess.run(['git', 'tag'], capture_output=True, text=True, cwd=cwd).stdout.split()
    best = {}
    for tag in tags:
        m = re.fullmatch(r'v(\d+)\.(\d+)\.(\d+)', tag)
        if not m:
            continue
        if subprocess.run(['git', 'cat-file', '-e', f'{tag}:docs/conf.py'],
                          capture_output=True, cwd=cwd).returncode != 0:
            continue  # this release has no documentation
        ver = tuple(int(g) for g in m.groups())
        if ver[:2] not in best or ver > best[ver[:2]]:
            best[ver[:2]] = ver
    return ['v%d.%d.%d' % v for v in best.values()]


_TAGS = sorted(_latest_patch_tags(), key=lambda t: tuple(int(x) for x in t[1:].split('.')), reverse=True)
# sphinx-multiversion sorts the refs alphabetically (e.g., v1.10.0 < v1.9.0). The Makefile hands
# this newest-first order to the templates via `-D html_context.release_order=...`.
RELEASE_ORDER = ','.join(_TAGS)
smv_tag_whitelist = r'^(%s)$' % '|'.join(re.escape(t) for t in _TAGS) if _TAGS else r'^$'
smv_branch_whitelist = r'^$'  # only releases are published
smv_remote_whitelist = None
smv_outputdir_format = '{ref.name}'

# Render the version switcher on every page (and in all versions, since
# sphinx-multiversion uses the templates of the ref it is run from).
html_sidebars = {'**': ['versions.html']}
