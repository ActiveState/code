static int getargs(int argc, char **argv)
{
    int opt = 0;

    char *optstring = "acdh";

    opt = getopt(argc, argv, optstring);

    while (opt != -1) {
        switch (opt) {
            case 'a':
                printf("all\n");
                break;
            case 'c':
                printf("confirm\n");
                break;
            case 'd':
                printf("delete\n");
                break;
            case 'h':
                printf("help\n");
                break;
            default:
                printf("other %s\n", optstring);
                break;
        }
        opt = getopt(argc, argv, optstring);
    }

    printf("non-options\n");
    while( optind < argc ){
        printf("%s\n", argv[optind]);
        optind++;
    }
    return 0;
}
