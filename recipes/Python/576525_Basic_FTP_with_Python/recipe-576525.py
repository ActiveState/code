import ftplib                                          
session = ftplib.FTP('SERVER NAME','USERNAME','PASSWORD') 
myfile = open('YOUR FILE','rb')                        
session.storbinary('STOR YOUR FILE', myfile)           
myfile.close()                                         
session.quit()                                         
