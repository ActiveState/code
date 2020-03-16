  
#include <stdlib.h>
#include <stdio.h>


struct binode {
  int value ; 
  struct binode *next_ptr ;
  struct binode *back_ptr ; 
};

void createDLLFromArray(struct binode *dll, int *arr, int arr_size){
    
    // first binode configuration
    dll->back_ptr = NULL;
    dll->value = *arr; // first element of array 
    
    struct binode *prev = dll ;  
    
    // second node and onwards.. 
    for(int i = 1 ; i < arr_size ; i ++ ){
        
        struct binode *new_node = (struct binode *)malloc(sizeof(struct binode)) ; 
        new_node->value = *(arr+i) ; 
        new_node->back_ptr = prev ; 
        prev->next_ptr = new_node ; 
        prev = new_node ; 
    }
    
    prev->next_ptr = NULL;
    
}

void printDLL(struct binode *startNode){
    
    struct binode *ptr = startNode ;   
    
    printf("NULL <=> ");
    while(ptr!=NULL){
        printf("%d <=> ",ptr->value);
        ptr = ptr->next_ptr ; 
    }
    
    printf("NULL \n");
}


int main(){
    
    struct binode my_node; 
    int arr[10] = {2,4,6,8,10,12,14,16,18,20} ; 
    
    createDLLFromArray(&my_node,arr,10) ; 
    printDLL(&my_node);
    
    return 0; 
}
