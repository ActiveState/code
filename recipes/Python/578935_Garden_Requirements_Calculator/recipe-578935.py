'''
9-16-2014
Ethan D. Hann
Garden Requirements Calculator
'''

import math

#This program will take input from the user to determine the amount of gardening materials needed

print("Garden Requirements Calculator")
print("ALL UNITS ENTERED ARE ASSUMED TO BE IN FEET")
print("_____________________________________________________")
print("")

#Gather all necessary input from user
side_length = input("Enter the length of one side of garden: ")
spacing = input("Enter the spacing between plants: ")
depth_garden = input("Enter the depth of the garden soil: ")
depth_fill = input("Enter the depth of the fill: ")

#Convert input to floats so that we can do math with them
side_length = float(side_length)
spacing = float(spacing)
depth_garden = float(depth_garden)
depth_fill = float(depth_fill)

#Calculate radius of each circle and semi-circle
r = side_length / 4

#1 - Number of plants for all semi-circles
area = (math.pi * (r**2)) / 2
number_plants_semi = math.trunc(area / (spacing**2))

#2 - Number of plants for the circle garden
area = math.pi * (r**2)
number_plants_circle = math.trunc(area / (spacing**2))

#3 - Total number of plants for garden
total_number_plants = number_plants_circle + (number_plants_semi*4)

#4 - Soil for each semi-circle garden in cubic yards
volume = (math.pi * (r**2) * depth_garden) / 2
#Convert to cubic yards
cubic_volume = volume / 27
cubic_volume_rounded_semi = round(cubic_volume, 1)

#5 - Soil for circle garden in cubic yards
volume = math.pi * (r**2) * depth_garden
#Convert to cubic yards
cubic_volume = volume / 27
cubic_volume_rounded_circle = round(cubic_volume, 1)

#6 - Total amount of soil for the garden
total_soil = (cubic_volume_rounded_semi * 4) + cubic_volume_rounded_circle
total_soil_rounded = round(total_soil, 1)

#7 - Total fill for the garden
volume_whole = (side_length**2) * depth_fill
all_volume_circle = (math.pi * (r**2) * depth_garden) * 3
total_volume_fill = volume_whole - all_volume_circle
cubic_total_volume_fill = total_volume_fill / 27
cubic_total_volume_fill_rounded = round(cubic_total_volume_fill, 1)

#Print out the results
print("")
print("You will need the following...")
print("Number of plants for each semi-circle garden:", number_plants_semi)
print("Number of plants for the circle garden:", number_plants_circle)
print("Total number of plants for the garden:", total_number_plants)
print("Amount of soil for each semi-circle garden:", cubic_volume_rounded_semi, "cubic yards")
print("Amount of soil for the circle garden:", cubic_volume_rounded_circle, "cubic yards")
print("Total amount of soil for the garden:", total_soil_rounded, "cubic yards")
print("Total amount of fill for the garden:", cubic_total_volume_fill_rounded, "cubic yards")
