# Check that string 'source' represents an integer

try:
    stripped = str(int(source))
except:
    # 'source' does not represent an integer
    .....

# Additionally, it's easy to check if 'source' has blanks around the number
if source != stripped:
    # 'source' has blanks before or after the number, or both
    .....



# A simpler version if you don't need the stripped value:
try:
    dummy = int(source)
except:
    # 'source' does not represent a number
    .....
