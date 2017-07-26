import sys

class progressBar:
    def __init__(self, minValue = 0, maxValue = 100, totalWidth=75):
        """ Initializes the progress bar. """
        self.progBar = ""   # This holds the progress bar string
        self.oldprogBar = ""
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done 
        self.updateAmount(0)  # Build progress bar string

    def appendAmount(self, append):
        """ Increases the current amount of the value of append and 
        updates the progress bar to new ammount. """
        self.updateAmount(self.amount + append)
    
    def updatePercentage(self, newPercentage):
		""" Updates the progress bar to the new percentage. """
		self.updateAmount((newPercentage * float(self.max)) / 100.0)

    def updateAmount(self, newAmount = 0):
        """ Update the progress bar with the new amount (with min and max
        values set at initialization; if it is over or under, it takes the
        min or max value as a default. """
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = int(round(percentDone))

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # Build a progress bar with an arrow of equal signs; special cases for
        # empty and full
        if numHashes == 0:
            self.progBar = "[>%s]" % (' '*(allFull-1))
        elif numHashes == allFull:
            self.progBar = "[%s]" % ('='*allFull)
        else:
            self.progBar = "[%s>%s]" % ('='*(numHashes-1), ' '*(allFull-numHashes))

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = ' '.join([self.progBar, percentString])
    
    def draw(self):
        """ Draws the progress bar if it has changed from it's previous value.  """
        if self.progBar != self.oldprogBar:
            self.oldprogBar = self.progBar
            sys.stdout.write(self.progBar + '\r')
            sys.stdout.flush()      # force updating of screen

    def __str__(self):
        """ Returns the current progress bar. """
        return str(self.progBar)
