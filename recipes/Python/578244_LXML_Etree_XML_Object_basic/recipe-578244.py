from lxml import etree, objectify

def formatXML(parent):
    """                                                                                                       
    Recursive operation which returns a tree formated                                                         
    as dicts and lists.                                                                                       
    Decision to add a list is to find the 'List' word                                                         
    in the actual parent tag.                                                                                 
    """
    ret = {}
    if parent.items(): ret.update(dict(parent.items()))
    if parent.text: ret['__content__'] = parent.text
    if ('List' in parent.tag):
        ret['__list__'] = []
        for element in parent:
            if element.tag is not etree.Comment:
                ret['__list__'].append(formatXML(element))
    else:
        for element in parent:
            if element.tag is not etree.Comment:
                ret[element.tag] = formatXML(element)
    return ret
