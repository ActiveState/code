#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

void divert (int sig) {
    printf("signal received=%d\n",sig);
}

int main() {
    sigset_t mask, pending;

    if (signal(SIGINT, divert)== SIG_ERR) {
        perror("signal(SIGINT, divert) failed");
        exit(1);
    }
    printf("going to sleep for 5 secs, during which Ctrl-C will wake up the process\n");
    sleep(5);

    sigemptyset(&mask);
    sigaddset(&mask,SIGINT);
    if(sigprocmask(SIG_BLOCK, &mask, 0) < 0) {
        perror("sigprocmask");
        exit(1);
    }

    printf("sleeping again for 5 secs, delaying the response to Ctrl-C\n");
    sleep(5);

    if(sigpending(&pending) <0) {
        perror("sigpending");
        exit(1);
    }

    if(sigismember(&pending, SIGINT))
        printf("SIGINT pending\n");

    if(sigprocmask(SIG_UNBLOCK,&mask,0) < 0) {
        perror("sigblockmask");
        exit(1);
    }

    printf("SIGINT unblocked\n");
}

/*
going to sleep for 5 secs, during which Ctrl-C will wake up the process
signal received=2
sleeping again for 5 secs, delaying the response to Ctrl-C
SIGINT pending
signal received=2
SIGINT unblocked

*/
