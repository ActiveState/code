#!/usr/bin/env python
# Author: Mark Connolly
# Dedicated to my favorite sister, Caroline
# Contact: mark_connolly at acm dot org


class Monty_Hall(object):
  """Monty, teach me probabilities.
  
  Monty_Hall is a gameshow host that proves that it is statistically better to switch
  when offered the chance after getting additional knowledge in a fair game.  The caveat
  is "statistically better", which means any single trial can have unwanted results.
  But "statistically better" is exactly where the fist-fights at bars and family reunions
  start, so no matter the single trial outcomes.
  
  Monty has a game set, which has doors.  Monty has a scoreboard which keeps track of
  wins and losses.  You tell Monty waht to do, Monty does it.
  
  You create an instance of Monty_Hall and send him messages.  For example:
  (when you start python, you first want to 
  
>>> import gameshow
  
  then you have access to what you need)
  
  
>>> monty = gameshow.Monty_Hall() # get yourself a gameshow Monty_Hall and attach its reference to a variable
  
>>> monty.choose_door(2)  # 1. tell your Monty_Hall to choose a door (number 2 in this case)
>>> monty.switch()        # 2. tell your Monty_Hall you'd like to switch
>>> monty.start_game()    # 3. tell your Monty_Hall to start a new game, Monty_Hall will keep score

  You can repeat the three steps to you heart's content.  Stay with the same Monty_Hall
  for he knows the score.  Once you think you have suffered a sufficient number of games:
>>> monty.tell_me_the_score()  # and your Monty_Hall will
  
  You can also tell your Monty_Hall
>>> monty.start_new_series()
  
  And your Monty_Hall will clear the scoreboard and start gathering statistics anew.
  If Monty's music is bringing you down, you can set the wait to zero seconds:
>>> monty.music_duration = 0   # or any number of seconds.  There is no actual music!
  
  
  If you are lazy, you can have the gameshow automaton play for you:
>>> gameshow.automaton()  # plays 100 games (by default) and has its Monty_Hall print out the statistics
  
  You can have the gameshow automaton play any number of games for you with the form
>>> gameshow.automaton(iterations=1000)

  Notes:  The prize is randomly distributed to Monty's three game set doors for each game.  The 
  statistical results will vary around the expected values 1/3 and 2/3.  Variance is to be expected,
  but large numbers of trials should be very close to the expected values.  Mendel cooked his books.
  
  """
  def __init__(self, music_duration = 4):
    """
    Do all the initialization stuff when a new 
    instance of Monty_Hall is created.  Granted,
    this aint much.
    """
    self.music_duration = music_duration
    self.start_new_series()
   
  def start_game(self):
    """
    Starts a new game without resetting the scoreboard
    """
    self.game_set = Game_Set()
    print("\nYou can now choose a door.\n")
   
  def start_new_series(self):
    """
    A series is a set of games for which win/loss statistics are created.  
    Starting a new series clears the scoreboard and starts a new game.
    """
    self.scoreboard = Scoreboard()
    print("Scoreboard has been cleared")
    self.start_game()
   
  def choose_door(self, door_number):
    """
    Monty gives you the door you ask for, then he opens a door you did not pick.
    """
    import time
    try:
      self.game_set.select_door(door_number)
      print("I will now open a door you did not select.")
      print("(music plays)(no music actually plays)")
      time.sleep(self.music_duration)
      self.game_set.open_door()
    except ValueError, explanation:
      pass
      print explanation
   
  def switch(self):
    """
    Monty switches your door with the one you did not pick.  Monty then opens 
    your new selection to reveal the prize or the goat.
    """
    try:
      self.game_set.switch_door()
      result = self.game_set.open_selected_door()
      print("Door contains %s" % result)
      if (result == "prize"):
        print("You win!")
        self.scoreboard.won_switched()
      else:
        print("Baaaaa!")
        self.scoreboard.lost_switched()
    except ValueError, explanation:
      print explanation
      pass
   
  def stay(self):
    """
    Monty understands you would like to stay.  Monty shrugs and opens 
    your door to reveal the prize or the goat.
    """
    result = self.game_set.open_selected_door()
    print("Door contains %s" % result)
    if (result == "prize"):
      print("You win!")
      self.scoreboard.won_stayed()
    else:
      print("Baaaaa!")
      self.scoreboard.lost_stayed()
   
  def tell_me_the_score(self):
    """
    Monty has his scoreboard print itself out with the wins, losses, and percentages.
    """
    self.scoreboard.tell_me_the_score()


class Scoreboard(object):
  def __init__(self):
    self.stats = {"Won switched" : 0.0, # this is a hash structure
                  "Lost switched": 0.0, # it is composed of keys and values
                  "Won stayed": 0.0,    # values are set as float numbers (has a decimal
                                        # component) as opposed to integers.
                  "Lost stayed": 0.0}   # The reason is that the value will be used in 
                                        # calculating percentages.  Integers would render 
                                        # integers and the decimal would be lost.
   
  def won_switched(self):
    self.stats["Won switched"] += 1
   
  def lost_switched(self):
    self.stats["Lost switched"] += 1
   
  def won_stayed(self):
    self.stats["Won stayed"] += 1
   
  def lost_stayed(self):
    self.stats["Lost stayed"] += 1
   
  def tell_me_the_score(self):
    play_made = "Stayed"
    won = self.stats["Won stayed"]
    lost = self.stats["Lost stayed"]
    self.print_score(play_made, won, lost)
    play_made = "Switched"
    won = self.stats["Won switched"]
    lost = self.stats["Lost switched"]
    self.print_score(play_made, won, lost)
  
  def print_score(self, play, w, l):
    print("\nStats for " + play)
    if (w + l > 0):
      print(
        "wins: %i losses: %i, percent win: %5.2f%%" # Text with formatting placeholders
        %(w, l, (w / (w + l) * 100.0))       # The collection of ordered values to
                                             # substitute and format
        )                                    # The %% prints a single % literal at
                                             # the end of the formatted string
    else:
      print("No statistics for %s" % play)


class Game_Set(object):
  """
  A collection of doors.  Each door can hold something desireable
  or something not so desireable.  However, only one door in a game
  can hold something desireable.
  """
  def __init__(self):
    import random
    doors = {
             0: Door(1),
             1: Door(2),
             2: Door(3)}
    # random.randrange(startInt,endInt) generates a random integer in the range
    # of startInt (which is included in the possibilities) to endInt (which is
    # not included in the possibilities.
    prize_door = random.randrange(0,3)
    doors[prize_door].contents = "prize"
    doors[((prize_door + 1) % 3)].contents = "goat"
    doors[((prize_door + 2) % 3)].contents = "goat"
    
    self.keep_track = {"doors": doors,
                       "prize": doors[prize_door],
                       "selected": None,
                       "opened": None}
    
  def select_door(self, door_number):
    """
    Select a door by number.
    """
    # Has a door already been selected or switched this game?
    if (self.keep_track["selected"]):
      # raise an error to the caller and do no more
      raise ValueError, "You have already selected a door."
    # is an appropriate door being selected?
    if door_number in (1,2,3):
      # appropriate door number, transform to door key by subtracting 1
      door_number = door_number - 1
    else:
      # raise an error to the caller and do no more
      raise ValueError, "You entered %s, which is not a recognized door." % door_number
    # that takes care of the possible errors
    # now, moved the selected door out of the collection
    self.keep_track["selected"] = self.keep_track["doors"][door_number]
    del self.keep_track["doors"][door_number]
    print("\nYou have selected door number %s.\nYou have a 1 in 3 chance of holding the prize." 
          % self.keep_track["selected"].label)
    print("The house has a 2 in 3 chance of holding the prize.\n")
    
  def open_door(self):
    """
    Open one of the doors that has not been selected.  One of the doors may have
    the prize.  Don't open that one.
    """
    keys = self.keep_track["doors"].keys()
    for key in keys:
      if self.keep_track["doors"][key] == self.keep_track["prize"]:
        pass
      else:
        self.keep_track["opened"] = self.keep_track["doors"][key]
        del self.keep_track["doors"][key]
        print("\nDoor %s is open and contains a %s.\n" 
              % (self.keep_track["opened"].label, self.keep_track["opened"].contents)
              )
        print("Your odds of holding the prize behind door number %s have not changed." 
              % self.keep_track["selected"].label)
        print("The house odds have not changed just because one of the house doors has been opened.")
        print("You now know which of the two doors held by the house does not contain the prize.")
        print("Switching your selection is the same as switching to both doors held by the house.")
        print("This is because you have taken the open door out of the selection options.")
        print("Switching to the open door would just be silly, unless you want the goat.")
        print("Switching to the house's closed door exchanges your odds (1 in 3) for the house odds (2 in 3)\n")
        break
  
  def switch_door(self):
    """
    Exchange the selected door to the unopened door
    """
    keys = self.keep_track["doors"].keys()
    key = keys[0] # only one door left in the collection
                  # one removed when selected. one removed when opened
    # swap the doors
    hold_this_a_second = self.keep_track["doors"][key]
    self.keep_track["doors"][key] = self.keep_track["selected"]
    self.keep_track["selected"] = hold_this_a_second
    print("\nYou now hold door %s.\n" % self.keep_track["selected"].label)
  
  def open_selected_door(self):
    """
    Opens the selected door to see if the prize is THE prize or a goat
    """
    return self.keep_track["selected"].contents


class Door(object):
  def __init__(self, label):
    self.contents = None
    self.label = label

def automaton(iterations=100, select_door="random"):
  """
  Plays the game with its own Monty_Hall.  Turns off the music so
  the games proceeds apace.
  
  default iterations is 100
  
  door selection is random unless specified by the named variable select_door
  """
  import random
  "create a function that either returns a random door or a specified door"
  if (select_door == "random"):
    select_a_door = lambda : random.randrange(1,4)
  else:
    select_a_door = lambda : select_door
    
  monty = Monty_Hall(music_duration=0)
  for i in range(1,iterations):
    select_door = select_a_door()
    monty.choose_door(select_door)
    monty.switch()
    monty.start_game()
    monty.choose_door(select_door)
    monty.stay()
    monty.start_game()
  
  "finish up with the scores"
  monty.tell_me_the_score()

"""
print a little help at import or reload
"""
help(Monty_Hall)
