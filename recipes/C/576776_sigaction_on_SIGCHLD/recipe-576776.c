  /* 设定信号处理函数 */
   act.sa_handler = NULL;
   act.sa_sigaction = child_handler;
   sigemptyset(&act.sa_mask);
   act.sa_flags = SA_SIGINFO;
   //sigaction(SIGCHLD, &act, NULL);



/**
  *@brief 接受退出信号而后创建新的进程
  *
  */
static void child_handler(int sig, siginfo_t *si, void *data)
{
   int i;
   pid_t *ptr;

   //也许是processing进程
   ptr = (pid_t *)pros_mem;
   for( i = 0; i< pros_num; i++){
       ptr += i;

       if(*ptr == si->si_pid){
           printf("processing process created\n");
           creat_processes((char *)ptr, 1, processing);
           return;
       }
   }

   //也许是caching进程
   ptr = (pid_t *)cach_mem;
   for( i = 0; i< cach_num; i++){
       ptr += i;

       if(*ptr == si->si_pid){
           printf("caching process created\n");
           creat_processes((char *)ptr, 1, caching);
           return;
       }
   }
}
