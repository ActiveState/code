def grab_email(files = []):
    # if passed a list of text files, will return a list of
    # email addresses found in the files, matched according to
    # basic address conventions. Note: supports most possible
    # names, but not all valid ones.
    
    found = []
    if files != None:
        mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        
        for file in files:            
            for line in open(file,'r'):                
                found.extend(mailsrch.findall(line))    

    # remove duplicate elements
    # borrowed from Tim Peters' algorithm on ASPN Cookbook
    u = {}
    for item in found:
        u[item] = 1

    # return list of unique email addresses
    return u.keys()
