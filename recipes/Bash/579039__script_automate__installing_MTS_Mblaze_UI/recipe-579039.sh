#!/bin/bash
#This Script is written by emilgeorgejames - emilgeorgejames@gmail.com           date : 9-2-2015
#                                          - emilgeorgejames.wordpress.com
#                                          - emil.george.james@hotmail.com
# script to automatic installation of mts mblaze UI


echo "
 +-+-+-+-+-+-+-+-+-+-+-+-+
 |  MTS MBLAZE UI        |
 +-+-+-+-+-+-+-+-+-+-+-+-+
"
# define common function 

echo "MTS MBLAZE WIRELESSS DATA USB MODEM TERMINAL INSTALLATION GUIDE"
echo ""
echo "Select model  for your MTS MBLAZE modem"
sleep 2
echo ""
echo "There are two types of modem "
echo "
`printf "1"``echo  ""`  MTS-MBLAZE-MINI
`printf "2"``echo  ""` MTS -MBLAZE-ULTRA"
echo ""
sleep 1
echo "Type (1 to 2): "
while read Input
do
# for mts-mblaze-mini
if [ $Input = "1" ]; then
{
  echo "You have selcted MTS-MBLAZE-MINI"
  sleep 1
  echo "starting installation.................. "
  sleep 1
  echo "Downloading and installing ....."
  sleep 2
  cd && wget -O Linux.zip https://www.dropbox.com/s/2osuilo99kc3h15/Linux.zip?dl=0
  unzip -o Linux.zip -d $HOME/
  rm Linux.zip
  cd && wget -O install_linux.sh https://www.dropbox.com/s/jk0wrpcok02r6wt/install_linux.sh?dl=0
  cd && chmod +x install_linux.sh && ./install_linux.sh
}
break;
# for mts-mblaze-ultra
elif [ $Input = "2" ]; then
{
  echo "You have selcted MTS-MBLAZE-ULTRA"
  sleep 1
  echo " starting installation................"
  sleep 1
  echo "Downloading and installing ....."
  sleep 2
  cd && wget -O Linuxx.zip https://www.dropbox.com/s/yirj4d1cpet1i1a/Linuxx.zip?dl=0
  unzip -o Linuxx.zip -d $HOME/
  rm Linuxx.zip
  cd && wget -O install_linux2.sh https://www.dropbox.com/s/tuggjr3jqdnlwil/install_linux2.sh?dl=0
  cd && chmod +x install_linux2.sh && ./install_linux2.sh
}
break;
else
	echo "Input is invalid!!!"
	echo "Type right model of modem."
	echo ""
	echo "Type from (1 to 2): "
fi # closed
done # all done 

     
