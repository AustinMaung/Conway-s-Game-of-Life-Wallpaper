import os
import ctypes
from PIL import Image
import numpy
import random
import time

#global variables
resolution = 40

def getScreenSize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(screensize)
    return screensize

def createArray(screensize):# Create a 1024x1024x3 array of 8 bit unsigned integers
    data = numpy.zeros((screensize[1], screensize[0], 3), dtype=numpy.uint8)#col = x value, row = y
    return data

def square(data,x,y,res,color):
    for i in range(res - 5):# subtract 5 to add lines to the board
        for j in range(res - 5):
            data[i + x][j + y] = color

def firstGen(data):
    cols = (int)(data.shape[0] / resolution)#amount of squares that can fit on x axis
    rows = (int)(data.shape[1] / resolution)#amount of squares that can fit on y axis
    #print(str(cols) + " " + str(rows))

    gameBoard = numpy.zeros((cols, rows), dtype=numpy.uint8)#create 2d array that stores 1 or 0's
    
    #randomize the values in gameBoard
    for i in range(cols):
        for j in range(rows):
            gameBoard[i][j] = random.randint(0,1)
   
    return gameBoard
    
def convertBoardToData(gameBoard,data):
    WHITE = [255,255,255] #color of squares
    BLACK = [0,0,0]
    #resolution = 40#size of squares
    cols = gameBoard.shape[0]
    #print(cols)
    rows = gameBoard.shape[1]

    #change the appropriate pixel data to the gameboard data
    for i in range(cols):
        for j in range(rows):
            if gameBoard[i][j] == 1:
                square(data,i * resolution, j * resolution,40,WHITE)
            else:
                square(data,i * resolution, j * resolution,40,BLACK)
    return data


def createImage(data):#creates an image from array data and returns name of image for reference
    imageName = 'createdImage.png'

    if os.path.isfile(imageName):
        os.remove(imageName)
        print("File Removed!")        

    image = Image.fromarray(data)
    image.save(imageName)
    return imageName

def drawToWallpaper(imageName):
    print(imageName)
    path_user = os.path.expanduser('~')
    print(path_user) # this print C:\Users\teckn

    path_to_file = os.path.join(path_user, 'Documents', 'Projects', 'Python', imageName)
    print(path_to_file) # this print C:\Users\teckn\Pictures\Saved Pictures

    #set wallpaper to png
    SPI_SETDESKWALLPAPER = 20
    value = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path_to_file, 0)
    #print("done")

def countNeighbors(gameboard,x,y):
    cols = gameboard.shape[0]
    rows = gameboard.shape[1]
    count = 0

    for i in range(-1,2):
        for j in range(-1,2):
            newX = (x + i + cols) % cols
            newY = (y + j + rows) % rows
            count += gameboard[newX][newY]

    count -= gameboard[x][y]
    return count

def loop(gameboard,data):
    updatedData = convertBoardToData(gameboard,data)
    image = createImage(updatedData)
    drawToWallpaper(image)

    cols = gameboard.shape[0]
    rows = gameboard.shape[1]
    newboard = numpy.zeros((cols, rows), dtype=numpy.uint8)

    for i in range(cols):
        for j in range(rows):
            current = gameboard[i][j]
            neighbors = countNeighbors(gameboard,i,j)

            if current == 0 and neighbors == 3:
                newboard[i][j] = 1
            elif current == 1 and neighbors < 2 or neighbors > 3:
                newboard[i][j] = 0
            else:
                newboard[i][j] = current
    loop(newboard,updatedData)

def main():
    screenSize = getScreenSize()
    data = createArray(screenSize)
    gameboard = firstGen(data)
    loop(gameboard,data)

main()
