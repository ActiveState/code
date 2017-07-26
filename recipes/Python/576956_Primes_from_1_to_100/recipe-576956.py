print [i+2 for i, numberList in enumerate([[i for x in range(2, i+1) if i % x == 0 and i != x] for i in range(2,100)]) if not numberList]
