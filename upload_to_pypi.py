#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written by Christoph Federrath (2022)

import argparse
import os
from cfpack import read_ascii, write_ascii, run_shell_command, print, stop

# ===== MAIN Start =====
# ===== the following applies in case we are running this in script mode =====
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Prepare and upload to pypi')
    args = parser.parse_args()

    path = "pypi/"
    dist_dir = path+"dist/"
    pyproject_file = "setup.py"

    # check and update version
    lines = read_ascii(path+pyproject_file, plain=True)
    new_lines = []
    for line in lines:
        if line.find("    version=") == 0: # find "version = " line
            version = line.split("=")[1].strip("\" ,") # extract version string
            intver = int("".join(version.split('.'))) # extract integer version
            intver = intver + 1 # increment version
            new_version = ".".join(f"{intver:03d}") # create new version string
            line = '    version="'+new_version+'",' # overwrite version line with new version string
        new_lines.append(line) # append for output

    # user input
    input("\nPress enter to update from version "+version+" to "+new_version+" and upload...\n")

    # make backup copy of pyproject_file
    cmd = "cp "+path+pyproject_file+" "+path+pyproject_file+".old"
    run_shell_command(cmd)

    # write new py project file, with new version number
    write_ascii(path+pyproject_file, new_lines, plain=True)

    # make backup copy of current (new) version
    cmd = "cp -r "+path+" "+path[:-1]+"_"+new_version
    run_shell_command(cmd)

    # display version change
    cmd = "git diff "+path+pyproject_file
    run_shell_command(cmd)

    # user input
    input("\nCheck changes and press enter to proceed...\n")

    # prepare pip
    cmd = "python3 -m pip install --user --upgrade pip"
    run_shell_command(cmd)
    cmd = "python3 -m pip install --user --upgrade build"
    run_shell_command(cmd)
    cmd = "python3 -m pip install --user --upgrade pkginfo"
    run_shell_command(cmd)
    cmd = "python3 -m pip install --user --upgrade twine"
    run_shell_command(cmd)

    # delete dist directory
    if os.path.isdir(dist_dir):
        cmd = "rm -r "+dist_dir
        input("\nPress enter to delete dist directory '"+dist_dir+"'\n")
        run_shell_command(cmd)

    # build dist(ribution)
    cmd = "cd "+path+"; python3 -m build"
    run_shell_command(cmd)

    # revert back to backup file, so we only replace after successful upload
    cmd = "cp "+path+pyproject_file+" "+path+pyproject_file+".new"
    run_shell_command(cmd)
    cmd = "cp "+path+pyproject_file+".old "+path+pyproject_file
    run_shell_command(cmd)

    # upload
    cmd = "python3 -m twine upload "+dist_dir+"*"
    input("\nPress enter to upload using command '"+cmd+"'\n")
    run_shell_command(cmd)

    # finally, update py project file and clean
    input("\nIf upload was successful, press enter to finalise update\n")
    cmd = "cp "+path+pyproject_file+".new "+path+pyproject_file
    run_shell_command(cmd)
