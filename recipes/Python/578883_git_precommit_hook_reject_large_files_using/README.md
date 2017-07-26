## git pre-commit hook to reject large files using Python

Originally published: 2014-05-23 21:05:04
Last updated: 2015-03-10 09:36:28
Author: Albert-Jan Roskam

This script should be saved in the templatedir, so it ends up in .git/hooks whenever you do a new git init.\nBy default, commits that contain files larger than 5 Mb are blocked. This is useful for preventing accidental large commits that are not caught by .gitignore. You can easily bypass the hook by specifing "--no-verify" with git commit. (in a previous version of this script, this did not work correctly)