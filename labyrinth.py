import random
import math

class tile:
  # a tile is the basic unit used for the game
  def __init__(self,x:int,y:int,pic:list):
    self.co=[x,y]
    self.x=x
    self.y=y
    self.pic=pic
  def updateCoords(self,x:int,y:int):
    self.x=x
    self.y=y
    self.co=[x,y]
      
topLeft=tile(-1,-1,[" ▒ ","▒▒ ","   "])
topRight=tile(-1,-1,[" ▒ "," ▒▒","   "])
bottomLeft=tile(-1,-1,["   ","▒▒ "," ▒ "])
bottomRight=tile(-1,-1,["   "," ▒▒"," ▒ "])
hori=tile(-1,-1,["   ","▒▒▒","   "])
vert=tile(-1,-1,[" ▒ "," ▒ "," ▒ "])
triLeft=tile(-1,-1,[" ▒ "," ▒▒"," ▒ "])
triRight=tile(-1,-1,[" ▒ ","▒▒ "," ▒ "])
triBottom=tile(-1,-1,[" ▒ ","▒▒▒","   "])
triTop=tile(-1,-1,["   ","▒▒▒"," ▒ "])

#switches the images in the tiles for ones with xs instead of spaces to indicate they can't be moved
def makeFixedPic(tile):
  z=[]
  for n in range(3):
    z.append(tile.pic[n].replace(" ","x"))
  return z

def makeEndPic(tile):
  z=[]
  for n in range(3):
    z.append(tile.pic[n].replace("▒","▓"))
  return z

def randTile():
  return random.choice([topLeft,topRight,bottomLeft,bottomRight,hori,vert,triLeft,triRight,triBottom,triTop]).pic

# defines the order in which a tile rotates by listing them in order
tilesList=[topLeft,topRight,bottomRight,bottomLeft,topLeft,hori,vert,hori,triLeft,triTop,triRight,triBottom,triLeft]

topLeftFixedPic=makeFixedPic(topLeft)
topRightFixedPic=makeFixedPic(topRight)
bottomLeftFixedPic=makeFixedPic(bottomLeft)
bottomRightFixedPic=makeFixedPic(bottomRight)
horiFixedPic=makeFixedPic(hori)
vertFixedPic=makeFixedPic(vert)
triLeftFixedPic=makeFixedPic(triLeft)
triRightFixedPic=makeFixedPic(triRight)
triBottomFixedPic=makeFixedPic(triBottom)
triTopFixedPic=makeFixedPic(triTop)

savedTile=tile(-5,-5,[0,0,0,0,0,0,0,0,0])
fStr=""

def checkCoords():
  # go through every tile in order (left to right, bottom to top) and check that the coordinates are right.If not, for every incorrect coordinate, output a list with entry 0 the actual coordinates and entry 1 the supposed coordinates
  coordList=[]
  for n in range(0,11):
    for m in range(0,7):
      if boardList[n][m].co[0]!=n or boardList[n][m].co[1]!=m:
        coordList.append([str(n)+","+str(m),boardList[n][m].co])
  return coordList

def displayTile(displayee:tile):
  print("+---+\n|"+displayee.pic[0]+"|\n|"+displayee.pic[1]+"|\n|"+displayee.pic[2]+"|\n+---+")

# left() and right() determine what character should go on either side of a row in the final picture
def right(n:int,m:int):
  if n%2==1: return("|← ")
  elif n%2==0 and m==1: return "| "+str(6-n)
  else: return("|  ")
def left(n:int,m:int):
  if n%2==1: return("  →|")
  elif n%2==0 and m==1: return " "+str(6-n)+" |"
  else: return("   |")

def updateFStr():
  # make the string that is printed, including the extra tile portion
  global fStr
  fStr="     0  ↓↓↓  2  ↓↓↓  4  ↓↓↓  6  ↓↓↓  8  ↓↓↓  10\n   +---+---+---+---+---+---+---+---+---+---+---+\n"
  for n in range(0,7):
    for m in range(0,3):
      fStr+=left(n,m)
      for p in range(0,11):
        fStr+=(boardList[p][6-n].pic[m])
        if p!=10:fStr+="|"
      fStr+=(right(n,m)+"\n")
    fStr+="   +---+---+---+---+---+---+---+---+---+---+---+\n"
  fStr+="     0  ↑↑↑  2  ↑↑↑  4  ↑↑↑  6  ↑↑↑  8  ↑↑↑  10\n\n  Extra Tile:\n\n     +---+\n     |"+extraTile.pic[0]+"|\n     |"+extraTile.pic[1]+"|\n     |"+extraTile.pic[2]+"|\n     +---+\n"
  while "▓" not in fStr:
    #about once every ten times the board was generated the end tiles wouldn't be colored correctly and i couldnt figure out why so this fixes that if it happens
    boardList[endCo1[0]][endCo1[1]].pic=makeEndPic(boardList[endCo1[0]][endCo1[1]])
    boardList[endCo2[0]][endCo2[1]].pic=makeEndPic(boardList[endCo2[0]][endCo2[1]])
    updateFStr()

def rotateTile(spTile:tile,direction:str):
  # function that outputs a tile rotated the specified direction
  if direction=="cw":
    for n in range(len(tilesList)):
      if tilesList[n].pic==spTile.pic:
        spTile.pic=tilesList[n+1].pic
        return spTile.pic
        break
    return "error: 01"
  elif direction=="ccw":
    for n in range(len(tilesList)):
      if tilesList[(len(tilesList)-n-1)].pic==spTile.pic:
        spTile.pic=tilesList[len(tilesList)-n-2].pic
        return spTile.pic
        break
    return "error: 02"
  else: 
    return "error: 03"

connections={}
def updateConnections():
  # connections is a dictionary with keys for all tiles in form "x,y" <-str. The values start out as corresponding to all tiles the key supposedly connects to (the key points to them). values should be in counterclockwise order from bottom (below tile, right tile, above tile, left tile)
  for x in range(11):
    for y in range(7):
      connections[str(x)+","+str(y)]=[]
      if boardList[x][y].pic[2][1]=="▒" and y!=0 or boardList[x][y].pic[2][1]=="▓" and y!=0:
        connections[str(x)+","+str(y)].append(str(x)+","+str(y-1))
      if boardList[x][y].pic[1][2]=="▒" and x!=10 or boardList[x][y].pic[1][2]=="▓" and x!=10:
        connections[str(x)+","+str(y)].append(str(x+1)+","+str(y))
      if boardList[x][y].pic[0][1]=="▒" and y!=6 or boardList[x][y].pic[0][1]=="▓" and y!=6:
        connections[str(x)+","+str(y)].append(str(x)+","+str(y+1))
      if boardList[x][y].pic[1][0]=="▒" and x!=0 or boardList[x][y].pic[1][0]=="▓" and x!=0:
        connections[str(x)+","+str(y)].append(str(x-1)+","+str(y))
  # this part corrects the error inherent in only worrying about which way the key tile points by deleting all values that aren't mutual i.e. if 1,0 points to 1,1 but 1,1 doesn't point to 1,0, then 1,1 is eliminated from 1,0's values
  for x in range(11):
    for y in range(7):
      #if x,y isn't in the tile next to it but the tile next to it IS in x,y, then remove it from x,y. the four loops are for the four directions
      if str(x-1)+","+str(y) in connections[(str(x)+","+str(y))] and str(x)+","+str(y) not in connections[(str(x-1)+","+str(y))] and x>0:
        connections[(str(x)+","+str(y))].remove(str(x-1)+","+str(y))
      if str(x+1)+","+str(y) in connections[(str(x)+","+str(y))] and str(x)+","+str(y) not in connections[(str(x+1)+","+str(y))] and x<10: 
        connections[(str(x)+","+str(y))].remove(str(x+1)+","+str(y))
      if str(x)+","+str(y-1) in connections[(str(x)+","+str(y))] and str(x)+","+str(y) not in connections[(str(x)+","+str(y-1))] and y>0: 
        connections[(str(x)+","+str(y))].remove(str(x)+","+str(y-1))
      if str(x)+","+str(y+1) in connections[(str(x)+","+str(y))] and str(x)+","+str(y) not in connections[(str(x)+","+str(y+1))] and y<6:
        connections[(str(x)+","+str(y))].remove(str(x)+","+str(y+1))


def move(x:int,y:int):
  # function that slides the pieces on the board
  global boardList
  global extraTile
  global endCo1
  global endCo2
  if x==2 or x==4 or x==6 or x==8 or y==2 or y==4 or (x+y)%2==0: 
    return "error: 04"
  elif y==0:
    boardList[x].insert(0,extraTile)
    extraTile=boardList[x][7]
    if endCo1==[x,6]: endCo1=[-2,-2]
    elif endCo2==[x,6]: endCo2=[-2,-2]
    boardList[x].pop(7)
    for n in range(7):
      if boardList[x][n]==endTile2: endCo2=[x,n]
      if boardList[x][n]==endTile1: endCo1=[x,n]
      boardList[x][n].updateCoords(x,n)
  elif y==6:
    boardList[x].append(extraTile)
    extraTile=boardList[x][0]
    if endCo1==[x,0]: endCo1=[-2,-2]
    elif endCo2==[x,0]: endCo2=[-2,-2]
    boardList[x].pop(0)
    for n in range(7):
      if boardList[x][n]==endTile2: endCo2=[x,n]
      if boardList[x][n]==endTile1: endCo1=[x,n]
      boardList[x][n].updateCoords(x,n)
  elif x==0:
    savedTile=boardList[10][y]
    if endCo1==[10,y]: endCo1=[-2,-2]
    elif endCo2==[10,y]: endCo2=[-2,-2]
    for n in range(10):
      boardList[10-n][y]=boardList[9-n][y]
      if boardList[10-n][y]==endTile2: endCo2=[10-n,y]
      if boardList[10-n][y]==endTile1: endCo1=[10-n,y]
      boardList[10-n][y].updateCoords(10-n,y)
    boardList[0][y]=extraTile
    boardList[0][y].updateCoords(0,y)
    if endCo1==[-2,-2] and "▓" in boardList[0][y].pic[1]: endCo1=[0,y]
    elif endCo2==[-2,-2] and "▓" in boardList[0][y].pic[1]: endCo2=[0,y]
    extraTile=savedTile
  elif x==10:
    savedTile=boardList[0][y]
    if endCo1==[0,y]: endCo1=[-2,-2]
    elif endCo2==[0,y]: endCo2=[-2,-2]
    for n in range(10):
      boardList[n][y]=boardList[n+1][y]
      if boardList[n][y]==endTile2: endCo2=[n,y]
      if boardList[n][y]==endTile1: endCo1=[n,y]
      boardList[n][y].updateCoords(n,y)
    boardList[10][y]=extraTile
    boardList[10][y].updateCoords(10,y)
    if endCo1==[-2,-2] and "▓" in boardList[10][y].pic[1]: endCo1=[10,y]
    elif endCo2==[-2,-2] and "▓" in boardList[10][y].pic[1]: endCo2=[10,y]
    extraTile=savedTile 
  else: return "error: 05"
  extraTile.updateCoords(-2,-2)
  updateConnections()
  updateFStr()
  #return checkCoords()

possibleMoves=[[0,1],[0,3],[0,5],[1,0],[1,6],[3,0],[3,6],[5,0],[5,6],[7,0],[7,6],[9,0],[9,6],[10,1],[10,3],[10,5]]

def runRandomMoves(num:int):
  for n in range(num):
    a = random.choice(possibleMoves)
    print(str(a[0])+","+str(a[1]))
    move(a[0],a[1])

pathList=[]
optionsList=[]
checkedList=[]


def erasedLoopStrs(inputList):
  #function that erases tile sequences from findPath that loop: i.e. if inputList=["1,0","2,0","2,1","2,0""1,0","1,1","1,2"] then ["1,0","1,1","1,2"] will be returned
  for m in range(len(inputList)):
    for n in range(len(inputList)):
      if inputList[m]==inputList[n] and m!=n:
        for z in range(min(m,n),max(m,n)):
          inputList.pop(min(m,n))
        return erasedLoopStrs(inputList)
  return inputList 
def findPath(start:str,end:str,dev=False):
  #findPath finds a path between the two tiles specified and outputs a list corresponding to the tiles needed to cross between the start and end points or, if there isnt a valid path, outputs False
  #I'll be honest I just started trying things and it worked eventually I'm not sure how good this is or if I messed something up
  global pathList
  global checkedList
  pathList.append(start)
  if len(pathList) > 100:
    pathList=[]
    checkedList=[]
    return 'error: search limit reached'
  if start!=end:
    if len(start)==3: optionsList=connections[start[0]+","+start[2]]
    elif len(start)==4: optionsList=connections[start[0]+start[1]+","+start[3]]
    else: return "error: start length"
    for n in range(len(optionsList)):
      #check for a tile that hasnt been traveled on yet
      if optionsList[n] not in pathList: 
        return findPath(optionsList[n],end)
    checkedList.append(start)
    for n in range(len(optionsList)):
      #check for a tile that hasn't been marked checked yet
      if optionsList[n] not in checkedList: 
        return findPath(optionsList[n],end) 
    pathList=[]
    checkedList=[]
    return False
  else: 
    if dev: 
      print("pathList:"+str(pathList))
      print("checkedList:"+str(checkedList))
    z=erasedLoopStrs(pathList)
    pathList=[]
    checkedList=[]
    return z
    
devCode=0
# devCode is a value that controls whether or not the program continues indefinitely so that when it's one I can send queries 
moveCount=0
#moveCount counts how many moves have been made in a round
def getMoveInput():
  inputMove=""
  #inputMove is a string with three characters that represents the type of movement (row/column), direction of movement (left/right or up/down), and the row/column that is moved (1,3,5,7,9). For testing purposes it allows for input to be a 2-entry coordinate list corresponding to what is necessary for the move() function
  global moveCount
  moveCount+=1
  global devCode
  inputMoveType=input("  Move:\n\n  Row or Column?  ")
  if inputMoveType=="devCode": 
    devCode=1
  # ^ checks if the devCode is entered
  elif len(inputMoveType)==5 and inputMoveType[0]=='[' and inputMoveType[1] in ['0','1','3','5','7','9'] and inputMoveType[2]==',' and inputMoveType[3] in ['0','1','3','5','6'] and inputMoveType[4]==']': 
    inputMove=[int(inputMoveType[1]),int(inputMoveType[3])]
  elif len(inputMoveType)==6 and inputMoveType[0]=='[' and inputMoveType[1]=='1' and inputMoveType[2]=='0' and inputMoveType[3]==',' and inputMoveType[4] in ['0','1','3','5','6'] and inputMoveType[5]==']':
    inputMove=[10,int(inputMoveType[4])]
  # ^ checks if inputMoveType is a list corresponding to what is necessary for the move() function
  else:
    while inputMoveType not in ["R","r","Row","ROW","row","c","C","Column","COLUMN","column"]:
      print("\n  Please enter a valid answer.\n")
      inputMoveType=input("  Row or Column?  ")
    if inputMoveType in ["R","r","Row","ROW","row"]:
      inputMove="r"
      #section for row number given row is chosen
      inputMoveNumber=input("\n  Number?  ")
      while inputMoveNumber not in ["1","3","5"]:
        inputMoveNumber=input("\n  Please enter a valid answer. (1, 3, or 5)\n\n  Number?  ")
      else:
        inputMove+=inputMoveNumber
        #section for left/right given row number
      inputMoveDirection=input("\n  Left or Right?  ")
      while inputMoveDirection not in ["R","r","Right","RIGHT","right","l","L","Left","LEFT","left"]:
        print("\n  Please enter a valid answer.")
        inputMoveDirection=input("\n  Left or Right?  ")
      if inputMoveDirection in ["R","r","Right","RIGHT","right"]:
        inputMove+="r"
      elif inputMoveDirection in ["l","L","Left","LEFT","left"]:
        inputMove+="l"
      else:
        return "error: incorrect move direction"

    elif inputMoveType in ["c","C","Column","COLUMN","column"]:
      inputMove="c"
      #section for column number given column is chosen
      inputMoveNumber=input("\n  Number?  ")
      while inputMoveNumber not in ["1","3","5","7","9"]:
        inputMoveNumber=input("\n\n  Please enter a valid answer. (1, 3, 5, 7, or 9)\n\n  Number?  ")
      else:
        inputMove+=inputMoveNumber
      #section for up/down given column number
      inputMoveDirection=input("\n  Up or Down?  ")
      while inputMoveDirection not in ["U","u","Up","UP","up","d","D","Down","DOWN","down"]:
        print("\n  Please enter a valid answer.")
        inputMoveDirection=input("\n  Up or Down?  ")
      if inputMoveDirection in ["U","u","Up","UP","up"]:
        inputMove+="u"
      elif inputMoveDirection in ["d","D","Down","DOWN","down"]:
        inputMove+="d"
      else:
        return "error: incorrect move direction"
      
    else:
      return "error: incorrect move type"
  
  if str(type(inputMove))=="<class 'list'>":
    print('\n\n\n\n\n\n\n')
    move(int(inputMove[0]),int(inputMove[1]))
  elif str(type(inputMove))=="<class 'str'>" and devCode==0:
    if inputMove[0]=="r":
      if inputMove[2]=="r":
        move(0,int(inputMove[1]))
      elif inputMove[2]=="l":
        move(10,int(inputMove[1]))
    elif inputMove[0]=="c":
      if inputMove[2]=="u":
        move(int(inputMove[1]),0)
      elif inputMove[2]=="d":
        move(int(inputMove[1]),6)
    else: print("error: inputMove")
  elif devCode==0: print("error: inputMove type")


titleStr ="\n  ██╗      █████╗ ██████╗ ██╗   ██╗██████╗ ██╗███╗   ██╗████████╗██╗  ██╗\n  ██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██║████╗  ██║╚══██╔══╝██║  ██║\n  ██║     ███████║██████╔╝ ╚████╔╝ ██████╔╝██║██╔██╗ ██║   ██║   ███████║\n  ██║     ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██╗██║██║╚██╗██║   ██║   ██╔══██║\n  ███████╗██║  ██║██████╔╝   ██║   ██║  ██║██║██║ ╚████║   ██║   ██║  ██║\n  ╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝\n\n      A game by Astra Coblentz, based on the\n      series of board games designed by Max Kobbert\n\n"

def resetBoard():
  # reset the board to a starting position and erases data
  global x0
  global x1
  global x2
  global x3
  global x4
  global x5
  global x6
  global x7
  global x8
  global x9
  global x10
  x0=[]
  x1=[]
  x2=[]
  x3=[]
  x4=[]
  x5=[]
  x6=[]
  x7=[]
  x8=[]
  x9=[]
  x10=[]
  # put random tiles in all spaces
  for n in range(0,7):
    x0.append(tile(0,int(n),randTile()))
    x1.append(tile(1,int(n),randTile()))
    x2.append(tile(2,int(n),randTile()))
    x3.append(tile(3,int(n),randTile()))
    x4.append(tile(4,int(n),randTile()))
    x5.append(tile(5,int(n),randTile()))
    x6.append(tile(6,int(n),randTile()))
    x7.append(tile(7,int(n),randTile()))
    x8.append(tile(8,int(n),randTile()))
    x9.append(tile(9,int(n),randTile()))
    x10.append(tile(10,int(n),randTile()))
  global extraTile
  global boardList
  boardList=[x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]
  extraTile=tile(-2,-2,randTile())
  # make the fixed tiles the correct ones
  x0[0].pic=topRightFixedPic
  x0[2].pic=triLeftFixedPic
  x0[4].pic=triLeftFixedPic
  x0[6].pic=bottomRightFixedPic
  x2[0].pic=triBottomFixedPic
  x2[2].pic=triTopFixedPic
  x2[4].pic=triBottomFixedPic
  x2[6].pic=triTopFixedPic
  x4[0].pic=triBottomFixedPic
  x4[2].pic=triLeftFixedPic
  x4[4].pic=triLeftFixedPic
  x4[6].pic=triTopFixedPic
  x6[0].pic=triBottomFixedPic
  x6[2].pic=triRightFixedPic
  x6[4].pic=triRightFixedPic
  x6[6].pic=triTopFixedPic
  x8[0].pic=triBottomFixedPic
  x8[2].pic=triBottomFixedPic
  x8[4].pic=triTopFixedPic
  x8[6].pic=triTopFixedPic
  x10[0].pic=topLeftFixedPic
  x10[2].pic=triRightFixedPic
  x10[4].pic=triRightFixedPic
  x10[6].pic=bottomLeftFixedPic
  #make the end tiles, make sure they aren't too close to each other physically
  global endCo1
  global endCo2
  global endTile1
  global endTile2
  endCo1=[random.randint(0,10),random.randint(0,6)]
  endCo2=[random.randint(0,10),random.randint(0,6)]
  while math.fabs(endCo1[0]-endCo2[0])+math.fabs(endCo1[1]-endCo2[1])<3:
    endCo1=[random.randint(0,10),random.randint(0,6)]
    endCo2=[random.randint(0,10),random.randint(0,6)]
  endTile1=boardList[endCo1[0]][endCo1[1]]
  endTile2=boardList[endCo2[0]][endCo2[1]]

def playGame():
  #actual command to play a round
  while findPath(str(endCo1[0])+","+str(endCo1[1]),str(endCo2[0])+","+str(endCo2[1]))==False and devCode==0 or findPath(str(endCo2[0])+","+str(endCo2[1]),str(endCo1[0])+","+str(endCo1[1]))==False and devCode==0:
    print(fStr)
    getMoveInput()
  if devCode==0:
    print(fStr)
    print("\n  You Win!!")
    print("\n  Your total move count was "+str(moveCount)+".")
    if input("\n  To play again, press enter. ")!="devCode":
      resetBoard()
      updateConnections()
      print("\n\n\n\n\n\n\n\n\n\n\n")
      updateFStr()
      playGame()
resetBoard()
updateConnections()
boardList[endCo1[0]][endCo1[1]].pic=makeEndPic(boardList[endCo1[0]][endCo1[1]])
boardList[endCo2[0]][endCo2[1]].pic=makeEndPic(boardList[endCo2[0]][endCo2[1]])
while findPath(str(endCo1[0])+","+str(endCo1[1]),str(endCo2[0])+","+str(endCo2[1]))!=False: 
  resetBoard()
  updateConnections()
updateFStr()

#begins the actual gameplay with inputs from the player and whatnot
print(titleStr)
input("  To begin, press enter...")
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
playGame()
