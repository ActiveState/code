    #!/usr/bin/env python

    import re, sys

    width = 79

    for line in sys.stdin:
      sys.stdout.write(re.sub(r'(.{1,%d})(\s|$)+' % width, r'\1\n', line))
