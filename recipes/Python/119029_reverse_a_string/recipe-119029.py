f = lambda s:s and f(s[1:])+s[0]
#or
f = lambda s:reduce(lambda a,b:b+a,s,'')
#or 
f = lambda s,l=[]:[l.extend(s),l.reverse(),''.join(l)][2]
#after Davids observations I was wondering how come third
#version is slower ...IT can't be as it uses builtin list functions
#that are in C
#then I came to know that in third version default variable l=[] keeps
#its previous info
#try
#f('anurag') twice
#so I changed it to

f = lambda s,l=[[]]:[l.pop(),l.append(list(s)),l[0].reverse(),''.join(l[0])][2]

#now it is the fastest one!!
