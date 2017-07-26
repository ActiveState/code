# 1, 2, 3
# 4, 5, 6
# 7, 8, 9
#Task: remove the middle column

temp = [[1,2,3],[4,5,6],[7,8,9]]
newTemp = [[x[0],x[2]] for x in temp]

#now newTemp is:
# 1, 3
# 4, 6
# 7, 9
