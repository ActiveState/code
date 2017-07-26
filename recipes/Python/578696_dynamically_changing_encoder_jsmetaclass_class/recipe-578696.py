    import json

    class smallDuck(object):
        def __init__(self, one, two, tree):
            self.one = one
            self.two = two
            self.tree = tree

    class myEncoder(json.JSONEncoder):

        def isInClasses(self, obj):
            for i in self.listOfClasses :
                if isinstance(obj, i):
                    return True
            return False

        def default(self, obj):
            if isinstance(obj, smallDuck):
                return { obj.__class__.__name__ : obj.__dict__ }
            return json.JSONEncoder.default(self, obj)

    def encoderFactory(listOfClasses):
        classDict = {"listOfClasses" : listOfClasses }
        return type("newEncoder", (myEncoder, ) , classDict)

    duck = [smallDuck("shit", 1, smallDuck(1,2,3)),2,3,4]
    with open("try.json", "w") as myf:
        string = json.dumps(duck, cls = encoderFactory([smallDuck]))
        myf.write(string)
