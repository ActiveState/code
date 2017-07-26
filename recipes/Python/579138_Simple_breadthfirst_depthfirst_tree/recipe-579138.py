"""
recipe_simple_tree_traversal.py

Simple breadth-first and depth-first tree traversal for any tree.

The recipe is contained within the first two functions. The rest is
a test bed for demonstration.
"""
__author__ = "Jack Trainor"
__date__ = "2015-12-16"

import sys
    
def get_breadth_first_nodes(root):
    nodes = []
    stack = [root]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        nodes.append(cur_node)
        for child in cur_node.get_children():
            stack.append(child)
    return nodes

def get_depth_first_nodes(root):
    nodes = []
    stack = [root]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        nodes.append(cur_node)        
        for child in cur_node.get_rev_children():
            stack.insert(0, child)
    return nodes

########################################################################
class Node(object):
    def __init__(self, id_):
        self.id = id_
        self.children = []
        
    def __repr__(self):
        return "Node: [%s]" % self.id
    
    def add_child(self, node):
        self.children.append(node) 
    
    def get_children(self):
        return self.children         
    
    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children         

########################################################################
def println(text):
    sys.stdout.write(text + "\n")
    
def make_test_tree():
    a0 = Node("a0")
    b0 = Node("b0")      
    b1 = Node("b1")      
    b2 = Node("b2")      
    c0 = Node("c0")      
    c1 = Node("c1")  
    d0 = Node("d0")   
    
    a0.add_child(b0) 
    a0.add_child(b1) 
    a0.add_child(b2)
    
    b0.add_child(c0) 
    b0.add_child(c1) 
    
    c0.add_child(d0)
    
    return a0                  

def test_breadth_first_nodes():
    root = make_test_tree()
    node_list = get_breadth_first_nodes(root)
    for node in node_list:
        println(str(node))

def test_depth_first_nodes():
    root = make_test_tree()
    node_list = get_depth_first_nodes(root)
    for node in node_list:
        println(str(node))

########################################################################
if __name__ == "__main__":
    test_breadth_first_nodes()
    println("")
    test_depth_first_nodes()
  
