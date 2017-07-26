def align(tree, text):
    """Aligns each ElementTree element with its offsets in the text.

    Returns a list of (element, start, stop) tuples.

    Keyword Arguments:
    tree -- An ElementTree for an XML document
    text -- The text to which the XML should be aligned. The text and
        XML should only differ in the presence or absence of XML
        elements and whitespace.
    """

    def align_helper(elem, elem_start):
        # skip whitespace in the text before the element
        while text[elem_start:elem_start + 1].isspace():
            elem_start += 1

        # advance the element end past any element text            
        elem_end = elem_start
        if elem.text is not None:
            for i, char in enumerate(elem.text):
                if not char.isspace():
                    while text[elem_end:elem_end + 1].isspace():
                        elem_end += 1
                    assert text[elem_end:elem_end + 1] == char
                    elem_end += 1

        # advance the element end past any child elements
        for child_elem in elem:
            elem_end = align_helper(child_elem, elem_end)

        # advance the start for the next element past the tail text
        next_start = elem_end
        if elem.tail is not None:
            for i, char in enumerate(elem.tail):
                if not char.isspace():
                    while text[next_start:next_start + 1].isspace():
                        next_start += 1
                    assert text[next_start:next_start + 1] == char
                    next_start += 1

        # add the element and its start and end to the result list
        result.append((elem, elem_start, elem_end))

        # return the start of the next element        
        return next_start

    result = []
    align_helper(tree, 0)
    return result
