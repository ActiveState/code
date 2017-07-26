###Move files with rename if required

Originally published: 2012-04-30 11:08:13
Last updated: 2012-04-30 11:09:05
Author: John Reid

A python script that renames (moves) files to a destination\ndirectory. However it will not overwrite existing files. The\nscript uses a renaming strategy where a count is incremented\nin order to avoid naming conflicts.\n\nExample usage::\n\n    mv-rename a.ext b.ext target-dir/\n\nwould mv a.ext and b.ext into the target directory. If::\n\n    target-dir/a.ext\n    target-dir/b.ext\n\nalready exist, the newly moved files would be named::\n\n    target-dir/a-<N>.ext\n    target-dir/b-<M>.ext\n\nwhere <N> and <M> are the lowest numbers such that there\nis no conflict.\n