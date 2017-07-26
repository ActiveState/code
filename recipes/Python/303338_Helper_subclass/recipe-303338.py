"""Helper code for win32pdhquery.

For clarification of discussion, a "tick" is a measurement taken after a pre-
defined amount of elapsed time.

Data is stored in the following format::

    {kind name :
        {instance name :
            {counter name : tick measurements}}}

If a counter does not have an applicable instance (such as memory counters),
the instance name is set to 'N/A'.

Typical usage is::

>>> query = QueryHelper(.1) # How often to measure, in seconds
>>> query.addcounter("Processor", "_Total", "% Processor Time")
>>> query.addcounter("Memory", None, "Page Faults/sec")
>>> query.start()
>>> query.stop()

Print the instance for a human-readable format.  Use csvoutput or csvsave for
CSV output.  Access to the results dict can be reached using 'results'. Use
picklesave to pickle the results dict.  The repr of the query can be used to see
what counters were used.

"""
from win32pdhquery import Query, QueryError
from itertools import izip, chain
from cStringIO import StringIO
from time import sleep
from datetime import datetime
import csv
import pickle

def interfacename(kind, inst):
    """Return first half of the name of a counter properly formatted"""
    if inst:
        return "%s(%s)" % (kind, inst)
    else:
        return kind

class QueryHelper(Query):
    """Subclass of win32pdhquery.Query with a cleaner interface and some helper methods"""

    def __init__(self, tick_freq):
        """Initialize instance while storing frequency of measurement ticks"""
        self.tick_freq = tick_freq
        self._counters = {}
        Query.__init__(self)

    def addcounter(self, kind, inst, counter):
        """Add a counter for 'inst' of 'type' obj (using PDH terminology).

        Arguments:

        - kind
            type of object for the counter to work on (Process, Network Interface,
            etc.)
        - inst
            instance of 'type' (IEXPLORE, etc.; set to None if not applicable)
        - counter
            counter name

        """
        interface_name = interfacename(kind, inst)
        self.rawaddcounter(interface_name, counter)
        kind_dict = self._counters.setdefault(kind, {})
        inst_dict = kind_dict.setdefault(inst, {})
        
    def start(self):
        """Start the counter with measurements at the frequency specified at
        instance creation"""
        self.starttime = datetime.utcnow()
        self.collectdatawhile(self.tick_freq)

    def stop(self):
        """Stop collecting data"""
        self.collectdatawhile_stop()
        # Need to make sure to wait long enough for any nagging measurement to
        # finish
        if self.tick_freq < 1:
            sleep(1)
        else:
            sleep(2 * self.tick_freq)
        self._parsedata()

    def _parsedata(self):
        """Take the measurement data and store it into self._results in the
        documented format"""
        results_dict = {}
        index_mapping = []
        for index, interface_and_counter in enumerate(self.curpaths):
            # Skip first split value since always an empty string
            interface,counter = interface_and_counter.split('\\')[1:]
            try:
                paren = interface.index('(')
            except ValueError:
                paren = len(interface)
            kind = interface[:paren]
            inst = interface[paren+1:-1]
            # Not having a specific instance (memory measurements, for instance)
            # leads to 'N/A' being used as the name
            if not inst:
                inst = 'N/A'
            index_mapping.append((kind, inst, counter))
            kind_dict = results_dict.setdefault(kind, {})
            inst_dict = kind_dict.setdefault(inst, {})
            inst_dict.setdefault(counter, [])
        # If the counter was stopped too quickly it may not have gotten
        # any values; just stick in empty values
        if not hasattr(self, "curresults"):
            for kind_dict in results_dict.itervalues():
                for inst_dict in kind_dict.itervalues():
                    for counter in inst:
                        inst_dict[counter] = ([], 0)
        else:
            for dataset in self.curresults:
                for index,data in enumerate(dataset):
                    kind,inst,counter = index_mapping[index]
                    results_dict[kind][inst][counter].append(data)
            for kind in results_dict.iterkeys():
                for inst in results_dict[kind].iterkeys():
                    for counter in results_dict[kind][inst].iterkeys():
                        ticks = results_dict[kind][inst][counter]
                        results_dict[kind][inst][counter] = ticks
        self._results = results_dict

    def instticks(self, kind, inst):
        """Return a two-item tuple; first item contains counter names,
        second contains a sequence of sequences containing values per tick"""
        counter_names = self._results[kind][inst].keys()
        ticks = izip(*[self._results[kind][inst][counter_name]
                       for counter_name in counter_names])
        return (counter_names, ticks)

    def results(self):
        """Return the results dict"""
        return self._results

    def __repr__(self):
        """Return the counter paths"""
        return str(self.paths)

    def __str__(self):
        """If counter is finished, print out results, else print out the counter
        paths"""
        if not hasattr(self, "_results"):
            return self.__repr__()
        else:
            str_file = StringIO()
            try:
                for kind_key, inst_dict in self._results.iteritems():
                    print>>str_file, kind_key
                    for inst_key in inst_dict.iterkeys():
                        print>>str_file, "\t%s" % inst_key
                        counters,ticks = self.instticks(kind_key, inst_key)
                        print>>str_file, "\t",
                        for counter in counters:
                            print>>str_file, "    %s" % counter,
                        else:
                            print>>str_file, "\n"
                        for tick in ticks:
                            print>>str_file, "\t",
                            for index,data in enumerate(tick):
                                print>>str_file, str(data).rjust(len(counters[index])+4),
                            else:
                                print>>str_file, "\n",
                        else:
                            print>>str_file, "\n",
                    print>>str_file, "\n",
            finally:
                results = str_file.getvalue()
                str_file.close()
                return results

    def csvsave(self, CSVFILE):
        """Save measurements in CSV format to the passed-in file object"""
        counter_triples = []
        for kind in self._results.iterkeys():
            for inst in self._results[kind].iterkeys():
                for counter in self._results[kind][inst].iterkeys():
                    counter_triples.append((kind, inst, counter))
        kind,inst,counter = counter_triples[0]
        tick_count = len(self._results[kind][inst][counter])
        csv_writer = csv.writer(CSVFILE)
        csv_writer.writerow(["\\%s\\%s" % (interfacename(kind,inst), counter)
                             for kind,inst,counter in counter_triples])
        for tick_index in xrange(tick_count):
            csv_writer.writerow([self._results[kind][inst][counter][tick_index]
                                 for kind,inst,counter in counter_triples])

    def csvoutput(self):
        """Output data in CSV format as a string"""
        FILE = StringIO()
        try:
            self.csvsave(FILE)
            results = FILE.getvalue()
        finally:
            FILE.close()
        return results

    def picklesave(self, PICKLEFILE):
        """Save measurements dict in a pickle file"""
        try:
            pickle.dump(self._results, PICKLEFILE, -1)
        finally:
            PICKLEFILE.close()
