import random
h,t,sumh,sumt=0,0,0,0
for j in range(1,101):
    for i in range(1,101):
        x=random.randint(1,2)
        if (x==1):
            h=h+1
        else:
            t=t+1
    print "Heads are:", h, "Tails are", t
    sumh=sumh+h
    sumt=sumt+t
    h,t=0,0
print "Heads are:", sumh, "Tails are", sumt
