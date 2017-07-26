# SectionPath.py

"""This module provides a simple utility to follow the path to an item in a
recursive tree structure. It can be used to build the section numbers for a
table of contents.

Instances of the SectionPath class are immutable and do not need to be
instantiated directly. Instead, use the "start" instance to begin the
descent into your tree.

Example:

>>> import SectionPath
>>> SectionPath.start
<SectionPath.SectionPath object at 0x4022580c>
>>> print SectionPath.start
1
>>> print SectionPath.start.sibling
2
>>> print SectionPath.start.sibling.child
2.1
>>> print SectionPath.start.sibling.child.child
2.1.1
>>> print SectionPath.start.sibling.child.child.sibling
2.1.2
>>> print SectionPath.start.sibling.child.child.sibling.sibling
2.1.3

See the bottom of this file for a real example of this module's use.
"""

class SectionPath(object):
    """Represents a path through the sections of a document tree."""

    def __init__(self, init_path):
        self.path = init_path

    def child(self):
        return SectionPath((1, self.path))
    child = property(child)

    def sibling(self):
        head, tail = self.path
        return SectionPath((head + 1, tail))
    sibling = property(sibling)

    def __str__(self):
        result = []
        path = self.path
        while path is not None:
            head, tail = path
            result.append(str(head))
            path = tail
        result.reverse()
        return '.'.join(result)

# Singleton instance. Use this to start your descent.
start = SectionPath((1, None))

if __name__ == '__main__':
    import SectionPath

    # Create a recursive tree structure. Each node in the tree is represented
    # by a (string, node list) tuple. In a more realistic scenario, objects
    # representing the content of the section could be stored instead of just
    # titles.
    tree = [
        ("About me", [
            ("My life", []),
            ("My cats", []),
            ("My lanta", []),
         ]),

        ("Portfolio", [
            ("Art", []),
            ("Music", [
                ("Vocal", []),
                ("Instrumental", []),
             ]),
            ("Poetry", [
                ("Bad", [])
             ]),
         ]),

        ("Conclusion", [
            ("Recursion is hard", []),
            ("Python makes it easier", []),
         ]),

        # etc.
    ]

    def print_toc(tree):
        def recurse(sections, path):
            for section in sections:
                # Unpack each tree node as (string, list) tuple.
                title, children = section

                # Print the current section number and its title.
                # Converting "path" to a string yields the section number.
                print '%s. %s' % (path, title)

                # Call this function recursively for each child, passing the
                # "child" property of the path.
                recurse(children, path.child)

                # Advance the path to the next sibling.
                path = path.sibling

        # Call the recursive function, using the "start" path to begin
        # generating section numbers starting at "1".
        recurse(tree, SectionPath.start)

    # Pass the recursive tree structure into the table of contents printer.
    print_toc(tree)

    # Expected output:
    #
    # 1. About me
    # 1.1. My life
    # 1.2. My cats
    # 1.3. My lanta
    # 2. Portfolio
    # 2.1. Art
    # 2.2. Music
    # 2.2.1. Vocal
    # 2.2.2. Instrumental
    # 2.3. Poetry
    # 2.3.1. Bad
    # 3. Conclusion
    # 3.1. Recursion is hard
    # 3.2. Python makes it easier
