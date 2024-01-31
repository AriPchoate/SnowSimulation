'''
Ari, Aureliano
Date: 2/2/24
Sources:
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
    Average snow fall : https://training.fema.gov/emiweb/downloads/is111_unit%206.pdf
        - on average 0.5 inches per hour
 
Reflection: A lot of work was put into this project. Originally we thought of doing a much simpiler simulation just on a small 3d object, but there was an idea of scaling it up to Choate and the area around choate. We first had to find a height map of wallingford which turned out to be one of the most challenging aspects of the simulation. Originally the heightmap included unnecessary overlays of roads, buildings, and text, which messed up the simulation. We wrote a program to remove all of the unnecessary things. The next problem we ran into was with how the height map represented its values, a gradient from blue to green to yellow to red. This is very clear to the human eye but a lot harder for a computer to understand. Our first thought was to imagine the colors in 3d space and take the distance between the color coordinate and the lowest possible color. (R, G, B) would correspond to (X, Y, Z). However the green was a lot closer to the red which gave us a height map where the blue was really low and the green and red were about the same height and really high. Our next idea was to convert the image to CMY(see HeightGen.py for explanation), which was the idea we ended up sticking with. The simulation itself was coded off of many factors and research. We researched the terminal velocity of snowflakes, wind patterns and movement, rate of change of wind's direction, and the general fall speed of snow. The simulation code came together generally well with little issues, the harderst and most tedious part was extracting the data from the height map. There are many things that we can improve on. Around the edges of the final image we see that there is very little snow. This is because the wind carries the snow either away from the edges or it carries it all the way to the edge of the image; when the snowflake hits the edge it's respawned randomly for simplicity. In order to increase the amount of snow fall on the edges we could increase the area of snowfall, extending it beyond the image around 500 feet.

On my honor
'''
from perlin_noise import PerlinNoise
import random
import numpy as np
from alive_progress import alive_bar
from PIL import Image
from math import *
from math import pi
from dataclasses import dataclass

# Image set up
heightMapPath = "./Images/FinalHeight.png"  #This image holds our height map
heightMapImg = Image.open(heightMapPath).convert('RGB')
width, height = heightMapImg.size[0], heightMapImg.size[1]  # 992x540

# Generates an extra level of detail, may not be more accurate but it will be more realistic
def generateNoise(octs : int, size : tuple, scale = 1, shift = 0) -> list:
    print("\nGenerating terrain noise...")
    # Creates the PerlinNoise object
    # Octaves is just the frequency of the height change
    noiseMap = PerlinNoise(octaves=octs) 
    noiseValues = [] # initializes a matrix for the height values
    with alive_bar(size[1]) as bar:
        for y in range(size[1]):
            bar()
            noiseValues.append([])
            for x in range(size[0]):
                # Iterates through every coordinate and extracts the height value
                # Shift adds or subtracts a value from all of the height values
                # Scale multiplys or divides a vale from all of the height values
                noiseValues[y].append((noiseMap([y/size[0], x/size[1]]) + shift) * scale)
    return noiseValues

# Code to generate the height value image
def generateImage(imgValues, size):
    print("\nGenerating terrain height map image...")
    # Initializes the image
    img = Image.new("RGB", (size[0], size[1]))
    with alive_bar(size[0]) as bar:
        for x in range(size[0]):
            bar()
            for y in range(size[1]):
                # Iterates through every pixel and places a pixel with the given color
                value = np.clip(int(imgValues[x][y]), 0, 255)
                # 3 element tuple becaue put pixel couldnt take a single number as input
                valueColor = (value, value, value) 
                img.putpixel((x, y), valueColor)
    # img.show()  #NOTE: Uncomment

def generateTerrain(img, hasNoise = False):
    # Adds an extra level of detail
    if hasNoise == True:
        noiseValues = generateNoise(30, (width, height), 2.5)
    
    print("Extracting Height values...")
    heightMap = []
    with alive_bar(width) as bar:
        # Iterates through every pixel
        for x in range(width):
            bar()
            heightMap.append([])
            for y in range(height):
                # Since the height map is in black and white the rgb values for a specific color are all the same
                # for example (79, 79, 79) so to extract the height it takes the first value
                if hasNoise == True:
                    # Adds the extra noise detai 
                    heightMap[x].append(img.getpixel((x, y))[0] + noiseValues[y][x])
                else:
                    # getpixel returns a color tuple
                    heightMap[x].append(img.getpixel((x, y))[0])
    
    # generateImage(heightMap, (width, height))
    return heightMap

@dataclass
class Vector:
    dir : float = 0.0
    mag : float = 0.0

class Snowflake:
    def __init__(self, pos = [0, 0, 0], velocity2D = Vector()) -> None:
        self.pos = pos
        self.velocity2D = velocity2D # initialized as an empty Vector

    def updatePos(self):
        # Takes the x and y components of the velocity vector and adds it to the position
        self.pos[0] += self.velocity2D.mag * cos(self.velocity2D.dir)
        self.pos[1] += self.velocity2D.mag * sin(self.velocity2D.dir)
        # Based off of the data colleted snow falls at a speed between 0.5 and 13.2 f/s but on average 2.2 f/s
        self.pos[2] -= random.triangular(0.5, 13.2, 2.2) 

    def updateVelocity(self, mainWind):
        # Takes in the general direction of the wind and applies a slight offset of 10 degrees
        self.velocity2D.dir = mainWind.dir + random.uniform(-pi/18, pi/18)
        # offsets based off the general wind magnitude
        # Terminal velocity is 6 f/s, caps it at that
        self.velocity2D.mag = np.clip(mainWind.mag + random.uniform(-1.0, 1.0), 0, 6)

    def respawn(self):
        # respawns the snowflake once it lands in order to safe memory and reuse objects
        self.pos = [random.randint(0, width), random.randint(0, height), random.randint(180, 200)]
        self.velocity2D.mag = 0
        self.velocity2D.dir = 0

terrainHeight = generateTerrain(heightMapImg)

chunkNum = [width, height]
# chunkNum = [int(width / 4), int(height / 4)]
chunkSpacing = [width / chunkNum[0], height / chunkNum[1]]
chunkMatrix = [[0 for y in range(chunkNum[1])] for x in range (chunkNum[0])]

snowflakeList = [Snowflake() for y in range(height) for x in range(width)]
for snowflake in snowflakeList:
    snowflake.respawn()

mainWind = Vector(3*pi / 2, 41.0667)
# mainWind = Vector(random.uniform(0, 2 * pi), 41.0667)
# mainWind = Vector(random.uniform(0, 2 * pi), random.triangular(0, 41.0667, 13.56667))

# --------------------- MAIN SIMULATION ---------------------
print("\nSimulating snow...")
secondNum = 60 * 60  #Amount of seconds that the sim will run
seconds = 0  #Keeps track of amount of seconds that have been simulated
with alive_bar(secondNum) as bar:
    # Simulates each second of snowfall
    # Seconds because most of the data was in feet per second
    while seconds < secondNum:
        for snowflake in snowflakeList:
            # Iterates through every snowflake
            # Updates velocity and position based on a wind vector
            snowflake.updateVelocity(mainWind)
            snowflake.updatePos()

            # If statement to check if the snowflakes position is within range of the focused area
            # Checks if the snowflake is still in bounds
            if (0 <= snowflake.pos[0] < width) and (0 <= snowflake.pos[1] < height):
                # Checks to see if the snowflake has landed yet
                # If the height of the snowflake is less than the height value at the given terrain (x, y) position -> intersection
                if snowflake.pos[2] <= terrainHeight[int(snowflake.pos[0])][int(snowflake.pos[1])]:
                    # Updates the chunk's data
                    chunkMatrix[int(snowflake.pos[0] / chunkSpacing[0])][int(snowflake.pos[1] / chunkSpacing[1])] += 1
                    # Respanws the snowflake for memory and performance optimization
                    snowflake.respawn()
            else:
                # If the snowflake goes out of bounds then respawn it
                snowflake.respawn()

            # research shows that the wind changes around 20 degrees every 5 minutes
            # Updates the wind vector direction by 2.52 in either direction
            # See windChangeValue.py file
            mainWind.dir += random.uniform(-0.04358, 0.04358)

        seconds += 1
        bar()
# -----------------------------------------------------------

dataFile = "./data/data-Temp.txt"

#Stores the data in a text file so that we could mess around with the algorithm without having to run the sim every time
def storeData(filePath, data):
    with open(filePath, 'w') as file:
        with alive_bar(len(data)) as bar:
            for line in data:   #Each line is one chunk of the chunkMatrix
                file.write(str(line))
                file.write("\n")
                bar()

print("\nStoring snow data...")
storeData(dataFile, chunkMatrix)