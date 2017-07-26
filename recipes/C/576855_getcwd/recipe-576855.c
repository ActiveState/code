 {
        char cwd[1024] = {0};
        getcwd(cwd, 1023);
        printf("current dir %s\n", cwd);
    }
