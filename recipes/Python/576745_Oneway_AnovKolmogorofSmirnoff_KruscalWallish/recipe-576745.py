# Donyo Ganchev, Agricultural University, Plovdiv, Bulgaria
# donyo@abv.bg
from statlib import anova



choice=None

def an():

      num_ob=input('Enter the number of observations: ')

      var=[0]*num_ob

      control=[0]*num_ob

      an=[0]*2

      ks=[0]*2

      kw=[0]*2

      index=0

      while index<num_ob:

                  print index+1

                  var[index]=input('Enter the values of the variant: ')

                  index+=1

      print \

           """

     """

      index1=0

      while index1<num_ob:

            print index1+1

            control[index1]=input('Enter the values of the control: ')

            index1+=1



     

      an=anova.F_oneway(var, control)

      ks=anova.ks_2samp(var, control)

      kw=anova.kruskalwallish(var, control)

      

    

      print \

            """

      """

           

      print "ANOVA p-value is: ", an[1]

      if an[1]<0.05:

            print "There is statisticaly significant differences"

      else:

            print "There is no statisticaly significant differences" 

      print \

             """

"""

      print "Kolmogorov - Smirnoff p-value is: ", ks[1]

      if ks[1]<0.05:

            print "There is statisticaly significant differences"

      else:

            print "There is no statisticaly significant differences" 

      print "Kruskal-Wallish p-value is: ", kw[1]

      print \

             """

"""

      if kw[1]<0.05:

           print "There is statisticaly significant differences"

      else:

            print "There is statisticaly significant differences"

            



while choice!="0":

      print \

      """

     One-way ANOVA, Kolmogorov - Smirnoff and Kruskal-Wallish Test Calculation Program



     Used module: Python - Statlib



     Created by Donyo Ganchev, Agricultural University, Plovdiv, Bulgaria

     

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             an ()
