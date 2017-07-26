import struct

a=["MZ",176,"PE",332,1,224,259,267,9,16,64,16,2,5,32,2,2,132]+[16]*5+[".text",16,2,2,16,96,"3\xc0\xc3"]
f="60sL112x4sHH12x3HB14xB12xHxB3xB10xH7xB3xB6xHxBxxBxxB4xBxxB6xB131x13sB3xB3xB14xB2xB48x512s"
b=struct.pack(f,*a)
file("test.exe","wb").write(b)
