import string
import speech

while True:
    print "Talk:"
    phrase = speech.input()
    speech.say("You said %s" % phrase)
    print "You said {0}".format(phrase)
    #if phrase == "turn off":
    if phrase.lower() == "goodbye":
        break
