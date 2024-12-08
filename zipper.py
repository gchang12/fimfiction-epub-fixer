#!/usr/bin/python3
"""
Replaces ampersands in FimFiction epub files that make them unreadable.
"""

from zipfile import ZipFile
import logging
import os.path
import os
import sys
from pathlib import Path

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
    subdir = filename.replace('.epub', '') \
        .replace(QUEUEDIR_NAME, '')
    path = '/'.join([OUTPUTDIR_NAME, subdir]).replace('//', '/')
    logging.debug(
        "Extracting epub contents into %r",
        path,
    )
    zipfile.extractall(path=path)

def edit_file(dirname):
    """
    Removes problematic ampersands from book.* files.
    """
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
    epub_name = dirname.replace(OUTPUTDIR_NAME, "") \
        .strip('/') \
        + ".epub"
    os.system("zip -X0 %r mimetype 2>/dev/null" % epub_name)
    os.system("zip -Xur9D %r * 2>/dev/null" % epub_name)
    os.system("mv %r ../" % epub_name)
    logging.debug(
        "Fixed epub file is in output/%s",
        epub_name,
    )

filename = sys.argv[1]
unzip(filename)
dirname = OUTPUTDIR_NAME \
    + "/" \
    + filename.split('/')[-1] \
    .replace('.epub', '/') \
    .replace("//", "/")
# edit
edit_file(dirname)
# rezip
rezip(dirname)

