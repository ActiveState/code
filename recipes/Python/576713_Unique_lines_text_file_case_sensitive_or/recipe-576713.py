# Unique lines case insensitive
filename = r"h:\keywords.txt"
li = list(file(filename))
# Note: listifying file() leaves \n at end of each list element
st = "".join(li)
# comment out next line to get case-sensitive version
st = st.lower()
se = set(st.split("\n"))
result = "\n".join(sorted(se))
print result
