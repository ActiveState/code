import random

# Version 1.1 - Extended reporting. Donald 'Paddy' McCarthy 2004-04-25


def rand_jobs(jobs = 10001,             # number of jobs in a regression
          jobtime_spread = [90, 1,9],   # 90% take 1..4 mins, 1% take 4..20 mins
          jobtime_split = [5,21,41]):   # and 9% take 20..40 mins to complete
    'randomly generate jobs to a profile'
    assert sum(jobtime_spread)==100
    shortjobs = [ random.randrange(1,jobtime_split[0])
                  for x in xrange(jobs*jobtime_spread[0]/100)]
    mediumjobs = [ random.randrange(jobtime_split[0],jobtime_split[1])
                   for x in xrange(jobs*jobtime_spread[1]/100)]
    longjobs = [ random.randrange(jobtime_split[1],jobtime_split[2])
                 for x in xrange(jobs*jobtime_spread[2]/100)]
    return shortjobs + mediumjobs + longjobs

def sort_and_sow(job, bins):
    ''' sorts the jobs by time then put them in bin[0..bins-1] in the order bin[o..bins..0..bins..]'''
    job.sort()
    bin = list()
    for i in range(bins):
	bin.append(job[i::2*bins] + job[2*bins-1-i::2*bins])
	bin[-1].sort()  # Sort makes more tests finish early
    return bin
def rev_sort_and_sow(job, bins):
    ''' reverse sorts the jobs by time then put them in bin[0..bins-1] in the order bin[o..bins..0..bins..]'''
    job.sort()
    job.reverse()
    bin = list()
    for i in range(bins):
	bin.append(job[i::2*bins] + job[2*bins-1-i::2*bins])
	bin[-1].sort(); bin[-1].reverse() 
    return bin
def sort_and_place(job, bins):
    ''' sorts the jobs by time then put them in bin[0..bins-1] in the order bin[o..bins,0..bins,...]'''
    job.sort()
    bin = list()
    for i in range(bins):
	bin.append(job[i::bins])
    return bin
def rev_sort_and_place(job, bins):
    ''' reverse sorts the jobs by time then put them in bin[0..bins-1] in the order bin[o..bins,0..bins,...]'''
    job.sort()
    job.reverse()
    bin = list()
    for i in range(bins):
	bin.append(job[i::bins])
    return bin
def rand_binning_avg_count(job, bins):
    'fill bins randomly, but with averaged items in a bin'
    random.shuffle(job)
    return [job[i::bins] for i in range(bins)]
def pure_rand(job, bins):
    'fill bins randomly'
    bin = [list() for i in range(bins)]
    random.shuffle(job)
    for j in job:
        bin[random.randrange(bins)] += [j]
    return bin

def binning_stats(binning, filler='', pr=False):
    'Prints stats on the how the bins are filled'
    bin_times = [sum(bin) for bin in binning]
    target_time = sum(bin_times)/1.0/len(bin_times)
    regression_time = max(bin_times)
    closeness = test_completion_stats(binning, target_time)
    if pr: print "%-25s [50, 75, 87.5, 100]%% of tests finish after %s%% of Target time: %7.3f" % (filler,
            ["%5.1f" % c for c in closeness], target_time )
    return closeness

def time_accumulator(t):
    ' Do "time_accumulator.t = 0" before use'
    time_accumulator.t += t
    return time_accumulator.t

def test_completion_stats(binning, target_time):
    'How long for 50,75,87.5, and 100% of tests to complete (as a percentage of target_time'
    # change run times to times of completion for each bin
    completion_bins = list()
    for bin in binning:
        time_accumulator.t = 0.0
        completion_bins.append(
            [time_accumulator(duration) for duration in bin]
            )
    #merge completion times for each bin
    completion_times = sum(completion_bins,[])
    completion_times.sort()
    #find the times for tests to complete
    end_time = completion_times[-1] # last element
    num_tests = len(completion_times)
    num50 = num_tests*50/100-1
    num75 = num_tests*75/100-1
    num87 = num_tests*875/1000-1 # 87.5%
    time_to_50 = time_to_75 = time_to_87 = time_to_100 = 0
    for n,ct in enumerate(completion_times):
        if n==num50:
            #found when 50% tests finished
            time_to_50 = ct
        if n==num75:
            #found when 75% tests finished
            time_to_75 = ct
        if n==num87:
            #found when 87.5% tests finished
            time_to_87 = ct
            break
    time_to_100 = end_time
            
    return [time_to_50*1.0/target_time*100, time_to_75*1.0/target_time*100,
            time_to_87*1.0/target_time*100, time_to_100*1.0/target_time*100]
            
def hm(mins):
    ' convert minutes to hours+minutes as string'
    return '%02i:%5.2f' % (int(mins / 60), mins-60*int(mins / 60))



if __name__ == "__main__":
    repititions = 100           # Number of regressions to run
    job_slots = 99              # number of LSF jobs I can run
    tests = 10001               # Number of tests in a regression
    jobtime_spread = [90, 9,1]  # y[0]% in first range below, ...y[2]% in third
    jobtime_split = [4,16,61]   # 1 to x[0]-1, x[0] to x[1]-1, x[1] to x[2]-1 
    pr = False                  # Print as we go?
    '''
    repititions = 1           # Number of regressions to run
    job_slots = 2              # number of LSF jobs I can run
    tests = 20               # Number of tests in a regression
    jobtime_spread = [90, 9,1]  # y[0]% in first range below, ...y[2]% in third
    jobtime_split = [4,16,61]   # 1 to x[0]-1, x[0] to x[1]-1, x[1] to x[2]-1 
    pr = True                   # Print as we go?
    '''

    algorithms = [(sort_and_sow,"sort_and_sow"),
                    (rev_sort_and_sow,"rev_sort_and_sow"),
                    (sort_and_place,"sort_and_place"),
                    (rev_sort_and_place,"rev_sort_and_place"),
                    (rand_binning_avg_count,'rand_binning_avg_count'),
                    (pure_rand,'pure_rand'),
                    ]
    closeness = dict()      # for cumulative stats
    last_bin  = dict()      # debug copy of last bins
    mean_target_time = 0.0  # Calculates theoretical minimum time for avg Regression
    #
    for x in xrange(repititions):
        jobs = rand_jobs(jobtime_spread=jobtime_spread,
                         jobtime_split = jobtime_split,
                         jobs=tests)
        mean_target_time += sum(jobs)*1.0/job_slots
        for algo, algo_name in algorithms:
            binning = algo(jobs[:],job_slots)
            last_bin[algo_name] = binning
            tmp = binning_stats(binning, algo_name, pr=pr)
            closeness[algo_name] = [
                sum(percent)
                 for percent in
                   zip(closeness.get(algo_name,[0,0,0,0]), tmp)
                ]
        if pr: print ''

    mean_target_time /= repititions

    print ''
    print 'Results from %i regressions each of %i tests using %i job_slots' % (repititions, tests, job_slots)
    print '  Random test times profile is:'
    print '    %-3s from %2i to %2i minutes' % (`jobtime_spread[0]`+'%',
                                                  1, jobtime_split[0]-1)
    print '    %-3s from %2i to %2i minutes' % (`jobtime_spread[1]`+'%',
                                                  jobtime_split[0], jobtime_split[1]-1)
    print '    %-3s from %2i to %2i minutes' % (`jobtime_spread[2]`+'%',
                                                    jobtime_split[1], jobtime_split[2]-1)
    print '    Target time for a Regression run is %.1f minutes (%s)\n' % (mean_target_time,
                                                                           hm(mean_target_time))
    for algo, algo_name in algorithms:
        print " %-23s [50, 75, 87.5, 100]%% tests finish in %s%% of Target time - %s" % (algo_name+':',
                                          ["%5.1f" % (c*1.0/repititions)
                                           for c in closeness[algo_name]],
                                           hm(mean_target_time*closeness[algo_name][-1]/100.0/repititions) )
