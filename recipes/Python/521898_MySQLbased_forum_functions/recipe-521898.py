import MySQLdb
from datetime import *
import string

class ForumBase:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host = "HOST",
            user = "USER",
            passwd = "PASSWORD",
            db = "DATABSE")
        self.cursor = self.connection.cursor()
        self.userid = 1
        self.users = self.Users(self)
        self.threads = self.Threads(self)
        self.messages = self.Messages(self)
    
    def date(self):
        return str(datetime.now()).split(" ")[0]
    
    def time(self):
        return str(str(datetime.now()).split(" ")[1]).split(".")[0]
    
    def safe(self, input):
        input = string.replace(input, "'", "\\'")
        input = string.replace(input, '"', '\\"')
        input = string.replace(input, ";", "\\;")
        input = string.replace(input, "%", "\\%")
        input = string.replace(input, "_", "\\_")
        return input
    
    class Users:
        def __init__(self, parent):
            self.parent = parent
        
        def maxID(self):
            self.parent.cursor.execute("SELECT max(id) FROM users")
            values = self.parent.cursor.fetchall()
            return values[0][0]
        
        def userData(self, userid):
            userid = int(userid)
            self.parent.cursor.execute("SELECT * FROM users WHERE id='"+str(userid)+"'")
            values = self.parent.cursor.fetchall()
            return values[0]
        
        def userMessageCount(self, userid):
            self.parent.cursor.execute("SELECT COUNT(*) FROM messages WHERE authorid='"+str(userid)+"'")
            values = self.parent.cursor.fetchall()
            return values[0][0]
        
        def newUser(self, name, password, sig):
            self.parent.cursor.execute("INSERT INTO users (name, signature, password) VALUES('"+name+"', '"+sig+"', '"+password+"')")
            return self.maxID()
        
        def userSig(self, userid):
            return self.userData(userid)[2]
        
        def userName(self, userid):
            return self.userData(userid)[1]
        
        def userPass(self, userid):
            return self.userData(userid)[3]
        
        def changeSig(self, userid, sig):
            sig, userid = self.parent.safe(sig), int(userid)
            self.parent.cursor.execute("UPDATE users SET sig='"+sig+"' WHERE id='"+str(userid)+"'")
        
        def idOfName(self, name):
            name = self.parent.safe(name)
            self.parent.cursor.execute("SELECT id FROM users WHERE name='"+name+"'")
            values = self.parent.cursor.fetchall()
            try: temp = values[0][0]
            except: temp = 0
            return temp
        
        def changeName(self, userid, name):
            name, userid = self.parent.safe(name), int(userid)
            if not self.idOfName(name):
                self.parent.cursor.execute("UPDATE users SET name='"+name+"' WHERE id='"+str(userid)+"'")
    
    class Threads:
        def __init__(self, parent):
            self.parent = parent
        
        def threadsWithMessage(self, messageid):
            threads, regExes = [], []
            regExes.append("SELECT id FROM threads WHERE messages LIKE '% "+str(messageid)+" %'") # middle message
            regExes.append("SELECT id FROM threads WHERE messages LIKE '% "+str(messageid)+"'") # last message
            regExes.append("SELECT id FROM threads WHERE messages='"+str(messageid)+"'") # only message
            regExes.append("SELECT id FROM threads WHERE messages LIKE '"+str(messageid)+" %'") # first message
            for regEx in regExes:
                self.parent.cursor.execute(regEx)
                newthreads = self.parent.cursor.fetchall()
                for thread in newthreads:
                    threads.append(thread[0])
            return threads
        
        def cleanThread(self, messageid):
            targetThreads = self.threadsWithMessage(messageid)
            print targetThreads
        
        def maxID(self):
            self.parent.cursor.execute("SELECT max(id) FROM threads")
            values = self.parent.cursor.fetchall()
            return values[0][0]
        
        def messagesInThread(self, threadid):
            self.parent.cursor.execute("SELECT messages FROM threads WHERE id="+str(threadid))
            values = self.parent.cursor.fetchall()
            messages = values[0][0]
            return messages.split(" ")
        
        def nameOfThread(self, threadid):
            self.parent.cursor.execute("SELECT title FROM threads WHERE id="+str(threadid))
            values = self.parent.cursor.fetchall()
            return values[0][0]
        
        def getContentsOfThread(self, threadid, page):
            name = self.nameOfThread(threadid)
            temp = []
            messages = self.messagesInThread(threadid)
            for messageid in messages:
                temp.append(self.parent.messages.contentOfMessage(messageid))
            return name, temp, page
        
        def newThread(self, title, firstmessageid):
            self.parent.cursor.execute("INSERT INTO threads (title, messages, edited) VALUES ('"+title+"', "+str(firstmessageid)+", '"+self.parent.date()+" "+self.parent.time()+"')")
            return self.maxID()
        
        def addMessageToThread(self, threadid, messageid):
            self.parent.cursor.execute("SELECT messages FROM threads WHERE id="+str(threadid))
            values = self.parent.cursor.fetchall()
            messages = values[0][0]+" "+str(messageid)
            edited = str(datetime.now())
            edited = edited.split(".")[0]
            self.parent.cursor.execute("UPDATE threads SET messages='"+messages+"', edited='"+edited+"' WHERE id="+str(threadid))
        
        def getThreads(self, page):
            self.parent.cursor.execute("SELECT id, title FROM threads ORDER BY edited DESC")
            values = self.parent.cursor.fetchall()
            l, tmp = len(values), []
            if (page-1)*20 > l: page = int(l/20)+1
            elif page < 1: page = 1
            for i in range(l): tmp.append([values[i+20*(page-1)][0], values[i+20*(page-1)][1]])
            return tmp, page
    
    class Messages:
        def __init__(self, parent):
            self.parent = parent
        
        def maxID(self):
            self.parent.cursor.execute("SELECT max(id) FROM messages")
            values = self.parent.cursor.fetchall()
            return values[0][0]
        
        def contentOfMessage(self, messageid):
            self.parent.cursor.execute("SELECT * FROM messages WHERE id="+str(messageid))
            values = self.parent.cursor.fetchall()
            tmp = [values[0][1], values[0][2], values[0][3], values[0][4], values[0][5], values[0][6]]
            tmp.append(self.parent.users.userName(values[0][6]))
            tmp.append(self.parent.users.userSig(values[0][6]))
            return tmp
        
        def newMessage(self, content):
            content = self.parent.safe(content)
            self.parent.cursor.execute("INSERT INTO messages (content, created, createdtime, edited, editedtime, authorid) VALUES ('"+content+"', '"+self.parent.date()+"', '"+self.parent.time()+"', '"+self.parent.date()+"', '"+self.parent.time()+"', '"+str(self.parent.userid)+"');")
            return self.maxID()
        
        def editMessage(self, messageid, newcontent):
            newcontent, messageid = self.parent.safe(newcontent), int(messageid)
            self.parent.cursor.execute("UPDATE messages SET content='"+newcontent+"', edited='"+self.parent.date()+"', editedtime='"+self.parent.time()+"') WHERE id='"+str(messageid))+"'"
        
        def deleteMessage(self, messageid):
            messageid = int(messageid)
            self.parent.cursor.execute("SELECT COUNT(*) FROM threads WHERE messages LIKE '"+str(messageid)+" %'")
            count = self.parent.cursor.fetchall()[0][0]
            self.parent.cursor.execute("SELECT COUNT(*) FROM threads WHERE messages='"+str(messageid)+"'")
            count = count + self.parent.cursor.fetchall()[0][0]
            if count > 0:
                self.parent.cursor.execute("DELETE FROM messages WHERE id=")
                self.parent.threads.cleanThreads(messageid)
        
        def cleanMessages(self):
            self.parent.cursor.execute("SELECT id FROM messages ORDER BY id ASC")
            values = self.parent.cursor.fetchall()
            allIDs = []
            for id in values:
                allIDs.append(id[0])
            for id in allIDs:
                count = len(self.parent.threads.threadsWithMessage(id))
                if count == 0: self.parent.cursor.execute("DELETE FROM messages WHERE id="+str(id))
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        self = None
