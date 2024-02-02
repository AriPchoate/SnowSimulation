'''
Ari, Aureliano
Date: 2/2/24
This code removes all of the buildings, roads, and general residential items in the Cartolightview image.
Sources: No sources
Reflection: On snowSimulation.py file
On my honor
'''
# 124, 231, 190
# 121, 231, 179
# 142, 249, 206
import math
from PIL import Image

dimx, dimy = 1557, 785

newImage = Image.new("RGB", (dimx, dimy))

img = Image.open("./Images/Cartolightview.png")
img.convert("RGB")

width, height = img.size

values = []

for y in range(0, height):
    for x in range(0, width):  #goes through all the pixels
        points = img.getpixel((x,y))  #Gets the rgb values
        values.append(points[:-1])  #Takes out the last rgb value, which is the tranparancy, and adds rgb to list

firstImage = False
progressOld = 0
print("0%")
finalPix = []
deviation = 15  #Amount of deviation acceted

for spot in range(len(values)): #Goes through each index value of the list
    pixlist = []
    r, g, b = values[spot][0], values[spot][1], values[spot][2]
    for y in range(-20, 21):
        for x in range(-20, 21):  #Looks through all of the x and y values around within 20 of the original x, y value.
            pixTry = spot+(y*1557)+x  #This converts the changed x an y values into a new pixel index to check
            try:
                pix = values[pixTry]  #Gets the pixel rgb of the index from pixTry

                if r-pix[0] < deviation and g-pix[1] < deviation and b-pix[2] < deviation:  #If there is a low difference between the original value and the pix value, it adds it to the pixList. This basically assures that if there is a building, which is darker than the surrounding, the surrounding lighter area is added to the pixList and not the building. Therefore, eliminating the buildings in the picture.
                    pixlist.append(pix)
            except:
                continue
    red = 0
    green = 0
    blue = 0
    for val in pixlist: #Adds up all of the rgb values of the pixlist
        red += val[0]
        green += val[1]
        blue += val[2]

    length = len(pixlist)
    try:
        avR, avG, avB = round(red/length), round(green/length), round(blue/length)  #Averages all of the rgb values
    except:
        avR, avG, avB = values[spot][0], values[spot][1], values[spot][2] #Sometimes the there are no values around the original pixel that fulfills the if statement in line 46. Therefore, the length of pixList would be 0, which would throw and error. This makes the color equal to the original
    
    color = (avR, avG, avB)

    y = int(spot/1557) #Gets the respective x,y values from the index numbers
    x = spot-(y*1557)
    progressNew = (y/dimy*100)  #Gets the percent of the code that has been completed
    
    if progressNew != progressOld:   #Instead of printing the progress for each line, I only print it when the progress percent has changed
        print(str(progressNew) + "%")

    newImage.putpixel((x, y), color)  #Puts the pixel on the image

    progressOld = progressNew

newImage.show()