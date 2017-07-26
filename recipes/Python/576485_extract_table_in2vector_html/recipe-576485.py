def extract_table(table_str):
    rsts=[]
    row_re=re.compile("<tr[^<>]*>.*?</tr>",re.S|re.I)
    col_re= re.compile("<td[^<>]*>.*?</td>",re.S|re.I)
    tag_re =re.compile("<[^<>]+>",re.S|re.I)
    blank_re=re.compile('\s+',re.S|re.I)
    rows=row_re.findall(table_str)
    for row_str in rows:
        cols=col_re.findall(row_str)
        cols=[tag_re.sub('',col_str) for col_str in cols]
        cols=[blank_re.sub('',col_str) for col_str in cols]
        rsts.append(cols)
    return rsts    
