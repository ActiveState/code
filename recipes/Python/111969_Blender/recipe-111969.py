import types

class Blender:
    """blends values into the given pattern.replace
        if neither values nor pattern are defined a default
        pattern is being created that prints the values of
        the instance in the format [name1: value1, name2 = value2, ...]
        """

    def __init__(self, pattern = None, values = None,
                 startToken = "${", endToken = "}"):
        """initializes the instance with defaultvalues.
        that is the start and the end token
        """
        self.BlendPattern = pattern
        self.BlendValues = values
        self.StartToken = startToken
        self.EndToken = endToken

    def blend(self, values = None, pattern = None):
        """blends the values into the given pattern"""
        values = self.getValues(values)
        pattern = self.getPattern(pattern, values)
        for name in values.keys():
            id = self.getTokenName(name)
            value = values[name]
            pattern = pattern.replace(id, str(value))
        return pattern

    def getValues(self, values):
        """ returns the dictionary of values.
            if no values are supplied this
            instance is returned as a dictionary."""
        if values == None:
            if self.BlendValues == None:
                values = self.__dict__
            else:
                values = self.BlendValues
        if type(values) != types.DictionaryType:
            values = values.__dict__
        return values

    def getBasePattern(self, values):
        """returns a pattern in the format
            [name1: value1, name2: value2, ...]
            excluding the instance-attributes of this class
            """
        names = values.keys()
        names.sort()
        result = "["
        for name in names:
            if name not in ["BlendPattern",
                            "BlendValues",
                            "StartToken",
                            "EndToken"]:
                result += name + ": " + self.getTokenName(name) + ", "
        return result[0:-2] + "]"

    def getPattern(self, pattern, values):
        """returns a pattern for this instance. if no pattern is defined
            returns a default-pattern.
            """
        if pattern == None:
            if self.BlendPattern == None:
                pattern = self.getBasePattern(values)
            else:
                pattern = self.BlendPattern
        return pattern

    def getTokenName(self, name):
        """returns the tokenname bound by the start and end token.
        """
        return self.StartToken + name + self.EndToken

    def __str__(self):
        return self.blend()

class Person(Blender):
    def __init__(self, name, lastName):
        Blender.__init__(self)
        self.Name = name
        self.LastName = lastName

class User(Person):
    def __init__(self, id, name, lastName):
        Person.__init__(self, name, lastName)
        self.ID = id

class Login(Blender):
    def __init__(self):
        Blender.__init__(self)
        self.BlendPattern = """
            Hello ${Name} ${LastName}!
            Your Userid is: ${ID}.
            You are logged into domain ${Domain}.
        """

class UserQuery(Blender):
    def __init__(self, values):
        pattern = """
            SELECT *
            FROM User
            WHERE
                id = ${ID} AND
                domain like '${Domain}'
            """
        Blender.__init__(self, pattern, values)

if __name__ == "__main__":
    p = Person("Robert", "Kuzelj")
    print p

    u = User("007", "Robert", "Kuzelj")
    print u

    login = Login()
    login.Name = "Robert"
    login.LastName = "Kuzelj"
    login.ID = 7
    login.Domain = "python.org"
    print login
    
    sql = "SELECT * from User WHERE id=:{ID} AND domain like ':{Domain}'"
    print Blender(sql, {"Domain": "python.org", "ID": "007"}, ":{", "}")

    print UserQuery(login)
