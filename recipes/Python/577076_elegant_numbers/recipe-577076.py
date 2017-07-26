w=1
counter=0
e=0


print"how many input"
x=input()


while w<=x:
    print'what number'
    y=raw_input()
    y=int(y)
    for i in range(2,100000000):
        q=0
        qq=0
        qqq=0
        qqqq=0
        qqqqq=0
        while i%2==0 and q%2==0:
            while q<>0 and q%2==0:
                q=q/2
            if q%2<>0:
                break
        
            if q==0:
                q=i/2
        while i%3==0 and qq%3==0:
            while qq<>0 and qq%3==0:
                qq=qq/3
            if qq%3<>0:
                break
            

            if q==0:
                qq=i/3
            if q<>0:
                qq=q/3
            
            
        while i%5==0 and qqq%5==0:
            while qqq<>0 and qqq%5==0:
                qqq=qqq/5
            if qqq%5<>0:
                break
            
            if q==0 and qq==0:
                qqq=i/5
            if q==0 and qq<>0:
                qqq=qq/5
            if q<>0 and qq==0:
                qqq=q/5
            if q<>0 and qq<>0:
                qqq=qq/5
            
                
                
        while i%7==0 and qqqq%7==0:
            while qqqq<>0 and qqqq%7==0:
                qqqq=qqqq/7
            if qqqq%7<>0:
                break
            
            
            if q==0 and qqq==0 and qq==0:
                qqqq=i/7
            if q<>0:
                qqqq=q/7
            if qq<>0:
                qqqq=qq/7
            if qqq<>0:
                qqqq=qqq/7
            
        while i%11==0:
            while qqqqq<>0 and qqqqq%11==0:
                qqqqq=qqqqq/11
            if qqqqq%11<>0:
                break
            

            if q==0 and qq==0 and qqq==0 and qqqq==0:
                qqqqq=i/11
            if q<>0:
                qqqqq=q/11
            if qq<>0:
                qqqqq=qq/11
            if qqq<>0:
                qqqqq=qqq/11
            if qqqq<>0:
                qqqqq=qqqq/11
                
        if qqqqq==1 or q==1 or qq==1 or qqq==1 or qqqq==1:
             counter=counter+1
        if counter==y:
            e=e+1
            print 'case',e,'the number is',i
            w=w+1
            counter=0
            break
                
    
