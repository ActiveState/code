import re, os, sys
from difflib import SequenceMatcher, context_diff
from datetime import datetime
from itertools import islice

vline = re.compile(r'\.V(?:_\S+)? (\S+) (\S+) ?(.*)').match
nline = re.compile(r'\.N (.*)').match
cline = re.compile(r'\.C (\d+) (\d+)').match
iline = re.compile(r'\.I (\d+)').match

def get_version(repo_fn, v=None):
    # Return version *v* or the last version if *v* is None.
    if not os.path.exists(repo_fn):
        return ''

    currver = 0
    curr = []
    f = iter(open(repo_fn, 'r'))
    line = next(f, '')
    while line and (v is None or currver < v):

        # Start building up next version from the last
        currver += 1
        prev, curr = curr, []

        # Process mandatory .V line and optional .N msg lines
        assert line.startswith('.V')
        for line in f:
            if not line.startswith('.N'):
                break

        # Process the .I and .C instructions
        while line and line.startswith(('.I', '.C')):
            if line.startswith('.I'):
                n = int(iline(line).group(1))
                curr.extend(islice(f, n))
            else:
                m, n = map(int, cline(line).groups())
                curr.extend(prev[m-1:n])
            line = next(f, '')

    return ''.join(curr)

def print_log(repo_fn, v=None):
    # Print log entries. *v* is a specific version number or None to print all.
    currver = 0
    f = iter(open(repo_fn, 'r'))
    line = next(f, '')
    while line:

        # Process mandatory .V line and optional .N msg lines
        assert line.startswith('.V')
        repo_fn, datetime, msg = vline(line).groups()
        for line in f:
            if line.startswith('.N'):
                msg += '\n' + nline(line).group(1)
            else:
                break

        currver += 1
        if v is None:
            print "%s %d %18s %s" % (repo_fn, currver, datetime, msg)
        elif currver == v:            
            print "%s %d %18s %s" % (repo_fn, currver, datetime, msg)
            return

        # Skip through the .I and .C instructions
        while line and line.startswith(('.I', '.C')):
            if line.startswith('.I'):
                n = int(iline(line).group(1))
                for line in islice(f, n):
                    pass
            line = next(f, '')

def diff(repo_fn, vnum1=None, vnum2=None, context=False):
    # vnum1 or vnum2 can be None to indicate last version in repository
    # vnum2 can be a filename to compare to
    v1 = get_version(repo_fn, vnum1).splitlines(True)
    if isinstance(vnum2, int) or vnum2 is None:
        v2 = get_version(repo_fn, vnum2).splitlines(True)
    else:
        v2 = open(vnum2).readlines()
    results = []
    if context:
        return ''.join(context_diff(v1, v2))
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, v1, v2).get_opcodes():
        if tag in ('replace', 'insert'):
            results.append('.I %d\n' % (j2-j1))
            results.extend(v2[j1:j2])
        elif tag == 'equal':
            results.append('.C %d %d\n' % (i1+1, i2))
    return ''.join(results)

def make_header(filename, msg, create):
    first = '_,03000' if create else ''
    datestring = datetime.now().strftime('%d-%b-%y,%H:%M:%S')
    return '.V%(first)s %(filename)s %(datestring)s %(msg)s' % locals()

def get_repo_fn(filename):
    path, fullname = os.path.split(filename)
    base, ext = os.path.splitext(fullname)
    ext = ext or '.'
    newext = ext[:2] + '$' + ext[3:]
    result = os.path.join(repo_dir, base + newext)
    return result

repo_dir = os.environ.get('VCS', '.')

# ------- Command-line interface -------

help_msg = '''
Usage:
    vcs add foo.bar "Checkin message"
    vcs extract foo.bar [revnum]
    vcs log foo.bar [revnum]
    vcs diff foo.bar [revnum1 [revnum2]]

Repository:
    %s
    ''' % repo_dir

def talkback(msg, help=False, code=1):
    print >> sys.stderr, msg
    if help:
        print >> sys.stderr, '\n' + help_msg
    sys.exit(code)

def main(argv):
    # XXX add support for branching
    # XXX support .N for output
    if len(argv) <= 1:
        talkback(help_msg, code=0)
    if len(argv) < 3:
        talkback('Not enough arguments. Need a command and filename.', help=True)
    command = argv[1].lower()
    if command not in 'log extract diff add update l e d a u'.split():
        talkback('Unknown command: ' + command, help=True)
    command = command[:1]
    filename = argv[2]
    repo_fn = get_repo_fn(filename)

    if command in 'le':
        if not os.path.exists(repo_fn):
            talkback(repo_fn + ' not found')
        v = int(argv[3]) if len(argv) >= 4 else None
        if command == 'l':
            print_log(repo_fn, v)
        else:
            print get_version(repo_fn, v),
    elif command == 'd':
        v1 = int(argv[3]) if len(argv) >= 4 else None
        v2 = int(argv[4]) if len(argv) >= 5 else filename
        print diff(repo_fn, v1, v2, context=True),
    elif command in 'au':
        if not os.path.exists(filename):
            talkback('Cannot find file: ' + filename)
        d = diff(repo_fn, None, filename)
        if len(d.splitlines()) == 1:
            talkback('File is already current. There are no changes.', code=0)
        msg = ' '.join(argv[3:])
        create = not os.path.exists(repo_fn)
        repo_file = open(repo_fn, 'a+')
        print >> repo_file, make_header(filename, msg, create)
        print >> repo_file, d,
        repo_file.close()
        talkback('Added to ' + repo_fn, code=0)
    else:
        talkback('Unreachable')


if __name__ == '__main__':
    main(sys.argv)
