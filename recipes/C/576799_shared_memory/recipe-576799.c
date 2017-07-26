  /* 共享内存记录pid列表, 组有读写执行的权利. 子进程只能读共享内存，确定其在列表中的位置  */
    pros_shm = shmget(IPC_PRIVATE, pros_num * sizeof(pid_t), IPC_CREAT | S_IRWXU | S_IRWXG);
    if( -1 == pros_shm){
        printf("unable to create shared memory %s\n", strerror(errno));
        return -1;
    }


   /* 挂载共享内存 */
   pros_mem = shmat(pros_shm, NULL, SHM_RND);
   if(-1 == (int)pros_mem ){
       printf("unable to attach shared memory at the parent process %s\n", strerror(errno));
       return -1;
   }
