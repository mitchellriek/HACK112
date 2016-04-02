# HACK112

from pydub import AudioSegment
import pygame
from pydub.playback import play

def getTrack(trackName): # sets up track on computer
    track = AudioSegment.from_file(trackName, format="wav")
    return track

def repeatTrack(track):
    newTrack = track + track
    return newTrack

def updateTrack(track, path):
    fileHandle = track.export(path, format='wav')
    return fileHandle

def getSegment(track, startTime, endTime):
    segment = track[startTime:endTime]
    return segment

def insertSegment(track, segment, time):
    firstPart = track[:time]
    secondPart = track[time:]
    newTrack = firstPart + segment + secondPart
    return newTrack

def changeVolume(track, dVolume):
    newTrack = track + dVolume
    loudness = newTrack.dBFS
    if loudness > 0:
        print(loudness)
        changeVolume(newTrack, -1)
    return newTrack

def reverseTrack(track):
    newTrack = track.reverse()
    return newTrack

def recursiveEcho(track, echoCount=2, delayLength=200):
    if echoCount <= 0:
        return track
    else:
        silence = AudioSegment.silent(duration=delayLength)
        currentTrack = silence + track
        return (currentTrack.overlay(recursiveEcho(currentTrack-20//echoCount, echoCount-1, delayLength))) 

def getRectangleSizes(track):
    trackLength = len(track)
    segLength = trackLength // 1000
    segmentEnergies = []
    for segStart in range(0, trackLength - segLength+1, segLength):
        segment = track[segStart:segStart+segLength]
        energy = segment.rms
        segmentEnergies.append(energy)
    return segmentEnergies

def saveFile(newTrack):
    text = input('Save Song as ---> ')
    path = "/Users/Mitchell/Documents/freshman year/spring 2016/15-112/%s"%(text)
    updateTrack(newTrack, path)

def loadFile():
    text = input('Track Name ---> ')
    track = getTrack(text)
    return track

def interLeaveSongs(length = 2):
    track1 = loadFile()
    track2 = loadFile()
    segments1 = []
    segments2 = []
    for startTime in range(0, len(track1), length*1000):
        segment = track1[startTime:startTime+length*1000]
        segments1.append(segment)
    for startTime in range(0, len(track2), length*1000):
        segment = track2[startTime:startTime+length*1000]
        segments2.append(segment)
    newTrack = interleave(segments1, segments2)
    newSong = AudioSegment.silent(duration=1)
    for segment in newTrack:
        newSong += segment
    return newSong

def interleave(list1, list2): #taken from notes
    # assume list1 and list2 are same-length lists
    if (len(list1) == 0):
        return []
    elif (len(list1) == 1):
        return [list1[0], list2[0]]
    else:
        mid = len(list1)//2
        return (interleave(list1[:mid], list2[:mid]) +
                interleave(list1[mid:], list2[mid:]))

def panTrack(track, dPan):
    newTrack = track.pan(dPan)
    return newTrack

########################################################
# Visual
########################################################

pygame.init()
clock = pygame.time.Clock()
# create the display surface
screen = pygame.display.set_mode((600, 600))
playing = True
#colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
purple = (255,0,255)
colorList = [red, green, blue, darkBlue, purple, pink]
buttonList = [(0,400,200,100),(200,400,200,100),(400,400,200,100),
              (0,500,200,100),(200,500,200,100),(400,500,200,100)]
buttonNames = ['Echo', 'Repeat', 'Reverse', 'Volume', 'Interleave', 'Pan']
currentlyPlaying = False
volumePressed = False
panPressed = False
startLoad = True
dB = 0
startX = 25
width = 550
track = AudioSegment.silent(duration=10000)
percent = 0
percentChange = 0
pygame.display.set_caption("Strawberry Beats v4.20 // by wpchu, jdangrem, mriek, jrrubens")
def almostEqual(d1, d2):
    epsilon = 10**(-3)
    return abs(d1-d2) <= epsilon
def mousePressed(event):
    global percentChange
    global currentlyPlaying
    global volumePressed
    global dB
    global track
    global panPressed
    global percent
    global startLoad
    myfont = pygame.font.SysFont("monospace", 25)
    (event.x, event.y) = event.pos 
    listOfLines = getRectangleSizes(track)
    for i in range(len(buttonList)):
        (x1,y1,width,height) = buttonList[i]
        (xPos, yPos) = event.pos
        if (x1 < xPos < x1 + width) and (y1 < yPos < y1 + height):
            pygame.draw.rect(screen, green, (x1+2,y1+2,width-4,height-4))
            label = myfont.render(buttonNames[i], 1, (255,0,0))
            screen.blit(label, (x1+25, y1))
            if i == 0:
                track = recursiveEcho(track)
                listOfLines = getRectangleSizes(track)
                if startLoad == False:
                    drawSong(listOfLines)
            if i == 1:
                track = repeatTrack(track)
                listOfLines = getRectangleSizes(track)
                pygame.draw.rect(screen,white,(startX-(width//len(listOfLines)),15,
                    560,105))
                if startLoad == False:
                    drawSong(listOfLines)
            if i == 2:
                track = reverseTrack(track)
                listOfLines = getRectangleSizes(track)
                pygame.draw.rect(screen,white,(startX-(width//len(listOfLines)),15,
                    560,105))
                if startLoad == False:
                    drawSong(listOfLines)
            if i == 3:
                volumePressed = True
                increaseVol = myfont.render("+",1,(0,0,0))
                screen.blit(increaseVol,(x1+150,y1+25))
                pygame.draw.rect(screen,black,(x1+148,y1+28,20,20),2)
                decreaseVol = myfont.render("-",1,(0,0,0))
                screen.blit(decreaseVol,(x1+150,y1+50))
                pygame.draw.rect(screen,black,(x1+148,y1+53,20,20),2)
                decibels = myfont.render("dB:"+str(dB),1,(0,0,0))
                screen.blit(decibels,(x1+50,y1+35))
            if i == 4:
                num = input('How many seconds do you want to interleave? ---> ')
                track = interLeaveSongs(int(num))
                startLoad = False
            if i == 5:
                panPressed = True
                rightSide = myfont.render("R",1,(0,0,0))
                screen.blit(rightSide,(x1+150,y1+45))
                pygame.draw.rect(screen,black,(x1+148,y1+48,20,20),2)
                leftSide = myfont.render("L",1,(0,0,0))
                screen.blit(leftSide,(x1+25,y1+45))
                pygame.draw.rect(screen,black,(x1+23,y1+48,20,20),2)
                percentage = myfont.render(str(percent)+"%",1,(0,0,0))
                screen.blit(percentage,(x1+65,y1+45))
            if volumePressed:
                if x1+148 < event.x < x1+168:
                    if y1+28 < event.y < y1+48:
                        if dB < 10:
                            dB += 1
                            track = changeVolume(track, 1)
                    elif y1+53 < event.y < y1+73:
                        if dB > -10:
                            dB -= 1
                            track = changeVolume(track, -1)
            if panPressed:
                if y1+48 < event.y < y1+68:
                    if x1+148 < event.x < x1+168:
                        if percent < 100:
                            percent += 5
                            percentChange += 0.05
                            if almostEqual(percentChange,1.0):
                                percentChange = 1.0
                    elif x1+23 < event.x < x1+43:
                        if percent > -100:
                            percent -= 5
                            percentChange += -0.05
                            if almostEqual(percentChange,-1.0):
                                percentChange = -1.0
        else:
            pygame.draw.rect(screen, white, (x1+2,y1+2,width-4,height-4))
            label = myfont.render(buttonNames[i], 1, (255,0,0))
            screen.blit(label, (x1+25, y1))
            if i == 3:
                increaseVol = myfont.render("+",1,(0,0,0))
                screen.blit(increaseVol,(x1+150,y1+25))
                pygame.draw.rect(screen,black,(x1+148,y1+28,20,20),2)
                decreaseVol = myfont.render("-",1,(0,0,0))
                screen.blit(decreaseVol,(x1+150,y1+50))
                pygame.draw.rect(screen,black,(x1+148,y1+53,20,20),2)
                decibels = myfont.render("dB:"+str(dB),1,(0,0,0))
                screen.blit(decibels,(x1+50,y1+35))
            if i == 5:
                rightSide = myfont.render("R",1,(0,0,0))
                screen.blit(rightSide,(x1+150,y1+45))
                pygame.draw.rect(screen,black,(x1+148,y1+48,20,20),2)
                leftSide = myfont.render("L",1,(0,0,0))
                screen.blit(leftSide,(x1+25,y1+45))
                pygame.draw.rect(screen,black,(x1+23,y1+48,20,20),2)
                percentage = myfont.render(str(percent)+"%",1,(0,0,0))
                screen.blit(percentage,(x1+65,y1+45))
    if 200 < event.x < 400 and 300 < event.y < 375:
        drawSong(listOfLines)
        currentlyPlaying = not(currentlyPlaying)
        drawPlayButton(currentlyPlaying)
        track = panTrack(track, percentChange)
        pygame.display.update()
        play(track)
        currentlyPlaying = not(currentlyPlaying)
        drawPlayButton(currentlyPlaying)
        pygame.display.update()
    if 140 < event.y < 180:
        if 25 < event.x < 105:
            track = loadFile()
            startLoad = False
        elif 115 < event.x < 195:
            saveFile(track)
            print('File Successfully Saved!')
        else:
            drawLoadSave(0)
    pygame.display.update()

def gameInit():
    global currentlyPlaying
    global dB
    global percent
    listOfLines = getRectangleSizes(track)
    myfont = pygame.font.SysFont("monospace", 25)
    screen.fill(white)
    for i in range((len(buttonList))):
        button = buttonList[i]
        pygame.draw.rect(screen, black, button)
        (x1,y1,width,height) = button
        pygame.draw.rect(screen, white, (x1+2,y1+2,width-4,height-4))
        label = myfont.render(buttonNames[i], 1, (255,0,0))
        screen.blit(label, (x1+25, y1))
        if i == 3:
            increaseVol = myfont.render("+",1,(0,0,0))
            screen.blit(increaseVol,(x1+150,y1+25))
            pygame.draw.rect(screen,black,(x1+148,y1+28,20,20),2)
            decreaseVol = myfont.render("-",1,(0,0,0))
            screen.blit(decreaseVol,(x1+150,y1+50))
            pygame.draw.rect(screen,black,(x1+148,y1+53,20,20),2)
            decibels = myfont.render("dB:"+str(dB),1,(0,0,0))
            screen.blit(decibels,(x1+50,y1+35))
        if i == 5:
            rightSide = myfont.render("R",1,(0,0,0))
            screen.blit(rightSide,(x1+150,y1+45))
            pygame.draw.rect(screen,black,(x1+148,y1+48,20,20),2)
            leftSide = myfont.render("L",1,(0,0,0))
            screen.blit(leftSide,(x1+25,y1+45))
            pygame.draw.rect(screen,black,(x1+23,y1+48,20,20),2)
            percentage = myfont.render(str(percent)+"%",1,(0,0,0))
            screen.blit(percentage,(x1+65,y1+45))
    drawSong(listOfLines)
    drawPlayButton(currentlyPlaying)
    drawLoadSave()
    
def drawLoadSave():
    pygame.draw.rect(screen,black,(25,140,80,40),2)
    myfont = pygame.font.SysFont("monospace", 25)
    load = myfont.render("Load",1,(0,0,0))
    screen.blit(load,(35,150))
    pygame.draw.rect(screen,black,(115,140,80,40),2)
    save = myfont.render("Save",1,(0,0,0))
    screen.blit(save,(125,150))

def drawSong(listOfLines):
    global startLoad
    global startX
    global width
    maxinList = max(listOfLines)
    if maxinList != 0:
        pygame.draw.rect(screen,white,(startX-(width//len(listOfLines)),15,
                    width+(width//len(listOfLines)),105))
        for i in range(len(listOfLines)):
            x = (i * (width/len(listOfLines))) + startX
            bottomY = 120
            topY = bottomY - ((listOfLines[i]/maxinList) * 100)
            pygame.draw.line(screen, red,(x,bottomY),(x,topY),1)
    if startLoad:
        myfont = pygame.font.SysFont("monospace", 25)
        load = myfont.render("Please Load A File",1,(0,0,0))
        screen.blit(load,(170,60))
    pygame.draw.rect(screen,black,(startX-(width//len(listOfLines)),15,
                    width+(width//len(listOfLines)),105),2)
    pygame.display.update()

def drawPlayButton(currentlyPlaying):
    if currentlyPlaying == False:
        pygame.draw.rect(screen,black,(200,300,200,75),2)
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("Play",1,(0,0,0))
        screen.blit(label, (210,325))
        pygame.draw.polygon(screen,red,((300,315),(300,360),(350,337.5)))
        pygame.draw.rect(screen,white,(180,240,240,60))
    elif currentlyPlaying:
        pygame.draw.rect(screen,red,(200,300,200,75),2)
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("Play",1,(255,0,0))
        screen.blit(label, (210,325))
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("Playing song...",1,(0,0,0))
        screen.blit(label, (180,265))
        pygame.draw.polygon(screen,black,((300,315),(300,360),(350,337.5)))

gameInit()

pygame.display.update()

while playing:
    time = clock.tick(100) # waits for the next frame
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed(event)
        if event.type == pygame.QUIT:
            playing = False
pygame.quit()