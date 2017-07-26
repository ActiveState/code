###smart copy

Originally published: 2015-02-06 09:44:10
Last updated: 2015-02-06 09:45:12
Author: yota 

take a glob expression, a source directory and a destination directory to copy each files matching the glob in the appropriate directory\n\n    glob = */*.txt\n    src_dir = ./a/b\n    dst_dir = /z/x/y\n\nif the glob match a file `./a/b/c/foo.txt`, it will copy it in `/z/x/y/c/foo.txt` (and create the missing directory if needed)\n\nRequire Python3.4, code tab indented