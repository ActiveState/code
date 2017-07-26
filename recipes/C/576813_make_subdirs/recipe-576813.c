/**
 *@brief 递归的创建一个路径下的所有子目录. 内存考虑， fullpath长度为 MAX_PATH_LEN,  对于n级目录， 需要的调用栈就
?,
 *       并不会等比级数的扩张
 *
 *@param[in] root 根目录,必须是文件件路径
 */
static int create_subdir(char *root,  mode_t mode, int depth){
    if(0 == depth){
        return EYOU_FILE_TRUE;
    }

    int i=0;
    char fname[2] = {0};
    char fullpath[MAX_PATH_LEN];

    while(i < 16){
        snprintf(fname, 2, "%x", i);
        if('/' == root[strlen(root)-1] ){
            snprintf(fullpath, MAX_PATH_LEN, "%s%s",root,fname);
        }
        else{
            snprintf(fullpath, MAX_PATH_LEN, "%s/%s", root, fname);
        }

        eyou_syslog("simple filed :%s\n", fullpath);
        if( -1 == mkdir(fullpath, mode)){
            eyou_syslog("simple filed :create dir %s : %s", fullpath, strerror(errno));
            return EYOU_FILE_FALSE;
        }

        /* 一旦出错就返回， 以避免重复创建。 其他错误需要人工处理 */
        if ( EYOU_FILE_FALSE == create_subdir(fullpath,mode,depth-1)){
            return EYOU_FILE_FALSE;
        }
        i++;
    }
                     return EYOU_FILE_TRUE;
}

/**
 *@brief 在配置文件指定的路径下，当这个路径被第一次分配时，  创建可能分配到的所有的子文件夹, 即文件夹0-9a-z. 
 *        这个功能由一个daemon负责， 不需要在程序中做， 以减少i/0操作.  
 *
 *       这个程序任然可以用做创建目录
 *
 *
 *@param[in] year_mon某年某月的目录, 比如200904. 当为空是， 设定为当前年月
 */
int eyou_create_dir(char *year_mon)
{

    SIMPLE_FILED_PATH_CONFIG *configs = NULL;
    char path[MAX_PATH_LEN];
    char date[7] = {0};

    mode_t mode = S_IRWXU | S_IRWXG | S_IRWXO ;

    if ( NULL == glb_flink_cfg){
        glb_flink_cfg = get_path_config();;
    }

    configs = get_path_config();
    if(NULL == configs){
        return EYOU_FILE_FALSE;
    }

    if(NULL == year_mon){
        /* 先创建文件夹  */
        time_t epoch_time = time(NULL);
        struct tm *cur_time = localtime(&epoch_time);
        cur_time->tm_year += 1900;
snprintf(date, 7, "%04d%02d", cur_time->tm_year, cur_time->tm_mon);

        year_mon = date;
    }
    
    while(configs){
        snprintf(path, MAX_PATH_LEN, "%s/%s", configs->str_path, year_mon);

        /* 创建以日期分类的目录 */
        if( -1 != mkdir(path, mode) ){
            create_subdir(path, mode, configs->hash_level);
        }
        configs = configs->next;
    }

    return EYOU_FILE_TRUE;
}   
    
