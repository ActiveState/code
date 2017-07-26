# Random Sound FX Using WAV File
# http://en.wikipedia.org/wiki/Amplitude_modulation
# http://en.wikipedia.org/wiki/Frequency_modulation
# FB36 - 20120701
import math, wave, array, random
duration = 5 # seconds
volume = 100 # percent
freqCR = random.randint(500, 3000) # frequency of the carrier wave (Hz) 
freqAM = random.randint(1, 10) # frequency of the AM wave (Hz) 
freqFM = random.randint(1, 10) # frequency of the FM wave (Hz) 
freqFMDev = random.randint(100, 400) # frequency deviation for FM (Hz) 
phaseCR = random.random() * math.pi * 2
phaseAM = random.random() * math.pi * 2
phaseFM = random.random() * math.pi * 2
# Assumed: ampCR = ampAM = ampFM = 1
data = array.array('h') # signed short integer (-32768 to 32767) data
dataSize = 2 # 2 bytes because of using signed short integers => bit depth = 16
numChan = 1 # of channels (1: mono, 2: stereo)
sampleRate = 44100 # of samples per second (standard)
numSamples = sampleRate * duration
# nSPC: number of Samples Per Cycle
nSPCCR = int(sampleRate / freqCR)
nSPCAM = int(sampleRate / freqAM)
nSPCFM = int(sampleRate / freqFM)
for i in range(numSamples):
    sample = 32767 * float(volume) / 100
    tCR = math.pi * 2 * (i % nSPCCR) / nSPCCR + phaseCR
    tFM = math.pi * 2 * (i % nSPCFM) / nSPCFM + phaseFM
    tAM = math.pi * 2 * (i % nSPCAM) / nSPCAM + phaseAM
    sample *= math.sin(tCR + math.sin(tFM) * freqFMDev / freqFM)
    sample *= (math.sin(tAM) + 1) / 2
    data.append(int(sample))
f = wave.open('RndSoundFX.wav', 'w')
f.setparams((numChan, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
f.writeframes(data.tostring())
f.close()
