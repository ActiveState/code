#!/usr/bin/python
import os, sys, thread, time

def __concurrent_batch(cmd,thread_num,completion_status_dict,exit_code_dict):
    """Helper routine for 'concurrent_batches."""

    exit_code_dict[thread_num] = os.system(cmd)
    completion_status_dict[thread_num] = 1  # for sum() routine

def concurrent_batches(batchlist,maxjobs=0,maxtime=0):
    """Run a list of batch commands simultaneously.

    'batchlist' is a list of strings suitable for submitting under os.system().
    Each job will run in a separate thread, with the thread ending when the
    subprocess ends.
    'maxjobs' will, if greater then zero, be the maximum number of simultaneous
    jobs which can concurrently run.  This would be used to limit the number of
    processes where too many could flood a system, causing performance issues.
    'maxtime', when greater than zero, be the maximum amount of time (seconds)
    that we will wait for processes to complete.  After that, we will return,
    but no jobs will be killed.  In other words, the jobs still running will
    continue to run, and hopefully finish in the course of time.

    example: concurrent_batches(("gzip abc","gzip def","gzip xyz"))

    returns: a dictionary of exit status codes, but only when ALL jobs are
             complete, or the maximum time has been exceeded.
             Note that if returning due to exceeding time, the dictionary will
             continue to be updated by the threads as they complete.
             The key of the dictionary is the thread number, which matches the
             index of the list of batch commands.  The value is the result of
             the os.system call.

    gotcha:  If both the maxjobs and maxtime is set, there is a possibility that
             not all jobs will be submitted.  The only way to detect this will be
             by checking for the absence of the KEY in the returned dictionary.
    """

    if not batchlist: return {}
    completion_status_dict, exit_code_dict = {}, {}
    num_jobs = len(batchlist)
    start_time = time.time()
    for thread_num, cmd in enumerate(batchlist):
        exit_code_dict[thread_num] = None
        completion_status_dict[thread_num] = 0 # for sum() routine
        thread.start_new_thread(__concurrent_batch,
              (cmd,thread_num,completion_status_dict,exit_code_dict))
        while True:
            completed = sum(completion_status_dict.values())
            if num_jobs == completed:
                return exit_code_dict      # all done
            running = thread_num - completed
            if maxtime > 0:
                if time.time() - start_time > maxtime:
                    return exit_code_dict
            if not maxjobs:
                if thread_num < num_jobs-1:  # have we submitted all jobs ?
                    break                  #  no, so break to for cmd loop
                else:
                    time.sleep(.2)         #  yes, so wait until jobs are complete
                    continue
            if running < maxjobs:
                break    # for next for loop
            time.sleep(.2)


if __name__ == "__main__":
    os.chdir("/tmp")
    for f in ("abc","def","xyz","abc.gz","def.gz","xyz.gz"):
        try:
            os.unlink(f)
        except:
            pass
    open("abc","w").write(str(globals()))
    open("def","w").write(str(globals()))
    open("xyz","w").write(str(globals()))
    batches = ("gzip abc","gzip def","gzip xyz","sleep 5","gzip mustfail")
    ret = concurrent_batches(batches,maxtime=3)
    try:
        os.unlink("abc.gz")
        os.unlink("def.gz")
        os.unlink("xyz.gz")
    except:
        print "Failed to delete compressed files, hence they were"
        print "not created, hence the concurrent routine has failed."
        sys.exit(1)
    print ret      # prints {0: 0, 1: 0, 2: 0, 3: None, 4: 256}
    time.sleep(6)
    print ret      # prints {0: 0, 1: 0, 2: 0, 3: 0, 4: 256}
    sys.exit(0)
