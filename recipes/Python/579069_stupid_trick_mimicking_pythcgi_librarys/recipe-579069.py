# The FakeStorage class mimics the FieldStorage object in this limited respect:
# 1. we can initialize our dummy 'form' like this:
#     form = FakeStorage()
#     form['sparqlQuery'] = "query string"
#     
# and access it like this:
#     form.getvalue("sparqlQuery")
#     
# OR
# 
# 2. we can initialize it as an ordinary dict like this:
#     form = {"serialize": FakeStorage('serialization format string')}
#     
# and access it like this:
#     form["serialize"].value


    class FakeStorage(dict):
        def __init__(self, s=None):
            self.value = s
        def getvalue(self, k):
            return self[k]

# opt. 1:
     form = FakeStorage()
     form['sparqlQuery'] = "query string"

# then access the form thus:
    form.getvalue("sparqlQuery")

# opt. 2: initialize `form` as an ordinary dict:
    form = {'serialize': FakeStorage('n3')}

# and access it like this:
    form["serialize"].value
