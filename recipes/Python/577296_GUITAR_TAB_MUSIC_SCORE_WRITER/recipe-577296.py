# writes tab scores for guitar
from winsound import *
from time import *
from Tkinter import *
nScaleFactor = 1.05946309436 # exp(log(2) / 12) # even temper diatonic
aListType    = [1,2,3] # for type testing
nBarsPerLine = 4
lBeep = True # If true it will play through the built in speaker.
              # otherwise it will search for associated wav files
              # One file per note needed
cSoundsFolder = 'Guitar/'

class TabNote:
    def __init__(self, nS, nF, nP, cFile):
        self.nString   = nS
        self.nFret     = nF
        self.nScalePos = nP
        self.nTone     = int(440 * nScaleFactor ** (nP - 6)) # concert pitch
        self.lPause    = False
        self.cSound    = cSoundsFolder + cFile # wav file
    def play(self, nI):
        if lBeep:
            Beep(self.nTone, nI)  # milliseconds
        else:
            nStartTime = time()
            PlaySound(self.cSound, SND_FILENAME + SND_ASYNC)
            sleep(nI + nStartTime - time())      # seconds
    def drawNote(self, canvas, nStart, aLines):    
        canvas.create_rectangle(nStart - 5, aLines[self.nString - 1] - 5, nStart + 5, aLines[self.nString - 1] + 5, width = 0,fill = 'white')
        canvas.create_text(nStart, aLines[self.nString - 1], text = str(self.nFret))
        

class TabPause:
    def __init__(self, nS, nF, nP, cFile):
        self.nString   = nS
        self.nFret     = nF
        self.nScalePos = nP
        self.lPause    = True
        self.nTone     = 37
        self.cSound    = cSoundsFolder + cFile
    def play(self, nI):
        if lBeep:
            sleep(nI / 1000) # milliseconds
        else:
            nStartTime = time()
            PlaySound(self.cSound, SND_FILENAME + SND_ASYNC)
            sleep(nI + nStartTime - time())      # seconds
    def drawNote(self, canvas, nStart, aLines):
        pass
    
def PlayNote(aB, nI):
    nDelta = 0
    if isinstance(aB, type(aListType)):
        for i in aB:
            nTime = time()
            PlayNote(i, nI / len(aB) - nDelta)
            nSpent = time() - nTime
            nDelta = nSpent - nI / len(aB) # catchup if going too slowly
            if nDelta < 0:
                nDelta = 0
    else:
        aB.play(nI)

def PlayTune(aBars):
    nDelta = 0
    if lBeep:
        nDuration = 1300 # beeps are in milliseconds
    else:    
        nDuration = 1.5  # seconds per bar
    for aB in aBars:
        nTime = time()
        PlayNote(aB, nDuration -nDelta)
        nSpent = time() - nTime
        nDelta = nSpent - nDuration # catchup if going too slowly
        if nDelta < 0:
            nDelta = 0

def DrawLines(canvas, nUp, nW, nLineH, nLineNo): 
    nStartX = nW * 0.1
    nStopX  = nW * 0.9
    nLineUp = nLineH * 0.75 / 6 # six strings
    nStartY = nUp + nLineUp
    nStopY  = nUp + 6 * nLineUp
    nXStep  = (nStopX - nStartX) / nBarsPerLine
    aLineBox = []
    aBarBox = []
    for i in range(6):
        canvas.create_line(nStartX, nUp + i * nLineUp + nLineUp, nStopX, nUp + i * nLineUp + nLineUp)
        aLineBox.append( nUp + i * nLineUp + nLineUp)

    for i in range(nBarsPerLine + 1):
        canvas.create_line(nStartX + i * nXStep, nStartY, nStartX + i * nXStep, nStopY)
        aBarBox.append([nStartX + i * nXStep, nXStep])
    canvas.create_text(nStartX - 20,nUp + 1.5 * nLineUp, text = "T", font = ('Courier', 14,'bold'))
    canvas.create_text(nStartX - 20,nUp + 3.5 * nLineUp, text = "A", font = ('Courier', 14,'bold'))
    canvas.create_text(nStartX - 20,nUp + 5.5 * nLineUp, text = "B", font = ('Courier', 14,'bold'))
    if nLineNo == 0: # time signature
        canvas.create_text(nStartX - 10, nUp + 2.5 * nLineUp, text = "2", font = ('Courier', 14,'bold'))
        canvas.create_text(nStartX - 10, nUp + 4.5 * nLineUp, text = "4", font = ('Courier', 14,'bold'))
    return [aLineBox, aBarBox]


def PlaceNote(canvas, aB, nI, nStart, aLines):
    if isinstance(aB, type(aListType)):    
        for i in aB:
            PlaceNote(canvas, i, nI / len(aB), nStart, aLines)
            nStart += nI / len(aB)
    else:
        aB.drawNote(canvas, nStart, aLines)
        
def PlaceParts(canvas, aPart, aBoxes):
    nBarStep = 0
    for i in aBoxes:
        aLines = i[0]
        for j in range(nBarsPerLine):
            if len(aPart) <= nBarStep:
                return
            aB = aPart[nBarStep]
            nBarStep = nBarStep + 1
            nDuration = i[ 1][ j][ 1] * 0.95 
            nStart    = i[1][ j][ 0] + nDuration * 0.1
            for k in aB:
                PlaceNote(canvas, k, nDuration/ len(aB), nStart, aLines)
                nStart += nDuration/ len(aB)

# EADGBE tuning

dl  = 0 # not needed here
dls = 0 # not needed here
p   = TabPause(0,0,1,'Pause.wav')     # pause
el  = TabNote(6,0,1,'Elow.wav')      # E low 
fl  = TabNote(6,1,2,'Flow.wav')      
fls = TabNote(6,2,3,'FlowSharp.wav')      # F low sharp
gl  = TabNote(6,3,4,'Glow.wav')
gls = TabNote(6,4,5,'GlowSharp.wav')
al  = TabNote(5,0,6,'Alow.wav')
blf = TabNote(5,1,7,'BlowFlat.wav')      # B low flat
bl  = TabNote(5,2,8,'Blow.wav')
cl  = TabNote(5,3,9,'Clow.wav')
cls = TabNote(5,4,10,'ClowSharp.wav')
dm  = TabNote(4,0,11,'Dmid.wav')
dms = TabNote(4,1,12,'DmidSharp.wav')
em  = TabNote(4,2,13,'Emid.wav')
fm  = TabNote(4,3,14,'Fmid.wav')
fms = TabNote(4,4,15,'FmidSharp.wav')
gm  = TabNote(3,0,16,'Gmid.wav')
gms = TabNote(3,1,17,'GmidSharp.wav')
am  = TabNote(3,2,18,'Amid.wav')
bmf = TabNote(3,3,19,'BmidFlat.wav')
bm  = TabNote(2,0,20,'Bmid.wav')
bmAlt = TabNote(3,4,20,'Bmid.wav') # B middle Alternate fingering
cm  = TabNote(2,1,21,'Cmid.wav')
cms = TabNote(2,2,22,'CmidSharp.wav')
d  = TabNote(2,3,23,'D.wav')
ds = TabNote(2,4,24,'Dsharp.wav')
e   = TabNote(1,0,25,'E.wav')
f   = TabNote(1,1,26,'F.wav')
fs  = TabNote(1,2,27,'FSharp.wav')
g   = TabNote(1,3,28,'G.wav')
gs  = TabNote(1,4,29,'GSharp.wav')
a   = TabNote(1,5,30,'A.wav')
bf  = TabNote(1,6,31,'BFlat.wav')
b   = TabNote(1,7,32,'B.wav')
c   = TabNote(1,8,33,'C.wav')
cs  = TabNote(1,9,34,'CSharp.wav')
dh   = TabNote(1,10,35,'Dhigh.wav')
dhs  = TabNote(1,11,36,'DhighSharp.wav')
eh  = TabNote(1,12,37,'Ehigh.wav') # E high
fh  = TabNote(1,13,38,'Fhigh.wav')
fhs = TabNote(1,14,39,'FhighSharp.wav')
gh  = TabNote(1,15,40,'Ghigh.wav')
ghs = TabNote(1,16,41,'gHighSharp.wav')
ah  = TabNote(1,17,42,'Ahigh.wav')
bhf = TabNote(1,18,43,'BhignFlat.wav')
bh  = TabNote(1,19,44,'Bhign.wav')
ch  = TabNote(1,20,45,'Chigh.wav')
chs = TabNote(1,21,46,'ChignSharp.wav')
dd  = TabNote(1,22,47,'DD.wav')
dds = TabNote(1,23,48,'DDsharp.wav')

aB1  = [[ el , e  , el, fs]    # First line Bar1 first part
       ,[ el , gm , el, am]]   # second part 
aB2  = [[ el , g  , el, ds]
       ,[ el , bmf, el, am]]
aB3  = [[ el , e  , el, fs]
       ,[ el , gm , el, am]]
aB4  = [[ el , g  , el, ds]
       ,[ el , bmf, el, am]]

aB5  = [[ el      ,[g,e] ,g  ,     fs]    # second line
       ,[ el      ,bl    ,el ,     al]]
aB6  = [[ds      ,e     ,[d,d],     d]    # << recursive tree structure
       ,[fls      ,gl    ,el     , bl]]
aB7  = [[[cms,cms],cms   ,[cm,cm], cm]
       ,[el       ,blf   ,el     , al]]
aB8  = [[[bm,e]   ,[cm,e],bm     , p]
       ,[el       ,al    ,el     ,[cl,bl]]]

aB9  = [[p       ,[gm,em],gm   ,fms]
       ,[blf             ,al       ]]
aB10 = [[cm      ,bm     ,[g,g], g]
       ,[gl      ,em     ,bmf  , em]]
aB11 = [[[fs,fs] ,fs     ,[e,e], e]
        ,[bl     ,fms    ,cls  , fms]]
aB12 = [[[ds,fs] ,[e,fs] ,ds   , p]
        ,[bl     ,cl     ,bl   , [gl,fls]]]

aB13 = [[el       ,[g,e] ,g      ,fs]
       ,[el       ,bm    ,el     ,am]]
aB14 = [[ds       ,e     ,[d,d]  ,d]
       ,[fms      ,gm    ,em     ,bmAlt]]
aB15 = [[[cms,cms],cms   ,[cm,cm],cm]
        ,[em      ,bmf   ,em     ,am]]
aB16 = [[[bm ,e]  ,[cm,e],bm     ,p]
        ,[em      ,am   ,em     ,[em,dm]]]

aB17 = [[p  , [e,cms] , e  , ds]
       ,[cls          , fms]]
aB18 = [[p  , [d ,bm] , d  , cms]
       ,[bl           , el]]
aB19 = [[p  , [cm,am] , cm , bm]
       ,[al           , dm]]
aB20 = [[p  , [dms,bm], em, p]
       ,[gl , fls     , el, p]]

aFirstPart = [aB1[0],aB2[0],aB3[0],aB4[0],aB5[0],aB6[0],aB7[0],aB8[0],aB9[0]
             ,aB10[0],aB11[0],aB12[0],aB13[0],aB14[0],aB15[0],aB16[0],aB17[0]
             ,aB18[0],aB19[0],aB20[0]]
aSecondPart = [aB1[1],aB2[1],aB3[1],aB4[1],aB5[1],aB6[1],aB7[1],aB8[1],aB9[1]
             ,aB10[1],aB11[1],aB12[1],aB13[1],aB14[1],aB15[1],aB16[1],aB17[1]
             ,aB18[1],aB19[1],aB20[1]]

# Unfortunately I cant work out a way to play both parts together using Beep,
# unless you use two computers.
# However if you are using PlaySound
#,( you will also need the associated sound files)
# You can make a second copy of the program (rename it SugarSecondPart)
# to play the second part alongside the first
# The section of code below will syncronise the two parts.

if not(lBeep):
    while (int(time()) % 10 == 0):
        sleep(1)
    t = int(time()) % 10
    while t % 10 <> 0:
        t = int(time())
        print 'syncronising', t % 10

print 'Playing first part' 
PlayTune(aFirstPart)
#sleep(2)
#print 'Playing second part'
#PlayTune(aSecondPart)

nW = 1400
nH = 800
canvas = Canvas( width = nW, height = nH, bg = 'white')
canvas.pack(expand = YES, fill = BOTH)

aBoxes = []
nW = nW * 0.75
nLines = (len(aFirstPart) + 0.0) / nBarsPerLine
if int(nLines) <> nLines:
    nLines = int(nLines + 1)

nLineStep = nH * 0.8 / nLines # 5 lines
canvas.create_text( 300, 50, text = 'SugarPlumFairy', font = ('Arial', 20, 'bold'))
for i in range(nLines):
    aBoxes.append(DrawLines(canvas, nLineStep * i  + 100, nW, nLineStep * 0.75, i))

PlaceParts(canvas, aFirstPart, aBoxes)
PlaceParts(canvas, aSecondPart, aBoxes)
