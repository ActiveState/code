#This program provides practice for the Doomsday Algorithm
#You should know how to use the alg before practicing

from random import *
import time

January = [1,31,31,3,4]
February = [2,28,29,28,29]
March = [3,31,31,7,7]
April = [4,30,30,4,4]
May = [5,31,31,9,9]
June = [6,30,30,6,6]
July = [7,31,31,11,11]
August = [8,31,31,8,8]
September = [9,30,30,5,5]
October = [10,31,31,10,10]
November = [11,30,30,7,7]
December = [12,31,31,12,12]
Months = [January,February,March,April,May,June,July,August,September,October,November,December]
WeekText = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
Years = [1800,2199]

for _ in xrange(5):
    month = Months[randint(0,11)][0]
    year = randint(Years[0],Years[1])

    if (year % 400) != 0 and (year % 4) != 0:
        day = randint(1,Months[month-1][1])
    else:
        day = randint(1,Months[month-1][2])

    print month, "/", day, "/", year

    if year < 1900:
        part1 = 6
        part2 = year - 1800
    elif year < 2000:
        part1 = 4
        part2 = year - 1900
    elif year < 2100:
        part1 = 3
        part2 = year - 2000
    else:
        part1 = 1
        part2 = year - 2100

    part3 = int(part2 / 12)
    part4 = part2 % 12
    part5 = int(part4 / 4)
    doomsDay = part3 + part4 + part5 + part1

    while doomsDay > 7:
        doomsDay = doomsDay - 7

    if month > 2:
        part6 = (day+14) - Months[month-1][3]
        myDay = doomsDay + part6
        while myDay > 7:
            myDay = myDay - 7
    else:
        if (year % 400) != 0 and (year % 4) != 0:
            part6 = (day+35) - Months[month-1][3]
            myDay = doomsDay + part6
            while myDay > 7:
                myDay = myDay - 7
        else:
            part6 = (day+35) - Months[month-1][4]
            myDay = doomsDay + part6
            while myDay > 7:
                myDay = myDay - 7

    start = time.clock()
    guess = raw_input("Enter your guess for the day of the week: ")

    print "The answer is: ", WeekText[int(myDay)-1]
    end = time.clock()

    totalTime = end - start

    print "It took you: ", round(totalTime,2), "seconds."
