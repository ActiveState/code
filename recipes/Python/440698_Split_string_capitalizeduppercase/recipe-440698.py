import re
def split_on_caps(str):
    
    rs = re.findall('[A-Z][^A-Z]*',str)
    fs = ""
    for word in rs:
        fs += " "+word
    
    return fs
#test
if __name__ == "__main__":
    print split_on_caps("DonkeyIsAGreatBeastYIP")


---> Donkey Is A Great Beast Y I P 
