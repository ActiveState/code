typedef struct __MAILOP_RECORD_{
    struct com_list_head list;
    char filename[16];
    char code[32];
    char id[16];
}sop;


int listtest(int argc, char **argv){

    struct com_list_head *node;
    
    sop *loghead;
    sop *lognode;

    loghead = (sop * )calloc(1, sizeof(sop));
    com_INIT_LIST_HEAD(&loghead->list);
    loghead->filename[0] = 'a';
    
    lognode =(sop * )calloc(1, sizeof(sop));
    lognode->filename[0] = 'b';
    com_list_add(&lognode->list, &loghead->list);
        
    lognode =(sop * )calloc(1, sizeof(sop));
    lognode->filename[0] = 'c';
    com_list_add_tail(&lognode->list, &loghead->list);
    
    com_list_for_each(node, &loghead->list){
        lognode = com_list_entry(node, sop, list);
        printf("--%s--\n", lognode->filename);
    }   
            
    printf("--%s--\n", loghead->filename);
        
    return 0;
            
        

    
}
