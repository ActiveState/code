# python Octree v.1

# UPDATED:
# Is now more like a true octree (ie: partitions space containing objects)

# Important Points to remember:
# The OctNode positions do not correspond to any object position
# rather they are seperate containers which may contain objects
# or other nodes.

# An OctNode which which holds less objects than MAX_OBJECTS_PER_CUBE
# is a LeafNode; it has no branches, but holds a list of objects contained within
# its boundaries. The list of objects is held in the leafNode's 'data' property

# If more objects are added to an OctNode, taking the object count over MAX_OBJECTS_PER_CUBE
# Then the cube has to subdivide itself, and arrange its objects in the new child nodes.
# The new octNode itself contains no objects, but its children should.

# Psyco may well speed this script up considerably, but results seem to vary.

# TODO: Add support for multi-threading for node insertion and/or searching

#### Global Variables ####

# This defines the maximum objects an LeafNode can hold, before it gets subdivided again.
MAX_OBJECTS_PER_CUBE = 10

# This dictionary is used by the findBranch function, to return the correct branch index
DIRLOOKUP = {"3":0, "2":1, "-2":2, "-1":3, "1":4, "0":5, "-4":6, "-3":7}

#### End Globals ####

# Try importing psyco, in case it makes any speed difference
# ( Speed increase seems to vary depending on system ).
try:
    import psyco
    psyco.full()
except:
    print "Could not import psyco, speed may suffer :)"

class OctNode:
    # New Octnode Class, can be appended to as well i think
    def __init__(self, position, size, data):
        # OctNode Cubes have a position and size
        # position is related to, but not the same as the objects the node contains.
        self.position = position
        self.size = size

        # All OctNodes will be leaf nodes at first
        # Then subdivided later as more objects get added
        self.isLeafNode = True

        # store our object, typically this will be one, but maybe more
        self.data = data
        
        # might as well give it some emtpy branches while we are here.
        self.branches = [None, None, None, None, None, None, None, None]

        # The cube's bounding coordinates -- Not currently used
        self.ldb = (position[0] - (size / 2), position[1] - (size / 2), position[2] - (size / 2))
        self.ruf = (position[0] + (size / 2), position[1] + (size / 2), position[2] + (size / 2))
        

class Octree:
    def __init__(self, worldSize):
        # Init the world bounding root cube
        # all world geometry is inside this
        # it will first be created as a leaf node (ie, without branches)
        # this is because it has no objects, which is less than MAX_OBJECTS_PER_CUBE
        # if we insert more objects into it than MAX_OBJECTS_PER_CUBE, then it will subdivide itself.
        self.root = self.addNode((0,0,0), worldSize, [])
        self.worldSize = worldSize

    def addNode(self, position, size, objects):
        # This creates the actual OctNode itself.
        return OctNode(position, size, objects)

    def insertNode(self, root, size, parent, objData):
        if root == None:
            # we're inserting a single object, so if we reach an empty node, insert it here
            # Our new node will be a leaf with one object, our object
            # More may be added later, or the node maybe subdivided if too many are added
            # Find the Real Geometric centre point of our new node:
            # Found from the position of the parent node supplied in the arguments
            pos = parent.position
            # offset is halfway across the size allocated for this node
            offset = size / 2
            # find out which direction we're heading in
            branch = self.findBranch(parent, objData.position)
            # new center = parent position + (branch direction * offset)
            newCenter = (0,0,0)
            if branch == 0:
                # left down back
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
                
            elif branch == 1:
                # left down forwards
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 2:
                # right down forwards
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 3:
                # right down back
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )

            elif branch == 4:
                # left up back
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )

            elif branch == 5:
                # left up forward
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
                
            elif branch == 6:
                # right up forward
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )

            elif branch == 7:
                # right up back
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            # Now we know the centre point of the new node
            # we already know the size as supplied by the parent node
            # So create a new node at this position in the tree
            # print "Adding Node of size: " + str(size / 2) + " at " + str(newCenter)
            return self.addNode(newCenter, size, [objData])
        
        #else: are we not at our position, but not at a leaf node either
        elif root.position != objData.position and root.isLeafNode == False:
            
            # we're in an octNode still, we need to traverse further
            branch = self.findBranch(root, objData.position)
            # Find the new scale we working with
            newSize = root.size / 2
            # Perform the same operation on the appropriate branch recursively
            root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, objData)
        # else, is this node a leaf node with objects already in it?
        elif root.isLeafNode:
            # We've reached a leaf node. This has no branches yet, but does hold
            # some objects, at the moment, this has to be less objects than MAX_OBJECTS_PER_CUBE
            # otherwise this would not be a leafNode (elementary my dear watson).
            # if we add the node to this branch will we be over the limit?
            if len(root.data) < MAX_OBJECTS_PER_CUBE:
                # No? then Add to the Node's list of objects and we're done
                root.data.append(objData)
                #return root
            elif len(root.data) == MAX_OBJECTS_PER_CUBE:
                # Adding this object to this leaf takes us over the limit
                # So we have to subdivide the leaf and redistribute the objects
                # on the new children. 
                # Add the new object to pre-existing list
                root.data.append(objData)
                # copy the list
                objList = root.data
                # Clear this node's data
                root.data = None
                # Its not a leaf node anymore
                root.isLeafNode = False
                # Calculate the size of the new children
                newSize = root.size / 2
                # distribute the objects on the new tree
                # print "Subdividing Node sized at: " + str(root.size) + " at " + str(root.position)
                for ob in objList:
                    branch = self.findBranch(root, ob.position)
                    root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, ob)
        return root

    def findPosition(self, root, position):
        # Basic collision lookup that finds the leaf node containing the specified position
        # Returns the child objects of the leaf, or None if the leaf is empty or none
        if root == None:
            return None
        elif root.isLeafNode:
            return root.data
        else:
            branch = self.findBranch(root, position)
            return self.findPosition(root.branches[branch], position)
            

    def findBranch(self, root, position):
        # helper function
        # returns an index corresponding to a branch
        # pointing in the direction we want to go
        vec1 = root.position
        vec2 = position
        result = 0
        # Equation created by adding nodes with known branch directions
        # into the tree, and comparing results.
        # See DIRLOOKUP above for the corresponding return values and branch indices
        for i in range(3):
            if vec1[i] <= vec2[i]:
                result += (-4 / (i + 1) / 2)
            else:
                result += (4 / (i + 1) / 2)
        result = DIRLOOKUP[str(result)]
        return result

## ---------------------------------------------------------------------------------------------------##


if __name__ == "__main__":

    ### Object Insertion Test ###
    
    # So lets test the adding:
    import random
    import time

    #Dummy object class to test with
    class TestObject:
        def __init__(self, name, position):
            self.name = name
            self.position = position

    # Create a new octree, size of world
    myTree = Octree(15000.0000)

    # Number of objects we intend to add.
    NUM_TEST_OBJECTS = 2000

    # Number of collisions we're going to test
    NUM_COLLISION_LOOKUPS = 2000

    # Insert some random objects and time it
    Start = time.time()
    for x in range(NUM_TEST_OBJECTS):
        name = "Node__" + str(x)
        pos = (random.randrange(-4500.000, 4500.000), random.randrange(-4500.00, 4500.00), random.randrange(-4500.00, 4500.00))
        testOb = TestObject(name, pos)
        myTree.insertNode(myTree.root, 15000.000, myTree.root, testOb)
    End = time.time() - Start

    # print some results.
    print str(NUM_TEST_OBJECTS) + "-Node Tree Generated in " + str(End) + " Seconds"
    print "Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each."

    ### Lookup Tests ###

    # Look up some random positions and time it
    Start = time.time()
    for x in range(NUM_COLLISION_LOOKUPS):
        pos = (random.randrange(-4500.000, 4500.000), random.randrange(-4500.00, 4500.00), random.randrange(-4500.00, 4500.00))
        result = myTree.findPosition(myTree.root, pos)
        
        ##################################################################################
        # This proves that results are being returned - but may result in a large printout
        # I'd just comment it out and trust me :)
        # print "Results for test at: " + str(pos)
        # if result != None:
        #    for i in result:
        #        print i.name, i.position,
        # print
        ##################################################################################
        
    End = time.time() - Start

    # print some results.
    print str(NUM_COLLISION_LOOKUPS) + " Collision Lookups performed in " + str(End) + " Seconds"
    print "Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each."

    x = raw_input("Press any key (Wheres the any key?):")
