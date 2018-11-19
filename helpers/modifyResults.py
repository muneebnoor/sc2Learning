import numpy as np

results_data = np.load("D:\\thesis\\resultsListall.txt")

for r in results_data:
    if r == [0]:
        r = [0,1]
    else:
        r = [1,0]

print(results_data)