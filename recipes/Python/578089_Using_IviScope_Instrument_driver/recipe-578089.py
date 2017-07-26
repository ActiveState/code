from comtypes.client import CreateObject, GetModule

#### Using the IviScope interface ####
GetModule('IviScopeTypeLib.dll')
from comtypes.gen import IviScopeLib

ivi_scope = CreateObject('Tkdpo2k3k4k.Tkdpo2k3k4k', interface=IviScopeLib.IIviScope)
ivi_scope.Initialize('USB0::0x0699::0x0411::C012048::INSTR', False, False, '')

ivi_scope.Acquisition.ConfigureRecord(TimePerRecord=.1, MinNumPts=1000, AcquisitionStartTime=0)
ch1 = ivi_scope.Channels.Item('CH1')
ch1.Configure(Range=.1, Offset=0.1, Coupling=IviScopeLib.IviScopeVerticalCouplingDC, ProbeAttenuation=1, Enabled=True)

ch1.Offset = 0.05 # Channel parameters can be configured using properties

waveform = ivi_scope.Measurements.Item('CH1').ReadWaveform(MaxTimeMilliseconds=100)

print "Waveform :", waveform[0]
print "Time Origin :", waveform[1]
print "Time Step :", waveform[2]

#### Using the Tkdpo2k3k4k interface ####
from comtypes.gen import Tkdpo2k3k4kLib

tkdpo_scope = CreateObject('Tkdpo2k3k4k.Tkdpo2k3k4k')
tkdpo_scope.Initialize('USB0::0x0699::0x0411::C012048::INSTR', False, False, '')

# The vertical position of the trace, is not part of the IVIScope specification
# It can be access with the Tkdpo2k3k4k interface
tkdpo_scope.Channels.Item('CH1').Position = .5 # units are in divisions

# However the Tkdpo2k3k4k interface is not compatible with the IVIScope interface
# For example to read waveform, you need to use the ITkdpo2k3k4k.WaveformTransfer.ReadWaveform methods
# Also, for example, the Channel configuration (ITkdpo2k3k4kChannels.Configure) need more keywords
waveform = tkdpo_scope.WaveformTransfer.ReadWaveform(WaveformSource=Tkdpo2k3k4kLib.Tkdpo2k3k4kSourceCH1,
                                                     MaxTimeMiliseconds=100) # !!! Mili not Milli .... 
print "Waveform :", waveform[0]
print "Time Origin :", waveform[1]
print "Time Step :", waveform[2]
