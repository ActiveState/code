"""
an lp-based *nix printer module
"""
import subprocess
import os

def checkBins(*bin):
    bins = list(bin)
        
    searchPaths = os.environ["PATH"].split(":")
    for path in searchPaths:
        for bin in bins:
            if os.path.exists(os.path.join(path, bin)):
                bins.remove(bin)
        if bins == []: return
    raise IOError, "required binaries not %s found" % ", ".join(bins)

checkBins("lpr")

class Printer(object):
    def __init__(self, opts={}):
        """initializes the printer with options"""
        self.options = []
        self.setOptions(opts)
    
    def write(self, text):
        """prints a string"""
        stdin = subprocess.Popen(["lpr", " ".join(self.options)], stdin=subprocess.PIPE).stdin
        stdin.write(text)
        stdin.close()
        
    def writeFile(self, file):
        """prints a file"""
        # do the proper expansions
        file = os.path.expanduser(file)
        file = os.path.abspath(file)
        
        if not os.path.exists(file):
            raise IOError, "file not found"
        
        # all is well
        subprocess.Popen(["lpr", file, " ".join(self.options)])
        
    def setOption(self, key, value=None):
        if value is None:
            option = "-o %s" % key
        else:
            option = "-o %s=%s" % (key, value)
        self.options.append(option)
    
    def setOptions(self, opts):
        """sets printer options from a dictionary"""
        for (key, value) in opts.items():
            self.setOption(key, value)
            
    def reset(self):
        """puts the printer back in its default state"""
        self.options = []

def main():
    printerOptions = {
        "cpi": 20,
        "lpi": 12
    }
    p = Printer(printerOptions)
    p.writeFile("~/testfile.txt")

if __name__ == "__main__": main()
