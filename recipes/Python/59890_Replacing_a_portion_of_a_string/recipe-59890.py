# Use slicing to extract those parts of the original string to be kept
s = s[:position] + replacement + s[position+length_of_replaced:]

# Example: replace 'sat' with 'slept'
text = "The cat sat on the mat"
text = text[:8] + "slept" + text[11:]
