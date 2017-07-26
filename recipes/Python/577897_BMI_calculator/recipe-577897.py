#!/usr/bin/env python

##Author: Alex Cruz

# If user types in q, program terminates
# If user types in other than q, program
# continues and calcualtes bmi
def main():
  quit = False
  count = 0

  answer = raw_input('\nEnter "q" to quit: ')
  if answer == 'q':
      quit = True

# Caclulates bmi 3 times prompting user to type in 'q'
# or another letter to continue with bmi calculation
  while (not quit and count < 10):
      print '-------------------------'
      print 'This is to '
      print '-------------------------'
      weight = float(input('Enter weight in pounds: '))
      height = float(input('Enter height in inches: '))

# Weight cannot be less than 0 or greater than 500
      if weight <= 0 or weight > 500:
          print 'Weight cannot be less than 0 or greater than 500'
          continue

# Height cannot be less than or equal to 0 inches
      elif height <= 0:
          print 'Height cannot be less than 0'
          continue
      else:
          bmi = (weight / (height * height)) * 703.0
          print 'Your BMI is %.2f' % bmi
          if bmi <= 18.5:
              print 'Your weight status is Underweight'
          elif bmi >= 18.5 and bmi <= 24.9:
              print 'Your weight status is Normal weight'
          elif bmi >= 25 and bmi <= 29.9:
              print 'Your weight status is Overweight'
          elif bmi >= 30:
              print 'Your weight status is Obese'

# increments bmi calculation by 1 with a total of 3 bmi calculations
      count = count + 1
      if count < 10:
        answer = raw_input('\nEnter "q" to quit: ')
        if answer == 'q':
            quit = True

main()
raw_input('\n<enter> to exit')
