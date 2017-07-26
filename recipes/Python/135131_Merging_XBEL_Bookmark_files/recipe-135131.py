#!/usr/bin/env python
from __future__ import generators
from xml.dom import Node
from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint


def in_order_iterator_filter(node, filter_func):
    if filter_func(node):
        yield node
    for child in node.childNodes:
        for cn in in_order_iterator_filter(child, filter_func):
            if filter_func(cn):
                yield cn
    return


def get_elements_by_tag_name_ns(node, ns, local):
    return in_order_iterator_filter(
               node,
               lambda n: n.nodeType == Node.ELEMENT_NODE and \
                         n.namespaceURI == ns and n.localName == local
           )


def string_value(node):
    text_nodes = in_order_iterator_filter(
        node, lambda n: n.nodeType == Node.TEXT_NODE)
    return u''.join([ n.data for n in text_nodes ])


def get_title(node):
    return string_value(
        get_elements_by_tag_name_ns(node, None, 'title').next())


def merge_folders(folder_node1, folder_node2):
    #Folder element children of folder1
    folder1_folders = \
        [ n for n in folder_node1.childNodes if n.nodeName == 'folder' ]
    #Yes, the list must be copied to avoid mutate-while-iterate bugs
    for elem in folder_node2.childNodes[:]:
        #No need to copy title element
        if elem.nodeName == 'title':
            continue
        #
        elif elem.nodeName == 'folder':
            title = get_title(elem)
            for a_folder in folder1_folders:
                if title == get_title(a_folder):
                    merge_folders(a_folder, elem)
                    break
            else:
                folder_node1.appendChild(elem)
        else:
            folder_node1.appendChild(elem)


def xbel_merge(xbel1, xbel2):
    xbel1_top_level = \
        [ n for n in xbel1.documentElement.childNodes \
            if n.nodeType == Node.ELEMENT_NODE ]
    xbel1_top_level_folders = \
        [ n for n in xbel1_top_level if n.nodeName == 'folder' ]
    xbel1_top_level_bookmarks = \
        [ n for n in xbel1_top_level if n.nodeName == 'bookmark' ]
    xbel2_top_level = \
        [ n for n in xbel2.documentElement.childNodes \
            if n.nodeType == Node.ELEMENT_NODE ]
    for elem in xbel2_top_level:
        if elem.nodeName == 'folder':
            title = get_title(elem)
            for a_folder in xbel1_top_level_folders:
                if title == get_title(a_folder):
                    merge_folders(a_folder, elem)
                    break
            else:
                xbel1.documentElement.appendChild(elem)
        elif elem.nodeName == 'bookmark':
            xbel1.documentElement.appendChild(elem)
    return xbel1


if __name__ == "__main__":
    import sys
    xbel1 = NonvalidatingReader.parseUri(sys.argv[1])
    xbel2 = NonvalidatingReader.parseUri(sys.argv[2])
    new_xbel = xbel_merge(xbel1, xbel2)
    PrettyPrint(new_xbel)
