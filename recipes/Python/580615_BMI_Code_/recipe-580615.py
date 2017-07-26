weight = float(input("Enter your weight in pounds: "))
height = float(input("Enter your height in inches: "))

height <= 0
weight <= 0

height_m = height/39.37
weight_kg = weight/2.2046
height_m = float()
weight_kg = float()

BMI1 = (weight/(height**2))
BMI2 = (weight_kg/(height_m**2))

print("Your BMI in in/lbs is: ", round(BMI1, 1))
print("\nYour BMI in m/kg is: ", round(BMI2,1))
