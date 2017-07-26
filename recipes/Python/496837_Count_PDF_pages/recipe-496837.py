import re

rxcountpages = re.compile(r"$\s*/Type\s*/Page[/\s]", re.MULTILINE|re.DOTALL)

def countPages(filename):
    data = file(filename,"rb").read()
    return len(rxcountpages.findall(data))

if __name__=="__main__":
    print "Number of pages in PDF File:", countPages("test.pdf")
