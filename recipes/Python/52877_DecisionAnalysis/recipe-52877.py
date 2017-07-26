print "A General Decision Analysis Program."
print
print "Have You Ever Had to Make Up Your Mind?"
print





def decisionanalysis():
    # This code is placed in the public domain
    print
    print "This is a general decision program, and you can define your choices and criteria."
    print
    print "When prompted, please enter the options or choices that you need to decide amongst."
    print
    print "Then, when prompted, enter the criteria for making this decision."
    def get_list(heading, prompt):
                  
            print heading
            print
            print "(enter a blank line to end the list)"
            ret = []
            i = 1
            while 1:
                    line = raw_input(prompt % i)
                    if not line:
                            break
                    ret.append(line)
                    i=i+1
            print
            return ret

    def get_number(prompt):
           
            res = None
            while res is None:
                    try:
                            res = float(raw_input(prompt))
                    except ValueError: pass
            return res

    # First, ask the user to enter the lists
    options = get_list("Enter your options:", "Option %d: ")
    criteria = get_list("Now, enter your criteria:", "Criterion %d: ")

    # Next, get the user to rank his criteria.  I use a system where higher
    # is better, so that an undesirable characteristic can be given a negative
    # weight.
    #
    # {} is a dictionary, it can be indexed by (nearly) any expression,
    # and we will index it with the names of the criteria.
    # number of the criterion)
    print "A program to help you make decisions."
    rankings = {}
    print
    print "Enter relative importance of criteria (higher is more important)"
    print
    for c in criteria:
                    rankings[c] = get_number("Criterion %s: " % c)

    # Next, get the user to score each option on all the criteria.
    # Here, we index the dictionary on the pair (option, criterion).
    # This is similar to a two-dimensional array in other languages

    score = {}
    print
    print "Enter score for each option on each criterion"
    print
    for o in options:
            print
            print "Scores for option %s" % o
            print
            for c in criteria:
                    score[o, c] = get_number("Criterion %s: " % c)

    # Calculate the resulting score for each option.  This equation
    # is different from Rod Stephen's original program, because I
    # make more important criteria have higher rankings, and even let
    # bad criteria have negative rankings.

    # The "result" dictionary is indexed with the names of the options.
    result = {}
    for o in options:
            value = 0
            for c in criteria:
                    print o, c, rankings[c], score[o, c]
                    value = value + rankings[c] * score[o, c]
            result[o] = value

    # Now, I want to take the dictionary result, and turn it into a ranked list

    results = result.items()        # A list of tuples (key, value)
    results.sort(lambda x, y: -cmp(x[1], y[1]))
                                # Sort the list using the reverse of the
                                # "value" of the entry, so that higher
                                # values come first

    print
    print "Results, in order from highest to lowest score"
    print
    print "%5s %s" % ("Score", "Option")

    # Take the pairs out of results in order, and print them out
    for option, result in results:
            print "%5s %s" % (result, option)

   

def ProgramLanguageFinal():
    print "This is a program to help give you an idea which programming languages you should consider learning."
    print "While there are any number of languages you might consider, this program considers only 11 of the most popluar ones."
    print
    print "The program will ask you to input a ranking or weighting for a number of criteria that may be of importance"
    print "in choosing your next programming language."
    def get_list(heading, prompt):
        
           print heading
           print
           print "(enter a blank line to end the list)"
           ret = []
           i = 1
           while 1:
                    line = raw_input(prompt % i)
                    if not line:
                            break
                    ret.append(line)
                    i=i+1
           print
           return ret

    def get_number(prompt):
            """ get_number(prompt) -> float

    This function prompts for a number.  If the user enters bad input, such as
    "cat" or "3l", it will prompt again.
    """
            res = None
            while res is None:
                    try:
                            res = float(raw_input(prompt))
                    except ValueError: pass
            return res


    options = ["Python", "Perl", "Ruby", "Tcl", "JavaScript", "Visual Basic", "Java", "C++", "C", "Lisp", "Delphi"]
    criteria = ["ease of learning", "ease of use", "speed of program execution", "quality of available tools", "popularity", "power & expressiveness", "cross platform?", "cost"]


    rankings = {}
    print
    print "Enter relative importance of criteria (higher is more important)"
    print
    for c in criteria:
                    rankings[c] = get_number("Criterion %s: " % c)

    # Next, get the user to score each option on all the criteria.
    # Here, we index the dictionary on the pair (option, criterion). 
    # This is similar to a two-dimensional array in other languages

    score = {("Python", "ease of learning"):100, ("Python", "ease of use"):100, ("Python", "speed of program execution"):10, ("Python", "quality of available tools"):70, ("Python", "popularity"):50, ("Python", "power & expressiveness"):100, ("Python", "cross platform?"):100, ("Python", "cost"):100,
    ("Perl", "ease of learning"):50, ("Perl", "ease of use"):60, ("Perl", "speed of program execution"):20, ("Perl", "quality of available tools"):50, ("Perl", "popularity"):85, ("Perl", "power & expressiveness"):70, ("Perl", "cross platform?"):100, ("Perl", "cost"):100,
    ("Ruby", "ease of learning"):50, ("Ruby", "ease of use"):100, ("Ruby", "speed of program execution"):20, ("Ruby", "quality of available tools"):20, ("Ruby", "popularity"):10, ("Ruby", "power & expressiveness"):100, ("Ruby", "cross platform?"):80, ("Ruby", "cost"):100, 
    ("Tcl", "ease of learning"):100, ("Tcl", "ease of use"):100, ("Tcl", "speed of program execution"):10, ("Tcl", "quality of available tools"):50, ("Tcl", "popularity"):40, ("Tcl", "power & expressiveness"):10, ("Tcl", "cross platform?"):100, ("Tcl", "cost"):100,
    ("JavaScript", "ease of learning"):70, ("JavaScript", "ease of use"):75, ("JavaScript", "speed of program execution"):10, ("JavaScript", "quality of available tools"):50, ("JavaScript", "popularity"):100, ("JavaScript", "power & expressiveness"):40, ("JavaScript", "cross platform?"):50, ("JavaScript", "cost"):100, 
    ("Visual Basic", "ease of learning"):50, ("Visual Basic", "ease of use"):100, ("Visual Basic", "speed of program execution"):20, ("Visual Basic", "quality of available tools"):100, ("Visual Basic", "popularity"):100, ("Visual Basic", "power & expressiveness"):50, ("Visual Basic", "cross platform?"):1, ("Visual Basic", "cost"):1,
    ("Java", "ease of learning"):15, ("Java", "ease of use"):50, ("Java", "speed of program execution"):50, ("Java", "quality of available tools"):100, ("Java", "popularity"):90, ("Java", "power & expressiveness"):100, ("Java", "cross platform?"):100, ("Java", "cost"):100,
    ("C++", "ease of learning"):10, ("C++", "ease of use"):25, ("C++", "speed of program execution"):90, ("C++", "quality of available tools"):90, ("C++", "popularity"):80, ("C++", "power & expressiveness"):100, ("C++", "cross platform?"):90, ("C++", "cost"):100,
    ("C", "ease of learning"):15, ("C", "ease of use"):20, ("C", "speed of program execution"):100, ("C", "quality of available tools"):80, ("C", "popularity"):80, ("C", "power & expressiveness"):80, ("C", "cross platform?"):110, ("C", "cost"):100,
    ("Lisp", "ease of learning"):40, ("Lisp", "ease of use"):50, ("Lisp", "speed of program execution"):80, ("Lisp", "quality of available tools"):60, ("Lisp", "popularity"):25, ("Lisp", "power & expressiveness"):110, ("Lisp", "cross platform?"):80, ("Lisp", "cost"):90,
    ("Delphi", "ease of learning"):50, ("Delphi", "ease of use"):110, ("Delphi", "speed of program execution"):85, ("Delphi", "quality of available tools"):100, ("Delphi", "popularity"):30, ("Delphi", "power & expressiveness"):100, ("Delphi", "cross platform?"):80, ("Delphi", "cost"):10}


    # Calculate the resulting score for each option.  
    # The "result" dictionary is indexed with the names of the options.
    result = {}
    for o in options:
            value = 0
            for c in criteria:
                
                    value = value + rankings[c] * score[o, c]
            result[o] = value

    # Now, I want to take the dictionary result, and turn it into a ranked list

    results = result.items()        # A list of tuples (key, value)
    results.sort(lambda x, y: -cmp(x[1], y[1]))
                                # Sort the list using the reverse of the
                                # "value" of the entry, so that higher
                                # values come first

    print
    print "Results, in order from highest to lowest score"
    print
    print "%5s %s" % ("Score", "Option")

    # Take the pairs out of results in order, and print them out
    for option, result in results:
            print "%5s %s" % (result, option)




def ProgramLanguageScript():
    print
    print "This is a program to help you choose a scripting language."
    print
    print "You will be asked to rank some important criteria as to their relative importance to you."
    print "These criteria are 'ease of learning', 'ease of use', 'speed of program execution'"
    "'quality of available tools', 'popularity', and 'power & expressiveness'"
    print
    print "Please rank each of the criteria with a number from 1 to 100 when prompted."
    print
    print "100 means of highest relative importance, 1 means of least importance."


    def get_list(heading, prompt):
            print heading
            print
            print "(enter a blank line to end the list)"
            ret = []
            i = 1
            while 1:
                    line = raw_input(prompt % i)
                    if not line:
                            break
                    ret.append(line)
                    i=i+1
            print
            return ret

    def get_number(prompt):
        
            res = None
            while res is None:
                    try:
                            res = float(raw_input(prompt))
                    except ValueError: pass
            return res

    # First, ask the user to enter the lists
    options = ["Python", "Perl", "Ruby", "Tcl", "JavaScript", "Visual Basic"]
    criteria = ["ease of learning", "ease of use", "speed of program execution", "quality of available tools", "popularity", "power & expressiveness", "cross platform?", "cost"]

    # Next, get the user to rank his criteria.  I use a system where higher
    # is better, so that an undesirable characteristic can be given a negative
    # weight.
    #
    # {} is a dictionary, it can be indexed by (nearly) any expression,
    # and we will index it with the names of the criteria.
    # (For a more traditional program, we could use a list and index by the
    # number of the criterion)

    rankings = {}
    print
    print "Enter relative importance of criteria (higher is more important)"
    print
    for c in criteria:
                    rankings[c] = get_number("Criterion %s: " % c)

    # Next, get the user to score each option on all the criteria.
    # Here, we index the dictionary on the pair (option, criterion). 
    # This is similar to a two-dimensional array in other languages

    score = {("Python", "ease of learning"):100, ("Python", "ease of use"):100, ("Python", "speed of program execution"):10, ("Python", "quality of available tools"):50, ("Python", "popularity"):50, ("Python", "power & expressiveness"):100, ("Python", "cross platform?"):100, ("Python", "cost"):100,
    ("Perl", "ease of learning"):50, ("Perl", "ease of use"):90, ("Perl", "speed of program execution"):30, ("Perl", "quality of available tools"):50, ("Perl", "popularity"):75, ("Perl", "power & expressiveness"):100, ("Perl", "cross platform?"):100, ("Perl", "cost"):100,
    ("Ruby", "ease of learning"):50, ("Ruby", "ease of use"):100, ("Ruby", "speed of program execution"):10, ("Ruby", "quality of available tools"):20, ("Ruby", "popularity"):10, ("Ruby", "power & expressiveness"):100, ("Ruby", "cross platform?"):80, ("Ruby", "cost"):100, 
    ("Tcl", "ease of learning"):100, ("Tcl", "ease of use"):100, ("Tcl", "speed of program execution"):5, ("Tcl", "quality of available tools"):50, ("Tcl", "popularity"):40, ("Tcl", "power & expressiveness"):10, ("Tcl", "cross platform?"):100, ("Tcl", "cost"):100,
    ("JavaScript", "ease of learning"):70, ("JavaScript", "ease of use"):75, ("JavaScript", "speed of program execution"):10, ("JavaScript", "quality of available tools"):50, ("JavaScript", "popularity"):100, ("JavaScript", "power & expressiveness"):40, ("JavaScript", "cross platform?"):50, ("JavaScript", "cost"):100, 
    ("Visual Basic", "ease of learning"):50, ("Visual Basic", "ease of use"):100, ("Visual Basic", "speed of program execution"):20, ("Visual Basic", "quality of available tools"):100, ("Visual Basic", "popularity"):100, ("Visual Basic", "power & expressiveness"):50, ("Visual Basic", "cross platform?"):1, ("Visual Basic", "cost"):1}
    # Calculate the resulting score for each option.  This equation
    # is different from Rod Stephen's original program, because I
    # make more important criteria have higher rankings, and even let
    # bad criteria have negative rankings.

    # The "result" dictionary is indexed with the names of the options.
    result = {}
    for o in options:
            value = 0
            for c in criteria:
                    print o, c, rankings[c], score[o, c]
                    value = value + rankings[c] * score[o, c]
            result[o] = value

    # Now, I want to take the dictionary result, and turn it into a ranked list

    results = result.items()        # A list of tuples (key, value)
    results.sort(lambda x, y: -cmp(x[1], y[1]))
                                # Sort the list using the reverse of the
                                # "value" of the entry, so that higher
                                # values come first

    print
    print "Results, in order from highest to lowest score"
    print
    print "%5s %s" % ("Score", "Option")

    # Take the pairs out of results in order, and print them out
    for option, result in results:
            print "%5s %s" % (result, option)


def Basketball():


    print "This is a program to help you decide which team will win a basketball game"
    print
    print "When prompted, enter a number ranking each team on the prompted team skill"
    print "on a scale from 1 to 100, with 1 being terrible and 100 being the best imaginable"
    print
    team_one = raw_input ("What is the name of team one:")
    team_two = raw_input ("What is the name of team two:")

    criteria = {"speed":100, "size":66, "jumping_ability":50, "defense":60, "shooting":75, "ballhandling":50, "rebounding":50}
    scoreonespeed = input ("rank the team speed of %s on a scale of 1 to 100:" % team_one)
    scoretwospeed = input ("rank the team speed of %s on a scale of 1 to 100:" % team_two)
    scoreonesize= input ("rank the team size of %s on scale of 1 to 100" % team_one)
    scoretwosize= input ("rank the team size of %s on scale of 1 to 100" % team_two)
    scoreonejumping_ability= input("rank the jumping ability of %s" % team_one)
    scoretwojumping_ability= input("rank the jumping ability of %s" % team_two)
    scoreonedefense = input ("ramk the defense of %s" % team_one)
    scoretwodefense = input ("ramk the defense of %s" % team_two)
    scoreoneshooting = input ("rank the shooting ability of %s" % team_one)
    scoretwoshooting = input ("rank the shooting ability of %s" % team_two)
    scoreoneballhandling= input("rank the ballhandling ability of %s:" % team_one)
    scoretwoballhandling= input("rank the ballhandling ability of %s:" % team_two)
    scoreonerebounding = input ("rank the rebounding ability of %s" % team_one)
    scoretworebounding = input ("rank the rebounding ability of %s" % team_two)

    scoreteamone = (criteria["speed"])*(scoreonespeed) + (criteria["size"])*(scoreonesize) +(criteria["jumping_ability"])*(scoreonejumping_ability) +(criteria["defense"])*(scoreonedefense) + (criteria["shooting"])*(scoreoneshooting) +(criteria["ballhandling"])*(scoreoneballhandling) +(criteria["rebounding"])*(scoreonerebounding)

    scoreteamtwo = (criteria["speed"])*(scoretwospeed) + (criteria["size"])*(scoretwosize) +(criteria["jumping_ability"])*(scoretwojumping_ability) +(criteria["defense"])*(scoretwodefense) + (criteria["shooting"])*(scoretwoshooting) +(criteria["ballhandling"])*(scoretwoballhandling) +(criteria["rebounding"])*(scoretworebounding)

    print "%s has a power ranking of %d" % (team_one, scoreteamone)
    print
    print "%s has a power ranking of %d" % (team_two, scoreteamtwo)

    if scoreteamone > scoreteamtwo:
        print "%s wins!!!" % team_one
        
    elif scoreteamone == scoreteamtwo:
        print "the two teams are a toss-up!!!"
    else:
        print "%s wins!!!" % team_two

                
def YesNo():
    

    def get_list(heading, prompt):
            
            print heading
            print
            print "(enter a blank line to end the list)"
            ret = []
            i = 1
            while 1:
                    line = raw_input(prompt % i)
                    if not line:
                            break
                    ret.append(line)
                    i=i+1
            print
            return ret

    def get_number(prompt):
        
            res = None
            while res is None:
                    try:
                            res = float(raw_input(prompt))
                    except ValueError: pass
            return res


    options = ["Yes", "No"]
    criteria = get_list("Enter your criteria ...", "Criterion %d: ")



    rankings = {}
    print
    print "Enter relative importance of criteria (higher is more important)"
    print
    for c in criteria:
                    rankings[c] = get_number("Criterion %s: " % c)


    score = {}
    print
    print "Enter score for each option on each criterion"
    print
    for o in options:
            print
            print "Score for a %s decision "% o
            print
            for c in criteria:
                    score[o, c] = get_number("Criterion %s: " % c)

# Calculate the resulting score for each option.  This equation
# is different from Rod Stephen's original program, because I
# make more important criteria have higher rankings, and even let
# bad criteria have negative rankings.

# The "result" dictionary is indexed with the names of the options.
    result = {}
    for o in options:
            value = 0
            for c in criteria:
                
                    value = value + rankings[c] * score[o, c]
            result[o] = value


    results = result.items()        # A list of tuples (key, value)
    results.sort(lambda x, y: -cmp(x[1], y[1]))
                                # Sort the list using the reverse of the
                                # "value" of the entry, so that higher
                                # values come first

    print
    print "The results are"
    print
    print "%5s %s" % ("Score", "Option")


    for option, result in results:
            print "%5s %s" % (result, option)


    if results[0] > results[1]:
            print "You should decide Yes!!!"

    else:
            print
            print "You should decide No!!!"
            print
                

    







while 1:    # loop forever

    print "Please enter the number for the type of decision you wish to analayze:" 
    print "1. General Decision Analysis, you choose the options, criteria, etc."
    print "2. Help in Choosing Programming Language amongst 11 popular languages"
    print  "3. Help in choosing scripting programming language amongst 6 scripting languages"
    print  "4. Which Basketball Team will win the Game???"
    print  "5. Questions with Yes or No type answers"
    choice = input("Please type in the number of the type of decision-program you wish to run from above and hit enter:")
    if choice ==1:
        decisionanalysis()

        
              
    elif choice ==2: 
        ProgramLanguageFinal()
    elif choice ==3:
        ProgramLanguageScript()
    elif choice ==4:
        Basketball()
    elif choice ==5:
        YesNo()
    elif choice =="quit":
        break    # exit from infinite loop
    else:
        print "Invalid operation"
