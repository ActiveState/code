#include <string.h>
#include <ctype.h>

#include "jy_common.h"


char *itoa(int i){
    char *buf = calloc(sizeof(i)+1, 1);
    if(buf == NULL){
        return NULL;
    }

    sprintf(buf, "%d", i);
    return buf;
}


char *trim(char *string){
    if(NULL == string){
        return NULL;
    }
    int start = 0;
    int end = strlen(string);
    while( start < end && (isspace(string[start]) || isblank(string[start])) ){
        start++;
    }

    while( end > start && (isspace(string[end-1]) || isblank(string[end - 1]))){
        end--;
    }

    char *ret = calloc(end - start +1, sizeof(char));
    if(NULL == ret){
        perror("calloc for trim\a");
        return NULL;
    }

    return strncpy(ret, string+start, end-start);

}
