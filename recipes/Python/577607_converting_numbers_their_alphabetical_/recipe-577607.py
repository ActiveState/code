# this is program to convert mathematical number to alphabetical numbers
# this can easily change to any language (but not for example japanese, i think!) by modifying the list below
def translate(d):
    lst1=['one ','two ','three ','for ','five ','six ','seven ','eight','nine','ten','eleven','twelve ','thirteen ','fourteen ','fifteen ','sixteen ','seventeen ','eighteen ','nineteen ']
    lst2=['twenty ','thirty ','forty ','fifty ','sixty ','seventy ','eighty ','ninety ']
    lst3=['one hundred ','two hundred ','three hundred ','for hundred ','five hundred ','sixe hundred ','seven hundred ','eight hundred ','nine hundred ']
    lst4=['thousand ','million ','billion ','trillion '] 
    s=''
    t=int();y=int(d)
    if d==0:
        return 'zero'
    while d!=0: #--------- main LOOP

        if d<20: #------if number < 20
            s=s+lst1[d-1]+' '
            return s
        if d>=100 and d<1000:  #------if 100<number < 1000
            s=s+lst3[d/100-1]
            if d%100==0:
                return s
            while(d>99):
                d-=100
        if d>19 and d<100:  #------if number < 100
            y=d%10
            t=d-(d%10)
            s=s+lst2[(t/10)-2]+' '
            if y!=0:
                s=s+lst1[y-1]+' '
            return s
        
        if d>1000000000000:  # ---------------if number < 1000 trilions
            first=str()
            first=translate(d/1000000000000)
            s+=first+' '+lst4[3]+' '
            if d%1000000000000==0:
                return s
            while d>1000000000000:
                d-=1000000000000

        if d>1000000000: #------if number < one triliion
            first=str()
            first=translate(d/1000000000)
            s+=first+' '+lst4[2]+' '
            if d%1000000000==0:
                return s
            while d>1000000000:
                d-=1000000000
                
        if d>=1000000:  #------if number < one bilion  
            first=str()
            first=translate(d/1000000)
            s=s+first+' '+lst4[1]+' '
            if d%1000000==0:
                return s
            while (d>1000000): 
                d-=1000000
        if d==1000:
            return 'One thousand '
                
        if d>1000: #------if number < 1000
            first=str()
            first=translate(d/1000)
            s=s+first+' '+lst4[0]+' '
            if d%1000==0:
                return s
            while (d>1000):
                d-=1000

 # --------------------------------
if __name__=="__main__":
        d=raw_input('enter number or q to quit: ')
        if d=='q':
            exit()
        d=int(d)
        print translate(d)
        print '\n'


    
