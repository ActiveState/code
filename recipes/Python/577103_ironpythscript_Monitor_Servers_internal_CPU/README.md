## ironpython script to Monitor Servers internal CPU temprature using WMI MSAcpi_ThermalZoneTemperature with e-mail alerting capability

Originally published: 2010-03-12 05:25:51
Last updated: 2010-03-12 05:25:52
Author: mgarrana Garrana

ironpython script. It reads a txt file called servers.txt where it contains server names each in a separate line . it executes the function remoteconnect on each server name , the function connects to the server and reads the internal CPU TEMP from the WMI class MSAcpi_ThermalZoneTemperature located in namespace \\root\\WMI\nif internal CPU temp exceeds a certian Threshold , the function sends an alerting e-mail , it can also execute any other desired action using the same concept like sending an alerting sms