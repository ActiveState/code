"""This is a program to calculate the estimated final score for a one day cricket match, whilst it is still in progress, also if it is a 50 over game it gives
a duckworth lewis score.  There are 2 classes one to calcuate the result the other for the gui"""

from Tkinter import *
class Cricket(object):

    def __init__(self, numberruns,numofoverssofar,x,numofoversingame, win, originalscore=0, orignoovers=0, wold=0, yold=0):
        '''Default agruments, this is the calculating class'''
    
    def numberofballs(self,numofoverssofar):
        """Convert overs to number of balls so far"""
        y = float(numofoverssofar)
        b = int(numofoverssofar)
        numberofballsinthisover = (y-b)*10
        numberofballsbefore = b*6
        totalnumberofballs = numberofballsinthisover + numberofballsbefore
        return totalnumberofballs
        
    
    def scoreperball(self,numberruns,numberballs):
        """Runs per ball"""
        #numberruns is the number of runs ssocre and numberballs is the number of balls so far
        numberruns = float(numberruns)
        numberballs = float(numberballs)
        runsperball = numberruns/numberballs
        return runsperball
        
    def ifnotout(self,scoreperball,numofovers):
        #y score per ball
        #numofovers number of overs in game 
        numofovers = numofovers * 6
        a = scoreperball * numofovers 
        a = int(a) 
        return a    
    

    
    
    def ifallout(self,x,w):
        #predicts score if they will not last numofovers overs
        #x is the score per ball
        #w is number of balls to get them out
        b = x * w
        b = int(b)
        return b 
    
    
    def willsurvive(self,w,y,numofovers, wold, yold):
        #looks to see if the team will be bowled out or not returns alloutearly which says if they are bowled out or not
        #w number of wickets so far
        #y how many balls so far
        w = float(w) 
        y = float(y)
        numofovers = float(numofovers)
        #how many balls to get a wicket
        try:
            wlost = y/w
        #if no wickets have been taken a) we will get an error and b) at current
        #state play they will not get bowled out so just ignore this calculations
        #and return that they will survive
        
        #numberofballs to get them allout if this the first time we look at all 10 wickets
        #the second just the number of wickets that were running that time
            allout = ((10 - wold) * wlost) + yold
            numballsingame = numofovers * 6
            if allout < numballsingame: 
                alloutearly = allout 
            else: 
                alloutearly = 0 
        except:
            alloutearly = 0
        return alloutearly


    def formatresults(self, resulttext, score, originalscore):
        #create text to return to GUI
        score = int(score) + int(originalscore)
        score = str(score)
        resulttext = str(resulttext) + score
        return resulttext




    def usedbefore(self, w,y,x,numofovers, win,used_before, battingfirst):
        #this function a) is the function called by the GUI and b) is the function that decides if information from last time
        #this program was called should be used to get a more accurate picture
        x = int(x)
        dlruns = x
        dlovers = int(y)
        dlwicks = w
        wold = 0
        yold = 0
        originalscore = 0
        orignoovers = 0
        if used_before == 'N':
            #it has not been used before so just use the info entered
            results = self.runfuns(w,y,x,numofovers, win, originalscore, orignoovers, wold, yold, dlruns, dlovers, dlwicks, battingfirst )
        else:
            #x score, y number of overs, w number of wickets
            originalscore, yold, wold = self.openlasttime()
            #if it is more than 5 overs and the score has increased or stayed the same use the values from last time
            if int(y) - int(yold) > 5 and int(wold) >= int(w) and x >= int(originalscore) :
            #code to get the results from last time
                results = self.runfuns(w,y,x,numofovers, win, originalscore, orignoovers, wold, yold, dlruns, dlovers, dlwicks, battingfirst)
                #it goes wrong on the line above
            else:
                originalscore = 0
                yold = 0
                wold = 0
                results = self.runfuns(w,y,x,numofovers, win, originalscore, orignoovers, wold, yold, dlruns, dlovers, dlwicks, battingfirst)
        #we want to save the current state
        self.savecurrentstate(x,y,w)
        return results
    
 

    def duckworthlewis(self, dlruns, dlovers, dlwicks, numofovers, batting_first):
        """In case of rain we need to have a duckworth lewis score.  The formula used by the D/L system is:
        Z(u, w) = Zo(w)[1 - exp{-b(w)u}]
        where Z(u, w) is the expected number of runs
        to be scored in u overs when w wickets have been lost.
        Z0(w) is the average total score if an unlimited number
        of overs were available and when w wickets have been lost.
        b(w) is a decay constant that varies with w, the number of wickets lost."""
        dlewisdict1 = {0:[293.80, .033468],1:[241.93,0.043685],2:[217.21,0.044921],3:[173.32,0.059491],4:[142.84,.071912],
                       5:[102.94,0.10011],6:[81.705,.12843],7:[51.471,.21507],8:[26.708,.41548],9:[17.995, .26668 ]}
        dlewisdict2 = {0:[505.00, .012079 ],1:[574.99, .0094898 ],2:[503.97, .010765 ],3:[323.64, .017383 ],4:[189.16, .033475 ],5:[127.16, .043809 ],6:[101.90, .056269 ],7:[56.657, .089155 ],8:[29.729, .15891 ],9:[17.853, .13203 ]}
        if batting_first == 'N':
            dlewisdict1 = dlewisdict2
        listvalues = dlewisdict1[dlwicks]
        Zo = listvalues[0]
        w = listvalues[1]
        #the above code gets the right value for the constants
        bw = 1-(math.exp(-w*(numofovers-dlovers)))
        Z = Zo * bw
        Z = int(Z)
        Z = Z + dlruns
        return Z  


    
    #create a function to run all functions
    def runfuns(self, w,y,x,numofovers, win, originalscore, orignoovers, wold, yold, dlruns, dlovers, dlwicks, battingfirst):
        """This is to get all functions to run"""
        numberofovers = orignoovers
        #numberofovers = numofovers
        #Cricket = Cricket()
        numberofoversplayed = float(y)
        y = self.numberofballs(y)
        #y = numberofballs(y)
        runsperball = self.scoreperball(x,y)
    #see if they will survive numofovers overs
        alloutearly = self.willsurvive(w,y,numofovers, wold, yold)
        x = int(x)
        numofovers = float(numofovers) -numberofoversplayed
        if alloutearly == 0:
            #take off the number of overs they have already had
            a = self.ifnotout(runsperball,numofovers)
            a = a + x
            #a = a + originalscore
            #a = str(a)
            #resulttext = "Predicted score is", a + originalscore
            resulttext = "Predicted score is "
            resulttext = self.formatresults(resulttext, a, originalscore)
        else:
            b = self.ifallout(runsperball,alloutearly)
            b = b + x
            resulttext = "Predicted score is all out for "
            resulttext = self.formatresults(resulttext, b, originalscore)
            a = self.ifnotout(runsperball, numofovers)
            resulttext2 = "\n" + " However if they do not get out, they will get "
            #resulttext2 = self.formatresults(resulttext2, a, originalscore)
            resulttext2 = self.formatresults(resulttext2, a, originalscore)
            #resulttext2 = self.formatresults(resulttext2, b, originalscore)
            resulttext = resulttext + resulttext2
        if dlovers >20 and battingfirst != 'Not entered':
            dresults = self.duckworthlewis(dlruns, dlovers, dlwicks, numofovers, battingfirst)
            dtest = 'The duckworth lewis score in case of rain would be '
            dtest = self.formatresults(dtest, dresults, 0)
            resulttext = resulttext + "\n" + dtest
        return resulttext
        
    def savecurrentstate(self, x,y,w):
        listcurrentstate = [x,y,w]
        #save x score, y number of overs, w number of wickets
        pickle_file = open("cricket1.dat","w")
        cPickle.dump(listcurrentstate, pickle_file)
        pickle_file.close()
    
    def openlasttime(self):
        """Get the state of play last time"""
        try:
            pickle_file = open("cricket1.dat", "r")
            laststateofplay = cPickle.load(pickle_file)
            
        except:
            #as unable to use the file just use 0
            laststateofplay = [0,0,0]
        xold = laststateofplay[0]
            
        yold = laststateofplay[1]
            
        wold = laststateofplay[2]
            
        return xold, yold, wold

class CricketGUI(Frame):
    """GUI to enter the info for the cricket class"""
    def __init__(self, master):
        """Initilianumofoverse Frame."""
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def update_text(self):
        #get number of overs
        number_of_overs = self.numberovers.get()
        



    def create_widgets(self):
        #create runs label
        self.runs_lbl = Label(self, text = "Enter the number of runs")
        self.runs_lbl.grid(row = 0, column = 0, columnspan = 2, sticky = W)
        #create overs label
        self.overs_lbl = Label(self, text = "Enter the number of overs")
        self.overs_lbl.grid(row = 1, column = 0, columnspan = 2, sticky = W)
        #create wickets label
        self.wickets_lbl = Label(self, text = "Enter the number of wickets")
        self.wickets_lbl.grid(row = 2, column = 0, columnspan = 2, sticky = W)
        #create results label
        self.result_lbl = Label(self, text = "The result is")
        self.result_lbl.grid(row = 7, column = 0, columnspan = 2, sticky = W)
        #create entry to put in number of runs
        self.runs_ent = Entry(self)
        self.runs_ent.grid(row=0, column = 1, columnspan = 2, sticky = W)
        #create entry to put in number of overs
        self.overs_ent = Entry(self)
        self.overs_ent.grid(row=1, column = 1, columnspan = 2, sticky = W)    
        #create entry to put in number of wickets
        self.wickets_ent = Entry(self)
        self.wickets_ent.grid(row=2, column = 1, columnspan = 2, sticky = W)    
        #create checkbutton to see if he they have done it before for this game
        self.yes_no = BooleanVar()
        Checkbutton(self, text ="Have you used this before  for this game, click if yes otherwise leave blank",
                    variable = self.yes_no).grid(row = 4, column = 0, sticky = W)
        #need to create a submit button
        Button(self, text = "Click for result", command = self.cricket_getinfo).grid(row = 6, column = 0, columnspan = 4)
        #show results        
        self.results_txt = Text(self, width = 50, height = 10, wrap = WORD)
        self.results_txt.grid(row = 10, column = 0, columnspan = 4)
        results = 'This is a program that will predict the score of a limited overs inning, put in the number of overs, number of runs, wickets and the number of the overs in the innings and if you wish to get the Duckworth Lewis score whether they are batting first or second.'
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0,results)
        
        #code to enter the number of wickets
        self.numberovers = StringVar()
        #Radio buttons to enter the number of overs
        Radiobutton(self, text="50 overs", variable = self.numberovers, value = '50',
                    command = self.update_text).grid(row=6, column = 0, sticky = W)
        Radiobutton(self, text="20 overs", variable = self.numberovers, value = '20',
                    command = self.update_text).grid(row=6, column = 1, sticky = W)
        Radiobutton(self, text="Other enter below", variable = self.numberovers, value = 'X',
                    command = self.update_text).grid(row=6, column = 2, sticky = W)
        self.numberoversentered = Entry(self)
        self.numberoversentered.grid(row=7, column = 2, columnspan = 2, sticky = W)  
        #code to see if
        self.battingfirst = StringVar()
        Radiobutton(self, text="Batting first", variable = self.battingfirst, value = 'Y',
                    command = self.update_text).grid(row=7, column = 0, sticky = W)
        Radiobutton(self, text="Batting second", variable = self.battingfirst, value = 'N',
                    command = self.update_text).grid(row=7, column = 1, sticky = W)
        

    def cricket_getinfo(self):
        """Get values from the GUI and submit for calculation"""
        print "test"
        runs = self.runs_ent.get()
        wickets = self.wickets_ent.get()
        overs = self.overs_ent.get()
        if self.yes_no.get():
            used_before = 'Y'
        else:
            used_before = 'N'
        #self.yes_no = 'N'
        
        #need to create code to call the calculations
        #numofovers = 50
        numovers = self.numberovers.get()
        if numovers == 'X':
            numovers = self.numberoversentered.get()
        #see if the team is batting first or second,  this is not compulsory as it only matters for Duckworth Lewis calculations
        battingfirst = self.battingfirst.get()
        if battingfirst == '':
            battingfirst = 'Not entered'
        win = 10
        win = int(win)
        #the line below calculates the result if the user has put all the correct
        #info in
        #obviously you can not have played more overs than then number of overs in a game
        try:
            wickets = int(wickets)
            overs = int(overs)
            numovers = int(numovers)
            if numovers < overs:
                results = "You entered the wrong number of overs"
            elif wickets > 9:
                results = "You entered the wrong number of wickets"
            else:
                results = self.getresults(wickets,overs,runs,numovers, win, used_before, battingfirst)
        except:
        #this ensures that if bad info has been entered the user gets a message to improve it
            results = self.badentry(wickets,overs, runs, numovers)
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0,results)

    def badentry(self, wickets,overs, runs, numovers):
        result = 'You entered the information incorrectly  :- '
        try:
            wickets = float(wickets)
        except (ValueError):
            result = result + '\n' +' Please enter wickets as a number'
        except:
            result = result + '\n' +' Please check what you entered for wickets'
        try:
            overs = float(overs)
        except (ValueError):
            result = result + '\n' +' Please enter overs as a number'
        except:
            result = result + '\n' +' Please check what you entered for overs'
        try:
            retval = float(runs)
        except (ValueError):
            result = result + '\n' +' Please enter runs as a number'
        except:
            result = result + '\n' +' Please check what you entered for runs'
        try:
            retval = float(numovers)
        except:
            result = result + '\n' + 'Please enter number of overs'
        return result


    def getresults(self,wickets,overs,runs,numofovers, win, used_before, battingfirst):
        #code to get the actual info if everything goes well
        Cricketobj = Cricket(wickets,overs,runs,numofovers, win)
  #      if used_before == 'N':
        win = 10
        #originalscore = 0
        #wold = 0
        #yold = 0
        #orignovoers = 0
        results = Cricketobj.usedbefore(wickets, overs, runs,numofovers, win,used_before, battingfirst)
        return results
#main 
import cPickle, shelve
import math
from Tkinter import *
root = Tk()
root.title("Cricket Results")
app = CricketGUI(root)
root.mainloop()
