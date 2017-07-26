import zipfile

z = zipfile.ZipFile("zipfile.zip", "rb")
for filename in z.namelist():
        print filename
        bytes = z.read(filename)
        print len(bytes)
