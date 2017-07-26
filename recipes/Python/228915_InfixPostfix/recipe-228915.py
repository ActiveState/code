##################################################################################
##
##	Author:		Premshree Pillai
##	Date:		14/07/03	
##	File Name:	infix-postfix.py
##	Description:	-Converts infix expressions to postfix and vice-versa
##			-You can also evaluate infix and postfix expressions
##	Website:	http://www.qiksearch.com
##
##################################################################################

def push_stack(stackArr,ele):
    stackArr.append(ele)

def pop_stack(stackArr):
    return stackArr.pop()

def isOperand(who):
    if(not(isOperator(who)) and (who != "(") and (who != ")")):
        return 1
    return 0

def isOperator(who):
    if(who == "+" or who == "-" or who == "*" or who == "/" or who == "^"):
        return 1
    return 0

def topStack(stackArr):
    return(stackArr[len(stackArr)-1])

def isEmpty(stackArr):
    if(len(stackArr) == 0):
        return 1
    return 0

def prcd(who):
    if(who == "^"):
	return(5)
    if((who == "*") or (who == "/")):
	return(4)
    if((who == "+") or (who == "-")):
	return(3)
    if(who == "("):
	return(2)
    if(who == ")"):
	return(1)

def ip(infixStr,postfixStr = [],retType = 0):
    postfixStr = []
    stackArr = []
    postfixPtr = 0
    tempStr = infixStr
    infixStr = []
    infixStr = strToTokens(tempStr)
    for x in infixStr:
	if(isOperand(x)):
            postfixStr.append(x)
            postfixPtr = postfixPtr+1
        if(isOperator(x)):
            if(x != "^"):
                while((not(isEmpty(stackArr))) and (prcd(x) <= prcd(topStack(stackArr)))):
                    postfixStr.append(topStack(stackArr))
                    pop_stack(stackArr)
                    postfixPtr = postfixPtr+1
            else:
                while((not(isEmpty(stackArr))) and (prcd(x) < prcd(topStack(stackArr)))):
                    postfixStr.append(topStack(stackArr))
                    pop_stack(stackArr)
                    postfixPtr = postfixPtr+1
            push_stack(stackArr,x)
        if(x == "("):
                push_stack(stackArr,x)                
        if(x == ")"):
            while(topStack(stackArr) != "("):
                postfixStr.append(pop_stack(stackArr))
                postfixPtr = postfixPtr+1
            pop_stack(stackArr)
            
    while(not(isEmpty(stackArr))):
        if(topStack(stackArr) == "("):
            pop_stack(stackArr)
        else:
            postfixStr.append(pop_stack(stackArr))

    returnVal = ''
    for x in postfixStr:
        returnVal += x

    if(retType == 0):
        return(returnVal)
    else:
        return(postfixStr)

def pi(postfixStr):
    stackArr = []
    tempStr = postfixStr
    postfixStr = []
    postfixStr = tempStr
    for x in postfixStr:
	if(isOperand(x)):
            push_stack(stackArr,x)
	else:
            temp = topStack(stackArr)
	    pop_stack(stackArr)
	    pushVal = '(' + topStack(stackArr) + x + temp + ')'
	    pop_stack(stackArr)
	    push_stack(stackArr,pushVal)
    return(topStack(stackArr))

def strToTokens(str):
    strArr = []
    strArr = str
    tempStr = ''	
    tokens = []
    tokens_index = 0
    count = 0
    for x in strArr:
        count = count+1
        if(isOperand(x)):
            tempStr += x
        if(isOperator(x) or x == ")" or x == "("):
            if(tempStr != ""):
                tokens.append(tempStr)
                tokens_index = tokens_index+1
            tempStr = ''
            tokens.append(x)
            tokens_index = tokens_index+1 
        if(count == len(strArr)):
            if(tempStr != ''):
                tokens.append(tempStr)
    return(tokens)

def PostfixSubEval(num1,num2,sym):
    num1,num2 = float(num1),float(num2)
    if(sym == "+"):
        returnVal = num1 + num2
    if(sym == "-"):
        returnVal = num1 - num2
    if(sym == "*"):
        returnVal = num1 * num2
    if(sym == "/"):
        returnVal = num1 / num2
    if(sym == "^"):
        returnVal = pow(num1,num2)
    return returnVal

def PostfixEval(postfixStr):
    temp = postfixStr
    postfixStr = []
    postfixStr = temp
    stackArr = []
    for x in postfixStr:
        if(isOperand(x)):
            push_stack(stackArr,x)
        else:
            temp = topStack(stackArr)
            pop_stack(stackArr)
            pushVal = PostfixSubEval(topStack(stackArr),temp,x)
            pop_stack(stackArr)
            push_stack(stackArr,pushVal)
    return(topStack(stackArr))

def InfixEval(infixStr):
    return PostfixEval(ip(infixStr,[],1))

def menu():
    def again():
        flag = raw_input('Continue (y/n)?')
        if flag not in ('y','n'):
            again()
        if(flag == 'y'):
            menu()
        if(flag == 'n'):
            exit

    print '\n############################'
    print '# Infix-Postfix Calculator #'
    print '############################'    
    print '\n(1) Infix to Postfix'
    print '(2) Postfix to Infix'
    print '(3) Evaluate Infix'
    print '(4) Evaluate Postfix'
    print '(5) Exit'
    opt = raw_input("Enter option (1/2/3/4/5): ")
    if opt in ('1','2','3','4','5'):
        if(opt == '1'):
            what = raw_input('\nEnter Infix String: ')
            print 'Postfix String: ', ip(what)
        if(opt == '2'):
            what = raw_input('\nEnter Postfix String: ')
            print 'Infix String: ', pi(what)
        if(opt == '3'):
            what = raw_input('\nEnter Infix String: ')
            print 'Infix Value: ', InfixEval(what)
        if(opt == '4'):
            what = raw_input('\nEnter Infix String: ')
            print 'Postfix Value: ', PostfixEval(what)
        if(opt == '5'):
            exit
        if(opt != '5'):
            again()
    else:
        menu()

menu()
