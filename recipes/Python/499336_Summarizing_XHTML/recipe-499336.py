# -*- encoding: utf-8 -*-
import re

_tagopenre = re.compile(r'(?P<starws>\s?)<(?P<tagname>[^/][^> /]*)(?P<tagcontents>[^>]*)>(?P<endws>\s?)',re.MULTILINE)
_tagclosere = re.compile(r'(?P<startws>\s?)</(?P<tagname>[^>]+)>(?P<endws>\s?)')
_tagselfre = re.compile(r'(?P<startws>\s?)<(?P<tag>[^\d/>][^/>]*)/>(?P<endws>\s?)',re.MULTILINE)
_tagre = re.compile(r'<([^>]+)>', re.MULTILINE)
_selfclosere = re.compile('/\s*>\s*$')
_wsre = re.compile('\s+', re.MULTILINE)
_wsgtre = re.compile('\s+|>', re.MULTILINE)

def _find_ws(s, start=0, end=None):
    '''Find whitespace. Interface similar to str.find.'''
    if end is not None:
        s = s[start:end]
    else:
        s = s[start:]
    x = _wsre.search(s)
    if x:
        return x.start()+start
    else:
        return -1

def _find_ws_or_gt(s, start=0, end=None):
    '''Find whitespace or greater than ('>') sign. Interface similar to str.find.'''
    if end is not None:
        s = s[start:end]
    else:
        s = s[start:]
    x = _wsgtre.search(s)
    if x:
        return x.start()+start
    else:
        return -1

def summarize_html(html, maxwords = 25):
    if html is None:
        return ''
    tagopen = _tagopenre
    tagclose = _tagclosere
    tagre = _tagre
    tagself = _tagselfre
    tags = [0]
    taglist = []
    def tagopen_sub(match):
        tag = match.string[match.start():match.end()]
        taglist.append(tag)
        if _selfclosere.search(tag):
            r = '<%d/>'%tags[0]
        else:
            r = '<%d>'%tags[0]
        tags[0] += 1
        return r
    def tagclose_sub(match):
        r = '</%d>'%tags[0]
        taglist.append(match.string[match.start():match.end()])
        tags[0] += 1
        return r
    def tagself_sub(match):
        r = '<%d/>'%tags[0]
        taglist.append(match.string[match.start():match.end()])
        tags[0] += 1
        return r
    # preprocess text, fill taglist
    tagged = html.replace('&nbsp;', ' ')
    tagged = tagopen.sub(tagopen_sub, tagged)
    tagged = tagclose.sub(tagclose_sub, tagged)
    tagged = tagself.sub(tagself_sub, tagged)
    tagged = tagre.sub(r' <\1> ', tagged)
    # setup for processing
    splittags = tagged.split()
    alist = [None]*len(splittags)
    words = 0
    tagstack = []
    addspace = False
    do_not_add_dots = False
    is_table_row = 0    # misnamed: used to count nested table rows
    was_table_row = False
    for i,elem in enumerate(splittags):
        # modifying the list you're iterating is a crime, so we make ourselves
        # another one and fill it when needed
        alist[i] = elem

        # end condition
        if words >= maxwords and not is_table_row:
            # special case: tables
            if was_table_row:
                do_not_add_dots = True
            break
        # an usual word
        if not elem.startswith('<'):
            words += 1
            if addspace:
                alist[i] = ' '+elem
            addspace = True
        # a opening tag
        elif not elem.startswith('</') and not elem.endswith('/>'):
            tag = taglist[int(elem[1:-1])]
            tested = tag.strip()
            if tested[:3] == '<tr' and _find_ws(tested[:4]) in (-1, 3):
                is_table_row += 1
            # comment tags need not be closed
            if not tested.startswith('<!'):
                tagstack.append(tag)
            alist[i] = tag
            addspace = False
        # a closing tag
        elif not elem.endswith('/>'):
            addspace = False
            try:
                top = tagstack[-1]
            except IndexError:
                raise ValueError('tag not opened: %s'%elem)
            # extract the tagname from top of the stack
            top = top[top.find('<')+1:top.find('>')]
            cut = _find_ws(top)
            if cut > 0:
                top = top[:cut]
            # extract the tagname from the tag list
            fromlist = taglist[int(elem[2:-1])]
            tag = fromlist[fromlist.find('/')+1:fromlist.find('>')]

            if top != tag:
                raise ValueError('tag not closed properly: %s, got %s'%(top, tag))
            # special case: tables
            # some other tags could use special-casing, like dt/dd
            if top == 'tr':
                is_table_row -= 1
                was_table_row = True
                if is_table_row < 0:
                    is_table_row = 0
            else:
                was_table_row = False
            # close the tag
            tagstack.pop()
            alist[i] = fromlist
        # a self-closing tag
        else:
            tag = taglist[int(elem[1:-2])]
            alist[i] = tag
            addspace = False
    else:
        do_not_add_dots = True
        i += 1
    if words < maxwords:
        # normalize whitespace (actually not needed... makes the tests pass, though)
        return _wsre.sub(' ', html)
    # take care so no monstrousities like '......' appear at the end of output
    if alist[i-1][-1] in ('.', ',', ':', '?', '!'):
        alist[i-1] = re.sub(r'[\.,:?!]+$', '', alist[i-1])
    # close remaining open tags
    tagstack.reverse()
    if not do_not_add_dots:
        result = alist[:i] + ['...'] + ['</%s>'%x[x.find('<')+1:_find_ws_or_gt(x,1)] for x in tagstack]
    elif was_table_row:
        result = alist[:i] + ['</%s>'%x[x.find('<')+1:_find_ws_or_gt(x,1)] for x in tagstack]
    else:
        result = alist[:i] + ['</%s>'%x[x.find('<')+1:_find_ws_or_gt(x,1)] for x in tagstack]
    # normalize whitespace...
    r = _wsre.sub(' ', ''.join(result))
    return r
