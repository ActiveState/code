int openlog()
{

    int fd = open(LOG,O_RDWR | O_APPEND |O_CREAT, 0666);
    if (-1 == fd)
    {
        eyou_syslog("open eyoucron log failed : %s\n", strerror(errno));
        return -1;
    }

    if( -1 == dup2(fd, STDOUT_FILENO)){
        eyou_syslog("dup stdout failed : %s\n", strerror(errno));
        goto openerr;
    }

    if( -1 == dup2(fd, STDERR_FILENO)){
        eyou_syslog("dup stderr failed : %s\n", strerror(errno));
        goto openerr;
    }

    if( -1 == setvbuf(stdout, NULL, _IOLBF, 0)){
        eyou_syslog("set lined-buffer for log failed : %s\n", strerror(errno));
        goto openerr;
    }
    return 0;

openerr:
    return -1;
}
