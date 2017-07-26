#!/usr/bin/python

import MySQLdb

class Tree(object):
    class Anon: pass
    
    def __init__(self, conn):
        self.conn = conn
    
    def insert_siblings(self, names, siblingname):
        self.conn.begin()
        sibling = self.retrieve(siblingname)
        cur = self.conn.cursor()
        cur.execute("UPDATE tree SET lhs = lhs + %s WHERE lhs > %s", (len(names)*2, sibling.rhs))
        cur.execute("UPDATE tree SET rhs = rhs + %s WHERE rhs > %s", (len(names)*2, sibling.rhs))
        
        cur.executemany("INSERT INTO tree SET (lhs, rhs, parent, name) VALUES  (%s, %s, %s, %s)",
                        [(sibling.rhs + 2*offset + 1,
                          sibling.rhs + 2*offset + 2,
                          sibling.parent, name) for offset, name in enumerate(names)])
        self.conn.commit()

    def insert_children(self, names, parentname):
        self.conn.begin()
        parent = self.retrieve(parentname)
        cur = self.conn.cursor()
        cur.execute("UPDATE tree SET lhs = lhs + %s WHERE lhs >= %s", (len(names)*2, parent.rhs))
        cur.execute("UPDATE tree SET rhs = rhs + %s WHERE rhs >= %s", (len(names)*2, parent.rhs))
        
        cur.executemany("INSERT INTO tree (lhs, rhs, parent, name) VALUES (%s, %s, %s, %s)",
                        [(parent.rhs + 2*offset,
                          parent.rhs + 2*offset + 1,
                          parent.ref, name) for offset, name in enumerate(names)])
        self.conn.commit()

    def delete(self, nodename):
        self.conn.begin()
        node = self.retrieve(nodename)
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tree WHERE lhs BETWEEN %s AND %s", (node.lhs, node.rhs))
        diff = node.rhs - node.lhs + 1;
        cur.execute("UPDATE tree SET lhs = lhs - %s WHERE lhs > %s", (diff, node.rhs))
        cur.execute("UPDATE tree SET rhs = rhs - %s WHERE rhs > %s", (diff, node.rhs))
        self.conn.commit()

    def create_root(self, name):
        self.conn.begin()
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(rhs) FROM tree");
        maxrhs = cur.fetchall()[0][0]
        if maxrhs is None: maxrhs = 1
        else: maxrhs = int(maxrhs)
        cur.execute("INSERT INTO tree (lhs, rhs, parent, name) VALUES (%s, %s, NULL, %s)", (maxrhs+1, maxrhs+2,name))
        self.conn.commit()

    def retrieve(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT ref, lhs, rhs, parent FROM tree WHERE name = %s", (name,))
        result = cur.fetchall()[0]
        retval = self.Anon()
        retval.name = name
        retval.ref = int(result[0])
        retval.lhs = int(result[1])
        retval.rhs = int(result[2])
        if(result[3]):
            retval.parent = int(result[3])
        else:
            retval.parent = None
        return retval

    def all_children_of(self, rootname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t1.lhs BETWEEN t2.lhs AND t2.rhs AND t1.name != t2.name AND t2.name = %s
            ORDER BY t1.lhs""", (rootname,))
        return [result[0] for result in cur.fetchall()]

    def exact_children_of(self, rootname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t1.parent = t2.ref AND t2.name = %s
            ORDER BY t1.lhs""", (rootname,))
        return [result[0] for result in cur.fetchall()]
    
    def all_siblings_of(self, siblingname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t1.parent = t2.parent AND t2.name = %s AND t1.name != %s
            ORDER BY t1.lhs""", (siblingname, siblingname))
        return [result[0] for result in cur.fetchall()]
    
    def leaves_below(self, rootname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t1.lhs BETWEEN t2.lhs AND t2.rhs AND t1.lhs + 1 = t1.rhs AND t2.name = %s
            ORDER BY t1.lhs""", (rootname,))
        return [result[0] for result in cur.fetchall()]

    def parent_of(self, childname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t1.ref = t2.parent AND t2.name = %s""", (childname,))
        return cur.fetchall()[0][0]
    
    def path_to(self, childname):
        cur = self.conn.cursor()
        cur.execute(
            """SELECT t1.name FROM tree AS t1, tree AS t2
            WHERE t2.lhs BETWEEN t1.lhs AND t1.rhs AND t2.name = %s
            ORDER BY t1.lhs""", (childname,))
        return [result[0] for result in cur.fetchall()]
    
################
# Demo functions
################

def draw_tree(tree, rootname):
    root = tree.retrieve(rootname)
    cur = tree.conn.cursor()
    cur.execute(
        """SELECT COUNT(t2.name) AS indentation, t1.name 
        FROM tree AS t1, tree AS t2
        WHERE t1.lhs BETWEEN t2.lhs AND t2.rhs
        AND t2.lhs BETWEEN %s AND %s
        GROUP BY t1.name
        ORDER BY t1.lhs""", (root.lhs, root.rhs))
    for result in cur.fetchall():
        print " " * (int(result[0])-1) + result[1]

def create_tree(tree, children_of, nameprefix = "", recursion_depth = 5):
    names = [nameprefix + str(i) for i in xrange(recursion_depth)]
    tree.insert_children(names, children_of)
    for name in names:
        create_tree(tree, name, name, recursion_depth-1)

if __name__ == "__main__":
    import sys

    conn = MySQLdb.Connect(user = sys.argv[1], passwd = sys.argv[2], db = sys.argv[3])
    cur = conn.cursor()
    
    try:
        cur.execute("DROP TABLE tree")
    except:
        pass
    cur.execute(
        """CREATE TABLE tree(ref int PRIMARY KEY AUTO_INCREMENT, parent int,
        lhs int, rhs int, name varchar(255), UNIQUE INDEX(name)) TYPE=InnoDB""")

    tree = Tree(conn)
    tree.create_root("root")
    create_tree(tree, "root")
    
    draw_tree(tree, "root")
    
    print "Number of children of root:", len(tree.all_children_of("root"))
    print "Number of leaves below root:", len(tree.leaves_below("root"))
    print "Exact children of root:", tree.exact_children_of("root")
    print "All siblings of 1:", tree.all_siblings_of("1")
    print "Parent of 11:", tree.parent_of("11")
    print "Path to 1220:", tree.path_to("1220")
