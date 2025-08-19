#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written by Christoph Federrath (2022)

import argparse
import os
from cfpack import read_ascii, run_shell_command, print, stop

# ===== MAIN Start =====
# ===== the following applies in case we are running this in script mode =====
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate documentation with sphinx.')
    args = parser.parse_args()

    path = "pypi/"
    doc_dir = path+"doc/"
    pyproject_file = "setup.py"

    # delete doc directory
    doc_dirs = ['./doc', doc_dir]
    for doc_dir in doc_dirs:
        if os.path.isdir(doc_dir):
            cmd = "rm -r "+doc_dir
            input("\nPress enter to delete doc directory '"+doc_dir+"'\n")
            run_shell_command(cmd)

    # check and update version
    lines = read_ascii(path+pyproject_file, plain=True)
    for line in lines:
        if line.find("    version=") == 0: # find "version = " line
            version = line.split("=")[1].strip("\" ,") # extract version string

    # install sphinx
    cmd = "pip install --user --upgrade sphinx"
    run_shell_command(cmd)

    cmd = "cd "+path+"; sphinx-apidoc . --full -o doc -H 'CFpack' -A 'Christoph Federrath' -V '"+version+"'"
    run_shell_command(cmd)

    cmd = "cd "+doc_dir+"; make html"
    run_shell_command(cmd)

    cmd = "mv "+doc_dir+" ."
    run_shell_command(cmd)

    target_dir = '$HOME/public_html/codes/cfpack/doc'
    cmd = "cp -r doc/_build/html/* "+target_dir
    run_shell_command(cmd)
