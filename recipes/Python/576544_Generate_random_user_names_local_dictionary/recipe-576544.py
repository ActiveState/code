import random

names_file = file('/etc/dictionaries-common/words')
num_dict_lines = 9900            # A-Z, no apostrophes, approximate!
bytes = num_dict_lines * 10 * 8  # lines * avg word len * bytes/char
rand_words = [ln for ln in names_file.readlines(bytes) if "'" not in ln]
names_file.close()

def gen_name():
    idx = random.randint(2, num_dict_lines)
    username = rand_words[idx]
    #print 'last:', rand_words[num_dict_lines]
    return username.strip()

# Generate a few samples.
for i in range(3):
    print gen_name(),

# Printed: Sister Frankfort Babbitt
