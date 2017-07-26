# Invert a dictionary
mydict = {"Apple": "red", "Banana": "yellow", "Carrot": "orange"}

inverted_dict = dict([[v,k] for k,v in mydict.items()])

print inverted_dict["red"]
