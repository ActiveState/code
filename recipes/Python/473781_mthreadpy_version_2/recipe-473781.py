# #include <windows.h>
import thread
# #include <math.h>
import math
# #include <stdio.h>
import sys
# #include <stdlib.h>
import time

# static int runFlag = TRUE;
runFlag = True

# void main(int argc, char *argv[]) {
def main(argc, argv):
    global runFlag
    # unsigned int runTime
    # PYTHON: NO CODE

    # SYSTEMTIME now;
    # PYTHON: NO CODE
    # WORD stopTimeMinute, stopTimeSecond;
    # PYTHON: NO CODE

    # // Get command line argument, N
    try:
        N = abs(int(argv[1]))
    except:
        sys.exit(1)
    # // Get the time the threads should run, runtime
    try:
        runTime = abs(int(argv[2]))
    except:
        sys.exit(1)
    # // Calculate time to halt (learn better ways to do this later)
    # GetSystemTime(&now);
    now = time.localtime()
    # printf("mthread: Suite starting at system time
    #   %d:%d:%d\n", now.wHour, now.wMinute, now.wSecond);
    sys.stdout.write('mthread: Suite starting at system time %d:%d:%d\n' \
          % (now.tm_hour, now.tm_min, now.tm_sec))
    # stopTimeSecond = (now.wSecond + (WORD) runTime) % 60;
    stopTimeSecond = (now.tm_sec + runTime) % 60
    # stopTimeMinute = now.wMinute + (now.wSecond +
    #   (WORD) runTime) / 60;
    stopTimeMinute = now.tm_min + (now.tm_sec + runTime) / 60

    # // For 1 to N
    # for (i = 0; i < N; i++) {
    for i in range(N):
        # // Create a new thread to execute simulated word
        thread.start_new_thread(threadWork, ())
        # Sleep(100);               // Let newly created thread run
        time.sleep(0.1)
    # }
    # PYTHON: NO CODE

    # // Cycle while children work ...
    # while (runFlag) {
    while runFlag:
        # GetSystemTime(&now);
        now = time.localtime()
        # if ((now.wMinute >= stopTimeMinute)
        #     &&
        #     (now.wSecond >= stopTimeSecond)
        #    )
        if now.tm_min >= stopTimeMinute \
           and now.tm_sec >= stopTimeSecond:
            # runFlag = FALSE;
            runFlag = False
        # Sleep(1000);
        time.sleep(1)
    # }
    # PYTHON: NO CODE
    # Sleep(5000);
    time.sleep(5)
# }
# PYTHON: NO CODE

# // The code executed by each worker thread (simulated work)
# DWORD WINAPI threadWork(LPVOID threadNo) {
def threadWork():
    threadNo = thread.get_ident()
    # // Local variables
    # double y;
    # PYTHON: NO CODE
    # const double x = 3.14159;
    x = 3.14159
    # const double e = 2.7183;
    e = 2.7183
    # int i;
    # PYTHON: NO CODE
    # const int napTime = 1000;             // in milliseconds
    napTime = 1000
    # const int busyTime = 40000;
    busyTime = 40000
    # DWORD result = 0;
    result = 0

    # // Create load
    # while (runFlag) {
    while runFlag:
        # // Parameterized processor burst phase
        # for (i = 0; i < busyTime; i++)
        for i in range(busyTime):
            # y = pow(x, e);
            y = math.pow(x, e)
        # // Parameterized sleep phase
        # Sleep(napTime);
        time.sleep(napTime / 1000.0)
        # // Write message to stdout
        sys.stdout.write('Thread %s just woke up.\n' % threadNo)
    # }
    # PYTHON: NO CODE
    # // Terminating
    # return result;
    return result
# }
# PYTHON: NO CODE

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
