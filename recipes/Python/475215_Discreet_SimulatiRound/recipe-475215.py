from os.path import basename    # returns filename of path
from sys import argv            # is arguments passed to program
from time import strftime       # returns time according to format

################################################################################

# logs the simulator's work in a file
class logger:

    # constructor
    def __init__(self, format=None, filename=None):
        try:
            assert 0 <= format <= 16                            # make sure that "titles" are not longer than 16
            self.__format = format                              # save the formatting size
            self.__log = file(filename, 'a')                    # attempt to open a file to add to
            self.__log.write(strftime('[%m/%d/%y %H:%M:%S]\n')) # write the start time of the logging
            self.__logging = True                               # logging object will actually work
        except:
            self.__logging = False                              # logging object will be dumb

    # destructor
    def __del__(self):
        if self.__logging:
            self.__log.write('\n')
            self.__log.close()

    # logs the strings to a file
    def log(self, *strings):
        if self.__logging:
            assert strings
            if self.__format:
                assert len(strings[0]) == self.__format
                prefix = '[' + strings[0] + '] '
            else:
                prefix = ''
            for index in range(int(bool(self.__format)), len(strings)):
                self.__log.write(prefix + strings[index] + '\n')
                
################################################################################

# simulates round robin scheduling
class simulator:

    # constructor
    def __init__(self, overhead, quanta, data, log):
        self.__injector = injector(data)    # create/setup an injector object
        self.__overhead = overhead          # save the overhead variable
        self.__quanta = quanta              # save the quanta variable
        self.__log = log                    # save the logger object
        self.__time = 0.0                   # this is the start time of the simulation (float)
        self.__robin = round_robin()        # create an empty round_robin object
        self.__heaven = []                  # this is where dead processes go

    # runs the simulation
    def run(self):
        while self.__injector or self.__robin:
            self.__schedule('scheduler started running at %s' % self.__time)
            self.__run_scheduler()
            self.__process('process started running at %s' % self.__time)
            self.__run_process()

    # returns the processes that went to heaven
    def results(self):
        return tuple(self.__heaven)

    # returns how much time has gone by
    def time(self):
        return self.__time

    # logs event under [SCHE]
    def __schedule(self, note):
        self.__log.log('SCHE', note)

    # logs event under [PROC]
    def __process(self, note):
        self.__log.log('PROC', note)

    # logs event under [BLOC]
    def __blocked(self, note):
        self.__log.log('BLOC', note)

    # logs event under [TERM]
    def __terminate(self, note):
        self.__log.log('TERM', note)

    # runs the duties of the scheduler
    def __run_scheduler(self):
        # take care of the scheduler's overhead first
        self.__time += self.__overhead
        # add new processes to the round robin
        self.__robin.inject(self.__injector.inject(self.__time))
        # if there is nothing in the robin, the scheduler blocks
        if not self.__robin:
            # find out when the next process arrives
            next_time = self.__injector.next()
            # log the blocking event
            self.__blocked('scheduler blocked for %s extra second(s)' % (next_time - self.__time))
            # update current time (for injection) and inject new process
            self.__time = next_time
            self.__robin.inject(self.__injector.inject(self.__time))

    # runs the duties (and cleanup) of a process
    def __run_process(self):
        # get the next process to run
        process = self.__robin.next_process()
        # run the process and update elapsed time
        time = process.run(self.__time, self.__quanta)
        self.__time += time
        # if the process just terminated, we aren't done yet
        if process.done():
            # update the simulator's log file
            self.__terminate('process ended after %s second(s)' % time)
            # remove the process from the robin
            self.__robin.remove_process()
            # send the process to heaven
            self.__heaven.append(process)
            

################################################################################

# delays the injection of processes
class injector:

    # constructor
    def __init__(self, schedule):
        self.__queue = [process(created, work) for created, work in schedule]   # create a queue of processes
        self.__queue.sort(None, process.created, True)                          # sort the processes according to creation time

    # returns the length (total contents) of the injector
    def __len__(self):
        return len(self.__queue)

    # returns processes coming before or at time
    def inject(self, time):
        threads = []
        while self.__queue:
            if self.__queue[-1].created() <= time:
                threads.append(self.__queue[-1])
                del self.__queue[-1]
            else:
                break
        return threads

    # returns when the next process will be injected
    def next(self):
        if len(self):
            return self.__queue[-1].created()

################################################################################

# abstracts the round robin concept
class round_robin:

    # constructor
    def __init__(self):
        self.__pointer = -1 # this points to the current process
        self.__ring = []    # this is the (round) robin

    # returns number of processes on the robin
    def __len__(self):
        return len(self.__ring)

    # injects new processes onto the robin
    def inject(self, process_list):
        self.__ring = self.__ring[:self.__pointer+1] + process_list + self.__ring[self.__pointer+1:]

    # returns the next process
    def next_process(self):
        self.__pointer = (self.__pointer + 1) % len(self)
        return self.__ring[self.__pointer]

    # removes the current process from the robin
    def remove_process(self):
        del self.__ring[self.__pointer]
        self.__pointer -= 1

################################################################################

# represents a process in the simulator
class process:

    # constructor
    def __init__(self, created, work):
        self.__created = created    # when does this process come into existence?
        self.__work = work          # how much work (time) will the process be doing?
        self.__started = False      # has this process started running yet?
        self.__start = None         # when did this process actually start to run?
        self.__end = None           # when did this process "die?"

    # allows processes to be printed out in a certain format
    def __repr__(self):
        return 'Process %s:\n  Created = %s\n  Started = %s\n  Finished = %s' % (id(self), self.__created, self.__start, self.__end)

    # returns when the processes will come into existence
    def created(self):
        return self.__created

    # runs up to quanta, updates internals, and returns time ran
    def run(self, time, quanta):
        if not self.__started:
            self.__started = True
            self.__start = time
        if quanta < self.__work:
            self.__work -= quanta
            return quanta
        else:
            self.__end = time + self.__work
            real_quanta = self.__work
            self.__work = 0
            return real_quanta

    # returns whether or not the process has finished its work
    def done(self):
        return not bool(self.__work)

    # returns the wait time of the process
    def wait_time(self):
        assert self.__started
        return self.__start - self.__created

    # returns the turnaround time of the process
    def turnaround_time(self):
        assert self.__work == 0
        return self.__end - self.__start

################################################################################

# show the general outline of the program
def main():
    # parse available data
    overhead = parse_overhead()
    quanta = parse_quanta()
    data = parse_data()
    log = parse_log()
    # run and evaluate simulation
    sim = simulator(overhead, quanta, data, log)
    sim.run()
    results = sim.results()
    wait_times = [process.wait_time() for process in results]
    turnaround_times = [process.turnaround_time() for process in results]
    # print the results
    print '-------------------------'
    print 'Overhead                =', overhead
    print 'Quanta                  =', quanta
    print '-------------------------'
    print 'Average Wait Time       =', sum(wait_times) / len(wait_times)
    print 'Average Turnaround Time =', sum(turnaround_times) / len(turnaround_times)
    print '-------------------------'
    print 'Total Simulation Time   =', sim.time()
    print '-------------------------'

# parse overhead for the scheduler
def parse_overhead():
    try:
        return abs(float(argv[1])) / 1000
    except Exception, error:
        end('Overhead', error)

# parse the quanta for the processes
def parse_quanta():
    try:
        return abs(float(argv[2])) / 1000
    except Exception, error:
        end('Quanta', error)

# parse the data into a useful format
def parse_data():
    try:
        data = [line.split() for line in file(argv[3], 'rU').read().split('\n')]
        for index, item in enumerate(data):
            assert len(item) == 2
            data[index] = abs(int(item[0])), abs(float(item[1]))
        return tuple(data)
    except Exception, error:
        end('Data file', error)

# create a logger object for the simulator
def parse_log():
    try:
        return logger(4, argv[4])
    except:
        return logger()

# something broke; give the user a report
def end(note, tech):
    print 'HELP:', basename(argv[0]),
    print '<overhead> <quanta> <data_file> [<log_file>]'
    print 'NOTE:', note, 'cannot be parsed.'
    print 'TECH:', tech
    raise SystemExit(1)

################################################################################

# Is this the main Python module?
if __name__ == '__main__':
    main()
