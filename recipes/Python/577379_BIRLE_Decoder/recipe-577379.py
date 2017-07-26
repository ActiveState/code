#!/usr/bin/python
#-*- coding:utf-8 -*-

#brsyuksel.com

from tempfile import TemporaryFile

class BI_RLE(object):
	def __init__(self,i,o):
		self.i = open(i)
		self.o = open(o,"w")
		self.tmp = TemporaryFile()
		
		if self.i.read(2) != 'BM':
			raise IOError, "Not BMP file"
		
		self.i.seek(10)
		of = self.i.read(4)#offset to start image data
		self.offset = sum([ord(of[i])<<8*i for i in range(len(of))])

		self.i.seek(18)
		w = self.i.read(4)#image width
		self.w = sum([ord(w[i])<<8*i for i in range(len(w))])

		h = self.i.read(4)#image height
		self.h = sum([ord(h[i])<<8*i for i in range(len(h))])

		self.i.seek(28)
		b = self.i.read(2)#channel:bit per pixel
		self.bpp = sum([ord(b[i])<<8*i for i in range(len(b))])

		if self.bpp != 4 and self.bpp != 8:
			raise IOError, "Not 4-Bit or 8-Bit BMP file"

		c = self.i.read(4)#compression type
		self.comp = sum([ord(c[i])<<8*i for i in range(len(c))])

		if self.comp != 2 and self.comp != 1:
			raise IOError, "Not Compressed file"

		self.tPix = self.w * self.h
		self.rPix = 0
		self.lns = 1

		self.c = 0
		self.EORLED = False#fix for EORLE

		self.i.seek(self.offset)
		self.enc = self.i.read()
		self.dec = ""
		self.buf = ""

	def Decode(self):
		mrk = {0:self.EOSL,1:self.EORLE,2:self.MOFF}#funcs for RLE Data markers

		while((self.lns*self.w)<=self.tPix):
			b = self.enc[self.c:self.c+2]
			self.c += 2
			if len(b) != 2: break
			b0, b1 = ord(b[0]), ord(b[1])
			if b0 == 0:
				mrk.get(b1,self.UENCD)(b0,b1)
			else:
				self.DENCD(b0,b1)

	def HPIX(self,pixel):
		""" Half-Byte Packing for 4-Bit and Pixel Data Handler """
		if self.bpp == 4:
			if self.buf == "":
				self.buf = chr(pixel<<4)
			else:
				self.buf = chr(ord(self.buf) | pixel)
				self.tmp.write(self.buf)
				self.buf = ""
		else:
			self.tmp.write(chr(pixel))

	def EOSL(self,*arg):
		""" 00 00: End Of Scan Line """
		remain = self.w - self.rPix
		if not self.EORLED:
			self.rPix = 0
			self.lns += 1
		if remain == 0: remain = 2#fix for EOSL
		for i in range(remain):
			self.HPIX(0x00)

	def MOFF(self,*arg):
		""" 00 02: Move Offset """
		mov = self.enc[self.c:self.c+2]
		self.c += 2
		mov = ord(mov[0]) + ord(mov[1])*self.w
		for i in range(mov):
			self.HPIX(0x00)
		self.rPix += mov
		self.lns += self.rPix // mov
		self.rPix %= mov

	def UENCD(self,*arg):
		""" 00 NN: Unencoded Data """
		p = arg[1] #unencoded pixels data
		if self.bpp == 4:
			#read bytes with padding byte for 4 bit
			b = int(round(p/2)) + (int(round(p/2))%2 | p%2) 
		else:
			#read bytes with padding byte for 8 bit
			b = p + p%2
		ue = self.enc[self.c:self.c+b]
		self.c += b
		delta = self.rPix + p
		for i in range(b):
			if self.rPix == delta: break
			if self.bpp == 4:
				for j in range(2):
					if self.rPix == delta: break
					self.HPIX((ord(ue[i])&(0x0F<<(4*((j+1)%2))))>>(4*((j+1)%2)))
					self.rPix += 1
			else:
				self.HPIX(ord(ue[i]))
				self.rPix += 1

	def DENCD(self,*arg):
		""" NN PP: Decode Encoded Data """
		b0, b1 = arg[0], arg[1] #piece, 2 pixels data
		for i in range(b0):
			if self.bpp == 4:
				self.HPIX((b1&(0x0F<<(4*((i+1)%2))))>>(4*((i+1)%2)))
			else:
				self.HPIX(b1)
			self.rPix += 1

	def EORLE(self,*arg):
		""" 00 01: End Of RLE Data, Writing Decoded File """
		self.EORLED = True
		self.EOSL()
		if not self.buf == "": self.tmp.write(self.buf)

		self.tmp.seek(0)
		self.dec = self.tmp.read()
		self.tmp.close()

		self.i.seek(0)
		self.o.write(self.i.read(2)) #'BM' signature

		fs = self.offset + len(self.dec) #FileSize: (Header + Color Palette) + ImageData
		fsize = "" #filesize string value
		for i in range(4): fsize+=chr((fs & (0xFF<<8*i))>>8*i)#ordering as little-endian
		self.o.write(fsize)

		self.i.seek(6)
		self.o.write(self.i.read(24))#writing 24-byte same data from 6 offset

		self.o.write('\x00\x00\x00\x00')#compression-type: none

		imgdsize = ""#image data size string value
		for i in range(4): imgdsize+=chr((len(self.dec)&(0xFF<<8*i))>>8*i)
		self.o.write(imgdsize)

		self.i.seek(38)
		self.o.write(self.i.read(self.offset-38))#writing left same data from 38

		self.o.write(self.dec)

		self.o.close()
		self.i.close()


#BI_RLE(inputfile,outputfile)
#obj = BI_RLE("/home/brs/m/4bitc.bmp","/home/brs/m/4bitc-dec.bmp")
#obj.Decode()
