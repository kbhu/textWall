# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:45:21 2018

@author: K
"""

import sys, getopt
from PIL import ImageDraw, ImageFont, Image

#TODO: Fix this, brightness overlaps to white too often
def bright(brightness, color):
    #Brighten it? for now, 1.3x
    color[:] = [x * 1.3 for x in color]
    
    #if no values above 255, then there's no problem.
    if max(color) <= 255:
        return (int(color[0]), int(color[1]), int(color[2]))
    

    sumColor = color[0] + color[1] + color[2]
    
    #If all values are greater than 255, set them all to 255
    if sumColor >= 3 * 255:
        return (255, 255, 255)
    
    #redistribute, for a more true color if there are some values above 255.
    x = (3 * 255 - sumColor) / (3 * max(color) - sumColor)
    gray = 255 - x * max(color)
    return (int(gray + x * color[0]), int(gray + x * color[1]), int(gray + x * color[2]))
    

def getAvgColor(rgb):
    color = [0, 0, 0]
    for rgbVal in rgb:
        color[0] += rgbVal[0]
        color[1] += rgbVal[1]
        color[2] += rgbVal[2]
    
    for i in range(3):
        color[i] = round(color[i] / (7 * 12))

    #Brightness draft 1, makes colors more vibrant but not bright, if that makes sense?
    """
    for i in range(3):
        if color[i] == max(color) and color[i] <= 225:
            color[i] += 30
    """
    
    return bright(1.3, color)        
    #return (color[0], color[1], color[2])

def centerImg(width, height):
    startPos = []
    startPos.append(int((1920 - width) / 2))
    startPos.append(int((1200 - height) / 2))
    
    return startPos
    

def generateText(pixels, width, height, word, newImage):

    rgb = []
    fnt = ImageFont.truetype('Monospace.ttf', 12)
    write = ImageDraw.Draw(newImage)
    #Go through, traverse entire width for each pixel of height.
    
    #TODO: find the pixel height/width for each letter using monospace font, with a fixed size
    #, then change increment to match.\
    
    #For now, just use 12 pt monospace as the default. w[7, 12]h
    #line spacing is 3-4 pixels. 4 is probably cleaner? 
    
    #Need to calculate the number of spaces needed, given length of the word and the width of the picture
    #wordXwordXwordXword
    numSpace = int((width / 7) / (len(word) + 1))
    
    #Use one space for now
    word += " "
    #print("1 space, goes till width: " + str((numSpace * len(word) * 7)))
    
    heightBound = int(height / 12) * 12
    widthBound = numSpace * len(word) * 7
    
    startPos = centerImg(widthBound, heightBound)
    textPositionVertical = startPos[1]

    for h in range(0, heightBound, 12):
        i = 0
        textPositionHorizontal = startPos[0]
        textPositionVertical += 12        
        for w in range(0, widthBound):
            
            if w % 7 == 0:
                #Gets the rgb color codes for pixels in a 7 x 12 pixel area, the size of one character.
                for heightNum in range(h, h + 12):
                    for widthNum in range(w, w + 7):
                        rgb.append(pixels[widthNum, heightNum])
                
                charColor = getAvgColor(rgb)
                #print(charColor)
                
            
                if i != len(word):
                    #Width, height for the .text function.
                    write.text((textPositionHorizontal, textPositionVertical), word[i], font = fnt, fill = charColor)
                else:
                    i = 0
                    write.text((textPositionHorizontal, textPositionVertical), word[i], font = fnt, fill = charColor)
                    
                i += 1
                textPositionHorizontal += 7
                
            rgb.clear()


    newImage.save("testimg.png")
    return
    
    
if __name__ == "__main__":
    
    #takes in the list of arguments.
    cmdArgs = sys.argv[1:]
    r = g = b = 0
    
    if (("-h" or "-help") in cmdArgs):
        print("Usage: \n -i {filename} to select base image \n -w {word}     to select word \n -c {r g b}    to select background color. Default is black")
    
    #Could have made this simpler by not using a loop, and having fixed positions for each flag, but this allows for flexibility in order/using not using flags.
    #Only checks that there are values at index positions, type checking still needs to be done
    for i in range(len(cmdArgs)):
        try:
            if cmdArgs[i] == "-i":
                imageName = cmdArgs[i + 1]
            elif cmdArgs[i] == "-w":
                theWord = cmdArgs[i + 1]
            elif cmdArgs[i] == "-c":
                r = cmdArgs[i + 1]
                g = cmdArgs[i + 2]
                b = cmdArgs[i + 3]
        except IndexError:
            print("Incorrect number of arguments. Use -h or -help to see proper usage.")
            sys.exit(0)
     
    #theWord = "toucan"
    
    #TODO: Type checking for passed in variables.
    
   #try:
    image = Image.open(imageName)
    #except IOError:
        #print("An error occured opening the file.")
        #sys.exit(0)
    #image = Image.open("vaporeon.jpeg")
    pixel = image.load()
    width, height = image.size
    print(f"Width: {width}, Height: {height}")
    
    newImage = Image.new('RGB', (1920, 1200), color = (r, g, b)) 
    #newImage = Image.new('RGB', (1920, 1200), color = (21,25, 30))

    
    generateText(pixel, width, height, theWord, newImage)




#openImage()
#main()