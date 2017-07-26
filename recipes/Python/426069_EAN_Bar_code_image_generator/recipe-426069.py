"""
This class generate EAN bar code, it required PIL (python imaging library)
installed.

If the code has not checksum (12 digits), it added automatically.

Create bar code sample :
   from EANBarCode import EanBarCode
   bar = EanBarCode()
   bar.getImage("9782212110708",50,"gif")

"""

# courbB08.pil PIL Font file uuencoded
courB08_pil ="""eJztl91rFkcUxp+Zt7vGFYzVtiJKICgYlLRWkaBBVGgDraFGCH5gsQp+QMBqabAVRYJYAlakCkoh
CpYgxaLkIu1NvLBeSAStglpqL6xQAsVe2AuL5u2buH3mzGaYPf9AKWTl8d3nl7MzZ2bnazvea9+9
7+PurFWut5e0Zu+s7VybYfKavP7LK3X/5TlM4Q3/OWbyf1ARD/6mgb2SjwtPhbpnq0iKZ6ahrmCj
wqbxdgamRnHOA69jimN5zvIS8cDcUEeVdYzRAw1FHcJYXgPvG4s6Jlgj7xeEequS3wLeNvGvnrEO
tq+Jt82szT+b86+WHlgS2jHGuHF6YHnog1zaupxqCcy3t4X3rVG9iXhgjW+bsFQ80BaxRDywTrF1
VId6toPaqOI2UlsV20ptV2w7tUuxXVSXYl3UvoIZ9kFFPPBJ6D/HLD3QXbwjyDjI6YHPiz5FXiN7
SQ8cDu/N9/1h3veEOP/Oe6gvQnmuvYYe+NL3qYyNVDxw2seF8XKa+jrKJREPnFdx56l+xfqpS4pd
ogZUeQPU91FcKh64GveBeOCaKu8adUM9e4O6reJuU/cUu0c9VM8+pB6r/B5TI+rZEerPUpyhB/6K
5lsqHniuyntO1VR5Nb5CU86FHqZOsTqqXrF66o2ojlQ8zDwVN4+aX86FHqYpXg9YLeevWRzPc7LF
ZG+V1wN6mKXxvMzH6GFaJua5zGNLD7MqmtNcc+hh1oT1oCb5cf6aNj92mbPMGXqY9jCPasLaqQ1h
jMv8pYfZpOI2UR9GcYl4mB1RnMtvB9me8N583B5qb3mNoIf5NGJc1+hhPvPrrjybioc5op49Qh0L
dfj8jlHHQ3s9O059Fc3zRDzMmVKcpYfpU+3oI/umxJyH+TYqLxUPc0X13xVqMMovFQ8zpPIbon6M
WCoeZljVMUz9VIqz9DAP1Dt6QP0a9gpZ7+lhHhXjysreaOhhfiv1vaGH+T2Mv5rbU+hh/uAaOnlN
Xv+Hy4/7mtv3OW5hnpTODIYe5mm0xqbiYf4OcbLv08NU1ZyuuqKLOEvm6sjhJkd8TjRustgkrO3u
vFGjh60r1uyiPHrY6eH84tb7l/SwM8vrAT3snHgNY9wcsoby+Y8edn5UxxTxsIuitrlcFpG9GcVx
/6CHXRrKk72MHrYl3stYB/ceu7I4X02wlWSrCmaF1ehhV7NrovWKHrattI4betj20Fc8r7E87kf2
g+gcy32BHnZDfKZmHPco2xnl4vqlk2yz6r/N1EfRPpiKh90d7VGpeNi9inGPst2lNdbSwx4McS8k
7iDVE/Ytz3qoXsV6qZOKnaTOBDYqjPuRPRfOkz7uHNUf4uQMQg/7XekMYulhB6JnE/GwP0T1JuJh
ryrGM6G9HuWSiIcdDnPmhTs70sPeCuPes1vUXcXuUvcDGxV2n/olOisn4mEfhfOVby/3KDsSlZeI
h32iGOe0faoY57R9ptgzajTKJREPOx7aJnOfHhUbxov0Mz0qU8v50aMyo/wu6VGZrdhsqqH8fnll
HEEz4zj6DNMxK+4X+gyv8cszyoU+4zfmjNAO9zuXrNGXF1gj2ULFFpI1K9ZMtiww//22jGwFXg39
535XkK0O+cl5gz7Du6iP5wd9hvfDs9LP9BnWR/U6tp6sU7FOsi1RLo5tIdsWled+t5HtVO3YSdal
WBfZftW2/WQHVH4HyA6F9+GfPUR2VOV3lKxXsV6yE4qdIDul2Cmys6ptZ8n6Qi7+m7OP7ELoU/8t
dIHsoo8L+V0ku6xyvkw2qNgg2VBgvg+GyK6XyrP0GW5ydE3EuXd5k+xOeOdVibtD9jNm/Qv15O4i"""

# courbB08.pbm font file uuencoded
courB08_pbm ="""eJxNkntM01cUx8+P2/1apUAZEpECq4KRjKhF0E55FYEp4yG6mglz2Q8Q1BhERhhls/zKI+CID4wb
IAPKpk4GAzqZPKKMX2GIUwGJG+ImtKwKjIzXcGuBtncV0Hn+uLnn5Nzv55xv7mdRkbusVjquBACr
0N3B+wCQi/m+ijAf4LGl/wgAiwkNDpRIyyABSjGkBQ/fa3c1bfLs4U8ulDcYUs/502rTpIlO9pyc
Kp/Buql6f3rmZ1NqvpO2SZXf0duY3j0563zjoZpW8AvHRmVeZ/Co36mFR8bERzlsxOMJ+oJshsS5
7rlfzFzmnZFEFnIEZjTGizgLsLzjl4QtrNprBRu10e+u9GgePHjG63bPDw/H87uix0Vtsvkqg9qO
lUimPLiOM4z69YfqIu5Pa2Sr/io6n9Xmf9e+57W1Iapo4lLQBdLSWc/z3KOSlgznDXTW/Flh21kX
IeUIX8FZVL9dwP4NBH5jglYxkBNFmWgMcfsAxM/9gEL5TTwYpnfElR8qQ+WiCgeTHOAfb2bW/cQC
/FozFOOQzAebtjRvQLI7HBtXvaZe25a3Q/1vZpPa+kd1XXKuflr5Cm48YUsUcjMXjsm/sf+22s6z
QAbGZ8mEXMzSE4y9AHhRpltwB1N9ynz5H2MOi0MEi4E5O1ov9ogrFU5cMWAcdgQb3xHFtFK+0pkh
VnYWxltx92j69p6jJ9OnHr+Cq5x5X6Mz70JcX2tEG5LIShM4EHIGoLIRsHzcvEuGwMYA4DZPn7gP
MA1QIgltnt82cTu7j5n76mmz3TU5Bh3PFRTHku52aBgaTnJD7m1c0a3hNjbWWjBtMsP/OFac/LYA
NAAWepdYodB58NBFIuOjNSQ4cgXplqP2RyOe8fd999T8weqBRwLwNFdQobHgA1/YTV8PH+TwV59v
Bo7Y1J4rmHFv3T9e8rmmXdGSuPpSbBnhYJ7V8ICz6AfGcdTpRkpCUU8WcOT8wb+dSHIb6QZapx0M
Y2DO4i7jYV2AUNkkErpQFHVYmFRmYD7OJhDyQSiow4IkrS3TbpQqFA9slE4jnj6peXMTC+N8buJ2
0Uv5eOothuGIiluyCDtff3miBzJHjncOIC3bPT8FLabRPd0TCWy346Mmn9Rz23WyNMJcsnqhQani
3CMFOZuYU7c20zTNVqNbGPNxALWnybeLEcTvXWpc10leI5ae/CI9qBqI686cnO6P6F33e2vAp0nz
9+hnbNeueh/261UJK5aVeSf73ZSXA7dOBXvkXODEb9hVww4KtPNAbPvaZbi0q9kICCl+CiBJSzLv
a8TlntYlC4UHvCRTlaXOy13VAbN0eae2v3hNesWXLsWPkjfOPq7e6zd1fOfc1TckDaylrvleinnT
8Ui87ScLMVhhEx7SUJ8U2zKrRR2Z1dEqZlkr7kDTuhFjpkvse9ZXN0R9H+DlYA4TXVm6/kXDQMyT
eGnJFXlLlSgva5iLUEcbiyDzNqf4Wr9kKYVUIcY40DrnsW4E4zW9QxnHVYx+bo64mIskDWjZgCrq
eVQFrS7Sh/uFLftIidKWbgj6Oq652d4c3v88Dw2JDK7bSWX/ByuaLZI="""


class EanBarCode:
   """ Compute the EAN bar code """
   def __init__(self):
      A = {0 : "0001101", 1 : "0011001", 2 : "0010011", 3 : "0111101", 4 : "0100011", 
           5 : "0110001", 6 : "0101111", 7 : "0111011", 8 : "0110111", 9 : "0001011"}
      B = {0 : "0100111", 1 : "0110011", 2 : "0011011", 3 : "0100001", 4 : "0011101",
           5 : "0111001", 6 : "0000101", 7 : "0010001", 8 : "0001001", 9 : "0010111"}
      C = {0 : "1110010", 1 : "1100110", 2 : "1101100", 3 : "1000010", 4 : "1011100",
           5 : "1001110", 6 : "1010000", 7 : "1000100", 8 : "1001000", 9 : "1110100"}
      self.groupC = C

      self.family = {0 : (A,A,A,A,A,A), 1 : (A,A,B,A,B,B), 2 : (A,A,B,B,A,B), 3 : (A,A,B,B,B,A), 4 : (A,B,A,A,B,B),
                     5 : (A,B,B,A,A,B), 6 : (A,B,B,B,A,A), 7 : (A,B,A,B,A,B), 8 : (A,B,A,B,B,A), 9 : (A,B,B,A,B,A)}


   def makeCode(self, code):
      """ Create the binary code
      return a string which contains "0" for white bar, "1" for black bar, "L" for long bar """
      
      # Convert code string in integer list
      self.EAN13 = []
      for digit in code:
         self.EAN13.append(int(digit))
         
      # If the code has already a checksum
      if len(self.EAN13) == 13:
         # Verify checksum
         self.verifyChecksum(self.EAN13)
      # If the code has not yet checksum
      elif len(self.EAN13) == 12:
         # Add checksum value
         self.EAN13.append(self.computeChecksum(self.EAN13))
      
      # Get the left codage class
      left = self.family[self.EAN13[0]]
      
      # Add start separator
      strCode = 'L0L'
      
      # Compute the left part of bar code
      for i in range(0,6):
         strCode += left[i][self.EAN13[i+1]]
      
      # Add middle separator 
      strCode += '0L0L0'
      
      # Compute the right codage class
      for i in range (7,13):
         strCode += self.groupC[self.EAN13[i]]
      
      # Add stop separator
      strCode += 'L0L'
      
      return strCode


   def computeChecksum(self, arg):
      """ Compute the checksum of bar code """
      # UPCA/EAN13
      weight=[1,3]*6
      magic=10
      sum = 0
      
      for i in range(12):         # checksum based on first 12 digits.
         sum = sum + int(arg[i]) * weight[i]
      z = ( magic - (sum % magic) ) % magic
      if z < 0 or z >= magic:
         return None
      return z


   def verifyChecksum(self, bits): 
      """ Verify the checksum """
      computedChecksum = self.computeChecksum(bits[:12])
      codeBarChecksum = bits[12]
      
      if codeBarChecksum != computedChecksum:
         raise Exception ("Bad checksum is %s and should be %s"%(codeBarChecksum, computedChecksum))


   def getImage(self, value, height = 50, extension = "PNG"):
      """ Get an image with PIL library 
      value code barre value
      height height in pixel of the bar code
      extension image file extension"""
      import Image, ImageFont, ImageDraw
      from string import lower, upper
      
      # Create a missing font file
      decodeFontFile(courB08_pil ,"courB08.pil")
      decodeFontFile(courB08_pbm ,"courB08.pbm")
      
      # Get the bar code list
      bits = self.makeCode(value)
      
      # Get thee bar code with the checksum added
      code = ""
      for digit in self.EAN13:
         code += "%d"%digit
      
      # Create a new image
      position = 8
      im = Image.new("1",(len(bits)+position,height))
      
      # Load font
      font = ImageFont.load("courB08.pil")
      
      # Create drawer
      draw = ImageDraw.Draw(im)
      
      # Erase image
      draw.rectangle(((0,0),(im.size[0],im.size[1])),fill=256)
      
      # Draw first part of number
      draw.text((0, height-9), code[0], font=font, fill=0)
      
      # Draw first part of number
      draw.text((position+7, height-9), code[1:7], font=font, fill=0)
         
      # Draw second part of number
      draw.text((len(bits)/2+6+position, height-9), code[7:], font=font, fill=0)
      
      # Draw the bar codes
      for bit in range(len(bits)):
         # Draw normal bar
         if bits[bit] == '1':
            draw.rectangle(((bit+position,0),(bit+position,height-10)),fill=0)
         # Draw long bar
         elif bits[bit] == 'L':
            draw.rectangle(((bit+position,0),(bit+position,height-3)),fill=0)
            
      # Save the result image
      im.save(code+"."+lower(extension), upper(extension))


def decodeFontFile(data, file):
   """ Decode font file embedded in this script and create file """
   from zlib import decompress
   from base64 import decodestring
   from os.path import exists
   
   # If the font file is missing
   if not exists(file):
      # Write font file
      open (file, "wb").write(decompress(decodestring(data)))


def testWithChecksum():
   """ Test bar code with checksum """
   bar = EanBarCode()
   assert(bar.makeCode('0000000000000')== 'L0L0001101000110100011010001101000110100011010L0L0111001011100101110010111001011100101110010L0L' )
   assert(bar.makeCode('1111111111116')== 'L0L0011001001100101100110011001011001101100110L0L0110011011001101100110110011011001101010000L0L' )
   assert(bar.makeCode('2222222222222')== 'L0L0010011001001100110110011011001001100110110L0L0110110011011001101100110110011011001101100L0L' )
   assert(bar.makeCode('3333333333338')== 'L0L0111101011110101000010100001010000101111010L0L0100001010000101000010100001010000101001000L0L' )
   assert(bar.makeCode('4444444444444')== 'L0L0100011001110101000110100011001110100111010L0L0101110010111001011100101110010111001011100L0L' )
   assert(bar.makeCode('5555555555550')== 'L0L0110001011100101110010110001011000101110010L0L0100111010011101001110100111010011101110010L0L' )
   assert(bar.makeCode('6666666666666')== 'L0L0101111000010100001010000101010111101011110L0L0101000010100001010000101000010100001010000L0L' )
   assert(bar.makeCode('7777777777772')== 'L0L0111011001000101110110010001011101100100010L0L0100010010001001000100100010010001001101100L0L' )
   assert(bar.makeCode('8888888888888')== 'L0L0110111000100101101110001001000100101101110L0L0100100010010001001000100100010010001001000L0L' )
   assert(bar.makeCode('9999999999994')== 'L0L0001011001011100101110001011001011100010110L0L0111010011101001110100111010011101001011100L0L' )   


def testWithoutChecksum():
   """ Test bar code without checksum """
   bar = EanBarCode()
   assert(bar.makeCode('000000000000')== 'L0L0001101000110100011010001101000110100011010L0L0111001011100101110010111001011100101110010L0L' )
   assert(bar.makeCode('111111111111')== 'L0L0011001001100101100110011001011001101100110L0L0110011011001101100110110011011001101010000L0L' )
   assert(bar.makeCode('222222222222')== 'L0L0010011001001100110110011011001001100110110L0L0110110011011001101100110110011011001101100L0L' )
   assert(bar.makeCode('333333333333')== 'L0L0111101011110101000010100001010000101111010L0L0100001010000101000010100001010000101001000L0L' )
   assert(bar.makeCode('444444444444')== 'L0L0100011001110101000110100011001110100111010L0L0101110010111001011100101110010111001011100L0L' )
   assert(bar.makeCode('555555555555')== 'L0L0110001011100101110010110001011000101110010L0L0100111010011101001110100111010011101110010L0L' )
   assert(bar.makeCode('666666666666')== 'L0L0101111000010100001010000101010111101011110L0L0101000010100001010000101000010100001010000L0L' )
   assert(bar.makeCode('777777777777')== 'L0L0111011001000101110110010001011101100100010L0L0100010010001001000100100010010001001101100L0L' )
   assert(bar.makeCode('888888888888')== 'L0L0110111000100101101110001001000100101101110L0L0100100010010001001000100100010010001001000L0L' )
   assert(bar.makeCode('999999999999')== 'L0L0001011001011100101110001011001011100010110L0L0111010011101001110100111010011101001011100L0L' )   


def testImage():
   """ Test images generation with PIL """
   bar = EanBarCode()
   bar.getImage("9782212110708",50,"gif")
   bar.getImage("978221211070",50,"png")


def test():
   """ Execute all tests """
   testWithChecksum()
   testWithoutChecksum()
   testImage()


if __name__ == "__main__":
   test()
