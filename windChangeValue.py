import random

count = 300
changeRange = 2.52

# value = 0
valueList = []

for _ in range(10000):
    value = 0
    for _ in range(count):
        value += random.uniform(-changeRange, changeRange)
    valueList.append(value)

print(sum(valueList) / len(valueList))
# meaning the wind changes 2.52 degrees per second random left or right
# 

