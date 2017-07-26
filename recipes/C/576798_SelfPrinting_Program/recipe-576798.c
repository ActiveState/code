#include <stdio.h>
char *program = "#include <stdio.h>%cchar *program = %c%s%c;%cint main()%c{%c
printf(program, 10, 34, program, 34, 10, 10, 10, 10, 10, 10);%c    return 0;%c}%c";
int main()
{
        printf(program, 10, 34, program, 34, 10, 10, 10, 10, 10, 10);
        return 0;
}
