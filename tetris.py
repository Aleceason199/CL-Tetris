import os
import time
import msvcrt
import random

#Making a clear function.
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

#Class for the nodes that make up the tetris board.
class node():
    def __init__(self, x: int, y: int, isFull: bool):
        self.x = x #x pos
        self.y = y #y pos
        self.isFull = isFull #bool for if node has block on it or not.
        self.simulatedPiece = False #bool for if it is the current pieces block.

#Class for the game
class tetris():
    #Inititates the tetris class, making variables and creating the nodes used for the board.
    def __init__(self):
        #dictionary of the possible rotations used to cycle through them left or right.
        self.rotations = ['left', 'down', 'right', 'up', 'left', 'up']
        #Checking if alive.
        self.alive = True
        #var for checking if there is currently a piece spawned in.
        self.movingPiece = False
        #var for storing the current moving piece.
        self.currPiece = node(0, 0, False)
        #var for storing the current piece type.
        self.currPieceType = 2
        #var for storing the current pieces rotation.
        self.currRotation = "down"
        #var for storing the time at which the last movePieceDown function was called.
        self.lastMove = time.time()
        #dictionary for storing the board nodes.
        self.nodeDic  = []
        #dictionary for storing the nodes highlighted based on the current piece type/rotation, e.g a I block will have the 3 nodes
        #above the current position highlighted.
        self.simulatedPieces = []
        #var for storing the score.
        self.score = 0
        #var for checking if the last line clear was a tetris.
        self.lastTetris = False

        #creating all of the nodes and adding them to the node dictionary.
        for y in range(0, 20):
            for x in range(0, 10):
                self.nodeDic.append(node(x, y, False))

        #game start.
        self.game()
    
    #returns the node from the node dictionary at the position.
    def getNode(self, x, y):
        return self.nodeDic[y*10+x]

    def testNode(self, x, y):
        
        #testing if a node is going out of bounds on the x paramaters
        if (x == -1)|(x == 10):
            return "hit"
        #if the getNode function trys to call something out of bounds it will except and return that it is hit therefore not viable.
        try:
            #if it hits a node other than its own pieces(simulated pieces) it will return hit.
            if self.getNode(x, y).isFull == True and self.getNode(x,y).simulatedPiece == False:
                return "hit"
            else:
                return self.nodeDic[y*10+x]
        except:
            return "hit"
    #Function for clearing and printing the board.
    #Works by looping through the lines and adding either a space or X to lines depending on a nodes value then printing it.
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
        #Runs a loop while alive.
        while(self.alive==True):
            
            if self.movingPiece == True:
                self.changeSPieces(self.currPieceType, False)

            #Testing if a key is pressed down.
            if msvcrt.kbhit()==True:
                #Gets the pressed key
                key = msvcrt.getch()
                
                #Moves the piece left if a is clicked.
                if str(key) == "b'a'":
                    self.movePiece("left")
                #Moves the key right if d is clicked.
                if str(key) == "b'd'":
                    self.movePiece("right")
                #If is is clicked move piece down quicker.
                if str(key) == "b's'":
                    if self.movingPiece!=False:
                        self.movePieceDown()
                #If space is clicked drop the piece to the bottom.
                if str(key) == "b' '":
                        while self.movingPiece==True:
                            self.changeSPieces(self.currPieceType, False)
                            self.movePieceDown()
                            
                #Rotate the pieces based on key clicked.
                if str(key) == "b'n'":
                    self.rotatePiece("left")
                if str(key) == "b'm'":
                    self.rotatePiece("right")
            
            #Once per second move the piece down.
            if (self.lastMove - time.time()+1) < 0:
                self.movePieceDown()

            #Simulate the nodes around the current piece.
            if self.movingPiece == True:
                self.changeSPieces(self.currPieceType, True)
            
            #Print the board and sleep for 0.08 seconds.
            self.printBoard()
            time.sleep(0.08)

    #Function for creating a piece of a random type.
    def createPiece(self):

        self.checkLineClear()
        node = self.getNode(4, 3)

        node.isFull = True

        self.currPieceType = random.randint(1, 7)
        self.currPiece = node
        self.currRotation = "down"

        self.movingPiece = True

    #Function for rotating a piece, takes a direction paramater and checks if the piece is able to be rotated without causing
    # any problems by testing all of the nodes first to make sure there are no problems.
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

    #Function for moving a piece down, which also runs the createPiece function if there is not one currently.
    #Works by testing the piece against all the nodes it will move to then moves the current piece there.
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

    #Function for moving a piece left or right.
    #Works by testing the piece against all the nodes it will move to then moves the current piece there.
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
            
    #Piece types:
    #1 SQUARE
    #2 I
    #3 L
    #4 rL
    #5 S
    #6 rS
    #7 T
    #Function for creating a dictionary of node positions based on the currents piece position, rotation and piecetype.
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

    #Runs the simulatePieces Function and changes the variables of those specific nodes.
    def changeSPieces(self, type, isFull):
        
        self.simulatedPieces = self.simulatePieces(type, self.currRotation)
        for node in self.simulatedPieces:
                    self.getNode(node[0], node[1]).isFull = isFull
                    self.getNode(node[0], node[1]).simulatedPiece = isFull
    
    #Function for checking each line to see if it is full then running the breakline command on each of them.
    #Adds score based on how many lines broken with the last move, with 100 per line, 800 for tetris(4 lines at once) and 1200
    #  for consecutive tetris's.
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
            if self.lastTetris == True:
                self.score = self.score + 1200
            else:
                self.score = self.score + 800

            self.lastTetris = True
        elif breakCount > 0:
            
            self.score = self.score + (breakCount*100)
            self.lastTetris = False

    #Function for deleting specific row and moving down all the rows above it.        
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
                
    
    


