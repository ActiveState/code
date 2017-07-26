Table Of Contents:
1.	Installing Perl Modules on Windows
1.1	Perl Modules
1.2 	Getting modules
1.3 	Installing modules using PPM tool
1.4 	Installing modules manually

2.	References


1. Installing Perl Modules on Windows

1.1 Perl Modules
A Perl module is a package (has .pm as extension) that can be reused and is defined in a library file whose name is the same as the name of the package. A module may provide following. 
i) Provide a mechanism for exporting some of its symbols into the symbol table of any other package using it. 
ii) It may also function as a class definition and make its operations available implicitly through method calls on the class and its objects, without explicitly exporting any symbols.
Usually Perl modules are included in a Perl program as following. To include a module ‘MyModule.pm’, write:
use MyModule;


1.2 	Getting packages

The first thing that you will need to do is to get the package for module. Usually zipn files are available for packages. Below are the steps for getting the zip file.
i) Go to http://ppm.activestate.com
ii) Go to ‘Zips’ tab.
iii) Click on one of ActivePerl5xx, ActivePerl6xx, or ActivePerl8xx links based on the build version of Active Perl in your Windows machine. You can go to Start->Settings->Control Panel->Add Remove Programs to find ActivePerl build 5xx, 6xx or 8xx in the list. 
iv) Click on Windows link.
v) Download the zip file you need (for example: Math-Stat.zip) into your local Windows machine in a temp folder (say C:/Test/).
vi) Similarly download any other zip files that you need to install.

1.3 	Installing modules using PPM tool.

The ppm program is the package manager for ActivePerl. It simplifies the task of locating, installing, upgrading and removing Perl packages. PPM is installed automatically with ActivePerl. 
All PPM operations and configuration can be performed at the command line. You can use 'ppm help' command in command prompt for more information.
After downloading zip files for the packages (as discussed in 1.2), you can follow below steps to use these zip files, for installing modules using PPM tool.
1.	Unzip the package to a temporary directory (say C:/Test/). 
2.	Go to command promots and install the package by specifying the name of ppd file directly:
ppm install C:\Test\Modulename.ppd
If the module installation is successful, you will see ‘Successfully installed…’ message on the command prompt.

After installing Math-Stat module, you can include the same in Perl file like following.

use Math::Stat;


1.4 	Installing modules manually

Unfortunately, not all modules can be installed via PPM. Also, many times you may not be able to use PPM tool to install modules, because of you being under-privileged user in Windows machine. In all such cases, if you need to install a module, you should be able to install it manually, as discussed below. After downloading zip files for the packages (as discussed in 1.2), you can use following steps.
i)  Unzip the package to a temporary directory (say C:/Test/).

ii) This will give .ppd file, a readme file and a folder (say, MSWin32-x86-multi-thread-5.8 for Math-Stat module). Ignore .ppd and readme files, then check the content inside this folder. If there is zip or tar file inside, then unzip it.

iii) Look for .pm file inside the subfolders (here you will find Stat.pm in blib\lib\Math\ folder.
If ActivePerl is installed in C:/Perl/ folder in your Windows machine, then put this .pm file into C:/Perl/site/lib/Math/ folder (If this Math folder does not exist, then crate one here). Please note correspondence between the common portion of path (\lib\Math\) here. This needs to be maintained when placing the .pm file.

iv) Look for .html file inside the subfolders again (here you will find Stat.html in blib\html\site\lib\Math\ folder). This file is a help file describing the functions available in corresponding .pm file). It is not mandatory to copy this file, however if you wish to copy, you can copy this into C:\Perl\html\site\lib\Math\ folder (If this Math folder does not exist, then crate one here) in your Windows machine.
  
v) Look for autosplit.ix file inside the subfolders again (here you will find this file in blib\lib\auto\Math\Stat\ location). then there   Put this file in C:/Perl/site/lib/auto/Math/Stat/ folder (If this Math folder does not exist, then crate one here).

Please note that every package may not have autosplit.ix file. In other words, autosplit.ix file may not be available for every package. If it is not available there, then there is no need to put it.

vi)  Now, open C:/Perl/site/lib/auto/Math/.packlist file (If this Math folder does not exist, then crate one here) and make an entry corresponding to the .pm file. For example, the entry will be like this in .packlist file.

vii) Repeat steps (iii) to (vi) for each of the .pm file present in the zip file for the package.
