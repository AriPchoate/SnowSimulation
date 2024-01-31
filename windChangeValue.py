'''
Ari, Aureliano
Date: 2/2/24
Sources:
https://earthscience.stackexchange.com/questions/980/why-does-the-wind-periodically-change-direction
    - wind changes around 20 degrees every 5 minutes

Reflection: On snowSimulation.py file    

On my honor
'''
import random
from math import pi
from alive_progress import alive_bar

# 300 seconds or 5 minutes
count = 300
changeRange = 0.04358 # Radians

# Value list to store data
valueList = []
# Amount of times the wind change is simulated
iterations = 100000
print("Simulating...")
with alive_bar(iterations) as bar:
    for i in range(iterations):
        value = 0 # Resets the value
        for j in range(count): # iterates through 300 seconds of change
            # Updates the value by the change range
            value += random.uniform(-changeRange, changeRange)
        # Takes the absolute value because it would average to zero if we didnt
        valueList.append(abs(value))
        bar()

# Final prints
print(f"{pi / 9} | Target | 20 degrees")
print(f"{sum(valueList) / len(valueList)} | Output from : {changeRange} Radians")