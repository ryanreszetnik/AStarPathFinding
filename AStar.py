import pygame
import numpy as np
from random import random

class Node:
    def __init__(self, xpos, ypos, to_end):
        self.xpos = xpos
        self.ypos = ypos
        self.to_end = to_end
        self.from_start = -1
        self.parentX = -1
        self.parentY = -1
        self.isCalculated = False
        self.isFinalized = False
    
    def getValue(self):
        if self.from_start<0:
            return -1
        # print(self.from_start,self.to_end,self.from_start+self.to_end)
        return self.from_start+self.to_end

    def setFromStart(self,val, px, py):
        if not self.isCalculated:
            possibleNodes.append(self)
        if self.from_start <0 or val<self.from_start:
            self.from_start=val
            self.isCalculated=True
            self.setParent(px,py)
        
    def showPath(self):
        drawRect(self.xpos,self.ypos,(100,100,100),False)
        if self.parentX != -1 and self.parentY != -1:
            nodes[self.parentX][self.parentY].showPath()

    def setParent(self,xval, yval):
        self.parentX=xval
        self.parentY = yval
    
    def setCompleted(self):
        self.isFinalized=True
        possibleNodes.remove(self)
        doneNodes.append(self)
        if self.xpos == endX and self.ypos == endY:
            print(self.from_start)
            self.showPath()
            global notDone 
            notDone = False
            

def distance(x1,x2,y1,y2):
    disX = abs(x2-x1)
    disY = abs(y2-y1)
    minval= min(disX, disY)
    maxval = max(disX, disY)
    dis = minval*14+(maxval-minval)*10
    return dis

def setValue(x,y,px, py, val):
    if x>=num_tilesX or x<0 or y>=num_tilesY or y<0:
        return
    nodes[x][y].setFromStart(val,px,py)
    drawRect(x,y,(255,255,0),False)

def checkAround(x,y):
    nodes[x][y].setCompleted()
    drawRect(x,y,(0,255,255),False)
    startVal = nodes[x][y].from_start
    for cx in range(3):
        for cy in range(3):
            if not (cx==1 and cy==1) and cx-1+x in range(num_tilesX) and cy-1+y in range(num_tilesY):
                if not nodes[cx-1+x][cy-1+y].isFinalized and walls[cx-1+x][cy-1+y]==0:
                    val = distance(x,cx-1+x,y,cy-1+y)
                    setValue(cx-1+x,cy-1+y,x,y,val+startVal)
def drawRect(x,y,color,yes):

    if not (x==startX and y==startY or x==endX and y ==endY) or yes:
        xpos = x*(tile_size+gap)+gap
        ypos = y*(tile_size+gap)+gap
        pygame.draw.rect(screen,color,(xpos,ypos,tile_size,tile_size))
        pygame.display.update()

def run():
    val = possibleNodes[0].getValue()
    bestNode = possibleNodes[0]
    values = []
    # for n in range(len(possibleNodes)-1,-1,-1):
    for n in range(len(possibleNodes)):
        temp = possibleNodes[n].getValue()
        values.append(temp)
        if temp<val or temp == val and possibleNodes[n].to_end<bestNode.to_end:
            val = temp
            bestNode = possibleNodes[n]
    # print(bestNode.xpos, bestNode.ypos)
    checkAround(bestNode.xpos,bestNode.ypos)
    # print("BEST: ", val, " num Poss: ", len(possibleNodes), values)

def setWall(xcoord, ycoord):
    xpos =  int(xcoord/(tile_size+gap))
    ypos = int(ycoord/(tile_size+gap))
    if xpos in range(num_tilesX) and ypos in range(num_tilesY):
        # print(xpos,ypos)
        walls[xpos][ypos] = 1
        drawRect(xpos,ypos,(0,0,0),False)
    

rect_color = (255,255,255)
tile_size = 20
num_tilesX = 25
num_tilesY = 25
gap = 2

screen=pygame.display.set_mode([gap+num_tilesX*(gap+tile_size), gap+num_tilesY*(gap+tile_size)])
screen.fill([150, 150, 150])
pygame.display.set_caption('A*')
notDone = True


# [score,from_start,to_end, parentx, parenty]

walls = []
nodes = []
doneNodes = []
possibleNodes = []
running = True
startX = int(random()*num_tilesX)
startY = int(random()*num_tilesY)
endX = int(random()*num_tilesX)
endY = int(random()*num_tilesY)
for i in range(num_tilesX):
    row = []
    rowWalls = []
    for p in range(num_tilesY):
        rowWalls.append(0) 
        
        xpos = i*(tile_size+gap)+gap
        ypos = p*(tile_size+gap)+gap
        row.append(Node(i,p,distance(i,endX,p,endY)))
        if i == startX and p == startY:
            color = (0,255,0)
        elif i == endX and p == endY:
            color = (255,0,0)
        else:
            color = rect_color
        pygame.draw.rect(screen,color,(xpos,ypos,tile_size,tile_size))
    nodes.append(row)
    walls.append(rowWalls)
possibleNodes.append(nodes[startX][startY])
nodes[startX][startY].from_start=0
nodes[startX][startY].isCalculated=True
pygame.display.update()

fullRun = False

while running:
    if fullRun and notDone:
        run()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if notDone:
                    # print('space')
                    run()
            if event.key == pygame.K_RETURN:
                fullRun = True
        # if event.type == pygame.MOUSEPRESSED:
           
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                setWall(pos[0],pos[1])
            except AttributeError:
                pass


