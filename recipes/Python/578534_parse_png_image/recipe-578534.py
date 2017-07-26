import binascii

class Chunk:
    Length=None
    type=None
    data=None
    CRC=None
    def hight_width(self):
        if self.type=='IHDR':
            width=int(self.data[0:8],16)
            hight=int(self.data[8:16],16)
            return [width,hight]
            

class PNG:
    header=''
    Chunks=[]
    FileName=''
    data=''
    width=''
    hight=''
    
    def byts(self,data):
      vals=[]
      count=0
      step=2
      for i in range(0, len(data), 2):
        vals.append(data[i:step])
        step=step+2
      return vals 
  
    def Find_Chunks(self):
        
      x=Chunk()
      total=0
      while x.type != 'IEND':
        x=Chunk()  
        x.Length=int(''.join(self.data[8+total:12+total]),16)
        x.type=''.join(self.data[12+total:16+total]).decode('hex')
        
        x.data=''.join(self.data[16+total:15+x.Length+total])
        x.CRC=''.join(self.data[16+x.Length+total:20+x.Length+total])
        w=x.hight_width()
        if w:
          self.width=w[0]
          self.hight=w[1]
        self.Chunks.append(x)
       
        total=total+x.Length+12
        
    
    def  __init__(self,file):
       self.FileName=file
       file=open(self.FileName,'r')
       data=file.read()
       data=binascii.hexlify(data)
       vals=self.byts(data)
       self.data=vals
       self.header=self.data[:8]
       self.header=''.join(self.header)
       self.Find_Chunks()
x=PNG('/root/th_grey3.png')   
print x.hight,x.hight
