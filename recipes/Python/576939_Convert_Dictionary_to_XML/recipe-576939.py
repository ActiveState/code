def dict2xml(dict, xml = ''):
    for key,value in dict.iteritems():
        exec 'content = '+ {'str': 'value', 'dict': 'dict2xml(value)'}[type(value).__name__]
        xml += '<%s>%s</%s>' % (key, str(content), key)
    return xml
