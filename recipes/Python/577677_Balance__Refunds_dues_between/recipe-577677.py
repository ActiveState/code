#!/usr/bin/python
#
# This script takes dues in input (std input) and compute an optimum
# list of refunds.
# Format of input list (a negative is a due)
# John -10
# Jack +20
# Jessie -
# 
# If the sum is not equal to zero, the algorithm never stops.

import sys

# CONSTANTS
BALANCE_THRESHOLD = 0.02

# Init map of dues
dues = {}

# Read std in
for line in sys.stdin :
    # Split into two parts
    (name, due) = line.strip().split()

    # Fill the map of dues
    dues[name] = float(due)


# Init list of refunds (from, to, sum)
refunds = []

# Loop until the balance is reached
while True :
    
    # Get the min/max due
    maxName = max(dues, key=dues.get)
    minName = min(dues, key=dues.get)

    # Min == Max ?? => exit
    if minName == maxName : break

    # Get dues
    minDue = dues[minName]
    maxDue = dues[maxName]

    # What can we exchange ?
    maxRefund = min(abs(minDue), abs(maxDue))

    # Balance reached ?
    if maxRefund <= BALANCE_THRESHOLD : break

    # Add a refund
    refunds.append((minName, maxName, maxRefund))

    # Update dues
    dues[minName] += maxRefund
    dues[maxName] -= maxRefund
   
# Print refunds
for (fromName, toName, refund) in refunds :
    print "%s => %s : %.2f" % (fromName, toName, refund)  
