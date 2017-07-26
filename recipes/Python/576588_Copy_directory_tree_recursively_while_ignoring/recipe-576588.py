import os
import shutil

SOURCE_DIR = os.getcwd()
TARGET_DIR = 'web'
IGNORE_PATTERNS = ('*.pyc','CVS','^.git','tmp','.svn')

if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)

shutil.copytree(SOURCE_DIR, TARGET_DIR, ignore=shutil.ignore_patterns(IGNORE_PATTERNS))
