# here's the obvious part!
sys.stdin.close()
sys.stdout.close()
sys.stderr.close()

# this is pretty obscure!
os.close(0)
os.close(1)
os.close(2)
