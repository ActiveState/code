import win32pdhutil, win32pdh,wmi,win32api,win32process
c = wmi.WMI ()#<-- this takes a ling time to set up. but after this initialiseation it is very quick

#to get a process's attributes you have to name them
a=str(win32pdhutil.FindPerformanceAttributesByName("explorer", counter="Virtual Bytes"))

print "Explorer virtual Bytes: ",a #will give you virtual bytes

#to get system you do it slightly differently
z=str(win32pdhutil.GetPerformanceAttributes("Memory", "Page Faults/sec"))

print "memory Page Faults",z # will give you memory page faults a second

#Now here is the fun bit to get the process's cpu-usage is very difficult
# it is not simple like i thought this
cpu=str(win32pdhutil.FindPerformanceAttributesByName("explorer", counter="% Processor Time"))
print "Explorer CPU Time is: ",cpu

#after searching high and low on the internet i finally found how to do it using WMI (so windows only)
process_info = {}
for p in c.Win32_PerfRawData_PerfProc_Process (name='explorer'):
  n1, d1 = long (p.PercentProcessorTime), long(p.Timestamp_Sys100NS)
  n0, d0 = process_info.get (id, (0, 0))
    
  try:
    percent_processor_time = (float (n1 - n0) / float (d1 - d0)) *100.0
  except ZeroDivisionError:
    percent_processor_time = 0.0
  print "Explorer CPU Time actually is: ", percent_processor_time
