#!/usr/bin/python3
"""
Replaces ampersands in FimFiction epub files that make them unreadable.
"""

from zipfile import ZipFile
import logging
import os.path
import os
import argparse
from pathlib import Path
import shutil

#zipfile = ZipFile()
#help(ZipFile)

logging.basicConfig(
    level=logging.DEBUG,
)

QUEUEDIR_NAME, OUTPUTDIR_NAME = "queue/", "output/"

for dirname in (QUEUEDIR_NAME, OUTPUTDIR_NAME):
    assert Path(dirname).exists() is True

def unzip(filename):
    """
    Extracts contents of epub file into a directory in OUTPUTDIR_NAME.
    """
    zipfile = ZipFile(filename)
    path = str(Path(OUTPUTDIR_NAME, Path(filename).with_suffix("").name))
    logging.debug(
        "Extracting epub contents into %r", path,
    )
    zipfile.extractall(path=path)
    logging.debug("Currently in directory: '%s'", os.getcwd())

def edit_file(dirname):
    """
    Removes problematic ampersands from book.* files.
    """
    logging.debug("Currently in directory: '%s'", os.getcwd())
    #os.system("vim %s/book.*" % dirname)
    #ampersand_replacement = "&#038;"
    ampersand_replacement = "&amp;#038;"
    #ampersand_replacement = "&amp;"
    for bookfile in Path(dirname).glob("book.*"):
        logging.debug(
            "Replacing '&' with %r in %r",
            ampersand_replacement, bookfile,
        )
        booktext = bookfile.read_text()
        fixed_booktext = booktext.replace('&', ampersand_replacement)
        bookfile.write_text(fixed_booktext)
        #os.system("vim %s/book.*" % dirname)

def rezip(dirname):
    """
    Repackages directory into an epub.
    """
    # https://www.reddit.com/r/vim/comments/gwcqd9/comment/fsuflnb/
    os.chdir(dirname)
    logging.debug("Currently in directory: '%s'", os.getcwd())
    epub_name = Path(dirname).with_suffix(".epub").name
    logging.debug("epub name: '%s'", epub_name)
    os.system("zip -X0 '%s' mimetype >/dev/null" % epub_name)
    os.system("zip -Xur9D '%s' * >/dev/null" % epub_name)
    os.system("mv '%s' ../" % epub_name)
    return epub_name

def cleanup(dirname):
    """
    Deletes unzipped directory.
    """
    #logging.debug("Invoking 'shutil.rmtree' on '%s'", dirname)
    os.chdir("../..")
    logging.debug("Currently in directory: '%s'", os.getcwd())
    shutil.rmtree(dirname)

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--delzip", type=bool, default=True)
args = parser.parse_args()
filename = args.filename
delzip = args.delzip

# main
logging.debug("Unzipping '%s'", filename)
unzip(filename)
dirname = Path(OUTPUTDIR_NAME, Path(filename).with_suffix("").name)
logging.debug("Editing unzipped directory: '%s'", dirname)
edit_file(dirname)
logging.debug("Rezipping folder: '%s'", dirname)
epub_name = rezip(dirname)
if delzip:
    logging.debug("Deleting folder: '%s'", dirname)
    cleanup(dirname)
    logging.debug("Deletion successful.")
logging.debug(
    "Fixed epub file is in 'output/%s'", epub_name,
)

