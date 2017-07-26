#!/usr/bin/python
'''
CompareCsv.py - Python script that will compare two CSV files based upon a unique ID field and record changes in this field as well as two secondary fields (qty & price).  The output is a CSV file. 
'''
#Imports (do not change)
from __future__ import division
import sys,csv

# ---------------------------------------------
#Globals - CHANGE ME
# ----------------------------------------------
OldFile = 'test1.csv'			# File Name For Old CSV File (Front Slashes / to separate paths)
NewFile = 'test2.csv'			# File Name For New CSV File (Front Slashes / to separate paths)
OutFile =  'test-out.csv'		# File To Save Results (Front Slashes / to separate paths)
CSVFilesHaveHeaderRow = True	# True or False if input files include a header row
IdColNumber = 0					# Column that contains the unique Item ID (Start counting with zero)
QtyColNumber = 1				# Column that contains the qty in stock
PriceColNumber = 2				# Column that contains the prices
DefaultMarkUpPercent = 0 		# Markup in percent - Needs to be whole number 0 = disable

# ---------------------------------------------
# Create CSV Objects 
CSVOld = csv.reader(open(OldFile,'rb'))
CSVNew = csv.reader(open(NewFile,'rb'))
CSVOut = csv.writer(open(OutFile,'wb'))
CSVOut.writerow(['ID','Price','Qty','Orderable','Status'])

# -----------------------------------------
# Load Old Data Into Memory
OldData = {}
FirstLine = True
for line in CSVOld:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		OldData[line[IdColNumber]] =  (line[QtyColNumber],line[PriceColNumber])

# -----------------------------------------
# Read Through New Data & Compare to Old
NewIDList = []
FirstLine = True
for line in CSVNew:
		
	# Skip Header In CSV Files
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
	
		# Assign New Values to locals for readability
		NewID = line[IdColNumber]
		NewQty = line[QtyColNumber]
		NewPrice = line[PriceColNumber]
		
		# Existing Items - Compare Secondary Fields
		if OldData.has_key(line[IdColNumber]):
			
			# Assign Old Values locals for readability
			OldID = OldData[line[IdColNumber]]
			OldQty = OldID = OldData[line[IdColNumber]][0]
			OldPrice = OldID = OldData[line[IdColNumber]][1]
			
			# Save ID Field To Test for deleted
			NewIDList.append(NewID)
			
			# Reset Status
			Status = ""
			
			# Define Current Orderable Status
			if NewQty == 0:
				Orderable = "NO"
			else:
				Orderable = "YES"
				
			# Check for Stock Status Change
			if int(OldQty) <= 0  and int(NewQty) > 0:
				Status += "In-Stock "	
			if int(OldQty) > 0  and int(NewQty) <= 0:
				Status += "Out-Stock "	
			
			# Check for Price Change
			if OldPrice != NewPrice:
				Status += "Price "
				if DefaultMarkUpPercent > 0:
					SellPrice = str(float(NewPrice) * (1+(DefaultMarkUpPercent / 100)))
				else:
					SellPrice = NewPrice
			else:
				SellPrice = NewPrice
				
			# Save to output only if the item has a changed status
			if Status:
				CSVOut.writerow([NewID,SellPrice,NewQty,Orderable,Status])
		else:
			
			# New Item ID 
			
			# Markup Price
			if DefaultMarkUpPercent > 0:
				SellPrice = str(float(NewPrice) * (1+(DefaultMarkUpPercent / 100)))
			else:
				SellPrice = NewPrice
			
			# Save to Output
			CSVOut.writerow([NewID,SellPrice,NewQty,'YES','NewItem'])
			
# Check For Deleted Items 
for id in OldData.keys():
	if id not in NewIDList:
		CSVOut.writerow([id,'','','NO','Deleted'])
