# -*- coding: utf-8 -*-
"""
Batch download all the pinned pictures in your Pinterest board to a local folder.
Be noted: you have to keep your internet browser signed in your Pinterest account first.
Please contact me @ alfred.hui.wong@gmail.com if any question
@author: awang
"""
URL_PinterestBoard=input("Please enter your Pinterest board url starting with Http:// ")

from tkinter import filedialog
Folder_saved=filedialog.askdirectory(title="Select a local folder where you want to put all the pinned pictures")

from lxml import html
import requests

page=requests.get(URL_PinterestBoard)
tree=html.fromstring(page.content)

pins=tree.xpath('//div[@class="pinHolder"]//@href')

del page, tree

import requests, bs4
import urllib

n=1
for singlePin in pins:
  page=requests.get('http://www.pinterest.com'+singlePin)
  page_soup=bs4.BeautifulSoup(page.text,"lxml")
  page_element=page_soup.select('img[src]')
  image_address=page_element[0].attrs['src']
  
  resource=urllib.request.urlopen(image_address)
  output=open(Folder_saved+"/"+"Image"+str(n)+".jpg","wb")
  output.write(resource.read())
  output.close()
  
  n=n+1
