// -*- Mode: C; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
// vim:tabstop=4:shiftwidth=4:expandtab:

/**
 * @file    dpopen.c
 *
 * Implementation of a duplex pipe stream.
 *
 * @version 1.10, 2004/08/31
 * @author  Wu Yongwei
 *
 * @ref http://www.ibm.com/developerworks/cn/linux/l-pipebid/index.html
 */

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>

#ifdef _REENTRANT
#include <pthread.h>
static pthread_mutex_t chain_mtx = PTHREAD_MUTEX_INITIALIZER;
#endif

#include "dpopen.h"

/** Struct to store duplex-pipe-specific information. */
struct dpipe_chain {
    FILE *stream;               ///< Pointer to the duplex pipe stream
    pid_t pid;                  ///< Process ID of the command
    struct dpipe_chain *next;   ///< Pointer to the next one in chain
};

/** Typedef to make the struct easier to use. */
typedef struct dpipe_chain dpipe_t;

/** Header of the chain of opened duplex pipe streams. */
static dpipe_t *chain_hdr;

/**
 * Initiates a duplex pipe stream from/to a process.
 *
 * Like \e popen, all previously #dpopen'd pipe streams will be closed
 * in the child process.
 *
 * @param command   the command to execute on \c sh
 * @return          a pointer to an open stream on successful
 *                  completion; \c NULL otherwise
 */
FILE *dpopen(const char *command)
{
    int     fd[2], parent, child;
    pid_t   pid;
    FILE    *stream;
    dpipe_t *chain;

    /* Create a duplex pipe using the BSD socketpair call */
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, fd) < 0)
        return NULL;
    parent = fd[0];
    child  = fd[1];

    /* Fork the process and check whether it is successful */
    if ( (pid = fork()) < 0) {
        close(parent);
        close(child);
        return NULL;
    }

    if (pid == 0) {                         /* child */
        /* Close the other end */
        close(parent);
        /* Duplicate to stdin and stdout */
        if (child != STDIN_FILENO)
            if (dup2(child, STDIN_FILENO) < 0) {
                close(child);
                return NULL;
            }
        if (child != STDOUT_FILENO)
            if (dup2(child, STDOUT_FILENO) < 0) {
                close(child);
                return NULL;
            }
        /* Close this end too after it is duplicated to standard I/O */
        close(child);
        /* Close all previously opened pipe streams, as popen does
----why the prviously opend pipes are closed?
----each time this func is called, a new chain_hdr is added into the global static variable, as well as a new child process and the **input stream** is forked. 

the chain is used to manage all the input streams for the parent process: the parent process is responsible for all the streams. Accturally, the parent need to close the stream(dpclose).

ONly the STDIN and STDOUT is valuable to the child proces, so we close all other streams.
         */
        for (chain = chain_hdr; chain != NULL; chain = chain->next)
            close(fileno(chain_hdr->stream));
        /* Execute the command via sh */
        execl("/bin/sh", "sh", "-c", command, NULL);
        /* Exit the child process if execl fails */
        _exit(127);
    } else {                                /* parent */
        /* Close the other end */
        close(child);
        /* Open a new stream with the file descriptor of the pipe */
        stream = fdopen(parent, "r+");
        if (stream == NULL) {
            close(parent);
            return NULL;
        }
        /* Allocate memory for the dpipe_t struct. chain is a static variable, which is allocated globally */
        chain = (dpipe_t *)malloc(sizeof(dpipe_t));
        if (chain == NULL) {
            fclose(stream);
            return NULL;
        }
        /* Store necessary info for dpclose, and adjust chain header : to the end of the chain*/
        chain->stream = stream;
        chain->pid = pid;
#ifdef _REENTRANT
        pthread_mutex_lock(&chain_mtx);
#endif
        chain->next = chain_hdr;
        chain_hdr = chain;
#ifdef _REENTRANT
        pthread_mutex_unlock(&chain_mtx);
#endif
        /* Successfully return here */
        return stream;
    }
}

/**
 * Closes a duplex pipe stream from/to a process.
 *
 * @param stream    pointer to a pipe stream returned from a previous
 *                  #dpopen call
 * @return          the exit status of the command if successful; \c -1
 *                  if an error occurs
 */
int dpclose(FILE *stream)
{
    int status;
    pid_t pid, wait_res;
    dpipe_t *cur;
    dpipe_t **ptr;

    /* Search for the stream starting from chain header */
#ifdef _REENTRANT
    pthread_mutex_lock(&chain_mtx);
#endif
    ptr = &chain_hdr;
    while ( (cur = *ptr) != NULL) {         /* Not end of chain */
        if (cur->stream == stream) {        /* Stream found */
            pid = cur->pid;
            *ptr = cur->next;
#ifdef _REENTRANT
            pthread_mutex_unlock(&chain_mtx);
#endif
            free(cur);



//the structure is freed, but the chain is not linked again??????????????????????????????/

            if (fclose(stream) != 0)
                return -1;
            do {
                wait_res = waitpid(pid, &status, 0);
            } while (wait_res == -1 && errno == EINTR);
            if (wait_res == -1)
                return -1;
            return status;
        }
        ptr = &cur->next;                   /* Check next */
    }
#ifdef _REENTRANT
    pthread_mutex_unlock(&chain_mtx);
#endif
    errno = EBADF;              /* If the given stream is not found */
    return -1;
}

/**
 * Flushes the buffer and sends \c EOF to the process at the other end
 * of the duplex pipe stream.
 *
 * @param stream    pointer to a pipe stream returned from a previous
 *                  #dpopen call
 * @return          \c 0 if successful; \c -1 if an error occurs
 */
int dphalfclose(FILE *stream)
{
    /* Ensure all data are flushed */
    if (fflush(stream) == EOF)
        return -1;
    /* Close pipe for writing */
    return shutdown(fileno(stream), SHUT_WR);
}
