"""Usage:
   Description: Determines the starting and ending date when the year and week are specified for a by-weekly plot.
   
   Input: year -> YYYY.
          week -> ww.
 
  Output:  Returns a list [sd, ed] of type datetime.
           sd: It is the plot's starting date..
           ed: sd + 2 weeks (14 days).
           
  Requirements:
  1. The plot shall start on Monday of the week of interest at 00:00:00 and end on a Monday 14 days later at 00:00:00.
  2. Only weeks starting in odd number shall be included in the plots. 
     ie Weeks 04-05 is of no interest, only Weeks 03-04 or Weeks 05-06.
  3. For years that contain 53 weeks, Week 51-53 shall be included in the plots instead of Week 51-52.
  4. The function shall return a list.
  5. The type of the list's elements returned shall be datetime.         
"""

import datetime

def main():

   years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", \
            "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030",]
   log_dir = "/Your_Directory/"
   log_filename = "find_sd_ed_out.txt"
   log_obj = open(log_dir + log_filename, 'w')
   for objs_1 in years:
      weeks = ['01', '51', '53']
#     weeks = ['02']
      log_obj.writelines("\n#####################################\n")
      for objs_2 in weeks:
         log_obj.writelines("\n#####################################\n")
         year = objs_1
         start_weekNo = objs_2
##################################################
##################################################
# NOTES: 1. Adjust indentation from here on to use it as a function.
#             2. The above code was included to test the function's implementation and simplify the logging capability. 
#                 Do not include the log object if desired.
#             3. Be aware that the return list is commented out as well as the function def.
#             4. Many elements of the function can be reduced quite a bit or eliminated, but they've been left for clarity.
##################################################
#def find_sd_ed(year, start_weekNo):
             
         start_weekNo_int = int(start_weekNo) 
         if start_weekNo_int % 2 != 1: # Req 2
            log_obj.writelines("\nWeek has to be an odd number\n\n")
            break     
         if start_weekNo_int < 53:
            end_weekNo_int = start_weekNo_int + 1
         if start_weekNo_int == 53: # Test for years with 53 weeks
            dec31_dt = datetime.datetime(int(year), 12, 31, 0, 0, 0)
            dec31_iso_weekNo =  dec31_dt.isocalendar()[1]
            if dec31_iso_weekNo != int(start_weekNo):
               log_obj.writelines("\nYear " + year + " does not have 53 weeks.\n")
               log_obj.writelines("dec31_iso_weekNo: " + str(dec31_iso_weekNo) + "\n")
               break
            else:
               end_weekNo_int = start_weekNo_int
               start_weekNo_int = start_weekNo_int - 2
            
         start_weekNo_str = str(start_weekNo_int)
         if start_weekNo_int < 10: 
            start_weekNo_str = "0" + start_weekNo_str # Used for cosmetic purposes to be included in the plot.
         if end_weekNo_int < 10:
            end_weekNo_str = "0" + str(end_weekNo_int) # Used for cosmetic purposes.
         else:
            end_weekNo_str = str(end_weekNo_int)
   
         jan01_dt = datetime.datetime(int(year), 1, 1, 0, 0, 0)
         jan01_weekday = jan01_dt.strftime('%a')

         jan01_iso_yearNo =  jan01_dt.isocalendar()[0]
         jan01_iso_weekNo =  jan01_dt.isocalendar()[1]
         jan01_iso_weekdayNo =  jan01_dt.isocalendar()[2]
         
         days_since_firstMonday_week01 = 14 * (start_weekNo_int - 1)/2         
         if jan01_iso_weekNo != 1:
            firstMonday_week01_dt = jan01_dt + datetime.timedelta(days=(8 - jan01_iso_weekdayNo))
            sd = firstMonday_week01_dt + datetime.timedelta(days=days_since_firstMonday_week01)
         else:
            firstMonday_week01_dt = jan01_dt - datetime.timedelta(days=(jan01_iso_weekdayNo - 1))                       
            sd = firstMonday_week01_dt + datetime.timedelta(days=days_since_firstMonday_week01)            
      
         ed = sd + datetime.timedelta(days=14)
         sd_ed = []
         sd_ed = [sd, ed]

##################################################
         log_obj.writelines("\njan01: " + str(jan01_dt) + "\n")
         log_obj.writelines("jan01_weekday: " + jan01_weekday + "\n")
         log_obj.writelines("\njan01_iso_yearNo: " + str(jan01_iso_yearNo) + "\n")
         log_obj.writelines("jan01_iso_weekNo: " + str(jan01_iso_weekNo) + "\n")
         log_obj.writelines("jan01_iso_weekdayNo: " + str(jan01_iso_weekdayNo) + "\n")         
         log_obj.writelines("\nWeek" + start_weekNo_str + "-" + end_weekNo_str + "\n")
         log_obj.writelines("Date firstMonday_week01_dt: " + str(firstMonday_week01_dt) + "\n")
         log_obj.writelines("days_since_firstMonday_week01: " + str(days_since_firstMonday_week01) + "\n")         
         log_obj.writelines("\nsd: " + str(sd) + "\n")
         log_obj.writelines("ed: " + str(ed) + "\n")
         
#        return sd_ed   

   log_obj.close()
#################################################################################

if __name__ == "__main__": main()
