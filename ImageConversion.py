from PIL import Image
import statistics, math

dimx, dimy = 1557, 785

newImage = Image.new("RGB", (dimx, dimy))

img = Image.open("Cartolightview.png")
img.convert("RGB")

width, height = img.size

values = []

for y in range(0, height):
    for x in range(0, width):  
        points = img.getpixel((x,y))
        values.append(points[:-1])

firstImage = False
progressOld = 0
print("0%")
finalPix = []
deviation = 30
for spot in range(len(values)):
# for spot in range(600000, 600002):
    
    pixlist = []
    r, g, b = values[spot][0], values[spot][1], values[spot][2]
    for y in range(-30, 31):
        for x in range(-30, 31):
            pixTry = spot+(y*1557)+x
            try:
                pix = values[pixTry]
                if r-pix[0] < deviation and g-pix[1] < deviation and b-pix[2] < deviation:
                    pixlist.append(pix)
            except:
                continue
    

    red = 0
    green = 0
    blue = 0

    for val in pixlist:
        red += val[0]
        green += val[1]
        blue += val[2]

    
    length = len(pixlist)
    avR, avG, avB = round(red/length), round(green/length), round(blue/length)
    color = (avR, avG, avB)

    

    y = int(spot/1557)
    x = spot-(y*1557)
    progressNew = (y/dimy*100)
    
    if progressNew != progressOld:
        print(str(progressNew) + "%")

    # newImage.putpixel((x, y), color)

    if progressNew > 10 and firstImage == False:
        firstImage = True
        newImage.show()


    progressOld = progressNew

newImage.show()

