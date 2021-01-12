#include <stdio.h>
#include <stdlib.h>

struct value {
    int v ; 
};
struct node {
    int val1 ;
    int val2 ; 
    int *val3 ; 
};

struct node2{
    int v1;
    int v2; 
};

struct node* createStructArr(int n, int **b){
    // defined n
    struct node *ptr = (struct node *)malloc(n*sizeof(struct node)) ; 
    
    // stores ppinter to the val1 for each struct.
    b = (int **)malloc(sizeof(int)*n);
    
    struct node *p = ptr ; 
    for(int i = 0 ; i < n ; i ++ ){
        p->val1 = i ; 
        p->val2 = i+1;
        
        
        b[i] = &(p->val1) ; 
        
        // CREATING MALLOC FOR POINTER SO THAT IT IS NOT LOST AFTER EXITING STACK FRAME OF THIS FUNCTION.
        int *v3 = (int *)malloc(sizeof(int));
        *v3=i+2;
        p->val3 = v3 ; 
        p++;
    
        
        
    }
    return ptr;
}

void printStructArr(struct node *a, int n){

    
    int first,second; 
    struct node *ptr = a ; 
    
    
    for(int i = 0 ; i < n ; i ++ ){
    
        // ACCESSING VIA ANOTHER MOVING POINTER.
        // NOT TOUCH THE BASE POINTER a 
        printf("(%d,%d,%d) ", ptr->val1,ptr->val2,*(ptr->val3)) ;  
        ptr++;

        // ACCESSING VIA BASE POINTER idx notation   
        printf("(%d,%d,%d) ", a[i].val1,a[i].val2,*(a[i].val3));
        
        // ACCESSING VIA BASE POINTER pointer notation   
        printf("(%d,%d,%d) ", (a+i)->val1, (a+i)->val2, *((a+i)->val3)); 
        
        
        printf("\n");
    }
    
}

void createAccessArr(){
    
    // dynamically increasing array without declaring dimension at time of declaration. 
    struct node2 *n = (struct node2 *)malloc(sizeof(*n));
    struct node2 *ptr = n ; 
    
    for(int i = 0 ; i < 10 ; i ++ ){
        
        // ACCESSING THROUGH MOVING PTR. 
        ptr->v1 = i ; 
        ptr->v2 = i+1 ; 
        ptr++; 

        // ACCESSING THROUGH BASE PTR pointer notation 
        (n+i)->v1 = i ; 
        (n+i)->v2 = i+3 ; 

    }
    
}

void printVal2FromVal1Reference(int **a, int n){

    int *addr ; 
    for(int i = 0 ; i < n ; i++ ){
        
        printf("%p ",addr);
    }    
}

int main()

{   
    int **b ; 
    int n = 10 ; 
    struct node *p = createStructArr(n,b);
    printStructArr(p,n);
    printVal2FromVal1Reference(b,n);
    return 0;
}

