import urllib2, urllib, urllister
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
while True:
    print "Welcome"
    print "Press Enter When Download Finishes and Q to quit"

    raw_i=raw_input("Song Name and Artist: ")
    x = urllib.quote_plus(raw_i)

    site1 = urllib2.urlopen('http://www.youtube.com/results?search_query=%s'%x)
    y = site1.read()
    parser = urllister.URLLister()
    parser.feed(y)

    parser.close()


    for url in parser.urls:
        if "watch?v=" in url: 
            v = url
        
            break


    vid = ("http://www.youtube.com%s"%v)

    driver = webdriver.Chrome()
    driver.get("http://www.youtube-mp3.org/")


    elem = driver.find_element_by_id("youtube-url")
    elem.clear()
    elem.send_keys(vid)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    download = driver.page_source

    parser = urllister.URLLister()
    parser.feed(download)
    parser.close


    for url in parser.urls:
       if "/get?video_id" in url: 
             down = url

    download_url = ("http://www.youtube-mp3.org%s"%down)
    driver.get(download_url)
    x = raw_input("")
    driver.quit()
    
    if x == 'q':
        quit()
    else:
        pass
    
