file('code.txt', 'w').write('\n'.join([line for line in file(raw_input('File? ')).read().splitlines() if not line.strip().startswith('#')]))
