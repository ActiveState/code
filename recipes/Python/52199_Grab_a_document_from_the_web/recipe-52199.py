from urllib import urlopen

doc = urlopen("http://www.python.org").read()
print doc
