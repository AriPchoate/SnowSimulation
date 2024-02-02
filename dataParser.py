'''
Ari, Aureliano 
Date: 2/2/24
This code is used to convert the text file generated from the chunkMatrix in the simulation to a greyscale image.
Also, the last lines of the code  create a histogram graph
Sources: 
    cubic inch snow weight: https://evogov.s3.amazonaws.com/141/media/109213.pdf 
        - on average 1.25 pounds per cubic inch of snow
    Weight of a snowflake: https://hypertextbook.com/facts/2001/JudyMoy.shtml#:~: 
        - on average 3mg per snowflake
    1.25 pounds is 566990.5mg
    566990.5 / 3 = 188996.83_ snowflakes per cubic inch


Reflection: On snowSimulation.py file. This was not a hard chunk of code to write. The only difficulty was finding a good algorithm
to convert the value at a certain chunk into a pixel value. The explanation for this is on a image file on git called "pixelValConversionMath.jpeg"
On my honor
'''
import statistics, math
from PIL import Image
from alive_progress import alive_bar
import matplotlib.pyplot as plt

def generateFinalImg(data, img):
    global width, height
    total = []
    for spot in data:
        for smallSpot in spot:
            total.append(int(smallSpot))  #Goes through every number in the data and appends it to a list

    avg = statistics.mean(total)  #Averages to list

    with alive_bar(width * height) as bar:
        for spot in range(len(data)):
            for smallSpot in range(len(data[spot])):
                val = int(data[spot][smallSpot])  #Takes the value of each spot
                if val <= 1:
                    finalPix = 0
                else:
                    pix1 = avg**(math.log(127)/math.log(val))  #This part of the code is explained in pixelValConversionMath.jpeg on git
                    finalPix = int(254 - pix1)
                color = (finalPix, finalPix, finalPix)  #Sets everything to same to make a black-white scale
                x, y = smallSpot, spot
                try:
                    img.putpixel((y, x), color)
                except:  #Sometimes the color becomes negative, so it the code makes it error. With this, it just makes the pixel 0
                    img.putpixel((y, x), (0, 0, 0))
                bar()
    img.show()

data = open("./data/data-OneHour.txt", "r") # using tempData temporarily just trying out some simulations

width, height = 1249, 754
FinalImage = Image.new("RGB", (width, height))

numList = []

for line in data:  #Takes all unnecessary components out of the line   
    #I know that everything equals line in this. For some reason if I don't keep the equaling, it doesn't work and the operation goes through
    line = line.replace(",", "")  #Takes out commas
    line = line[:-2]  #Takes out the ending brackets that were orignally part of the matrix
    line = line[1:]  #Takes out front bracket
    line = line.split() #Splits the numbers up by the spaces
    numList.append(line)


generateFinalImg(numList, FinalImage)

highest = int(numList[0][0])
lowest = int(numList[0][0])
# Iterates through every item in the numList matrix
for col in numList:
    for chunk in col:
        chunk = int(chunk)
        # Checks if theres a new highest snowflake value
        if chunk > highest:
            # Updates highest value
            highest = chunk
        # Checks if theres a new lowest snowflake value
        if chunk < lowest:
            # Updates lowest value
            lowest = chunk

print(f"Upper and lower values:\nLowest : {lowest} | Highest : {highest}")

# Converts the dataMatrix into an array so it can be used in matplotlib
dataList = []
for i in range(len(numList)):
    for item in numList[i]:
        # Iterates through the matrix
        # Adds all the items to the array
        dataList.append(int(item))

# Plots a histogram of the amount of snow
plt.hist(dataList, 250)
plt.show()