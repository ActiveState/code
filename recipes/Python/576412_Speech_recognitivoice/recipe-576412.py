import speech

# say() speaks out loud.
speech.say("I am speaking out loud.")

# input() waits for user input.  The prompt text is optional.
spoken_text = speech.input("Say something, user!")
print "You said: %s" % spoken_text

# You can limit user input to a set of phrases.
spoken_text = speech.input("Are you there, user?", ["Yes", "No", "Shut up, computer."])
print "You said: %s" % spoken_text

# If you don't want to wait for input, you can use listenfor() to run a callback
# every time a specific phrase is heard.  Meanwhile your program can move on to other tasks.
def L1callback(phrase, listener):
  print "Heard the phrase: %s" % phrase
# listenfor() returns a Listener object with islistening() and stoplistening() methods.
listener1 = speech.listenfor(["any of", "these will", "match"], L1callback)
       
# You can listen for multiple things at once, doing different things for each.
def L2callback(phrase, listener):
  print "Another phrase: %s" % phrase
listener2 = speech.listenfor(["good morning Michael"], L2callback)

# If you don't have a specific set of phrases in mind, listenforanything() will
# run a callback every time anything is heard that doesn't match another Listener.
def L3callback(phrase, listener):
  speech.say(phrase) # repeat it back
  if phrase == "stop now please":
    # The listener returned by listenfor() and listenforanything()
    # is also passed to the callback.
    listener.stoplistening()
listener3 = speech.listenforanything(L3callback)

# All callbacks get automatically executed on a single separate thread.
# Meanwhile, you can just do whatever with your program, or sleep.
# As long as your main program is running code, Listeners will keep listening.

import time
while listener3.islistening(): # till "stop now please" is heard
  time.sleep(1)

assert speech.islistening() # to at least one thing
print "Dictation is now stopped.  listeners 1 and 2 are still going."

listener1.stoplistening()
print "Now only listener 2 is going"

# Listen with listener2 for a while more, then turn it off.
time.sleep(30)

speech.stoplistening() # stop all remaining listeners
assert not speech.islistening()
