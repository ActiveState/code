"""
a secure password generator
"""
import random,string,sqlite3
def shuffle(cont):  # we can use random.shuffle but i prefer to use this
    "cont:container"
    lim=len(cont)-1
    c=list(cont)
    for _ in "."*(lim/2):  
        a=random.randint(0,lim)
        b=random.randint(0,lim)
        t=c[a]
        c[a]=c[b]
        c[b]=t
    return "".join(c)

def Gen_Pass(name):
    n=random.randint(7,10)  #Length of password 
    #--------------------Data Base
    conn=sqlite3.connect("pass.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS passwords(user TEXT UNIQUE,pass TEXT UNIQUE)")
    #--------------------
    rand=random.SystemRandom()
    lst=list(string.letters[26:52]+string.digits[1:])#lst=list(string.letters[:52])
    word=""
    for i in range(n):
        word+=lst[rand.randint(0,len(lst)-1)]
    word=shuffle(word)
    try:
        cur.execute("INSERT OR IGNORE INTO passwords(user,pass) VALUES (?,?)",(name,word))
        conn.commit()
        print "the pass is ",word
        print "ok , now it is inserted"
    except:
        print "there are some problems"
    cur.close()
    conn.close()
if __name__=="__main__":
    Gen_Pass("UserName")
