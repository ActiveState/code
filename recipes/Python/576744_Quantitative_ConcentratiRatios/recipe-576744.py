# Donyo Ganchev, Agricultural University, Plovdiv, Bulgaria
# donyo@abv.bg

choice=None

def qcr():

      gap=input('Enter general amount of pesticide: ')

      qr=raw_input('Enter quantitative ratios with colon between them: ')

      sqr=qr.split(':')

      fqr=[float(i) for i in sqr]

      sqr=sum(fqr)

      el_part=gap/sqr

      am_ratio=[el_part*x for x in fqr]

            

      print \

            """"

"""

      print "Calculated quantitative ratios are: " , am_ratio 

      

while choice!="0":

      print \

      """

     Calculation of quantitative concentration ratios

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             qcr()
