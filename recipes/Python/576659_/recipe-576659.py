#coding:utf-8
#全排列发生器


def a(n):
     li=[]
     for i in range(1,n+1):
          li.append(i)

     return li

def c(i,li_a):
     li=[]
     for j in li_a:
          if  j!=i:
               li.append(j)

     return li

def form(i,li_c,one):
     li=[]
     li.append(i)
     count=0
     for i in one:
          count=count+1
          li.insert(count,li_c[i-1])
     return li
          






def fun(n):
     if n==2:
          return [[1,2],[2,1]]
     else:
          back=[]#返回集合
          
          li_a=a(n)
          for i in li_a:#依次取li_a中的每一个
               li_c=c(i,li_a)#生成li_a中除去i的补集
               for one in fun(n-1):#取下一级的所有排列序
                    #li=函数(第一位i,补集li_c,序数列表one)
                    li=form(i,li_c,one)
                    back.append(li)
               
          return back





      
li=fun(5)
##dic={1:"圣",2:"诞",3:"节",4:"快乐"}
##for li_in in li:
##     word=""
##     for i in li_in:
##          word=dic[i]+word
##     word="预祝大家:"+word
##     print word
count=1
for i in li:
     print str(count)+":"+str(i)
     count=count+1





     

                    
