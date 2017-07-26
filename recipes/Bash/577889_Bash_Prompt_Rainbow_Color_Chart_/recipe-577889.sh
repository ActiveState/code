#!/bin/bash -   
#title          :colorscale.sh
#description    :Show a rainbow of colors.
#author         :bgw
#date           :20111002
#version        :0.1    
#usage          :./colorscale.sh
#notes          :       
#bash_version   :4.1.5(1)-release
#==============================================================================

for c in {0..255} ; do
    echo -e "\e[38;05;${c}m ${c} Bash Prompt Color Chart" 
done
