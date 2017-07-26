__author__ = 'stevenYANG'

import subprocess
from subprocess import PIPE

testCase = None           #The file name which store the ddmin result
PASS       = "PASS"
FAIL       = "FAIL"

def a_ddmin_linux(commandList):
    assert test([]) == PASS , 'ERROR-Different Result with empty test case!'
    assert test(commandList) == FAIL ,'This program just works fine! '

    commandLen = len(commandList) #length of the test case list
    if commandLen == 1:
        test(commandList)

    granularity_n = 2
    while commandLen >= 2:
        subsets = splitTestSet(commandList,granularity_n)
        assert len(subsets) == granularity_n
        some_complement_is_failing = 0 #flag
        print ">>>>>>Subsets are: "
        print subsets
        print
        for subset in subsets:
            #get the complement of subset using list comprehension.
            complement = [c  for c in commandList  if c not in subset]
            if test(complement) == FAIL:
                commandList = complement
                commandLen = len(commandList)
                print ">>>>>>New Failing Configuration: "
                print commandList
                granularity_n = max(granularity_n-1,2)
                print ">>>>>>Granularity now is: %d"  %granularity_n
                print
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if granularity_n == commandLen:
                break
            granularity_n = min(granularity_n*2,commandLen)
            print ">>>>>>Increase Granularity to : %d" %granularity_n
            print

        if commandLen == 1:
            #in this process schedule program each line is one command,and
            #can not be divided into parts
            pass

    return commandList

def splitTestSet(commandList,granularity_n):
    """
    Divide test case into granularity parts.
    """
    subsets = []
    start = 0
    for i in range(granularity_n):
        subset = commandList[start:start + (len(commandList) - start) / \
                                           (granularity_n - i)]
        subsets.append(subset)
        start = start + len(subset)
    assert len(subsets) == granularity_n
    for s in subsets:
        assert len(s) > 0
    return subsets

def test(commandList):
    """
    Test two program with the same test case.
    Different output leads to FAIL,
    otherwise PASS
    """
    print 'Testing set is: '
    print commandList
    commands = ''.join(commandList)
    failCmd = ['./a_fail','2','8','7']
    passCmd = ['./a_pass','2','8','7']
    a_fail = subprocess.Popen(failCmd,stdin=PIPE,stdout=PIPE)
    #return (stdout,stderr)
    a_fail_output = a_fail.communicate(commands)[0]

    a_pass = subprocess.Popen(passCmd,stdin=PIPE,stdout=PIPE)
    a_pass_output = a_pass.communicate(commands)[0]

    if a_fail_output != a_pass_output:
        print "Two result doesn't match ----> FAIL"
        anykeyContinue = raw_input('Any key to continue: ')
        return FAIL
    else:
        print "Two result match ----> PASS"
        anykeyContinue = raw_input('Any key to continue: ')
        return PASS


def startDebug():
    """
    1. Open test case file
    2. Store ddmin result in a file for further use.
    """
    global testCase
    path  = 'testcases/ft.6'
    testCase = path.split('/')[-1]
    with open(path,'r') as command_file:
        commandList = command_file.readlines()
        ddminResult = a_ddmin_linux(commandList)
        with open('testcases/minSet_'+testCase,'w') as min_result:
            min_result.write(''.join(ddminResult))
            min_result.close()

if __name__ == "__main__":
    startDebug()
