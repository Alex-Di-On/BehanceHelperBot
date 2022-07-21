





x = ['hello', '1', 'hi', '2', 'bye', '3']

a = {x[t]: x[t+1] for t in range(len(x))[::2] if t < len(x) - 1}



print(a)

