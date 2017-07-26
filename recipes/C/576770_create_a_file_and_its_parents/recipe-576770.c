int create_file(char *fullpath, mode_t mode){
    struct stat stat_buf;
    int i = 1;
    int fd = -1;

    while( '\0' != fullpath[i] ){

        if('/' == fullpath[i] ){
            fullpath[i] = '\0';
            errno = 0;
            if( -1 == (stat(fullpath, &stat_buf) ) && ENOENT == errno    ){
                if(-1 == mkdir(fullpath, mode)){
                    perror("");
                }
            }
            fullpath[i] = '/';
        }
        i++;
    }

    errno = 0;
    if(-1 == (fd = creat(fullpath, mode)) ){
        printf("create file error %s : %s\n", fullpath, strerror(errno));
        return -1;
    }
    else{
        close(fd);
    }

    return 0;
}
