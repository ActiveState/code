import re


output  = re.compile('<li>(.*?)</li>', re.DOTALL |  re.IGNORECASE).findall(input)
