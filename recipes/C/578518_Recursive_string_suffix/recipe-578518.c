#include <stdio.h>
#include <string.h>

void suffix(char text[]);

int main() {
    char text[1000];
    
    printf("Text: ");
    scanf("%s", text);
    
    suffix(text);
    
    return 0;
}

void suffix(char text[]) {
    if (strlen(text)) {
        printf("%s\n", text);
        text[strlen(text) - 1] = '\0';
        suffix(text);
    } else {
        return;
    }
}
