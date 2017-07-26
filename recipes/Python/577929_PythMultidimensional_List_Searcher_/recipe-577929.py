def find(searchList, elem):
        endList = []
        for indElem in range(0,len(elem)):
            resultList = []
            for ind in range(0, len(searchList)):
                if searchList[ind] == elem[indElem]:
                    resultList.append(ind)
            endList.extend([resultList])
        return endList
