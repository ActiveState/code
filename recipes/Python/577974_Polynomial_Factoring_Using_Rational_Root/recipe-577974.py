from math import ceil
listOfFactors = lambda n: {i for i in range(1,ceil(abs(n)/2)+1) if n%i == 0}
def removeDuplicates(mylist):
    if mylist:
        mylist.sort()
        last = mylist[-1]
        for i in range(len(mylist)-2, -1, -1):
            if last == mylist[i]:
                del mylist[i]
            else:
                last = mylist[i]
    return mylist

def polyRoots(polyListCoeff):
    allFactors = set()
    allFactorsListOld = list(allFactors.union(listOfFactors(polyListCoeff[0]),{polyListCoeff[0]},listOfFactors(polyListCoeff[-1]),{polyListCoeff[-1]}))
    allFactorsListOld.extend([-1*i for i in allFactorsListOld])
    allFactorsList = list()
    for k in allFactorsListOld:
        for j in allFactorsListOld:
            allFactorsList.append(k/j)
    allFactorsList = removeDuplicates(allFactorsList)
    polyListCoeff.reverse()
    roots = [i for i in allFactorsList if sum([pow(i,j)*polyListCoeff[j] for j in range(0,len(polyListCoeff))]) == 0]
    factorList = list()
    for i in roots:
        if i<0:
            factorList.append("(x+{})".format(-i))
        else:
            factorList.append("(x-{})".format(i))
    return "".join(factorList)
