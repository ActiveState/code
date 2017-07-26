## Invoking PowerShell script from batch file 
Originally published: 2012-11-01 18:39:55 
Last updated: 2012-11-01 18:39:55 
Author: greg zakharov 
 
I'm not sure that there is a way do it without temporary files and why it need at last, maybe for tuning PowerShell host at start? This sample demonstrates how to launch PowerShell host inside CommandPrompt session and change it caption on clock. (Note: be sure that you have enough rights to execute PowerShell scripts - Get-ExecutionPolicy).