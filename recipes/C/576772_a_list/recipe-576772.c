#include <stdlib.h>
#include <stdio.h>

#define null 0

//define the node structure
struct ilist{
    int elem;
    struct ilist *next;
};


//allocate the memory of target
void createNode(struct ilist **node, int elem){
    struct ilist *temp= malloc(sizeof(struct ilist));
    temp->elem = elem;
    temp->next = null;
   
    /* we cannot change the value of node, because the subroutine is running on a frame, within a copy of the actual parameters are created
     * if node is changed here, what changed is the copy
     * but we can change the value referenced by node, as the referenced values could be actually be changed.
     
     * everything is pass by value
     */
    *node = temp;
   
    return;
}


int main(int argc, char **argv){
    //construct a list
    struct ilist *list = null;
        struct ilist *visitor = null;
   
    int i = 7;
    while(i>0){
        if(list == null){
            createNode(&list, i);
           
            visitor = list;
           
        }
        else{
            struct ilist *temp = null;
            createNode(&temp, i);
           
           
            list->next = temp;
            list = temp;
       
        }
       
        i--;
    }
   
    //visit the list
   
    while(visitor != null){
        printf("%d\n",visitor->elem);
        visitor = visitor->next;
    }
   
    return 0;
}
