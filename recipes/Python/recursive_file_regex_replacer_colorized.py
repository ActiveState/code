#!/usr/bin/env python

"""



Recursively find and replace text in files under a specific folder with preview of changed data in dry-run mode
============

Example Usage
---------------

**See what is going to change (dry run):**

> flip all dates from 2017-12-31 to 31-12-2017

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "\3-\2-\1" --dry-run

**Do actual replacement:**

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "\3-\2-\1"

**Do actual replacement and create backup files:**

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "\3-\2-\1" --create-backup

**Same action as previous command with short-hand syntax:**

    find_replace.py -d project/myfolder -s "\d{4}-\d{2}-\d{2}" -r "\3-\2-\1" -b

Output of `find_replace.py -h`:

usage: find-replace-in-files-regex.py [-h] [--dir DIR] --search-regex
                                      SEARCH_REGEX --replace-regex
                                      REPLACE_REGEX [--glob GLOB] [--dry-run]
                                      [--create-backup] [--verbose]
                                      [--print-parent-folder]

USAGE:
    find-replace-in-files-regex.py -d [my_folder] -s <search_regex> -r <replace_regex> -g [glob_pattern]
"""

from __future__ import print_function
import os
import fnmatch
import sys
import shutil
import re

import argparse


class Colors:
    Default = "\033[39m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"
    NoColor = "\033[0m"


def find_replace(cfg):

    search_pattern = re.compile(cfg.search_regex)

    if cfg.dry_run:
        print('THIS IS A DRY RUN -- NO FILES WILL BE CHANGED!')

    for path, dirs, files in os.walk(os.path.abspath(cfg.dir)):
        for filename in fnmatch.filter(files, cfg.glob):

            if cfg.print_parent_folder:
                pardir = os.path.normpath(os.path.join(path, '..'))
                pardir = os.path.split(pardir)[-1]
                print('[%s]' % pardir)
            full_path = os.path.join(path, filename)

            # backup original file
            if cfg.create_backup:
                backup_path = full_path + '.bak'

                while os.path.exists(backup_path):
                    backup_path += '.bak'
                print('DBG: creating backup', backup_path)
                shutil.copyfile(full_path, backup_path)

            if os.path.islink(full_path):
                print("{}File {} is a symlink. Skipping{}".format(Colors.Red, full_path, Colors.NoColor))
                continue

            with open(full_path) as f:
                old_text = f.read()

            all_matches = search_pattern.findall(old_text)

            if all_matches:

                print('{}Found {} match(es) in file {}{}'.format(Colors.LightMagenta, len(all_matches), filename, Colors.NoColor))

                new_text = search_pattern.sub(cfg.replace_regex, old_text)

                if not cfg.dry_run:
                    with open(full_path, "w") as f:
                        print('DBG: replacing in file', full_path)
                        f.write(new_text)
                # else:
                #     for idx, matches in enumerate(all_matches):
                #         print("Match #{}: {}".format(idx, matches))

                if cfg.verbose or cfg.dry_run:
                    colorized_old = search_pattern.sub(Colors.LightBlue + r"\g<0>" + Colors.NoColor, old_text)
                    colorized_old = '\n'.join(['\t' + line.strip() for line in colorized_old.split('\n') if Colors.LightBlue in line])

                    colorized = search_pattern.sub(Colors.Green + cfg.replace_regex + Colors.NoColor, old_text)
                    colorized = '\n'.join(['\t' + line.strip() for line in colorized.split('\n') if Colors.Green in line])
                    print("{}BEFORE:{}\n{}".format(Colors.White, Colors.NoColor, colorized_old))
                    print("{}AFTER :{}\n{}".format(Colors.Yellow, Colors.NoColor, colorized))

            elif cfg.list_non_matching:
                print('File {} does not contain search regex "{}"'.format(filename, cfg.search_regex))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''DESCRIPTION:
    Find and replace recursively from the given folder using regular expressions''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''USAGE:
    {0} -d [my_folder] -s <search_regex> -r <replace_regex> -g [glob_pattern]

    '''.format(os.path.basename(sys.argv[0])))

    parser.add_argument('--dir', '-d',
                        help='folder to search in; by default current folder',
                        default='.')

    parser.add_argument('--search-regex', '-s',
                        help='search regex',
                        required=True)

    parser.add_argument('--replace-regex', '-r',
                        help='replacement regex',
                        required=True)

    parser.add_argument('--glob', '-g',
                        help='glob pattern, i.e. *.html',
                        default="*.*")

    parser.add_argument('--dry-run', '-dr',
                        action='store_true',
                        help="don't replace anything just show what is going to be done",
                        default=False)

    parser.add_argument('--create-backup', '-b',
                        action='store_true',
                        help='Create backup files',
                        default=False)

    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help="Show files which don't match the search regex",
                        default=False)

    parser.add_argument('--print-parent-folder', '-p',
                        action='store_true',
                        help="Show the parent info for debug",
                        default=False)

    parser.add_argument('--list-non-matching', '-n',
                        action='store_true',
                        help="Supress colors",
                        default=False)

    config = parser.parse_args(sys.argv[1:])

    find_replace(config)

