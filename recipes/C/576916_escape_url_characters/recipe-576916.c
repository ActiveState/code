/**
 *@brief 对于url中的一些特殊字符会被转义以利传输,
 *      并且， 归档服务器上, php写入cookie中的值可能存在特殊字符， 需要转换
 *         
 *参考: http://www.blooberry.com/indexdot/html/topics/urlencoding.htm
 *      http://www.december.com/html/spec/esccodes.html
 *
 *@param[in,out] data 需要处理的数据， 处理完后， 这个数据会被修改为期待的数据
 *@param[in] data_len data中的实际数据长度
 *
 */
int escape_url_character(char *data, int data_len)
{
    /* 下面只列出来了一些加密用到的字符， 而没有列出所有的字符, 主要是空格, /, +, = */
    char *transfer_table[][2] = { {"+", "2B"}, {"[","5B"},{"]","5D"},{"`","60"},{";","3B"},{"/","2F"},{"?","3F"},{":","3A"},{"@","40"},{"=","3D"},{"&","26"},{"$","24"},{" ","20"},{"<","3C"},{">","3E"},{"#","23"},{"%","25"},{"{","7B"},{"}","7D"},{"|","7C"},{"\\","5C"},{"^","5E"},{"~","7E"}, {NULL, NULL} };

    int i = 0, j;
    char *buf = calloc(data_len + 1, sizeof(char));

    while( i < data_len ){
        if( '%' != data[i]){
            strncat(buf, data+i, 1);
            i++;
            continue;
        }

        /* 查表 */
        j = 0;
        while( NULL != transfer_table[j][1] ){
            if( 0 == strncasecmp(data+i+1, transfer_table[j][1], 2 )){
                strncat(buf, transfer_table[j][0], 1);
                i += 3;
                break;
            }
            j++;
        }
        /* 对于表中不存在的字符不作处理, 但输出一条日志 */
        if( NULL == transfer_table[j][1] ){
            strncat(buf, data+i, 1);
            printf("escape_url_character: unhandled sequence: %s\n", data+i);
            i++;
        }
    }

    memset(data, 0, data_len);
    strcpy(data, buf);

    free(buf);
    return 0;
}
