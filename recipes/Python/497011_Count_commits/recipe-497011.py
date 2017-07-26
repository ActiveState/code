#! /usr/bin/env python
import pysvn, re

def repos(work_path):
    "Get the svn repository url"
    info = pysvn.Client().info(work_path)

    if info.repos:
        return info.repos

    # special case - checked out the trunk
    if info.url.endswith("/trunk"):
        return re.sub(r"/trunk$", "", info.url)

    # default to the current dir's url
    return info.url

def authors(repos):
    "Get the authors who have commited to the repository, one name per commit"
    return [log["author"] for log in pysvn.Client().log(repos)]

def histogram(seq):
    result = {}
    for x in seq:
        result.setdefault(x, 0)
        result[x] += 1
    return result

def format2cols(items):
    max_width = max(len(str(x)) for (x,y) in items)
    template = "%%%ds %%s" % max_width
    return "\n".join(template % (x, y) for (x, y) in items)

def sort_uniq_c(seq):
    "Duplicate unix's 'sort | uniq -c | sort -nr'"
    count_first = ((y,x) for (x,y) in histogram(seq).items())
    return format2cols(sorted(count_first, reverse=True))

if __name__ == "__main__":
    print sort_uniq_c(authors(repos(work_path = '.')))
