int main(int argc, char **argv)
{

    char *p;
    char *q;


    int num = 0;

    while(num < 512 ){
        printf("%d\n", num);
        p = calloc(128, 1);
        q = calloc(128,1);

        int i = 0;
        while( i < num){
            *(p+i) = 'a';
            i++;
        }

        printf("zzzz\n");
        free(p);
        printf("aaaa\n");
        free(q);
        num++;
    }


    return 0;
}

output:

zzzz
aaaa
132
zzzz
aaaa
133
zzzz
Segmentation fault


The above code indicates the Pre-Bufferoverflow. There's also post-Bufferoverflow, e.g.

char *p;
char *q;

p = malloc(...)
q = malloc(.N..)

strcpy(q, 2N)
