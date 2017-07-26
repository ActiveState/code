def LineIndent(text, indent, maxwidth=None):
    """ indent each new line with 'indent' """
    if maxwidth:
        parts = []
        for part in text.split('\n'):
            words = part.split(' ')
            lines = []
            tmpline = ''
            for word in words:
                if len(tmpline+' '+word) > maxwidth:
                    lines.append(tmpline.strip())
                    tmpline = word
                else:
                    tmpline += ' ' + word
                
            lines.append(tmpline.strip())
            start = "\n%s"%indent
            parts.append(indent + start.join(lines))
        return "\n".join(parts)
    else:
        text = indent+text
        text = text.replace('\n','\n%s'%indent)
    return text



def test__LineIndent():
    t='''There seems to be a problem with paragraphs that are long and on '''\
       '''multiple lines. Now there is a simple solution to this.

First you go to ASPN and look at this example, then you download it and use '''\
'''it in your own scripts. Let's hope you're lucky.'''
    
    print LineIndent(t, '*'*4, maxwidth=50)
    print "--------------------------------"
    print LineIndent(t, '> ', maxwidth=35)
    print "--------------------------------"    
    print LineIndent(t, '*'*4)
    
if __name__=='__main__':
    test__LineIndent()
