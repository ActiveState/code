import numpy as np

def cli_hist(data,bins=10):
    bars = u' ▁▂▃▄▅▆▇█'
    n,_ = np.histogram(data,bins=bins)
    n2=n*(len(bars)-1)/(max(n))
    res = u" ".join( bars[i] for i in n2 )
    return res

data = np.random.random(100)    

print cli_hist(data)
# ▆ ▄ ▃ ▅ █ ▄ ▅ ▁ ▅ ▇
print cli_hist(data,bins=5)
# ▆ ▅ █ ▄ ▇
