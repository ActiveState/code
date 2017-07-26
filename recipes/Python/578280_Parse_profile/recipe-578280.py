#!/usr/bin/env python3
import pprint
import re
import sys
TIC = "'"
QUOTE = '"'
def parse_profile(file_name):
    return_dict = dict()
    with open(file_name) as reader:
        for line in reader.readlines():
            line = re.sub(r"export\s+", "", line.strip())
            if "=" in line:
                key, value = line.split("=", 1)
                # Values that are wrapped in tics:  remove the tics but otherwise leave as is
                if value.startswith(TIC):
                    # Remove first tic and everything after the last tic
                    last_tic_position = value.rindex(TIC)
                    value = value[1:last_tic_position]
                    return_dict[key] = value
                    continue
                # Values that are wrapped in quotes:  remove the quotes and optional trailing comment
                elif value.startswith(QUOTE): # Values that are wrapped quotes
                    value = re.sub(r'^"(.+?)".+', '\g<1>', value)
                # Values that are followed by whitespace or comments:  remove the whitespace and/or comments
                else:
                    value = re.sub(r'(#|\s+).*', '', value)
                for variable in re.findall(r"\$\{?\w+\}?", value):
                    # Find embedded shell variables
                    dict_key = variable.strip("${}")
                    # Replace them with their values
                    value = value.replace(variable, return_dict.get(dict_key, ""))
                # Add this key to the dictionary
                return_dict[key] = value
    return return_dict

if __name__ == '__main__':
    pprint.pprint(parse_profile(sys.argv[1]))
