print "all amounts should be in dollars!"

while True:
	P=float(raw_input("enter Principal:"))
	i=float(raw_input("enter Percentage of interest rate:"))
	t=float(raw_input("enter Time(in years):"))
	I=P*t*(i/100)
	print "Interest is", I,"dollars"
