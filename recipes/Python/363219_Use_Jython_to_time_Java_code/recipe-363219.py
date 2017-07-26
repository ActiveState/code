jtimeit.py
===========
from java.lang import System
from java.net import URL
from java.io import *
import Main


def jtimeit(f,args):
    start=System.currentTimeMillis()
    f(*args)
    end=System.currentTimeMillis()
    
    return end-start


def sum(seq):
    # no sum in Jython 2.1, we will use reduce
    return reduce(lambda x,y:x+y,seq)
    
def avg(seq):
    return sum(seq)/len(seq)

def main():


    url1='http://www.google.com'
    url2='http://www.yahoo.com'

    # single hits
    print url1, ' takes ',jtimeit(Main.doHttpGet,[url1]),' ms\n'
    print url2, ' takes ',jtimeit(Main.doHttpGet,[url2]),' ms\n'

    # average over 10 hits
    g=[]
    y=[]
    for i in range(10):
      g.append(jtimeit(Main.doHttpGet,[url1]))
      y.append(jtimeit(Main.doHttpGet,[url2]))
    print url1, ' on average takes ', avg(g),' ms';
    print url2, ' on average takes ', avg(y),' ms';
    

if __name__=='__main__':
    main()



Main.java
==========
import java.net.*;
import java.io.*;


public class Main {

   
    public static void doHttpGet(String url) throws Exception {



	HttpURLConnection conn=(HttpURLConnection)(new URL(url)).openConnection();
	conn.setRequestMethod("GET");
	conn.connect();

	
	
      
	String inputLine;
    	    
	BufferedReader    reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
	    	
	while ((inputLine = reader.readLine()) != null) {
	    //  System.out.println(inputLine);
	}
	
	reader.close();
	conn.disconnect();


    }
