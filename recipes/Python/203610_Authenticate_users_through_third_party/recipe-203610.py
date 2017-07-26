# popauth.py  Authenticate user through POP server. 
# Copyright (c) 2002, Thinkware AB, SWEDEN 
# 2002-02-27 magnus@thinkware.se 
 
def popauth(popHost, user, passwd): 
    """ 
    Log in and log out, only to verify user identity. 
    Raise exception in case of failure. 
    """ 
    import poplib 
    try: 
        pop = poplib.POP3(popHost) 
    except: 
        raise StandardError, "Could not establish connection "+\ 
                             "to %s for password check" % popHost 
    try: 
        # Log in and perform a small sanity check 
        pop.user(user) 
        pop.pass_(passwd) 
        length, size = pop.stat() 
        assert type(length) == type(size) == type(0) 
        pop.quit() 
    except: 
        raise StandardError, "Could not verify identity. \n"+\ 
              "User name %s or password incorrect." % user 
        pop.quit() 
    del pop 
 
users = { 
    'Winston C': ('winstonc', 'pop.somedomain.xx'), 
    'Benny G': ('bgoodman', 'mail.anotherdomain.yy'), 
    'John L': ('lennon', 'pop.music-co.uk'), 
    } 
 
# The main routine is for testing purposes. 
def main(): 
    usernames = users.keys() 
    usernames.sort() 
    reply = "" 
    while reply == "" or reply[0] not in 'Qq': 
        print 
        for i, name in zip(range(len(usernames)), usernames): 
            print i, name 
        print 
        print 'Select the number before your name followed by [ENTER], ' 
        reply = raw_input("or type Q[ENTER] to quit: ") 
        username = '' 
        try: 
            i = int(reply) 
            username = usernames[i] 
        except: 
            # Continue in the loop 
            pass 
        if username: 
            # User successfully selected identity. 
            popAccount, popServer = users[username] 
            print 
            print "Hello %s. Let's see if you know the password for the " % \
                  username 
            print "email-account '%s' at the server '%s'." % \
                  (popAccount, popServer) 
            print 
            import getpass 
            passwd = getpass.getpass(
                      'Enter e-mail password, followed by [ENTER]: ') 
            print 
            try: 
                popauth(popServer, popAccount, passwd) 
                print "Congratulations! You have been authenticated!" 
            except StandardError, msg: 
                print msg 
     
if __name__ == '__main__': 
    main()
