"""
   @author  Thomas Lehmann
   @file    InMemoryZip.py
   @brief   inspired by http://www.kompato.com/post/43805938842/in-memory-zip-in-python
            providing an in memory zip with some more features
   @note    tested with Python 2.7.5 and with Python 3.3

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
import io
import os
import zipfile

class InMemoryZip:
    """ Basic idea behind was to be able to transfer single files or
        or a folder (with sub folders) as zipped memory via communication
        to another machine. """

    def __init__(self, data=None):
        """ creating an in memory file (zip archive) """
        self.inMemory = io.BytesIO()
        if data:
            self.setData(data)

    def getData(self):
        """ retrieving the whole file as buffer """
        self.inMemory.seek(0)
        return self.inMemory.read()

    def setData(self, data):
        """ creating new in memory file wit new content """
        self.inMemory = io.BytesIO()
        self.inMemory.write(data)

    def append(self, pathAndFileName):
        """ adding a file or a path (recursive) to the zip archive in memory """
        zf = zipfile.ZipFile(self.inMemory, "a", zipfile.ZIP_DEFLATED, False)

        if os.path.isfile(pathAndFileName):
            zf.write(pathAndFileName)
        else:
            path = pathAndFileName
            for root, folders, files in os.walk(path):
                for file in files:
                    fullName = os.path.join(root, file)
                    zf.write(fullName)

    def saveAs(self, pathAndFileName):
        """ does save the in memory zip archive to a file """
        file = open(pathAndFileName, "wb")
        file.write(self.getData())
        file.close()

    def readFrom(self, pathAndFileName):
        """ reading a file expected to be a ZIP file """
        self.setData(open(pathAndFileName, "rb").read())

    def extractAllAt(self, path):
        """ does extract all files in memory below given path;
            the underlying zipfile module is clever enough to
            create the necessary path if not existing """
        zf = zipfile.ZipFile(self.inMemory)
        zf.extractall(path)

    def listContent(self):
        """ getting list of zip files entries (ZipInfo instances) """
        zf = zipfile.ZipFile(self.inMemory)
        return zf.infolist()

def test():
    zm = InMemoryZip()
    zm.append(".")
    zm.saveAs("InMemoryZip_test.zip")

    zm2 = InMemoryZip(zm.getData())
    zm2.extractAllAt("./tmp")

    zm3 = InMemoryZip()
    zm3.readFrom("InMemoryZip_test.zip")
    for entry in zm3.listContent():
        print(entry.filename)

if __name__ == "__main__":
    test()
