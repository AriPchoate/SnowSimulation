'''
Height Map: https://en-us.topographic-map.com/map-4q8nh/Wallingford/?center=41.45721%2C-72.80699&zoom=15
Snow fall speed: https://www.metoffice.gov.uk/weather/learn-about/weather/types-of-weather/snow/10-facts-about-snow
    - "[high end] 9 mph(13.2 ft/sec)... will tend to... 1.5mph(2.2 ft/sec)"
    - random.triangular(0.5, 13.2, 2.2) 
Wind speeds: https://www.wunderground.com/history/monthly/us/ct/wallingford
    - "Average wind speed: 9.25 mph (13.56667 feet/second)"
    - "Ranging from 0 to 28 mph (41.0667 feet/second)"
    - triangular randomness
Wind direction: https://earthscience.stackexchange.com/questions/980/why-does-the-wind-periodically-change-direction
    - wind changes around 20 degrees every 5 minutes
Using photoshop:
    - 500 feet is 128 pixels
    - meaning 3.90625 feet per pixel
Image size (1557, 785) 1.98343949 : 1 aspect ratio around

https://www.britannica.com/science/snow-weather
    - snow falls at 16,000 feet on average

assuming 100 snowflakes per foot
1557 x 785 x 3.90625 x 100
590 x 311 x 3.90625 x 100

The average height is very close to 28m, more specifically 27.9995537111765
'''
from perlin_noise import PerlinNoise
import random
import numpy as np
from alive_progress import alive_bar
from PIL import Image
from math import *
from dataclasses import dataclass

cartoLightPath = "99Image.jpg"
# cartoLightPath = "./HeightMaps/Cartolightview.png"
cartoLight = Image.open(cartoLightPath).convert('RGB')
width, height = cartoLight.size[0], cartoLight.size[1]

def generateNoise(octs : int, size : tuple, scale = 1, shift = 0) -> list:
    noiseMap = PerlinNoise(octaves=octs)
    noiseValues = []
    with alive_bar(size[1]) as bar:
        for y in range(size[1]):
            bar()
            noiseValues.append([])
            for x in range(size[0]):
                noiseValues[y].append((noiseMap([y/size[0], x/size[1]]) + shift) * scale)
    return noiseValues

def generateImage(imgValues, size):
    img = Image.new("RGB", (size[0], size[1]))
    with alive_bar(size[0]) as bar:
        for x in range(size[0]):
            bar()
            for y in range(size[1]):
                value = np.clip(int(imgValues[x][y]), 0, 255)
                valueColor = (value, value, value)
                img.putpixel((x, y), valueColor)
    img.show()

def generateTerrain():
    print("\nGenerating terrain noise...")
    noiseValues = generateNoise(30, (width, height), 2.5)
    print("\nGenerating terrain height map...")
    heightMap = []
    with alive_bar(width) as bar:
        for x in range(width):
            bar()
            heightMap.append([])
            for y in range(height):
                # (151, 228, 244) lowest value in image
                # (96, 207, 255) lowest possible value
                # heightMap[x].append(dist(cartoLight.getpixel((x, y)), (141, 218, 234)) / 3)
                heightMap[x].append(dist(cartoLight.getpixel((x, y)), (141, 218, 234)) / 3 + noiseValues[y][x])
    
    print("\nGenerating terrain height map image...")
    generateImage(heightMap, (width, height))
    return heightMap

def lerpColor(color1, color2, t):
    blend = []
    for i in range(3):
        blend.append(int(color1[i] * (1 - t) + color2[i] * t))
    return tuple(blend)

@dataclass
class Vector:
    dir : float = 0.0
    mag : float = 0.0

class Snowflake:
    def __init__(self, pos = [0, 0, 0], velocity2D = Vector()) -> None:
        self.pos = pos
        self.velocity2D = velocity2D

    def updatePos(self):
        self.pos[0] += self.velocity2D.mag * cos(self.velocity2D.dir)
        self.pos[1] += self.velocity2D.mag * sin(self.velocity2D.dir)
        self.pos[2] -= random.triangular(0.5, 13.2, 2.2) 

    def updateVelocity(self, mainWind):
        self.velocity2D.dir = mainWind.dir + random.uniform(-pi/18, pi/18)
        self.velocity2D.mag = np.clip(mainWind.mag + random.uniform(-1.0, 1.0), 0, 6)

    def respawn(self):
        self.pos = [random.randint(0, width), random.randint(0, height), random.randint(28, 40)]
        self.velocity2D.mag = 0
        self.velocity2D.dir = 0

def startSnow(snowflakeList, startHeight):
    if startHeight >= 55:
        return
    for x in range(width):
        for y in range(height):
            snowflakeList.append(Snowflake([random.randint(0, width), random.randint(0, height), startHeight]))
    startSnow(snowflakeList, startHeight + 5)

terrainHeight = generateTerrain()

chunkNum = [width, height]
chunkSpacing = [width / chunkNum[0], height / chunkNum[1]]
chunkMatrix = [[0 for y in range(chunkNum[1])] for x in range (chunkNum[0])]

snowflakeList = []
startSnow(snowflakeList, 50)

# mainWind = Vector(pi / 2, 41.0)
mainWind = Vector(random.uniform(0, 2 * pi), 41.0667)
# mainWind = Vector(random.uniform(0, 2 * pi), random.triangular(0, 41.0667, 13.56667))

print("\nSimulating snow...")
secondNum = 3600 # one hour
seconds = 0
with alive_bar(secondNum) as bar:
    while seconds < secondNum:
        for snowflake in snowflakeList:
            snowflake.updateVelocity(mainWind)
            snowflake.updatePos()
            try:
                if snowflake.pos[2] <= terrainHeight[int(snowflake.pos[0])][int(snowflake.pos[1])]:
                    chunkMatrix[int(snowflake.pos[0] / chunkSpacing[0])][int(snowflake.pos[1] / chunkSpacing[1])] += 1
                    snowflake.respawn()
            except:
                continue
        
        mainWind.dir += random.uniform(-2.52, 2.52)

        seconds += 1
        bar()

highestChunk = 0
for row in chunkMatrix:
    for chunk in row:
        if chunk > highestChunk:
            highestChunk = chunk

lowColor = (0, 0, 0)
highColor = (255, 255, 255)
# lowColor = (144, 78, 149)
# highColor = (233, 100, 67)
print("\nGenerating final result...")
finalResults = Image.new("RGB", chunkNum)
with alive_bar(chunkNum[0]) as bar:
    for x in range(chunkNum[0]):
        bar()
        for y in range(chunkNum[1]):
            finalResults.putpixel((x, y), lerpColor(lowColor, highColor, chunkMatrix[x][y] / highestChunk))

finalResults.show()