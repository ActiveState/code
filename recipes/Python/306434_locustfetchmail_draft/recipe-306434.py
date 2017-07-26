#!/usr/bin/python
'''
This locust_fetchmail -----------------------------------------open source one
'''
import poplib, re, time, os, string

class re_ex:

    def __init__(self, domain):
        #self.user   = user
        self.domain = domain
        
    def split_user(self, str):
        user    = string.split(str, "@")
	user_	= string.split(user[1], "\012")
	user	= string.split(user[0], "Delivered-To: ")
        return user[1], user_[0]
    
    def list_user(self, domaiN):
	
        list = os.listdir("/home/vpopmail/domains/"+domaiN+"")
        return list

    def check_user(self,user, list):
        print user
	i = 0
        flag = 0
        while i < len(list):
            if user == list[i]:
                flag = 1
            else:
                flag = 0
	    i = i + 1
        if flag == 1 :
            return flag, user
        else:
            return flag, user

        
        
    def find(self):
        file    = open("../domains/"+self.domain+".txt","r")
        read1   = file.readlines()
        file.close()
	#user_len = 0
        i = 0              
        while i < len(read1):
            isi     = re.search("Return-Path",read1[i])
            re1	= read1[i]
            if isi != None:
                isi2 	= re.search("Delivered-To:",read1[i+1])
                re2	        = read1[i+1]
                list_	= []
                if isi2 != None :
		    #user_len = user_len + 1
		    list_.append(re1)
                    list_.append(re2)
                    i = i + 2
                    flag = 1
                    while 1 :
                        try:
                                isi3 	= re.search("Return-Path",read1[i])
                                re3	        = read1[i]
                                if isi3 != None:
                                    isi4 = re.search("Delivered-To:",read1[i+1])
                                    if isi4 != None :
                                        break
                                    else:
                                        list_.append(re3)
                                else:
                                    list_.append(read1[i])
                                    i = i + 1
                        except:
                                flag = 0
                                break
                                
                                             
                
                    if flag != 0:
                        
                        user , domain   = self.split_user(re2)
		        list_users      = self.list_user(domain)
                        check           = self.check_user(user, list_users)
			self.user       = user
   					
	               	if check[0] == 1 :
                            file_nm     = "locust_fetchmail_4_"+self.domain+"_"+str(i)+"_"+str(time.time())+".lfm"
                            write_mail  = open("/home/vpopmail/"+self.domain+"/"+self.user+"/Maildir/new/"+file_nm+"", "w")
                            
			    
			    for vol in list_:
                                write_mail.write(vol)
                            write_mail.close()
                            os.popen("chown vpopmail.vchkpw "+file_nm+"")
                        else:
                            file_nm     = "locust_fetchmail_4_"+self.domain+"_"+str(time.time())+".lfm"
                            write_mail  = open("/temp/"+file_nm+"", "w")
                            for vol in list_:
                                write_mail.write(vol)
                            write_mail.close()
                            os.popen("chown vpopmail.vchkpw "+file_nm+"")
                                
            
            
            


class fetch_mail:

    def __init__(self, user, pass_, domain, IP):

        self.user   = user
        self.pass_  = pass_
        self.domain = domain
        self.IP     = IP
        

    def pop3_(self):

        M = poplib.POP3(self.IP)
        M.user(self.user+"@"+self.domain)
        M.pass_(self.pass_)
        numMessages = len(M.list()[1])
        list_   = []
        for i in range(numMessages):
            for j in M.retr(i+1)[1]:
                list_.append(j)

        file    = open("../domains/"+self.domain+".txt","w")
        for k in list_:
        	
	   	file.write(k+"\n")
        file.close()
