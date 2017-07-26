"""
    @author   Thomas Lehmann
    @file     Learn2Calc.py
    @brief    Tools to train yourself in calculation

    Training on regularly base is something that really helps
    you to improve your calculations. Two main criteria are of
    importance: speed and accuracy.

    The basic statistic at the beginning and at the end
    allows you to monitor your training success.

    With the training parameters as provided with this script it
    took myself about one minute per session (average). You cannot
    say - I guess - that less than 5 minutes training per day is
    really much time you lose, do you?
"""
from datetime import datetime
import random
import sys
import os
import pickle

class Tools:
    """ some tool functions """
    @staticmethod
    def dateBack(theDateAndTime, precise=False, fromDate=None):
        """ provides a human readable format for a time delta.
            @param theDateAndTime this is time equal or older than now or the date in 'fromDate'
            @param precise        when true then milliseconds and microseconds are included
            @param fromDate       when None the 'now' is used otherwise a concrete date is expected
            @return the time delta as text

            @note I don't calculate months and years because those varies (28,29,30 or 31 days a month
                  and 365 or 366 days the year depending on leap years). In addition please refer
                  to the documentation for timedelta limitations.

            @see http://code.activestate.com/recipes/578113
        """
        if not fromDate:
            fromDate = datetime.now()

        if theDateAndTime > fromDate:    return None
        elif theDateAndTime == fromDate: return "now"

        delta = fromDate - theDateAndTime

        # the timedelta structure does not have all units; bigger units are converted
        # into given smaller ones (hours -> seconds, minutes -> seconds, weeks > days, ...)
        # but we need all units:
        deltaMinutes      = delta.seconds // 60
        deltaHours        = delta.seconds // 3600
        deltaMinutes     -= deltaHours * 60
        deltaWeeks        = delta.days    // 7
        deltaSeconds      = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
        deltaDays         = delta.days    - deltaWeeks * 7
        deltaMilliSeconds = delta.microseconds // 1000
        deltaMicroSeconds = delta.microseconds - deltaMilliSeconds * 1000

        valuesAndNames =[ (deltaWeeks  ,"week"  ), (deltaDays   ,"day"   ),
            (deltaHours  ,"hour"  ), (deltaMinutes,"minute"),
            (deltaSeconds,"second") ]
        if precise:
            valuesAndNames.append((deltaMilliSeconds, "millisecond"))
            valuesAndNames.append((deltaMicroSeconds, "microsecond"))

        text =""
        for value, name in valuesAndNames:
            if value > 0:
                text += len(text)   and ", " or ""
                text += "%d %s" % (value, name)
                text += (value > 1) and "s" or ""

        # replacing last occurrence of a comma by an 'and'
        if text.find(",") > 0:
            text = " and ".join(text.rsplit(", ",1))

        if not len(text):
            text = "a tick"

        return text

    @staticmethod
    def getDuration(started, finished):
        """ @return a float representing seconds """
        td = finished - started
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

class DivisionCache:
    """ provides possible integer divisions """
    divisions = {}

    @staticmethod
    def update(rangeLimit, tasksLimit):
        """ Using multiplication this mechanism tries to find
            valid integer division limited in range and
            number of tasks """
        for a in range(2, rangeLimit+1):
            for b in range(2, rangeLimit+1):
                if a == b:
                    continue

                if b % a == 0:
                    # stores tasks with two numbers
                    key = (len("%d" % b), len("%d" % a))
                    if not key in DivisionCache.divisions:
                        DivisionCache.divisions[key] = [(b, a)]
                    else:
                        DivisionCache.divisions[key].append((b, a))

                c   = a * b

                if not c == a and c % b == 0 and (c/b) % a == 0:
                    # stores tasks with three numbers
                    key = (len("%d" % c), len("%d" % b), len("%d" % a))
                    if not key in DivisionCache.divisions:
                        DivisionCache.divisions[key] = [(c, b, a)]
                    else:
                        DivisionCache.divisions[key].append((c, b, a))
        # deletes all divisions where not enough tasks can be done
        for key in list(DivisionCache.divisions.keys())[0:]:
            if len(DivisionCache.divisions[key]) < tasksLimit:
                del DivisionCache.divisions[key]

class Task(object):
    """ A task is one concrete calculation for which a user
        has to provide an answer. The task, the answer and
        the timing is stored for later evaluation. """
    def __init__(self, task):
        self.started       = None
        self.finished      = None
        self.task          = task
        self.answerByUser  = ""

    def getValidAnswer(self):
        """ @return a string of calculated correct answer """
        return str(int(eval(self.task)))

    def isValid(self):
        """ @return true, when the user has provided correct answer """
        return self.answerByUser == self.getValidAnswer()

    def getDuration(self):
        """ @return a float representing seconds """
        return Tools.getDuration(self.started, self.finished)

    def run(self):
        """ asking the user to answer for a concrete calculation """
        self.started      = datetime.now()
        self.answerByUser = input("%s = " % self.task)
        self.finished     = datetime.now()

class TrainingParameter(object):
    """ training parameter for one session """
    MODE_COUNT   = 0    # means: a certain number of tasks have to be done in a session
    MODE_TIMEOUT = 1    # means: you can do many tasks except the timeout has exceeded

    def __init__(self , digitsPerNumber=None , operation='*' , mode=MODE_COUNT , modeValue=10):
        if not digitsPerNumber: digitsPerNumber = [1 , 1]

        self.digitsPerNumber = digitsPerNumber
        self.operation       = operation
        self.mode            = mode
        self.modeValue       = modeValue

    def __hash__(self):
        """ @return identifies the "kind" of session to allow grouping of same sessions """
        return hash(str((self.operation, self.mode, self.modeValue, str(self.digitsPerNumber))))

    def __eq__(self, other):
        """ comparing two training parameter setups """
        if not self.digitsPerNumber == other.digitsPerNumber:
            return False
        if not self.operation == other.operation:
            return False
        if not self.mode == other.mode:
            return False
        if not self.modeValue == other.modeValue:
            return False
        return True

    def __repr__(self):
        return """operation: %(operation)c, digits per number: %(digitsPerNumber)s, mode: %(mode)d, modeValue: %(modeValue)d""" % self.__dict__

class Session(object):
    """ one sessions finally represents a number of tasks with all information like
        date, time, concrete tasks and the answer of the user """
    def __init__(self, trainingParameter):
        self.started           = None
        self.finished          = None
        self.trainingParameter = trainingParameter
        self.doneTasks         = []
        self.numberOfTasks     = 0

    def __iter__(self):
        """ provides iteration over tasks """
        return iter(self.doneTasks)

    def getKey(self):
        """ @return identifies the "kind" of session to allow grouping of same sessions """
        return self.trainingParameter

    def getDuration(self):
        """ @return a float representing seconds """
        return Tools.getDuration(self.started, self.finished)

    def getErrorRate(self):
        return sum([1 for task in self.doneTasks if not task.isValid()]) * 100.0 / len(self.doneTasks)

    def createNumber(self, digits):
        """ creates a random number >= 2 and with given number of digits """
        minimum = 10**(digits-1)
        if minimum == 1: minimum = 2
        return random.randrange(minimum, 10**digits - 1)

    def createTask(self):
        """ generates a new task which can be passed through the eval function """
        if self.trainingParameter.operation in ['*', '+', '-']:
            numbers = str([self.createNumber(digits) for digits in self.trainingParameter.digitsPerNumber])
            return numbers.replace(", " , " %c " % self.trainingParameter.operation)[1:-1]

        elif self.trainingParameter.operation == '/':
            key = tuple(self.trainingParameter.digitsPerNumber)
            if key in DivisionCache.divisions:
                divisions = DivisionCache.divisions[key]
                numbers   = str(divisions[random.randrange(0, len(divisions)-1)])
                return numbers.replace(", " , " %c " % self.trainingParameter.operation)[1:-1]
        # not supported
        return ""

    def run(self):
        """ generates tasks """
        exampleTask = self.createTask()
        if not len(exampleTask):
            print("Error: cannot create task for %s" % self.trainingParameter)
            return False

        print("\nNext session has the form %s = %s" % (exampleTask, int(eval(exampleTask))))

        if self.trainingParameter.mode == TrainingParameter.MODE_COUNT:
            input("Are you ready for %d tasks? (press enter)"
                  % self.trainingParameter.modeValue)
        elif self.trainingParameter.mode == TrainingParameter.MODE_TIMEOUT:
            input("Are you ready for as many tasks you can do in %s seconds? (press enter)"
                  % self.trainingParameter.modeValue)
        else:
            print("Error: not handled training parameter!")
            return False

        self.started = datetime.now()

        succeeded, failed = 0, 0
        results = []
        taskNr = 1

        while True:
            # displaying the task number before the task
            print("%2d)" % taskNr , end="   ")
            task = self.createTask()
            # ensure not to ask the same task twice
            while task in results:
                task = self.createTask()

            newTask = Task(task)
            newTask.run()

            if newTask.isValid():
                print("      ...right!")
                succeeded += 1
            else:
                print("      ...wrong, the right answer is %s" %
                      newTask.getValidAnswer())
                failed += 1

            print("      ...took %f second - %d succeeded and %d failed" %
                  (newTask.getDuration(), succeeded, failed))

            self.doneTasks.append(newTask)
            results.append(newTask.task)

            taskNr += 1

            # defined number of tasks done?
            if self.trainingParameter.mode == TrainingParameter.MODE_COUNT:
                if taskNr > self.trainingParameter.modeValue:
                    break

            # defined timeout exceeded?
            elif self.trainingParameter.mode == TrainingParameter.MODE_TIMEOUT:
                currentDuration = Tools.getDuration(self.started, datetime.now())
                if currentDuration > self.trainingParameter.modeValue:
                    break

        self.finished = datetime.now()
        self.numberOfTasks = taskNr-1
        return True

class Statistic:
    """ provides functionality to print summary and detailed statistic """
    def __init__(self, sessions):
        """ stores sessions by session key """
        self.sessionsByKey = {}

        for session in sessions:
            key = session.getKey()
            if not key in self.sessionsByKey: self.sessionsByKey[key] = [session]
            else: self.sessionsByKey[key].append(session)

    def printSummary(self):
        """ independent of type of session or task you get an overview """
        succeeded, failed = 0, 0
        taskDurations     = []
        sessionDurations  = []
        lastSession       = None

        for sessions in self.sessionsByKey.values():
            for session in sessions:
                sessionDurations.append(session.getDuration())
                for task in session:
                    taskDurations.append(task.getDuration())

                    if task.isValid():
                        succeeded += 1
                    else:
                        failed += 1

                if not lastSession:
                    lastSession = session
                elif session.finished > lastSession.finished:
                    lastSession = session

        # the first time you have no tasks yet
        if not len(taskDurations):
            return

        errorRate = failed * 100.0 / len(taskDurations)

        print("\n...last session has been %s"
              % (Tools.dateBack(lastSession.finished) + " ago"))
        print("...overall number of sessions is %d"
              % len(sessionDurations))
        print("...overall number of tasks is %d, %d succeeded, %d failed - error rate is about %.1f%%"
              % (len(taskDurations), succeeded, failed, errorRate))
        print("...best task time was %f seconds, longest task time was %f seconds"
              % (min(taskDurations), max(taskDurations)))
        print("...best session time was %f seconds, longest session time was %f seconds"
              % (min(sessionDurations), max(sessionDurations)))
        print("...average time over all kind of tasks is %f seconds"
              % (sum(taskDurations)/len(taskDurations)))
        print("...average time over all kind of sessions is %f seconds"
              % (sum(sessionDurations)/len(sessionDurations)))
        print("...overall session time %f seconds"
              % (sum(sessionDurations)))

    def printDetailedStatistic(self):
        """ prints a statistic per session key. The session key includes the
            math operation, how many numbers, the digits for the numbers
            and how many tasks; this is to have comparable sessions.
        """
        for key, sessions in self.sessionsByKey.items():
            print("\n...separate statistic for %s" % key)
            succeeded, failed = 0, 0
            taskDurations     = []
            sessionDurations  = []
            lastSession       = None

            for session in sessions:
                sessionDurations.append(session.getDuration())
                for task in session:
                    taskDurations.append(task.getDuration())

                    if task.isValid():
                        succeeded += 1
                    else:
                        failed += 1

                if not lastSession:
                    lastSession = session
                elif session.finished > lastSession.finished:
                    lastSession = session

            errorRate = failed * 100.0 / len(taskDurations)

            print("......last session has been %s"
                  % (Tools.dateBack(lastSession.finished) + " ago"))
            print("......number of sessions is %d"
                  % len(sessionDurations))
            print("......number of tasks is %d, %d succeeded, %d failed - error rate is about %.1f%%"
                  % (len(taskDurations), succeeded, failed, errorRate))
            print("......best task time was %f seconds, longest task time was %f seconds"
                  % (min(taskDurations), max(taskDurations)))
            print("......best session time was %f seconds, longest session time was %f seconds"
                  % (min(sessionDurations), max(sessionDurations)))
            print("......average time over all tasks is %f seconds"
                  % (sum(taskDurations)/len(taskDurations)))
            print("......average time over all sessions is %f seconds"
                  % (sum(sessionDurations)/len(sessionDurations)))
            print("......sessions time %f seconds"
                  % (sum(sessionDurations)))

class SessionManager:
    """ organizes load/save of sessions """
    def __init__(self):
        """ initializing to have no sessions initially """
        self.sessions = []
    def add(self, session):
        """ adding further session to be saved """
        self.sessions.append(session)
    def save(self, pathAndFileName):
        """ saving all sessions """
        pickle.dump(self.sessions, open(pathAndFileName, "wb"))
    def load(self, pathAndFileName):
        """ loading all sessions """
        if os.path.isfile(pathAndFileName):
            self.sessions = pickle.load(open(pathAndFileName, "rb"))

    def dumpStatistic(self, detailed=False):
        """ dumping some basic statistic to give you an overview
            about your training results """
        statistic = Statistic(self.sessions)
        statistic.printSummary()

        if detailed:
            statistic.printDetailedStatistic()

def main():
    """ application entry point to start your training """
    print("Learn2Calc v0.4 by Thomas Lehmann 2012")
    print("...Python %s" % sys.version.replace("\n", ""))
    sessionManager = SessionManager()
    # loading previous training results
    sessionManager.load("Learn2Calc.dat")
    sessionManager.dumpStatistic()

    # ensure at least 30 divisions per pattern (digits per number)
    # increase this if you need more but be aware that the creation
    # of the cache takes more time then!
    DivisionCache.update(250, 30)

    # here you can adjust your training parameters (each entry will finally represent one session):
    sessionParameter = [ # multiplication of three numbers (each one digit) with exact 10 tasks
                         TrainingParameter([1,1,1]  , '*', TrainingParameter.MODE_COUNT, 10),
                         # addition of four numbers (each one digit) with timeout of 1 minute
                         TrainingParameter([1,1,1,1], '+', TrainingParameter.MODE_TIMEOUT, 60),
                         # subtraction of three values (decreasing size) with exact 10 tasks
                         TrainingParameter([3,2,1]  , '-', TrainingParameter.MODE_COUNT, 10),
                         # multiplication of two numbers (decreasing size) with timeout of 1 minute
                         TrainingParameter([2,1]    , '*', TrainingParameter.MODE_TIMEOUT, 60),
                         # integer division of two numbers (decreasing size) with exact 10 tasks
                         TrainingParameter([3, 1]   , '/', TrainingParameter.MODE_COUNT, 10)
                       ]

    # creating and running sessions depending on your training parameters
    count = 0
    for parameter in sessionParameter:
        session = Session(parameter)
        if session.run():
            sessionManager.add(session)
            count += 1

    if count > 0:
        # storing current training results
        sessionManager.save("Learn2Calc.dat")
        sessionManager.dumpStatistic(True)

if __name__ == "__main__":
    main()
