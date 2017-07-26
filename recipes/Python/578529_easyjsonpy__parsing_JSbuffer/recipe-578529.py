"""
   @author  Thomas Lehmann
   @file    easyjson.py

   Copyright (c) 2013 Thomas Lehmann

   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
   documentation files (the "Software"), to deal in the Software without restriction, including without limitation
   the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
   and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all copies
   or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
def tokenize(buffer):
    """ tokenizes a JSON string """
    tokens   = []
    maxIndex = len(buffer)-1
    index    = 0
    while index <= maxIndex:
        if buffer[index] in ["{", "}", ":", ",", "[", "]"]:
            tokens.append(buffer[index])
            index += 1
        elif buffer[index] in ".1234567890":
            current = index + 1
            while current <= maxIndex and buffer[current] in ".1234567890":
                current += 1
            token = buffer[index:current]
            if token.find(".") >= 0: tokens.append(float(token))
            else: tokens.append(int(token))
            index = current
        elif buffer[index] == "\"":
            current = index+1
            while current <= maxIndex and (buffer[current-1] == "\\" or buffer[current] != "\""):
                current += 1
            tokens.append(buffer[index+1:current].replace("\\",""))
            index = current+1
        elif index+4 <= maxIndex and buffer[index:index+4] == "true":
            tokens.append(True)
            index += 4
        elif index+5 <= maxIndex and buffer[index:index+5] == "false":
            tokens.append(False)
            index += 5
        elif index+4 <= maxIndex and buffer[index:index+4] == "null":
            tokens.append(None)
            index += 4
        else:
            index += 1
    return tokens

def parse(tokens, object):
    """ does the parse of the scanned/tokenized JSON string
        @param tokens list of JSON tokens
        @param object final dictionary or one 'node' in the tree while parsing """
    name  = None
    array = None

    while len(tokens) > 0:
        token = tokens.pop()
        if token == "{":
            if array == None:
                if not name == None:
                    object[name] = object.__class__()
                    parse(tokens, object[name])
                    name = None
            else:
                subObject = object.__class__()
                array.append(parse(tokens, subObject))
        elif token == "}":
            return object
        elif token == "[":
            array = []
        elif token == "]":
            assert not name == None
            object[name] = array
            array        = None
            name         = None
        elif token in [':', ',']:
            pass
        elif token in [True, False, None]:
            if array == None:
                assert not name == None
                object[name] = token
            else:
                array.append(token)
        elif type(token) in [type(0), type(0.0)]:
            if array == None:
                assert not name == None
                object[name] = token
            else:
                array.append(token)
        elif type(token) == type(""):
            if array == None:
                if not name == None:
                    object[name] = token
                    name = None
                else:
                    name = token
            else:
                array.append(token)
    return object


def loadFromBuffer(buffer, dictionary = None):
    if not dictionary: dictionary = {}
    return parse(list(reversed(tokenize(buffer))), dictionary)

def loadFromFile(pathAndFileName, dictionary = None):
    if not dictionary: dictionary = {}
    return loadFromBuffer(open(pathAndFileName).read(), dictionary)

def test():
    def assertEqual(a, b):
        if not a == b:
            print("assertion has failed:\n    expected: '%s'\n    given: '%s'" % (a, b))
            assert False

    # Testing the tokenize function:
    # ==============================
    # one (name, value) pair
    expected  = ["{", "firstName", ":", "Thomas", "}"]
    assertEqual(expected, tokenize(""" { "firstName": "Thomas" } """))
    # two (name, value) pairs
    expected  = ["{", "firstName", ":", "Thomas", ",", "surName", ":", "Lehmann", "}"]
    assertEqual(expected , tokenize(""" { "firstName": "Thomas", "surName": "Lehmann" } """))
    # one pair with a name and a list of integers
    expected = [ "{", "squares", ":", "[", 1, ",", 2, ",", 4, ",", 8, ",", 12, "]", "}" ]
    assertEqual(expected, tokenize(""" { "squares": [1, 2, 4, 8, 12] } """))
    # one pair with a name and a boolean true
    expected = [ "{", "isTrue", ":", True, "}" ]
    assertEqual(expected, tokenize(""" { "isTrue": true } """))
    # one pair with a name and a boolean false
    expected = [ "{", "isTrue", ":", False, "}" ]
    assertEqual(expected, tokenize(""" { "isTrue": false } """))
    # one pair with a name and null value
    expected = [ "{", "value", ":", None, "}" ]
    assertEqual(expected, tokenize(""" { "value": null} """))
    # one pair with a name and an object as value
    expected = ['{', 'object', ':', '{', 'id', ':', 4711, '}', '}']
    assertEqual(expected, tokenize(""" { "object" : { "id": 4711 } } """))
    # one pair with a name and a strign value (string in string)
    expected = ['{', 'object', ':', 'abc "def" xyz', '}']
    assertEqual(expected, tokenize(""" { "object": "abc \\"def\\" xyz" } """))

    # Testing the loadFromBuffer function:
    # ====================================
    # one (name, value) pair
    expected = {'firstName': 'Thomas'}
    assertEqual(expected, loadFromBuffer(""" { "firstName": "Thomas" } """))
    # two (name, value) pairs
    expected = {'firstName': 'Thomas', 'surName': 'Lehmann'}
    assertEqual(expected, loadFromBuffer(""" { "firstName": "Thomas", "surName": "Lehmann" } """))
    # one pair with a name and a list of integers
    expected = {'squares': [1, 2, 4, 8, 12]}
    assertEqual(expected, loadFromBuffer(""" { "squares": [1, 2, 4, 8, 12] } """))
    # one pair with a name and a boolean true
    expected = {'isTrue': True}
    assertEqual(expected, loadFromBuffer(""" { "isTrue": true } """))
    # one pair with a name and a boolean false
    expected = {'isTrue': False}
    assertEqual(expected, loadFromBuffer(""" { "isTrue": false } """))
    # one pair with a name and a null value
    expected = {'value': None}
    assertEqual(expected, loadFromBuffer(""" { "value": null } """))
    # one pair with a name and an object as value
    expected = {'object': {'id': 4711}}
    assertEqual(expected, loadFromBuffer(""" { "object" : { "id": 4711 } } """))
    # one pair with a name and a list of objects
    expected = {'parent': [{'child-one': 1}, {'child-two': 2}]}
    assertEqual(expected, loadFromBuffer("""{ "parent" : [ { "child-one": 1 }, { "child-two": 2 } ] } """))

    class MyDict:
        def __init__(self):                self.data = {}
        def __setitem__(self, key, value): self.data[key] = value
        def __getitem__(self, key):        return self.data[key]
        def __repr__(self):                return "MyDict%s" % self.data

    expected = """MyDict{'object': MyDict{'value': 3.5}}"""
    assertEqual(expected, "%s" % loadFromBuffer(""" { "object" : { "value": 3.5 } } """, MyDict()))

if __name__ == "__main__":
    test()
