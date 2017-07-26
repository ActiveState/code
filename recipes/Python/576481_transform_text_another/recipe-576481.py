def regex_transform(expr,to_expr,text):
    """
    a$1$2b
    """
    to_expr_regex=re.compile('\$(\d)',re.S|re.I)
    expr_regex=re.compile(expr,re.S|re.I)
    rst=[]
    start=0
    while 1:
        m_input=expr_regex.search(text,start)
        if not m_input:break
        def f(m_var):
            var_id=int(m_var.group(1))
            var=m_input.group(var_id)
            return var
        to_line=to_expr_regex.sub(f,to_expr)
        rst.append(to_line)
        start=m_input.end()
        
        
    return rst
