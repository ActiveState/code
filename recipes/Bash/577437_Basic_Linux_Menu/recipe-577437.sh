#!/bin/bash
selection=
until [ "$selection" = "0"]; do
     echo ""
     echo "PROGRAM MENU"
     echo "1 - Display Files and Directorys"
     echo "2 - Remove Files Displayed"
     echo "3 - Copy Files Displayed"
     echo "4 - Make Directory"
     echo ""
     echo "0 - Exit program"
     echo ""
     echo -n "Enter Selection:"
     read selection
     echo ""
     case $selection in
         1 ) ls -f;;
         2 ) echo "This removes files"
             echo "Please type name of file to remove"
             read deletefiles  
             rm $deletefiles;;
         3 ) echo "This copies files from source to destination"
             echo "Please enter source file to copy:" 
             read source
             echo "Please enter destination of file to copy"
             read destination
             cp $source $destination;;
         4 ) echo This makes a Directory
             echo "Please enter Directory name"
             read destination
             mkdir $destination;;
         0 ) exit;;
         * ) echo "Please enter 1,2,3,4 or 0"
     esac
done
