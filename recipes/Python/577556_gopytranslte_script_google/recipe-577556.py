#!/usr/bin/python3
# Python gopytranslte
# Author : namakukingkong
# Site   : namakukingkong[dot]kandangbuaya[dot]com
# Email  : namakukingkong[at]gmail[dot]com
# dependency : linux,windows, python3, internet
# gopytranslte
#   .....|___gopytranslte.py
#   .....|___log-translate.txt
#   $mkdir gopytranslte
#   $cd  gopytranslte
#   $nano -w gopytranslte.py
#   $chmod +x gopytranslte.py
#   $python3 gopytranslte.py


import urllib.request, urllib.parse, urllib.error
import json
import sys
import os
from time import gmtime, strftime

logfile="log-translate.txt"
def cls():
    os.system(['clear','cls'][os.name == 'nt'])
    mulai()
    
def simpan(save):
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f=open(logfile,'a')
    f.write("\n--<"+time+">--------------------------------------------------------------\n")
    f.write("original  :"+texta+"\n"+"translate :"+save+"\n")
    rule="\nText ini akan disimpan dengan nama file <log-translate.txt> \n"\
         "berada di directory active tempat anda menjalankan script ini\n"\
         " \n---------------------------------namakukingkong[at]gmail[dot]com"
    f.close()
    print (rule)
    input ("\n press anykey to start again >")
    cls()
    mulai()

def ngarteke(dari,ke):
    global texta
    texta=input ("\n           word(kata)/sentence(kalimat) :")
    print ("=========================================================================\n")
    print ("  Loading translate ..................\n")
    langpair='%s|%s'%(dari,ke)
    alamate='http://ajax.googleapis.com/ajax/services/language/translate?'
    sintake = urllib.parse.urlencode({'v':1.0,'ie': 'UTF8', 'q': texta.encode('utf-8'),'langpair':langpair})
    url = alamate+sintake
    search_results = urllib.request.urlopen(url)
    jsondecode = json.loads(search_results.read().decode())
    artine = jsondecode['responseData']['translatedText']
    return artine
    
def mulai():
    judul="         ============ PYTHON TRANSLATOR ============\n"\
          "         1. indonesia   --> inggris\n"\
          "         2. inggris --> indonesia\n"\
          "         -----------------(close/exit ctrl+C)"
    print (judul)
    pilih=input ("          Language : ")
    if pilih == "2":
        save=(ngarteke(dari="en",ke="id"))
        print ("original  : "+texta)
        print ("translate : "+save)
        jawab=input ("\nApakah anda mau menyimpanya?\n yes: <y> / no: press <any key> ? ")
        if jawab== "y":
            simpan(save)
        else:
            cls()
    elif pilih == "1":
        save=(ngarteke(dari="id",ke="en"))
        print ("original  : "+texta)
        print ("translate : "+save)
        jawab=input ("\nApakah anda mau menyimpanya?\n yes: <y> / no: press <any key>")
        if jawab== "y":
            simpan(save)
        else:
            cls()
    else:
        print ("    pilihan salah... pilih lagi!!")
        mulai()

if __name__=='__main__':
  try:
    mulai()
  except KeyboardInterrupt:
    print ("  Program dihentikan \n")
    sys.exit(0)
