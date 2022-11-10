"""
We are looking to create a offset amp
The values in rValues contain all the standard resistors at our disposal
"""
import itertools
import math
import time
from tabulate import tabulate

start = time.time()


def Crunch(_set):
    ansLoad = vo(_set[0], _set[1], _set[2], _set[3], vInLoad)
    ansNoLoad = vo(_set[0], _set[1], _set[2], _set[3], vInNoLoad)
    if targetNoLoad - noLoadBounds < ansNoLoad < targetNoLoad + noLoadBounds:
        if targetLoad - loadBounds < ansLoad < targetLoad + loadBounds:
            finalList.append((ansLoad,) + (ansNoLoad,) + _set)


vInLoad = 2.355 # voltage under load
vInNoLoad = 2.733 # voltage under no load
targetLoad = 2.5 # target voltage under load
targetNoLoad = .5 # target voltage under no load

optimalError = 100 # needs a number otherwise will not make first calculation when finding error

loadBounds = 0.05 # bounds when creating the list of viable load solutions
noLoadBounds = 0.3 # bounds when creating the list of viable no load solutions

vo = lambda ra, rb, rc, rd, vIn: 5 * (rd / (rb + rd)) * (ra + rc) / ra - vIn * rc / ra  # Equation

# List initialization
ansListLoad = []
ansListNoLoad = []
finalList = []
optimal = []

#initilalization of resistor combo array
rValues = [100, 220, 470, 1000, 2200, 4700, 10000, 22000, 47000, 100000, 220000, 470000, 1000000,
           4700000]  # Possible resistors
rValuesDoubled = [i * 2 for i in rValues]
rValuesHalf = [i / 2 for i in rValues]
rValues = rValues + rValuesDoubled + rValuesHalf
#rValues.sort() #only sort if you want to graph

rSet = [p for p in itertools.product(rValues, repeat=4)]  # initilizes Resistor Array

for i in range(0, len(rSet)): # run the calculation in the entire array
    Crunch(rSet[i])


for i in range(len(finalList)): # finds the optimal value out of the possible solutions
    x = finalList[i][0]
    y = finalList[i][1]
    z = math.sqrt(x ** 2 + y ** 2)
    targetError = math.sqrt(targetNoLoad ** 2 + targetLoad ** 2)
    iError = abs((z - targetError) / targetError)
    if iError <= optimalError:
        if iError != optimalError:
            optimal = []
        optimal.append(finalList[i])
        optimalError = iError
"""
valueCount = dict()

for i in finalList: # wanted to know the distribution in the list of possible solutions to know if any resistor value did not appear therefore allowing for its removal
    for p in range(2, 6): 
        if i[p] in valueCount:
            valueCount[i[p]] += 1
        else:
            valueCount[i[p]] = 1
"""
col_names = ('Load', 'No Load', 'R1', 'R2', 'R3', 'R4')
print(tabulate(optimal, headers=col_names, tablefmt="grid", showindex="always"))
end = time.time()
print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")


'''print("The optimal resistor combo is", 
      " \n ra: ", optimal[1], 
      " \n rb: ", optimal[2],
      " \n rc: " ,optimal[3], 
      " \n rd: " ,optimal[4],
      " \n This gives a Vo of ", "{:.4f}".format(optimal[0]), "V and a error of ", "{:.4f}".format(optimalError*100), "%")
'''