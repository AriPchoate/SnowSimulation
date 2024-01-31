'''
Ari, Aureliano 
Date: 2/2/24
This code was used to convert the colored height image into a greyscale image where red was lightest, yellow second, blue darkest.
Reflection: We converted the pixel values into CMY colorspace for this code. We did this because
CMY has all the major color distinctions of the orignial photo. It makes it very easy to see
where there is red, yellow, and blue just from the CMY values. Because of this, it was easy
to create an algorithm to make red the brightest, yellow second, and blue the darkest.
Sources: No sources
On my honor
'''

from PIL import Image
import math

img = Image.open("./Images/FinalCarto.png")  #This is the colored image


width, height = img.size

newImage = Image.new("RGB", (width, height))

def rgb_to_cmy(r, g, b): 
    c = (1 - r / 255)  #Conversion rates
    m = (1 - g / 255)
    y = (1 - b / 255)
    return (c, m, y) 

rgbValues = []

for y in range(0, height):
    for x in range(0, width):  
        points = img.getpixel((x,y))  #Goes through all the pixels and gets the rgb values
        rgbValues.append(points)  #Appends each rgb value to the list

cmyValues = []

for spot in rgbValues:
    r, g, b = spot[0], spot[1], spot[2]
    cmyValues.append(rgb_to_cmy(r, g, b))  #Converts values to cmy and appends to list

progressOld = 0
print("0%")

for spot in range(len(cmyValues)):
    c, m, y = cmyValues[spot][0], cmyValues[spot][1], cmyValues[spot][2]  #Gets the values out
    scale = (m*60)**2 + (y*25)**2 - (c*5)**2  
    #This algorithm makes the heaviest weight of the colors the magenta. In the original picture,
    #Red it the highest. Then yellow is second heaviest, which makes a distinction between the yellow and cyan
    #Subtracting the cyan makes the low blue be even darker, making it be distinct
    if y*10 < c:  #If c is much greater than y, then the color is blue
        scale *= 0.5  #Makes it darker for even more distinction
    scale = int(scale)
    color = (scale, scale, scale)  #Everything equals scale so that it is on a greyscale

    y = int(spot/1557)  #Converts the spot values into the repective x and y coords
    x = spot-(y*1557)
    progressNew = (y/height*100)  #Creates the percent that has been completed
   
    if progressNew != progressOld:  #Instead of printing the progress for each line, I only print it when the progress percent has changed
        print(str(progressNew) + "%")

    newImage.putpixel((x, y), color)  #Putting the pixel on the image

    progressOld = progressNew  #Setting the new progress to old so that line 51 works

newImage.show()