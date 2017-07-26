# decisionmaker.py
# FB - 201010155
# Choose the best item from N options.
# Each item can have M constraints (non-zero).
# All constraints assumed to have equal importance (weight).
import sys

def makeDecision(constraintsTable, constraintTypes):
    # calculate item values
    itemValues = []
    for i in range(n):
        itemValues.append(float(1))
        for j in range(m):
            if constraintTypes[j] == 0: # min value is better
                itemValues[i] /= constraintsTable[i][j]
            else: # max value is better
                itemValues[i] *= constraintsTable[i][j]

    # choose the best item
    maxIndex = 0
    maxValue = itemValues[0]
    for i in range(n):
        if itemValues[i] > maxValue:
            maxValue = itemValues[i]
            maxIndex = i

    return itemNames[maxIndex]

# MAIN
n = int(raw_input('Number of items: '))
if n < 2:
    sys.exit()
m = int(raw_input('Number of constraints for each item: '))
if m < 2:
    sys.exit()

constraintNames = []
constraintTypes = [] # min or max is better
for j in range(m):
    constraintName = raw_input('Constraint ' + str(j + 1) + ' name: ')
    constraintNames.append(constraintName)
    constraintType = int(raw_input('Lower(0) or Higher(1) is better: '))
    if constraintType < 0 or constraintType > 1:
        sys.exit()
    constraintTypes.append(constraintType)

itemNames = []
constraintsTable = []
for i in range(n):
    itemName = raw_input('Item ' + str(i + 1) + ' name: ')
    itemNames.append(itemName)

    constraints = []
    for j in range(m):
        constraint = float(raw_input(constraintNames[j] + ': '))
        if constraint == 0.0:
            print 'Constraint value cannot be 0!'
            sys.exit()
        constraints.append(constraint)
    constraintsTable.append(constraints)

print 'Best item decided: ' + makeDecision(constraintsTable, constraintTypes)
