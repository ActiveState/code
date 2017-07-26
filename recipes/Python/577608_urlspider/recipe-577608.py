class url_spider(object):
    " it is like a spider aplication go through addresses and collect urls "
    def __init__(self,limit):
        self.limit=limit    # to limit extracting url

    def run(self):
        import sqlite3
        import urllib
        from re import findall

        


                           # ----------------------- #-
                     
        conn=sqlite3.connect('url_spider.db')
        cur=conn.cursor()
        
        cur.execute('CREATE TABLE IF NOT EXISTS urlbank(url TEXT UNIQUE,retv INTEGER,v INTEGER,times INTEGER)')
        #cur.execute('CREATE TABLE IF NOT EXISTS tags (url TEXT UNIQUE,tags TEXT)')
        # --url:the web adresses that is retrieved --retv:if we have searched through the link or not
        # --v: number of url's that another link have page to it --times:number of times that a url have retrieved
        
        
        c=1  # --limit control
        
        
                      # ---------------------- #-
        while True:            # for first time program prompt for an address and for secode time until limitation
            if c>self.limit:   # program use database and select a url that is not retieved
                return
            if c==1:
                host=raw_input('enter a url: ')    # where we start to collect url's
                
            if c>1 and c<=self.limit:       # ----second time loop
                try:
                    cur.execute('SELECT url,times FROM urlbank WHERE retv=0 LIMIT 1')
                    (host,t)=cur.fetchone()
                    t+=1
                    cur.execute('UPDATE urlbank SET times=? WHERE url=?',(t,host))
                except:
                    print 'there is a problem'
                    #return                # ----second time loop
                    
            else:        # ---continuing first time
                try: 
                   cur.execute('INSERT OR IGNORE INTO urlbank (url,retv,v,times) VALUES (?,0,0,1)',(host,))
                except:
                    cur.execute('SELECT times FROM urlbank WHERE url=?',(host,))
                    t=cur.fetchone()[0]
                    cur.execute('UPDATE urlbank SET times=? WHERE url=?',(t+1,host)) # ----end of first time
                                                                                    
            c+=1
            cur.execute('UPDATE urlbank SET retv=1 WHERE url=?',(host,))    # retv=1 becouse we are searcg through it
                        # --------------------- #-
                        
            try:
                if findall('.*(w3.org).*',host)[0]=='w3.org':  # --we would counter  a problem once we face to
                # ----this address so we ignore it.
                    continue
            except:
                pass
                       # --------------------- #-

                       
            try:
                doc=urllib.urlopen(host)   #---loading urs's destination
            except:                      
                continue


            for line in doc:    # ----- starting extract
                for link in findall('.*(http://\S+[.]{1}\S+[.]{1}[a-zA-Z]{2,4}[^\s"\<>.]+)/.*',line): # ---extracting usrl's
                    try:
                        cur.execute('SELECT v FROM urlbank WHERE url=?',(link,))
                        vis=cur.fetchone()[0]
                        cur.execute('UPDATE urlbank SET v=? WHERE url=?',(vis+1,link))
                    except:
                        cur.execute('INSERT OR IGNORE INTO urlbank (url,retv,v,times) VALUES (?,0,1,0)',(link,))
                        
                        

                        
                
                try:       # ----putting data in database by using try and except ----#-
                    conn.commit()
                except:
                    pass
                # ---------------------- - - -

                
                
            # ----------- END OF LOOP IS HERE --------- #-
            
        conn.close()
    
# ----------------------------------END OF class-----------------------------

# -----------------------------RUNNING:
###########################
if __name__=="__main__": ##
    t=url_spider(10)     ##
    t.run()              ##
###########################

            
                
        
