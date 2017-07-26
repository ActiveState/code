/**
 *@brief 判断一个进程还存不存在
 *
 */
int process_exist(pid_t pid){
    char buf[32] = {0};
    struct stat file_info;

    sprintf(buf, "/proc/%d",pid);

    errno = 0;
    if(-1 == stat(buf, &file_info) ){
        printf("\t\t\t %s : %s", buf, strerror(errno));
        return 0;
    }
    else{
        return 1;
    }
}
