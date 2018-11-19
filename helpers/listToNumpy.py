import pickle
import numpy as np

path = "D:\\thesis\\replays2000"

dataList = list()
resultsList = list()


with open('D:\\thesis\\dataList.txt', 'rb') as f:
    dataList = pickle.load(f)

with open('D:\\thesis\\resultsList.txt', 'rb') as f:
    resultsList = pickle.load(f)


dataListRefined = list()

for c in dataList:
    count = 0
    tempList = list()
    for key in c:
        value = [c[key]]
        tempList.extend(value)
    dataListRefined.append(tempList)

dataArray = np.array(dataListRefined)
resultsArray = np.array(resultsList)

dataFile = open("D:\\thesis\\DataArray.txt","wb")
resultsFile = open("D:\\thesis\\ResultsArray.txt","wb")

np.save(dataFile,dataArray)
np.save(resultsFile,resultsArray)

print("done")