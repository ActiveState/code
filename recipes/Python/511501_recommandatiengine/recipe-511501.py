f = open("rec_2.tmp")
try:
    for line in f:
        print line
finally:
    f.close()
sys.exit(0)
