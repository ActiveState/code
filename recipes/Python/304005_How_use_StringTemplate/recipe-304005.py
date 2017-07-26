import string

#With the new style, you mark a label in a string with with a $ and use a #dictionary to map that label to something else. 

new_style=string.Template('this is $thing')
print new_style%{'thing':5}      #produces:  this is 5                              
print new_style%{'thing':'test'} #produces: this is test

#With the old style you have to specify a type as a formatting code
#in this case, %s is used for a string format. Note how the old style 
#string is not as clean looking.

old_style='this is %(thing)s'
print old_style%{'thing':5}      #produces: this is 5
print old_style%{'thing':'test'} #produces: this is test

#Here is an example that shows 3 basic uses of the new Template.
#The standard mapping with $customer, handeling of the case where characters #not part of the label directly follow it with ${name}Inn, and finally the use #of $$ to insert an actual $ into the string.

form_letter='''Dear $customer,
I hope you are having a great time.
If you do not find Room $room to your satisfaction,
let us know. Please accept this $$5 coupon.
            Sincerely,
            $manager
            ${name}Inn'''
                                        
letter_template=string.Template(form_letter)

print letter_template%{'name':'Sleepy','customer':'Fred Smith',
                       'manager':'Barney Mills','room':307,
                      }
#produces:
Dear Fred Smith,
I hope you are having a great time.
If you do not find Room 307 to your satisfaction,
let us know. Please accept this $5 coupon.
            Sincerely,
            Barney Mills
            SleepyInn
