from xml.dom.minidom import Document

def get_tree_representation_of_loaded_python_modules(self):
        modules = sys.modules.keys()
        modules.sort()

        tree_data = Document()
        node = tree_data.createElement('li')
        text = tree_data.createTextNode('Loaded Python Modules')
        node.appendChild(text)
        tree_data.appendChild(node)
        map = {}
        for module in modules:
            ms = module.split('.')
            path = node
            for level in range(len(ms)):
                nodes = map.get(level)
                if nodes == None:
                    node1 = tree_data.createElement('ul')
                    node2 = tree_data.createElement('li')
                    textNode = tree_data.createTextNode(ms[level])
                    node2.appendChild(textNode)
                    node1.appendChild(node2)
                    path.appendChild(node1)
                    nodes = [node2]
                    map[level] = nodes
                else:
                    node2 = None
                    for tmpNode in nodes:
                        if tmpNode.firstChild.data == ms[level]:
                            node2 = tmpNode
                            node1 = node2.parentNode
                    if node2 == None:
                        node1 = path.childNodes.item(1)
                        if node1==None:
                            node1 = tree_data.createElement('ul')
                            path.appendChild(node1)
                        node2 = tree_data.createElement('li')
                        textNode = tree_data.createTextNode(ms[level])
                        node2.appendChild(textNode)
                        node1.appendChild(node2)
                        nodes += [node2]
                        map[level] = nodes
                path = node2

        str = tree_data.toprettyxml()
        str = str[len('<?xml version="1.0" ?>')+1:]
        return str
