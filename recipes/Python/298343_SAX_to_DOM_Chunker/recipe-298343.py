"""
sax2dom_chunker.py    version 1.1

A SAX handler that takes a set of element paths and
creates a series of DOM chunks matching the element paths
for individual processing.  Designed for Python 2.2. or greater.

Copyright 2004 Fourthought Inc, USA.
This work is licensed under Creative Commons Attribution 1.0
For details: http://creativecommons.org/licenses/by/1.0/
"""

from xml import sax
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE, EMPTY_NAMESPACE
import xml.dom.minidom

DUMMY_DOCELEM = u'dummy'
START_STATE = 0
TOP = -1

class _state_machine:
    """
    A simple state machine specialized for DOM chunking from SAX
    A state is "live" when it represents the successful completion
    of a path.
    This is generally a signal to the handler using this state machine
    to start creating the DOM fragment from the subset of SAX
    events until we transit to a non-live state
    """
    def __init__(self, trim_to_paths):
        if not trim_to_paths:
            self.event = self.event_nop
            self.is_live = self.is_live_nop
            return
        self._state_table = {START_STATE: {}}
        self._live_states = []
        #Use the given trim paths to generate a state table
        newest_state = START_STATE
        for path in trim_to_paths:
            last_state = START_STATE
            for segment in path:
                start_event = (1, segment[0], segment[1])
                end_event = (0, segment[0], segment[1])
                if self._state_table[last_state].has_key(start_event):
                    top_state = \
                        self._state_table[last_state][start_event]
                else:
                    newest_state += 1
                    top_state = newest_state
                    self._state_table[top_state] = {}
                self._state_table[last_state][start_event] = \
                    top_state
                self._state_table[top_state][end_event] = \
                    last_state
                last_state = top_state
            self._live_states.append(top_state)
        self._state = START_STATE
        self.chunk_completed = 0
        return

    def event(self, is_start, ns, local):
        """
        Register an event and effect ant state transitions
        found in the state table
        """
        #We only have a chunk ready for the handler in
        #the explicit case below
        self.chunk_completed = 0
        lookup_from = self._state_table[self._state]
        if lookup_from.has_key((is_start, ns, local)):
             new_state = lookup_from[(is_start, ns, local)]
             #If we have completed a chunk, we set a flag for
             #The chunker
             if (self._state in self._live_states and
                 new_state not in self._live_states):
                 self.chunk_completed = 1
             self._state = new_state
        return self._state

    def is_live(self):
        """
        1 if the curent state is considered live, else 0
        """
        return self._state in self._live_states

    def event_nop(self, is_start, ns, local):
        pass

    def is_live_nop(self):
        return 1


class sax2dom_chunker(sax.ContentHandler):
    """
    Note: ignores nodes prior to the document element, such as PIs and
    text nodes
    This filter is only designed to work if you set features
    sax.handler.feature_namespaces
    and
    sax.handler.feature_namespace_prefixes
    to 1 on the parser you use.  It will not work on drivers that
    do not support these features.  The default drv_expat works fine
    in this case, but of course has but very limited DTD processing.
    It also collapses CDATA sections into plain text

    trim_to_paths - a list of lists of tuples.  Each tuple is of
        the form (namespace, local-name), providing one segment
        in a path of contained elements
        [
          [ (None, u'monty'), (None, u'python') ],
          [ (None, u'monty'), (None, u'spam'), ('urn:dummy', u'eggs') ]
        ]
        If None (the default, a DOM node will be created representing
        the entire tree.

    chunk_consumer - a callable object taking a DOM node.  It will be
        invoked as each DOM chunk is prepared.
    
    domimpl - DOM implemention to build, e.g. mindom (the default)
        or cDomlette or pxdom (if you have the right third-party
        packages installed).
    
    owner_doc - for advanced uses, if you want to use an existing
        DOM document object as the owner of all created nodes.
    """
    def __init__(self,
                 trim_to_paths=None,
                 chunk_consumer=None,
                 domimpl=xml.dom.minidom.getDOMImplementation(),
                 owner_doc=None
                 ):
        self._impl = domimpl
        if owner_doc:
            self._owner_doc = owner_doc
        else:
            dt = self._impl.createDocumentType(DUMMY_DOCELEM, None, u'')
            self._owner_doc = self._impl.createDocument(
                DUMMY_DOCELEM, DUMMY_DOCELEM, dt)
        #Create a docfrag to hold all the generated nodes.
        root_node = self._owner_doc.createDocumentFragment()
        self._nodeStack = [ root_node ]
        self.state_machine = _state_machine(trim_to_paths)
        self._chunk_consumer = chunk_consumer
        return

    def get_root_node(self):
        """
        Only useful if the user does not register trim paths
        If so, then after SAX processing the user can call this
        method to retrieve resulting DOm representing the entire
        document
        """
        return self._nodeStack[0]

    #Overridden DocumentHandler methods
    def startElementNS(self, name, qname, attribs):
        self.state_machine.event(1, name[0], name[1])
        if not self.state_machine.is_live():
            return
        (ns, local) = name
        new_element = self._owner_doc.createElementNS(ns, qname or local)

        for ((attr_ns, lname), value) in attribs.items():
            if attr_ns is not None:
                attr_qname = attribs.getQNameByName((attr_ns, lname))
            else:
                attr_qname = lname
            attr = self._owner_doc.createAttributeNS(
                attr_ns, attr_qname)
            attr_qname = attribs.getQNameByName((attr_ns, lname))
            attr.value = value
            new_element.setAttributeNodeNS(attr)

        self._nodeStack.append(new_element)
        return

    def endElementNS(self, name, qname):
        self.state_machine.event(0, name[0], name[1])
        if not self.state_machine.is_live():
            if (self._chunk_consumer and
                self.state_machine.chunk_completed):
                #Complete the element being closed because it
                #Is the last bit of a DOM to be fed to the consumer
                new_element = self._nodeStack[TOP]
                del self._nodeStack[TOP]
                self._nodeStack[TOP].appendChild(new_element)
                #Feed the consumer
                self._chunk_consumer(self._nodeStack[0])
                #Start all over with a new doc frag so the old
                #One's memory can be reclaimed
                root_node = self._owner_doc.createDocumentFragment()
                self._nodeStack = [ root_node ]
            return
        new_element = self._nodeStack[TOP]
        del self._nodeStack[TOP]
        self._nodeStack[TOP].appendChild(new_element)
        return

    def processingInstruction(self, target, data):
        if self.state_machine.is_live():
            pi = self._owner_doc.createProcessingInstruction(
                target, data)
            self._nodeStack[TOP].appendChild(pi)
        return

    #Overridden LexicalHandler methods
    def comment(self, text):
        if self.state_machine.is_live():
            new_comment = self._owner_doc.createComment(text)
            self._nodeStack[TOP].appendChild(new_comment)
        return

    def characters(self, chars):
        if self.state_machine.is_live():
            new_text = self._owner_doc.createTextNode(chars)
            self._nodeStack[TOP].appendChild(new_text)
        return
