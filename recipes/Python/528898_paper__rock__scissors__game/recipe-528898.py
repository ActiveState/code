# The traditional paper scissors rock game
# best of five
import os
def clear():
   os.system("clear")
clear()
print "\n\nPaper, Rock, Scissors Game -(Best of five games)"
x = 0 ;  l = 0 ;  w = 0 ; d = 0 ; lt = 0 ; wt = 0 ; dt = 0
while x < 5:
  x = x + 1
  import random
  class Computer:
         pass
  comp_is = Computer()
  comp_is.opt = ('r','p','s')
  comp_is.rand = random.choice(comp_is.opt)

  if comp_is.rand == 'r':
            comp  = 'rock'
  elif comp_is.rand == 'p':
            comp  = 'paper'
  else:
        comp  = 'scissors'

  class Human:
       pass
  human_is = Human
  print
  human_is.player = raw_input(' Enter your choice of\n   r\
 for rock\n   p for paper or\n   s for scissors ... ')
  print
    
  class Result:
     pass
  Result_is = Result
  if comp_is.rand == human_is.player:
    print "draw - computer chose ",  comp
    print
    d = d + 1
    dt = dt + 1
  elif comp_is.rand == 'r' and human_is.player == 'p':
      print "  player beats computer -computer chose ",  comp
      print
      w = w + 1
      wt = wt + 1
  elif comp_is.rand == 'p' and human_is.player == 's':
      print "  computer chose ",  comp
      print "  player beats computer-because scissors cuts paper"
      print
      w = w + 1
      wt = wt + 1
  elif comp_is.rand == 's' and human_is.player == 'r':
     print " computer chose ", comp  
     print " player beats computer-because rock breaks scissors"
     w = w + 1
     wt = wt + 1
  else :
     print "   computer wins - computer chose  ", comp
     print
     l = l + 1
     lt = lt + 1
     
  if x == 5:
    print 
    print    
    print "  games  won ... ",  w
    print "  games lost ... ",  l
    print "  games drawn ... ",  d
    print 
    print "  Running total overall of games won ... ", wt
    print "  Running total overall of games lost ... ", lt
    print "  Running total overall of games drawn ... ", dt
    print 
    w = 0 ; l = 0 ; d = 0
    again = raw_input('Do you want to play again y for yes, n for no ..  ')
    if again == 'y':
       x = 0
    else:
      print 
      if lt > wt:
         print "You lost the game ha! ha!"
         print
         print 'finish'
