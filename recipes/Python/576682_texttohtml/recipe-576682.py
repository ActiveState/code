#文本原样到html中
#对换行符的处理
#需求产生于:Google Blog
line_break="\n"

data=file("e://untitled.txt","r").read()
out=data.replace(line_break,"<br/>")

file("c://out.txt","w").write(out)
