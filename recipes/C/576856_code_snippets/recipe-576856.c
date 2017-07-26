void log_tm(struct tm cur_time){
    printf("year: %d\n",cur_time.tm_year);
    printf("mon: %d\n", cur_time.tm_mon);
    printf("m-day: %d\n", cur_time.tm_mday);
    printf("w-day: %d\n", cur_time.tm_wday);
    printf("y-day: %d\n", cur_time.tm_yday);
    printf("hour: %d\n", cur_time.tm_hour);
    printf("min: %d\n", cur_time.tm_min);
    printf("sec: %d\n", cur_time.tm_sec);
}


{
        char cwd[1024] = {0};
        getcwd(cwd, 1023);
        printf("current dir %s\n", cwd);
}




#define E(c) do{\
    int loop_count = 0;\
    char loop_buf[40] = {0};\
    for(;loop_count < 39; loop_count++){\
        loop_buf[loop_count] = c;\
    }\
   printf("%s\n",loop_buf);\
}while(0)
