arr = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

# The subject should be regular, with all rows the same length

print [[r[col] for r in arr] for col in range(len(arr[0]))]

[[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]
