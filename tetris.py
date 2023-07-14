import os
import time
import msvcrt
import random

#making a clear function
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

#display board
#update every one second
#if line full delete

#class for the nodes
class node():
    def __init__(self, x: int, y: int, isFull: bool):
        self.x = x
        self.y = y
        self.isFull = isFull
        self.simulatedPiece = False

class tetris():
    def __init__(self):
        self.rotations = ['left', 'down', 'right', 'up', 'left', 'up']
        self.alive = True
        self.movingPiece = False
        self.currPiece = node(0, 0, False)
        self.currPieceType = 2
        self.currRotation = "down"
        self.lastMove = time.time()
        self.nodeDic  = []
        self.simulatedPieces = []
        self.score = 0

        for y in range(0, 20):
            for x in range(0, 10):
                self.nodeDic.append(node(x, y, False))

        self.game()
    
    def getNode(self, x, y):
        return self.nodeDic[y*10+x]

    def testNode(self, x, y):

        if (x == -1)|(x == 10):
            return "hit"
        try:
            if self.getNode(x, y).isFull == True and self.getNode(x,y).simulatedPiece == False:
                return "hit"
            else:
                return self.nodeDic[y*10+x]
        except:
            return "hit"

    def printBoard(self):

        clear()
        print("")
        print("")
        for y in range(0, 20):
            line = "                  ||"
            for x in range(0, 10):
                if(self.getNode(x, y).isFull==True):
                    line = line[:-1] + "X" + line[-1:]
                else:
                    line = line[:-1] + " " + line[-1:]
            if y == 3:
                line = line + "  TETRIS"
            if y == 5 or y == 8:
                line = line + " ##########"
            if y == 6:
                line = line + " # SCORE: #"
            if y == 7:
                line = line + " # " + str(self.score) + "   #"
            if y == 10:
                line = line + " ####################"
            if y == 11:
                line = line + " # CONTROLS:        #"
            if y == 12:
                line = line + " # MOVE: A/D        #"
            if y == 13:
                line = line + " # ROTATE: N/M      #"
            if y == 14:
                line = line + " # HARD DROP: SPACE #"
            if y == 15:
                line = line + " # SOFT DROP: S     #"
            if y == 16:
                line = line + " ####################"
            
            print(line)
             
    def game(self):

        while(self.alive==True):

            if self.movingPiece == True:
                self.changeSPieces(self.currPieceType, False)

            if msvcrt.kbhit()==True:
                key = msvcrt.getch()
                
                if str(key) == "b'a'":
                    self.movePiece("left")
                if str(key) == "b'd'":
                    self.movePiece("right")
                if str(key) == "b's'":
                    if self.movingPiece!=False:
                        self.movePieceDown()
                if str(key) == "b' '":
                        while self.movingPiece==True:
                            self.changeSPieces(self.currPieceType, False)
                            self.movePieceDown()
                            

                if str(key) == "b'n'":
                    self.rotatePiece("left")
                if str(key) == "b'm'":
                    self.rotatePiece("right")
                    
            if (self.lastMove - time.time()+1) < 0:
                self.movePieceDown()

            if self.movingPiece == True:
                self.changeSPieces(self.currPieceType, True)
            

            self.printBoard()
            time.sleep(0.08)

    def createPiece(self):

        self.checkLineClear()
        node = self.getNode(4, 3)

        node.isFull = True

        self.currPieceType = random.randint(1, 7)
        self.currPiece = node
        self.currRotation = "down"

        self.movingPiece = True

    def rotatePiece(self, dir):
        blocked = False
        if dir == "left":
            newRotation = self.rotations[self.rotations.index(self.currRotation)-1]
        else:
            newRotation = self.rotations[self.rotations.index(self.currRotation)+1]
        
        for x in self.simulatePieces(self.currPieceType, newRotation):
            if self.testNode(x[0], x[1])=="hit":
                blocked = True
                break

        if blocked==False:
            self.currRotation = newRotation

    def movePieceDown(self):

        self.lastMove = time.time()

        if(self.movingPiece==False):

            self.createPiece()

        else:

            for x in self.simulatedPieces:

                if self.testNode(x[0], x[1]+1)=="hit":
                    
                    self.movingPiece = False
                    for node in self.simulatedPieces:
                        self.getNode(node[0], node[1]).isFull = True
                        self.getNode(node[0], node[1]).simulatedPiece = False
                    break

            if self.movingPiece == True:

                self.currPiece = self.getNode(self.currPiece.x, self.currPiece.y+1)

    def movePiece(self, dir):
        move = True
        if dir == "left":
            for x in self.simulatedPieces:

                if self.testNode(x[0]-1, x[1])=="hit":
                    move = False

            if move == True:

                self.currPiece = self.getNode(self.currPiece.x-1, self.currPiece.y)

        if dir == "right":
            for x in self.simulatedPieces:

                if self.testNode(x[0]+1, x[1])=="hit":
                    move = False
                    break

            if move == True:

                self.currPiece = self.getNode(self.currPiece.x+1, self.currPiece.y)
            
    #piece types:
    #1 SQUARE
    #2 I
    #3 L
    #4 rL
    #5 S
    #6 rS
    #7 T
    def simulatePieces(self, type, rotation):

        if type==1:
            simulated = [[self.currPiece.x, self.currPiece.y],
                        [self.currPiece.x+1, self.currPiece.y], 
                        [self.currPiece.x+1, self.currPiece.y+1], 
                        [self.currPiece.x, self.currPiece.y+1]]

        elif type==2:
            if rotation=="down":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y-2], 
                            [self.currPiece.x, self.currPiece.y-3]]

            elif rotation=="up":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y-2], 
                            [self.currPiece.x, self.currPiece.y-3]]

            elif rotation=="left":

                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x-2, self.currPiece.y], 
                            [self.currPiece.x-3, self.currPiece.y]]

            elif rotation=="right":              

                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x+2, self.currPiece.y], 
                            [self.currPiece.x+3, self.currPiece.y]]

        elif type==3:
            if rotation=="down":

                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y-2]]

            elif rotation=="up":

                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1], 
                            [self.currPiece.x, self.currPiece.y+2]]

            elif rotation=="right":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x-2, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1]]

            elif rotation=="left":
                
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x+2, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1]]

        elif type==4:
            if rotation=="down":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y-2]]

            elif rotation=="up":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1], 
                            [self.currPiece.x, self.currPiece.y+2]]

            elif rotation=="right":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x-2, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1]]

            elif rotation=="left":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x+2, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1]]   
            
        elif type==5:
            if rotation=="down":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x+1, self.currPiece.y-1]]

            elif rotation=="up":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1], 
                            [self.currPiece.x-1, self.currPiece.y+1]]

            elif rotation=="right":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x+1, self.currPiece.y+1], 
                            [self.currPiece.x, self.currPiece.y-1]]

            elif rotation=="left":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x-1, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y+1]]
                      
        elif type==6:
            if rotation=="down":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1], 
                            [self.currPiece.x+1, self.currPiece.y+1]]
            elif rotation=="up":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x-1, self.currPiece.y-1], 
                            [self.currPiece.x+1, self.currPiece.y]]
            elif rotation=="left":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x+1, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y+1]]
            elif rotation=="right":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x-1, self.currPiece.y+1], 
                            [self.currPiece.x, self.currPiece.y-1]]
        elif type==7:
            if rotation=="down":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y+1]]
            if rotation=="up":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1]]
            if rotation=="left":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x-1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y+1]]
            if rotation=="right":
                simulated = [[self.currPiece.x, self.currPiece.y],
                            [self.currPiece.x+1, self.currPiece.y], 
                            [self.currPiece.x, self.currPiece.y-1], 
                            [self.currPiece.x, self.currPiece.y+1]]
        
        return simulated

    def changeSPieces(self, type, isFull):
        
        self.simulatedPieces = self.simulatePieces(type, self.currRotation)
        for node in self.simulatedPieces:
                    self.getNode(node[0], node[1]).isFull = isFull
                    self.getNode(node[0], node[1]).simulatedPiece = isFull
        
    def checkLineClear(self):
        breakCount=0
        for y in range(0, 20):
            c=0
            for x in range(0, 10):
                if self.getNode(x,y).isFull == True:
                    c = c + 1
                else:
                    break

            if c==10:
                self.breakLine(y)
                breakCount = breakCount + 1

        if breakCount == 4:
            self.score = self.score + 800
        elif breakCount > 0:
            self.score = self.score + (breakCount*100)
            
    def breakLine(self, row):

        for x in range(0, 10):
            self.getNode(x , row).isFull = False

        for y in range(row, 0, -1):
            for x in range(0, 10):
                try:
                    if self.getNode(x, y).isFull == True:
                        self.getNode(x, y).isFull = False
                        self.getNode(x, y+1).isFull = True
                except:
                    break

tetris()
                
    
    


