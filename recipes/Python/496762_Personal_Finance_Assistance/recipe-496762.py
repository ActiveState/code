#*******************************************************************************
#   Program Name : cash.py (Personal Finance Assistance)
#   Version      : 1.8
#   Desciption   : This program is menu-based program which can connect to database
#                  and then performming addition, updating, deletion and showing
#                  the summary. It use to record personal daily expenses.
#   Working in   : Null
#   Future       : Add "search" function,
#                  Add some "Analysis Tools"                  
#   Ext. Module  : sqlite (DB-API for SQLite)
#   Database     : SQLite (downloadable from www.sqlite.org)
#   Written By   : Chan Wai Keong (waikeong.chan@gmail.com)
#   Status       : Tested
#   Date         : 2005-07-20 (first version)
#*******************************************************************************

#imported library files
import sqlite
import re
import os
import time
import sys

#global variables
sqlite_path = "C:\\sqlite-3_0_8\\"
database = "cash.db"


# format = DD-MM-YYYY
date_format = r'^([0-3][\d])([-])([0-1][\d])([-])([\d]{4})$'
    

def main_menu():
    '''Display main menu (L0)'''
    os.system("cls")
    print "Personal Finance Assistance (PFA)"
    print "================================="
    print "1. ADD Record"
    print "2. MODIFY Record"
    print "3. DELETE Record"
    print "4. SHOW SUMMARY"
    print "5. Exit"
    resp = raw_input("Please enter your choice (1-5): ")
    resp_process(resp)
    

def resp_process(r):
    '''Process the response from user input (L1)'''
    if str(r).isdigit() == 1 and int(r) >= 0 and int(r) <= 5:
        if r == '1':
            add_rec()
        elif r == '2':
            edit_rec()
        elif r == '3':
            del_rec()
        elif r == '4':
            show_all()
#        elif r == '5':
#            show_summ()
        else:
            exit()
    else:
        print "You have enter an invalid input\n"
        time.sleep(2)
        # return to main menu
        main_menu()        

    
def add_rec():
    '''Add data to db from user input (L1)'''
    # get current date
    currDate = time.strftime("%d-%m-%Y", time.localtime(time.time()))
    cont = 1

    os.system("cls")

    #print function header
    print "ADD Record"
    print "=========="
    print "(Key in '-e' to back to main menu)"
    
    while cont == 1:
        print "\nKey in new record .. "
        # get input for date
        date = raw_input("Date : ")
        back_main_menu(date)

        if date == "":
            date = currDate
        else:
            while date_check(date) == 0:
                print "Error! It's not a date.\n"
                date = raw_input("Date : ")
                back_main_menu(date)
                if date == "":
                    date = currDate
                
        # get input for description
        desc = raw_input("For : ")
        back_main_menu(desc)

        # get input for amount
        amt = raw_input("Total : RM ")
        back_main_menu(amt)

        while amt_check(amt) == 0:
            print "Error! It's not a money.\n"
            amt = raw_input("Total : RM")
            back_main_menu(amt)
        amt = "%.2f" % float(amt)

        # insert to sqlite
        add_func(date, desc, amt)

        resp = raw_input("Continue ? ")
        resp = resp.upper()
        if resp == 'N':
            cont = 0
    # return to main menu
    main_menu()
    
        
def edit_rec():
    ''' Edit / Modify record in db(L1)'''
    os.system("cls")
    
    #print function header
    print "MODIFY Record"
    print "============="
    print "(Key in '-e' to back to main menu)"
    
    s_date = raw_input("Enter the DATE of record you want to modify: ")
    back_main_menu(s_date)

    col = "date"
    result = search_func(col, s_date)
    
    # print search result    
    if len(result) > 0:
        for i in range (len(result)):
            dt = result[i][0]
            ds = result[i][1]
            at = result[i][2]
            at = "%.2f" % float(at)
            print i+1, ")",  ("%s%s%s%s%s%s%s%s%s") % ((" " * (2 - (i + len(")")))), "Date: ", dt, (" " * (20 - len(dt))), "Desc: ", ds, (" " * (25 - len(ds))), "Amount: RM", at)

        row = raw_input("Enter the number of row you want to modify: ")
        back_main_menu(row)
        
        if row.isdigit() == 1:
            row = int(row)
            if row >= 0 and row <= i+1:
                rowNo = int(row) - 1
                last_date = result[rowNo][0]
                last_desc = result[rowNo][1]
                last_amt = result[rowNo][2]
                
                print "Key in the new version of record"
                print "(Press <enter> if no update on that field)"
                e_date = raw_input("NEW date: ")
                back_main_menu(e_date)

                if e_date == "":
                    e_date = last_date
                    
                e_desc = raw_input("NEW description: ")
                back_main_menu(e_desc)

                if e_desc == "":
                    e_desc = last_desc

                e_amt = raw_input("NEW amount: RM ")
                back_main_menu(e_amt)

                if e_amt == "":
                    e_amt = last_amt

                edit_func(e_date, e_desc, e_amt, last_date, last_desc, last_amt)
            
    else:
        print "Sorry, NO data match with '", s_date, "'"
    # return to main menu
    main_menu()
        

def del_rec():
    '''Delete record from db(L1)'''
    os.system("cls")
    
    #print function header
    print "DELETE Record"
    print "============="
    print "(Key in '-e' to back to main menu)"
    
    s_date = raw_input("Enter the DATE of record you want to delete: ")
    back_main_menu(s_date)

    col = "date"
    result = search_func(col, s_date)
    
    # print search result    
    if len(result) > 0:
        for i in range (len(result)):
            dt = result[i][0]
            ds = result[i][1]
            at = result[i][2]
            print i+1, ")",  ("%s%s%s%s%s%s%s%s%s") % ((" " * (2 - (i + len(")")))), "Date: ", dt, (" " * (20 - len(dt))), "Desc: ", ds, (" " * (25 - len(ds))), "Amount: RM", at)
    
        row = raw_input("Enter the number of row you want to delete: ")
        back_main_menu(row)

        if row.isdigit() == 1:
            row = int(row)
            if row >= 0 and row <= i+1:
                rowNo = int(row) - 1
                d_date = result[rowNo][0]
                d_desc = result[rowNo][1]
                d_amt = result[rowNo][2]
                print "You been choosen "
                print row, ")", "Date: ", d_date, "\tDesc: ", d_desc, "\t\tAmount: ", d_amt
                resp = raw_input("Are you sure want to delete? (Y/N): ")
                resp = resp.upper()
                back_main_menu(resp)

                if resp == 'Y':
                     delete_func(d_date, d_desc, d_amt)
    else:
        print "Sorry, NO data match with '", s_date, "'"
    # return to main menu
    main_menu()


def show_all():
    '''Get details of attribute for the records(L1)'''

    currDate = time.strftime("%d-%m-%Y", time.localtime(time.time()))
    nowDate = str(currDate).split("-")
    month = nowDate[1]
    year = nowDate[2][2:]
    
    os.system("cls")

    print "SHOW ALL Record"
    print "==============="
    print "Enter details of the record you want"
    print "Press <enter> for current year or month"
    print "(Key in '-e' to back to main menu)"
    
    yr = raw_input("Year (YY) : ")

    if yr == "":
        yr = year

   
    mth = raw_input("Month (MM) : ")
    back_main_menu(mth)
    
    if mth == "":
        mth = month
        fg = 1
    else:
        if 1 < int(mth) <= 12:
            fg = 1
        else:
            fg = 0

    if fg == 1:
        show_all_sql(yr, mth)
    else:
        print "Unvalid date"
        time.sleep(2)
        # return to main menu
        main_menu()
    

def show_summ():
    # unused function #
    '''Get details of attribute for the records(L1)'''

    currDate = time.strftime("%d-%m-%Y", time.localtime(time.time()))
    nowDate = str(currDate).split("-")
    month = nowDate[1]
    year = nowDate[2][2:]
 
    os.system("cls")

    print "SHOW SUMMARY Record"
    print "==================="
    print "Enter details of the record you want"
    print "Press <enter> for current year or month"
    print "(Key in '-e' to back to main menu)"
    
    #yr = raw_input("Year (YYYY) : ")
    #if yr == "":
    yr = year

    mth = raw_input("Month (MM) : ")
    back_main_menu(mth)
    
    if mth == "":
        mth = month
        fg = 1
    else:
        if 1 < int(mth) <= 12:
            fg = 1
        else:
            fg = 0
        
    if fg == 1:
        show_summ_sql(yr, mth)
    else:
        print "Unvalid date"
        time.sleep(2)
        # return to main menu
        main_menu()


def exit():
    '''Exit from the program(L1)'''
    os.system("cls")
    print "Thank you for using PFA v1.8"
    print "Closing Connections & Programs... "
    time.sleep(1)
    print "Good Bye\n"
    print "another waikeong-made program"
    print "All Rights Reserved (C)"
    time.sleep(2)
    sys.exit()


def add_func(dt, ds, at):
    '''Insert data into db(L2)'''
    sql_insert = """
    INSERT INTO expenses (date, desc, amount)
    VALUES ('%s', '%s', '%s')
    """ % (dt, ds, at)

    os.chdir(sqlite_path)

    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " +str(errmsg)

    # insert data into table
    try:
        cu = cx.cursor()
        cu.execute(sql_insert)
        cx.commit()
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()
    

def search_func(field, key):
    '''Search Function (L2)'''
    data = []
    
    os.chdir(sqlite_path)

    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " +str(errmsg)

    # select data from table
    try:
        cu = cx.cursor()
        cu.execute(""" SELECT * FROM expenses""" +
                   ' WHERE ("' +str(field)+ '") like ("' '%'+str(key)+'%' '")' )
        data = cu.fetchall()
        cx.commit()
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()
    return data


def edit_func(new_date, new_desc, new_amt, old_date, old_desc, old_amt):
    '''Edit / Update function (L2)'''
    os.chdir(sqlite_path)
    
    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " +str(errmsg)

    # select data from table
    try:
        cu = cx.cursor()
        cu.execute(""" UPDATE expenses """ +
                   ' SET date = ("' +str(new_date)+ '"), desc = ("' +str(new_desc)+ '"), amount = ("' +str(new_amt)+ '") WHERE date = ("' +str(old_date)+ '") AND desc = ("' +str(old_desc)+ '") AND amount = ("' +str(old_amt)+ '") ')
        cx.commit()
        print "Update Complete."
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()


def delete_func(del_date, del_desc, del_amt):
    '''Delete Function (L2)'''
    os.chdir(sqlite_path)
    
    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " +str(errmsg)

    # select data from table
    try:
        cu = cx.cursor()
        cu.execute(""" DELETE FROM expenses """ +
                   ' WHERE date = ("' +str(del_date)+ '") AND desc = ("' +str(del_desc)+ '") AND amount = ("' +str(del_amt)+ '") ')
        cx.commit()
        print "The record of "
        print del_date, del_desc, del_amt, " been Deleted."
        main_menu()
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()
   

def show_all_sql(y, m):
    '''Display the all of records(L2)'''

    j = -1
    
    os.chdir(sqlite_path)
    os.system("cls")
    
    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " + str(errmsg)

    # select data from table
    try:
        cu = cx.cursor()

        cu.execute("""SELECT * from expenses""" +
                  ' WHERE date like ("' '%-'+str(m)+'-%'+str(y)+ '") ORDER BY date')
        summ = cu.fetchall()

        cu.execute("""SELECT date, sum(amount) from expenses """ +
                   ' WHERE date like ("' '%-'+str(m)+'-%'+str(y)+ '") GROUP BY date ')
        dailySum = cu.fetchall()

        cu.execute("""SELECT SUM(amount) from expenses""" +
                   ' WHERE date like ("' '%-'+str(m)+'-%'+str(y)+ '")' )
        total = cu.fetchone()

        cx.commit()
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()
 
    if len(summ) > 0:
        # print function header
        print "\nFull Records for", m, "/", y
        print "==========================="

        # print the report
        print "Date", ('%s%s%s%s') % ((" " * (20 - len("Date"))), "Desc", (" " * (28 - len("Desc"))), "Total(RM)")
        print "====", ('%s%s%s%s') % ((" " * (20 - len("===="))), "====", (" " * (28 - len("===="))), "=========")

        for i in range(0, len(summ)):
            date = summ[i][0]
            desc = summ[i][1]
            amt = "%6.2f" % float(summ[i][2])
                    
            if date != summ[i-1][0]:
                # print daily subtotal
                if j > -1:
                    dailyTot = "%6.2f" % float(dailySum[j][1])
                    print ('%s%s') % (" " * 49, "--------")
                    print ('%s%s%s%s') % (" " * 49, "RM", dailyTot, "\n")
                j += 1

            #print daily expenses
            print date, ('%s%s%s%s') %((" " * (20 - len(date))), desc, (" " * (30 - len(desc))), amt)

        # print daily subtotal (for the current day)            
        dailyTot = "%6.2f" % float(dailySum[j][1])
        print ('%s%s') % (" " * 49, "--------")
        print ('%s%s%s%s') % (" " * 49, "RM", dailyTot, "\n")

        #print total of month
        tot = "%6.2f" % float(total[0])
        print "=========================================================="
        print "Grant total until", date, "\t\t\t RM", tot
                   
        wait = raw_input("\nPress <enter> to continue")
        
    else:
        print "No data for Month ", m, "\n"
        wait = raw_input("Press <enter> to continue")
        
    # return to main menu
    main_menu()


def show_summ_sql(y, m):
    # unused function #
    '''Display the summary of records(L2)'''

    os.system("cls")
    os.chdir(sqlite_path)
    
    # open connection to database
    try:
        cx = sqlite.connect(database)
    except sqlit.Error, errmsg:
        print "Can not open " + str(errmsg)

    # insert data into table
    try:
        cu = cx.cursor()

        cu.execute("""SELECT date, sum(amount) from expenses """ +
                   ' WHERE date like ("' '%-'+str(m)+'-%'+str(y)+ '") GROUP BY date ')
        summ = cu.fetchall()
        
        cu.execute("""SELECT SUM(amount) from expenses""" +
                   ' WHERE date like ("' '%-'+str(m)+'-%'+str(y)+ '")')
        total = cu.fetchone()

        cx.commit()
    except sqlite.Error, errmsg:
        print "Can not execute: " +str(errmsg)

    # close connection
    cx.close()

    if len(summ) > 0:
        # print function header
        print "\nDaily Based Summary for", m, "/", y
        print "================================="

        # print the report
        for i in range(len(summ)):
            date = summ[i][0]
            amt = "%6.2f" % float(summ[i][1])
            print "Date: ", date, "\t   Total: RM", amt

        tot = "%6.2f" % float(total[0])
        print "==========================================="
        print "Grant total until", date, "     RM", tot

        wait = raw_input("Press <enter> to continue")

    else:
        print "No data for month ", m, ", year", y, "\n"
        wait = raw_input("Press <enter> to continue")
        
    # return to main menu
    main_menu()


def date_check(data):
    '''Data validation for date'''
    if re.match(date_format, data) != None:
        return 1
    return 0


def amt_check(data):
    '''Check the data is in the form of money or not'''
#   format = 123.45
    data = str(data)
    if data.isdigit():
        return 1
    else: 
        try: 
            new = "%.2f" % float(data)
            return 1
        except:
            return 0


def back_main_menu(data):
    '''Check input data for requist back to main menu (L3)'''
    data = data.upper()
    if data == "-E":
        main_menu()
        

if __name__ == '__main__':
    main_menu()
    
